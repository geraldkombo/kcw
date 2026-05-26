// Kilimo Credit Web - Neo4j Graph Schema
// Cypher 25 compatible with AuraDB Free Tier

// ---- Constraints (uniqueness & existence) ----
CREATE CONSTRAINT farmer_id_unique IF NOT EXISTS FOR (f:FarmingHousehold) REQUIRE f.farmer_id IS UNIQUE;
CREATE CONSTRAINT loan_id_unique IF NOT EXISTS FOR (l:Loan) REQUIRE l.loan_id IS UNIQUE;
CREATE CONSTRAINT county_id_unique IF NOT EXISTS FOR (c:County) REQUIRE c.name IS UNIQUE;
CREATE CONSTRAINT crop_id_unique IF NOT EXISTS FOR (c:Crop) REQUIRE c.name IS UNIQUE;
CREATE CONSTRAINT sacco_id_unique IF NOT EXISTS FOR (s:SACCO) REQUIRE s.name IS UNIQUE;
CREATE CONSTRAINT pool_id_unique IF NOT EXISTS FOR (p:SecuritisationPool) REQUIRE p.pool_id IS UNIQUE;

CREATE CONSTRAINT farmer_exists IF NOT EXISTS FOR (f:FarmingHousehold) REQUIRE f.farmer_id IS NOT NULL;
CREATE CONSTRAINT loan_exists IF NOT EXISTS FOR (l:Loan) REQUIRE l.loan_id IS NOT NULL;

// ---- Vector index for semantic farmer search (1536d for text-embedding-3-small) ----
CREATE VECTOR INDEX farmer_embedding_idx IF NOT EXISTS
  FOR (f:FarmingHousehold) ON (f.embedding)
  OPTIONS { indexConfig: { "vector.dimensions": 1536, "vector.similarity_function": "cosine" } };

CREATE VECTOR INDEX loan_embedding_idx IF NOT EXISTS
  FOR (l:Loan) ON (l.purpose_embedding)
  OPTIONS { indexConfig: { "vector.dimensions": 1536, "vector.similarity_function": "cosine" } };

// ---- Node labels & properties documented below (schema is implicit) ----
// :FarmingHousehold {
//   farmer_id: STRING,
//   first_name: STRING,
//   last_name: STRING,
//   phone: STRING,
//   gender: STRING ("M"/"F"),
//   county: STRING,
//   sub_county: STRING,
//   village: STRING,
//   latitude: FLOAT,
//   longitude: FLOAT,
//   farm_size_ha: FLOAT,
//   primary_crop: STRING,
//   year_registered: INTEGER,
//   chama_member: BOOLEAN,
//   sacco_member: BOOLEAN,
//   has_mpesa_account: BOOLEAN,
//   credit_score: FLOAT,
//   probability_default: FLOAT,
//   status: STRING,
//   embedding: LIST[FLOAT]  // 1536d
// }
//
// :Loan {
//   loan_id: STRING,
//   farmer_id: STRING,
//   amount_kes: FLOAT,
//   purpose: STRING,
//   term_months: INTEGER,
//   interest_rate_annual: FLOAT,
//   status: STRING,
//   pd_at_origination: FLOAT,
//   disbursement_date: DATE,
//   due_date: DATE,
//   amount_repaid_kes: FLOAT,
//   purpose_embedding: LIST[FLOAT]  // 1536d
// }
//
// :County { name: STRING, region: STRING }
// :Crop { name: STRING, category: STRING }
// :SACCO { name: STRING, county: STRING, member_count: INTEGER }
// :SecuritisationPool { pool_id: STRING, status: STRING, total_notional_kes: FLOAT }
//
// ---- Relationships ----
// (f:FarmingHousehold)-[:HAS_LOAN]->(l:Loan)
// (f)-[:LOCATED_IN]->(c:County)
// (f)-[:GROWS]->(cr:Crop)
// (f)-[:MEMBER_OF]->(s:SACCO)
// (l)-[:PART_OF]->(p:SecuritisationPool)
// (f)-[:SIMILAR_TO {score: FLOAT}]->(f)   // via vector similarity
