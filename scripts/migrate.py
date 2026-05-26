#!/usr/bin/env python3
"""Neo4j schema migration & seed data loader.

Usage:
    python scripts/migrate.py          # apply schema only
    python scripts/migrate.py --seed    # apply schema + seed demo data
    python scripts/migrate.py --drop    # drop all constraints + nodes
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime, timezone

from neo4j import GraphDatabase, exceptions as neo4j_exc

from config.settings import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("migrate")

SCHEMA = [
    # Constraints
    "CREATE CONSTRAINT IF NOT EXISTS FOR (f:FarmingHousehold) REQUIRE f.farmer_id IS UNIQUE",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (l:Loan) REQUIRE l.loan_id IS UNIQUE",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Pool) REQUIRE p.pool_id IS UNIQUE",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (a:AuditEntry) REQUIRE a.entry_id IS UNIQUE",
    "CREATE INDEX IF NOT EXISTS FOR (f:FarmingHousehold) ON (f.county)",
    "CREATE INDEX IF NOT EXISTS FOR (f:FarmingHousehold) ON (f.status)",
    "CREATE INDEX IF NOT EXISTS FOR (l:Loan) ON (l.status)",
    "CREATE INDEX IF NOT EXISTS FOR (l:Loan) ON (l.farmer_id)",
    # Node properties via MERGE patterns (run idempotently)
]


def get_driver():
    return GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
        max_connection_pool_size=5,
    )


def apply_schema(driver):
    logger.info("applying schema...")
    for cypher in SCHEMA:
        try:
            driver.execute_query(cypher)
            logger.debug("OK: %s", cypher[:80])
        except neo4j_exc.CypherSyntaxError as e:
            logger.error("syntax error: %s", e)
            raise
    logger.info("schema applied")


def drop_all(driver):
    logger.warning("DROPPING all constraints and nodes...")
    constraints = driver.execute_query("SHOW CONSTRAINTS")
    for c in constraints.records:
        name = c["name"]
        driver.execute_query(f"DROP CONSTRAINT {name}")
        logger.info("dropped constraint: %s", name)
    driver.execute_query("MATCH (n) DETACH DELETE n")
    logger.info("all nodes deleted")


def seed_data(driver):
    logger.info("seeding demo data...")
    farmers = [
        {
            "farmer_id": "KCW-SEED001",
            "name": "Grace Wanjiku",
            "county": "Kiambu",
            "farm_size_ha": 2.5,
            "year_registered": 2021,
            "chama_member": True,
            "sacco_member": True,
            "mpesa_velocity": 15000,
            "gender": "female",
            "status": "approved",
        },
        {
            "farmer_id": "KCW-SEED002",
            "name": "John Kamau",
            "county": "Nakuru",
            "farm_size_ha": 1.2,
            "year_registered": 2023,
            "chama_member": False,
            "sacco_member": True,
            "mpesa_velocity": 8000,
            "gender": "male",
            "status": "pending",
        },
    ]
    for f in farmers:
        driver.execute_query(
            """
            MERGE (f:FarmingHousehold {farmer_id: $farmer_id})
            SET f.name = $name,
                f.county = $county,
                f.farm_size_ha = $farm_size_ha,
                f.year_registered = $year_registered,
                f.chama_member = $chama_member,
                f.sacco_member = $sacco_member,
                f.mpesa_velocity = $mpesa_velocity,
                f.gender = $gender,
                f.status = $status,
                f.created_at = $created_at
            """,
            parameters={**f, "created_at": datetime.now(timezone.utc).isoformat()},
        )
        logger.info("seeded farmer: %s (%s)", f["name"], f["farmer_id"])


def main():
    parser = argparse.ArgumentParser(description="Neo4j migration tool")
    parser.add_argument("--seed", action="store_true", help="seed demo data")
    parser.add_argument("--drop", action="store_true", help="drop all data")
    args = parser.parse_args()

    try:
        driver = get_driver()
        driver.verify_connectivity()
        logger.info("connected to Neo4j at %s", settings.neo4j_uri)
    except neo4j_exc.AuthError:
        logger.error("authentication failed — check NEO4J_USER/NEO4J_PASSWORD")
        sys.exit(1)
    except neo4j_exc.ServiceUnavailable:
        logger.error("Neo4j unreachable at %s", settings.neo4j_uri)
        sys.exit(1)

    if args.drop:
        drop_all(driver)

    apply_schema(driver)

    if args.seed:
        seed_data(driver)

    driver.close()
    logger.info("done")


if __name__ == "__main__":
    main()
