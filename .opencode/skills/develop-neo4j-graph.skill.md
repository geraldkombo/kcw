---
name: develop-neo4j-graph
description: Analyze CSV data, design ontology, ingest into Neo4j, and generate Cypher queries
triggers:
  - "/develop-neo4j-graph"
  - "/graph"
  - "develop graph"
inputs:
  data_source: ""
  model_name: ""
exit_criteria:
  - "Ontology designed and validated"
  - "Data ingested into Neo4j"
  - "Cypher queries generated for required use cases"
  - "All 117 tests still pass"
---

# Develop Neo4j Graph Workflow

## Phase 1: Analyze Data
Read the data source (CSV, JSON, or existing codebase structures).
Identify entities, relationships, and properties.

## Phase 2: Design Ontology
Map entities to Neo4j nodes, relationships, and labels.
Define property types and constraints.

## Phase 3: Ingest
Write Cypher queries to:
1. Create constraints and indexes
2. Load data using `LOAD CSV` or programmatic insertion
3. Validate data integrity

## Phase 4: Query Generation
Generate parameterized Cypher queries for the required use cases:
- Entity lookup by property
- Multi-hop relationship traversal
- Aggregate analytics

## Phase 5: Verify
Run `pytest tests/ -v -W error::DeprecationWarning` to confirm no regressions.
