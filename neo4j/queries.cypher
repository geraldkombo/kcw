// ============================================================
// KCW Cypher 25 Queries with In-Index Filtering
// ============================================================

// --- Q1: Find farmers by county with in-index filtering (pre-filter) ---
// Uses Cypher 25 SEARCH with pre-filter on county before vector similarity
PROFILE
MATCH (target:FarmingHousehold {farmer_id: $farmer_id})
WITH target.embedding AS target_emb, target.county AS target_county
CALL {
  WITH target_emb, target_county
  MATCH (f:FarmingHousehold)
  WHERE f.county = target_county AND f.farmer_id <> $farmer_id
  WITH f, vector.similarity.cosine(f.embedding, target_emb) AS sim
  WHERE sim > $min_similarity
  RETURN f, sim
  ORDER BY sim DESC
  LIMIT $top_k
}
RETURN f.farmer_id, f.first_name, f.last_name, f.credit_score, sim

// --- Q2: Find farmers with similar repayment patterns (post-filter) ---
// Uses SEARCH then filters by status
PROFILE
MATCH (target:FarmingHousehold {farmer_id: $farmer_id})
WITH target.embedding AS target_emb
CALL {
  WITH target_emb
  MATCH (f:FarmingHousehold)
  WHERE f.farmer_id <> $farmer_id
  WITH f, vector.similarity.cosine(f.embedding, target_emb) AS sim
  WHERE sim > $min_similarity
  RETURN f, sim
  ORDER BY sim DESC
  LIMIT $top_k
}
WITH f, sim WHERE f.status = 'active'
RETURN f.farmer_id, f.credit_score, f.probability_default, sim

// --- Q3: Multi-hop risk traversal ---
// Farmer -> County -> other farmers in same county -> their loan performance
MATCH (f:FarmingHousehold {farmer_id: $farmer_id})-[:LOCATED_IN]->(c:County)
MATCH (c)<-[:LOCATED_IN]-(peer:FarmingHousehold)
WHERE peer.farmer_id <> $farmer_id
MATCH (peer)-[:HAS_LOAN]->(l:Loan)
RETURN c.name AS county,
       COUNT(DISTINCT peer) AS peer_farmers,
       AVG(l.amount_kes) AS avg_loan_size,
       SUM(CASE WHEN l.status = 'defaulted' THEN 1 ELSE 0 END) * 1.0 / COUNT(l) AS default_rate

// --- Q4: POLE+O entity extraction aggregation ---
// Aggregate loan performance by person, location, event, organisation
MATCH (f:FarmingHousehold)
OPTIONAL MATCH (f)-[:LOCATED_IN]->(c:County)
OPTIONAL MATCH (f)-[:MEMBER_OF]->(s:SACCO)
OPTIONAL MATCH (f)-[:HAS_LOAN]->(l:Loan)
RETURN c.name AS location,
       s.name AS organisation,
       COUNT(DISTINCT f) AS farmer_count,
       AVG(f.credit_score) AS avg_credit_score,
       AVG(l.amount_kes) AS avg_loan_amount,
       SUM(CASE WHEN l.status = 'defaulted' THEN l.amount_kes ELSE 0 END) AS total_defaulted

// --- Q5: Build securitisation pool query ---
// Gather farmers eligible for pooling (active, scored, low PD)
MATCH (f:FarmingHousehold)
WHERE f.status = 'active'
  AND f.credit_score IS NOT NULL
  AND f.probability_default < $max_pd
MATCH (f)-[:HAS_LOAN]->(l:Loan)
WHERE l.status IN ['active', 'repaid']
WITH f, l
ORDER BY f.probability_default ASC
LIMIT $pool_size
RETURN f.farmer_id, f.credit_score, f.probability_default,
       l.loan_id, l.amount_kes, l.interest_rate_annual

// --- Q6: Farmer similarity via Agent Memory trace ---
// Retrieve LOng-Term Memory entities for a given farmer (POLE+O replay)
MATCH (f:FarmingHousehold {farmer_id: $farmer_id})
OPTIONAL MATCH (f)-[:LOCATED_IN]->(c:County)
OPTIONAL MATCH (f)-[:GROWS]->(cr:Crop)
OPTIONAL MATCH (f)-[:MEMBER_OF]->(s:SACCO)
RETURN f.first_name + ' ' + f.last_name AS person,
       c.name AS location,
       cr.name AS event_crop,
       s.name AS organisation
