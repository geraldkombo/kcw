from __future__ import annotations

import json
import logging
import sys
from typing import Any

from config.settings import settings
from masumi.escrow_lifecycle import EscrowLifecycle, EscrowState

logging.basicConfig(level=logging.WARNING, stream=sys.stderr)
logger = logging.getLogger("mcp-x402")


class X402MCPServer:
    """MCP server exposing x402 HTTP micropayment escrow lifecycle via stdio JSON-RPC."""

    _escrows: dict[str, EscrowLifecycle] = {}

    def handle_request(self, req: dict[str, Any]) -> dict[str, Any] | None:
        method = req.get("method", "")
        req_id = req.get("id")

        if method == "initialize":
            return self._jsonrpc({
                "protocolVersion": "2025-03-26",
                "capabilities": {
                    "tools": {"listChanged": False},
                    "resources": {"listChanged": False}
                },
                "serverInfo": {"name": "mcp-x402", "version": "1.0.0"}
            }, req_id)

        if method == "tools/list":
            return self._jsonrpc({"tools": [
                {
                    "name": "initiate_escrow",
                    "description": "Initiate an x402 escrow for agentic micropayment",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "amount_lovelace": {"type": "integer", "description": "Amount in lovelace (1 ADA = 1_000_000 lovelace)"}
                        },
                        "required": ["amount_lovelace"]
                    }
                },
                {
                    "name": "lock_escrow",
                    "description": "Lock funds in escrow contract",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "escrow_id": {"type": "string"}
                        },
                        "required": ["escrow_id"]
                    }
                },
                {
                    "name": "submit_data_hash",
                    "description": "Submit data hash to escrow for verification",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "escrow_id": {"type": "string"},
                            "data_hash": {"type": "string"}
                        },
                        "required": ["escrow_id", "data_hash"]
                    }
                },
                {
                    "name": "complete_escrow",
                    "description": "Complete escrow and release funds",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "escrow_id": {"type": "string"}
                        },
                        "required": ["escrow_id"]
                    }
                },
                {
                    "name": "refund_escrow",
                    "description": "Authorize refund for an escrow",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "escrow_id": {"type": "string"}
                        },
                        "required": ["escrow_id"]
                    }
                },
                {
                    "name": "get_escrow_status",
                    "description": "Get current state of an escrow",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "escrow_id": {"type": "string"}
                        },
                        "required": ["escrow_id"]
                    }
                },
                {
                    "name": "get_wallet_info",
                    "description": "Get Masumi wallet address and network info",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            ]}, req_id)

        if method == "resources/list":
            return self._jsonrpc({"resources": []}, req_id)

        if method == "tools/call":
            return self._handle_tool_call(req.get("params", {}), req_id)

        if method == "notifications/initialized":
            return None

        return self._jsonrpc({"error": f"Unknown method: {method}"}, req_id, is_error=True)

    def _handle_tool_call(self, params: dict[str, Any], req_id: Any) -> dict[str, Any]:
        name = params.get("name", "")
        args = params.get("arguments", {})

        try:
            if name == "initiate_escrow":
                amount = args.get("amount_lovelace", 1_000_000)
                escrow_id = f"escrow-{len(self._escrows) + 1}"
                escrow = EscrowLifecycle(escrow_id, amount)
                self._escrows[escrow_id] = escrow
                return self._jsonrpc({
                    "content": [{"type": "text", "text": json.dumps({
                        "escrow_id": escrow_id,
                        "amount_lovelace": amount,
                        "state": "initiated",
                        "wallet_address": settings.masumi_wallet_address or "not configured"
                    }, indent=2)}]
                }, req_id)

            elif name == "lock_escrow":
                eid = args["escrow_id"]
                escrow = self._escrows.get(eid)
                if not escrow:
                    return self._jsonrpc({"content": [{"type": "text", "text": f"Escrow {eid} not found"}]}, req_id)
                escrow.transition(EscrowState.LOCKED)
                return self._jsonrpc({
                    "content": [{"type": "text", "text": json.dumps(escrow.to_dict(), indent=2)}]
                }, req_id)

            elif name == "submit_data_hash":
                eid = args["escrow_id"]
                escrow = self._escrows.get(eid)
                if not escrow:
                    return self._jsonrpc({"content": [{"type": "text", "text": f"Escrow {eid} not found"}]}, req_id)
                escrow.data_hash = args["data_hash"]
                escrow.transition(EscrowState.SUBMITTED)
                return self._jsonrpc({
                    "content": [{"type": "text", "text": json.dumps(escrow.to_dict(), indent=2)}]
                }, req_id)

            elif name == "complete_escrow":
                eid = args["escrow_id"]
                escrow = self._escrows.get(eid)
                if not escrow:
                    return self._jsonrpc({"content": [{"type": "text", "text": f"Escrow {eid} not found"}]}, req_id)
                escrow.transition(EscrowState.COMPLETED)
                return self._jsonrpc({
                    "content": [{"type": "text", "text": json.dumps(escrow.to_dict(), indent=2)}]
                }, req_id)

            elif name == "refund_escrow":
                eid = args["escrow_id"]
                escrow = self._escrows.get(eid)
                if not escrow:
                    return self._jsonrpc({"content": [{"type": "text", "text": f"Escrow {eid} not found"}]}, req_id)
                escrow.transition(EscrowState.REFUND_AUTHORIZED)
                return self._jsonrpc({
                    "content": [{"type": "text", "text": json.dumps(escrow.to_dict(), indent=2)}]
                }, req_id)

            elif name == "get_escrow_status":
                eid = args["escrow_id"]
                escrow = self._escrows.get(eid)
                if not escrow:
                    return self._jsonrpc({"content": [{"type": "text", "text": f"Escrow {eid} not found"}]}, req_id)
                return self._jsonrpc({
                    "content": [{"type": "text", "text": json.dumps(escrow.to_dict(), indent=2)}]
                }, req_id)

            elif name == "get_wallet_info":
                return self._jsonrpc({
                    "content": [{"type": "text", "text": json.dumps({
                        "wallet_address": settings.masumi_wallet_address or "not configured",
                        "network": "Cardano Preprod (testnet)",
                        "api_url": settings.masumi_api_url
                    }, indent=2)}]
                }, req_id)

            else:
                return self._jsonrpc({"content": [{"type": "text", "text": f"Unknown tool: {name}"}]}, req_id)
        except ValueError as e:
            return self._jsonrpc({"content": [{"type": "text", "text": f"Transition error: {e}"}]}, req_id)
        except Exception as e:
            return self._jsonrpc({"content": [{"type": "text", "text": f"Error: {e}"}]}, req_id, is_error=True)

    def _jsonrpc(self, result: Any, req_id: Any, is_error: bool = False) -> dict[str, Any]:
        msg: dict[str, Any] = {"jsonrpc": "2.0"}
        if is_error:
            msg["error"] = result
        else:
            msg["result"] = result
        msg["id"] = req_id
        return msg

    def run(self) -> None:
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
    X402MCPServer().run()
