from __future__ import annotations

import json
import logging
import sys
from typing import Any

from neo4j import GraphDatabase

logging.basicConfig(level=logging.WARNING, stream=sys.stderr)
logger = logging.getLogger("mcp-neo4j-cypher")


class Neo4jCypherMCPServer:
    """MCP server exposing Neo4j Cypher query capabilities via stdio JSON-RPC."""

    def __init__(self) -> None:
        self.driver = None

    def connect(self) -> None:
        uri = "bolt://localhost:7687"
        user = "neo4j"
        password = ""
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()
        except Exception:
            self.driver = None

    def handle_request(self, req: dict[str, Any]) -> dict[str, Any]:
        method = req.get("method", "")
        req_id = req.get("id")
        params = req.get("params", {})

        if method == "initialize":
            return self._jsonrpc({
                "protocolVersion": "2025-03-26",
                "capabilities": {
                    "tools": {
                        "listChanged": False
                    },
                    "resources": {
                        "listChanged": False
                    }
                },
                "serverInfo": {
                    "name": "mcp-neo4j-cypher",
                    "version": "1.0.0"
                }
            }, req_id)

        if method == "tools/list":
            return self._jsonrpc({"tools": [
                {
                    "name": "get_neo4j_schema_and_indexes",
                    "description": "Read Neo4j schema: node labels, relationship types, indexes, and constraints",
                    "inputSchema": {"type": "object", "properties": {}, "required": []}
                },
                {
                    "name": "read_neo4j_cypher",
                    "description": "Execute a read-only Cypher query",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Cypher query (READ only)"},
                            "params": {"type": "object", "description": "Query parameters"}
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "write_neo4j_cypher",
                    "description": "Execute a write Cypher query (CREATE, MERGE, SET, DELETE)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Cypher query (WRITE)"},
                            "params": {"type": "object", "description": "Query parameters"}
                        },
                        "required": ["query"]
                    }
                }
            ]}, req_id)

        if method == "resources/list":
            return self._jsonrpc({"resources": []}, req_id)

        if method == "tools/call":
            return self._handle_tool_call(params, req_id)

        if method == "notifications/initialized":
            return None

        return self._jsonrpc({"error": f"Unknown method: {method}"}, req_id, is_error=True)

    def _handle_tool_call(self, params: dict[str, Any], req_id: Any) -> dict[str, Any]:
        name = params.get("name", "")
        args = params.get("arguments", {})

        if self.driver is None:
            return self._jsonrpc({"content": [{"type": "text", "text": "Neo4j not connected — start Neo4j and set NEO4J_PASSWORD"}]}, req_id)

        try:
            if name == "get_neo4j_schema_and_indexes":
                return self._get_schema(req_id)
            elif name == "read_neo4j_cypher":
                return self._read_query(args.get("query", ""), args.get("params", {}), req_id)
            elif name == "write_neo4j_cypher":
                return self._write_query(args.get("query", ""), args.get("params", {}), req_id)
            else:
                return self._jsonrpc({"content": [{"type": "text", "text": f"Unknown tool: {name}"}]}, req_id)
        except Exception as e:
            return self._jsonrpc({"content": [{"type": "text", "text": f"Error: {e}"}]}, req_id, is_error=True)

    def _get_schema(self, req_id: Any) -> dict[str, Any]:
        with self.driver.session() as session:
            labels = session.run("CALL db.labels()").value()
            rel_types = session.run("CALL db.relationshipTypes()").value()
            indexes = session.run("SHOW INDEXES").data()
            constraints = session.run("SHOW CONSTRAINTS").data()
        return self._jsonrpc({
            "content": [{"type": "text", "text": json.dumps({
                "labels": labels, "relationshipTypes": rel_types,
                "indexes": indexes, "constraints": constraints
            }, indent=2)}]
        }, req_id)

    def _read_query(self, query: str, params: dict[str, Any], req_id: Any) -> dict[str, Any]:
        with self.driver.session() as session:
            result = session.run(query, **params).data()
        return self._jsonrpc({
            "content": [{"type": "text", "text": json.dumps(result, indent=2, default=str)}]
        }, req_id)

    def _write_query(self, query: str, params: dict[str, Any], req_id: Any) -> dict[str, Any]:
        with self.driver.session() as session:
            result = session.run(query, **params)
            summary = result.consume()
            counters = {k: v for k, v in dict(summary.counters).items() if v > 0}
        return self._jsonrpc({
            "content": [{"type": "text", "text": json.dumps({"updates": counters})}]
        }, req_id)

    def _jsonrpc(self, result: Any, req_id: Any, is_error: bool = False) -> dict[str, Any]:
        msg: dict[str, Any] = {"jsonrpc": "2.0"}
        if is_error:
            msg["error"] = result
        else:
            msg["result"] = result
        msg["id"] = req_id
        return msg

    def run(self) -> None:
        self.connect()
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
                resp = self.handle_request(req)
                if resp is not None:
                    sys.stdout.write(json.dumps(resp) + "\n")
                    sys.stdout.flush()
            except json.JSONDecodeError:
                continue
            except SystemExit:
                raise
            except Exception as e:
                err = self._jsonrpc({"error": str(e)}, req.get("id"), is_error=True)
                sys.stdout.write(json.dumps(err) + "\n")
                sys.stdout.flush()


if __name__ == "__main__":
    Neo4jCypherMCPServer().run()
