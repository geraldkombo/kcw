// ============================================================
// KCW Seed Data - 15 synthetic Kenyan smallholder farmers
// Matches Apollo Agriculture profile: avg loan ~KES 17,942
// ============================================================

// Counties
MERGE (c:County {name: 'Kiambu', region: 'Central'});
MERGE (c:County {name: 'Nakuru', region: 'Rift Valley'});
MERGE (c:County {name: 'Kisumu', region: 'Nyanza'});
MERGE (c:County {name: 'Meru', region: 'Eastern'});
MERGE (c:County {name: 'Machakos', region: 'Eastern'});
MERGE (c:County {name: 'Uasin Gishu', region: 'Rift Valley'});
MERGE (c:County {name: 'Homa Bay', region: 'Nyanza'});
MERGE (c:County {name: 'Bungoma', region: 'Western'});
MERGE (c:County {name: 'Kilifi', region: 'Coast'});
MERGE (c:County {name: 'Nyeri', region: 'Central'});

// Crops
MERGE (cr:Crop {name: 'maize', category: 'cereal'});
MERGE (cr:Crop {name: 'beans', category: 'legume'});
MERGE (cr:Crop {name: 'coffee', category: 'cash'});
MERGE (cr:Crop {name: 'tea', category: 'cash'});
MERGE (cr:Crop {name: 'kale', category: 'vegetable'});
MERGE (cr:Crop {name: 'avocado', category: 'fruit'});
MERGE (cr:Crop {name: 'banana', category: 'fruit'});
MERGE (cr:Crop {name: 'dairy', category: 'livestock'});
MERGE (cr:Crop {name: 'tomato', category: 'vegetable'});
MERGE (cr:Crop {name: 'sugarcane', category: 'cash'});

// SACCOs
MERGE (s:SACCO {name: 'Kiambu Farmers SACCO', county: 'Kiambu', member_count: 1200});
MERGE (s:SACCO {name: 'Nakuru North SACCO', county: 'Nakuru', member_count: 850});
MERGE (s:SACCO {name: 'Kisumu Unity SACCO', county: 'Kisumu', member_count: 2100});
MERGE (s:SACCO {name: 'Meru Central SACCO', county: 'Meru', member_count: 3400});
MERGE (s:SACCO {name: 'Machakos Green SACCO', county: 'Machakos', member_count: 950});
MERGE (s:SACCO {name: 'Bungoma Farmers SACCO', county: 'Bungoma', member_count: 670});

// Farmers (matching Apollo profile: 51% women, diverse counties)
CREATE (f:FarmingHousehold {
  farmer_id: 'KCW-001',
  first_name: 'Grace', last_name: 'Wanjiku', phone: '+254712345001',
  gender: 'F', county: 'Kiambu', sub_county: 'Gatundu', village: 'Ithanga',
  latitude: -1.0092, longitude: 36.8990,
  farm_size_ha: 2.5, primary_crop: 'maize', year_registered: 2021,
  chama_member: true, sacco_member: true, has_mpesa_account: true,
  credit_score: 68.5, probability_default: 0.12, status: 'active',
  embedding: []
});

CREATE (f:FarmingHousehold {
  farmer_id: 'KCW-002',
  first_name: 'Peter', last_name: 'Kiprop', phone: '+254712345002',
  gender: 'M', county: 'Nakuru', sub_county: 'Molo', village: 'Elburgon',
  latitude: -0.2919, longitude: 35.9522,
  farm_size_ha: 4.0, primary_crop: 'maize', year_registered: 2022,
  chama_member: false, sacco_member: false, has_mpesa_account: true,
  credit_score: 45.0, probability_default: 0.33, status: 'active',
  embedding: []
});

CREATE (f:FarmingHousehold {
  farmer_id: 'KCW-003',
  first_name: 'Achieng', last_name: 'Odhiambo', phone: '+254712345003',
  gender: 'F', county: 'Kisumu', sub_county: 'Nyando', village: 'Ahero',
  latitude: -0.1750, longitude: 34.9167,
  farm_size_ha: 1.2, primary_crop: 'kale', year_registered: 2023,
  chama_member: true, sacco_member: false, has_mpesa_account: true,
  credit_score: 72.0, probability_default: 0.08, status: 'active',
  embedding: []
});

CREATE (f:FarmingHousehold {
  farmer_id: 'KCW-004',
  first_name: 'Mwangi', last_name: 'Kimani', phone: '+254712345004',
  gender: 'M', county: 'Meru', sub_county: 'Imenti', village: 'Nkubu',
  latitude: 0.0500, longitude: 37.6500,
  farm_size_ha: 3.0, primary_crop: 'coffee', year_registered: 2020,
  chama_member: false, sacco_member: true, has_mpesa_account: true,
  credit_score: 81.0, probability_default: 0.05, status: 'active',
  embedding: []
});

CREATE (f:FarmingHousehold {
  farmer_id: 'KCW-005',
  first_name: 'Mary', last_name: 'Mutua', phone: '+254712345005',
  gender: 'F', county: 'Machakos', sub_county: 'Mwala', village: 'Mbaani',
  latitude: -1.5167, longitude: 37.3333,
  farm_size_ha: 2.0, primary_crop: 'beans', year_registered: 2022,
  chama_member: true, sacco_member: false, has_mpesa_account: true,
  credit_score: 55.0, probability_default: 0.22, status: 'active',
  embedding: []
});

CREATE (f:FarmingHousehold {
  farmer_id: 'KCW-006',
  first_name: 'Jane', last_name: 'Chebet', phone: '+254712345006',
  gender: 'F', county: 'Uasin Gishu', sub_county: 'Ainabkoi', village: 'Kapsaos',
  latitude: 0.5160, longitude: 35.2800,
  farm_size_ha: 5.0, primary_crop: 'maize', year_registered: 2021,
  chama_member: true, sacco_member: true, has_mpesa_account: true,
  credit_score: 76.5, probability_default: 0.09, status: 'active',
  embedding: []
});

CREATE (f:FarmingHousehold {
  farmer_id: 'KCW-007',
  first_name: 'Benard', last_name: 'Ochieng', phone: '+254712345007',
  gender: 'M', county: 'Homa Bay', sub_county: 'Rachuonyo', village: 'Kendu Bay',
  latitude: -0.3667, longitude: 34.6500,
  farm_size_ha: 1.5, primary_crop: 'banana', year_registered: 2023,
  chama_member: true, sacco_member: false, has_mpesa_account: true,
  credit_score: 38.0, probability_default: 0.42, status: 'active',
  embedding: []
});

CREATE (f:FarmingHousehold {
  farmer_id: 'KCW-008',
  first_name: 'Sarah', last_name: 'Wekesa', phone: '+254712345008',
  gender: 'F', county: 'Bungoma', sub_county: 'Kanduyi', village: 'Chwele',
  latitude: 0.6583, longitude: 34.5847,
  farm_size_ha: 2.8, primary_crop: 'sugarcane', year_registered: 2022,
  chama_member: true, sacco_member: true, has_mpesa_account: true,
  credit_score: 61.0, probability_default: 0.17, status: 'active',
  embedding: []
});

CREATE (f:FarmingHousehold {
  farmer_id: 'KCW-009',
  first_name: 'Joseph', last_name: 'Nyaga', phone: '+254712345009',
  gender: 'M', county: 'Meru', sub_county: 'Tigania', village: 'Mikinduri',
  latitude: 0.1167, longitude: 37.9667,
  farm_size_ha: 1.0, primary_crop: 'avocado', year_registered: 2024,
  chama_member: false, sacco_member: false, has_mpesa_account: true,
  credit_score: 42.0, probability_default: 0.38, status: 'active',
  embedding: []
});

CREATE (f:FarmingHousehold {
  farmer_id: 'KCW-010',
  first_name: 'Faith', last_name: 'Njeri', phone: '+254712345010',
  gender: 'F', county: 'Nyeri', sub_county: 'Othaya', village: 'Kieni',
  latitude: -0.2833, longitude: 36.9500,
  farm_size_ha: 1.8, primary_crop: 'tea', year_registered: 2021,
  chama_member: true, sacco_member: true, has_mpesa_account: true,
  credit_score: 85.0, probability_default: 0.03, status: 'active',
  embedding: []
});

CREATE (f:FarmingHousehold {
  farmer_id: 'KCW-011',
  first_name: 'David', last_name: 'Kiplagat', phone: '+254712345011',
  gender: 'M', county: 'Nakuru', sub_county: 'Naivasha', village: 'Karunga',
  latitude: -0.7167, longitude: 36.4333,
  farm_size_ha: 6.0, primary_crop: 'dairy', year_registered: 2020,
  chama_member: false, sacco_member: true, has_mpesa_account: true,
  credit_score: 73.0, probability_default: 0.10, status: 'active',
  embedding: []
});

CREATE (f:FarmingHousehold {
  farmer_id: 'KCW-012',
  first_name: 'Agnes', last_name: 'Mwikali', phone: '+254712345012',
  gender: 'F', county: 'Kilifi', sub_county: 'Magarini', village: 'Gongoni',
  latitude: -3.0167, longitude: 39.9667,
  farm_size_ha: 0.8, primary_crop: 'tomato', year_registered: 2023,
  chama_member: true, sacco_member: false, has_mpesa_account: true,
  credit_score: 33.0, probability_default: 0.48, status: 'delinquent',
  embedding: []
});

CREATE (f:FarmingHousehold {
  farmer_id: 'KCW-013',
  first_name: 'Samuel', last_name: 'Kipruto', phone: '+254712345013',
  gender: 'M', county: 'Uasin Gishu', sub_county: 'Turbo', village: 'Eldoret',
  latitude: 0.5167, longitude: 35.2667,
  farm_size_ha: 7.0, primary_crop: 'maize', year_registered: 2020,
  chama_member: false, sacco_member: true, has_mpesa_account: true,
  credit_score: 90.0, probability_default: 0.02, status: 'completed',
  embedding: []
});

CREATE (f:FarmingHousehold {
  farmer_id: 'KCW-014',
  first_name: 'Beatrice', last_name: 'Akinyi', phone: '+254712345014',
  gender: 'F', county: 'Kisumu', sub_county: 'Kisumu West', village: 'Kogony',
  latitude: -0.0892, longitude: 34.7500,
  farm_size_ha: 1.0, primary_crop: 'kale', year_registered: 2024,
  chama_member: true, sacco_member: false, has_mpesa_account: true,
  credit_score: 48.0, probability_default: 0.28, status: 'active',
  embedding: []
});

CREATE (f:FarmingHousehold {
  farmer_id: 'KCW-015',
  first_name: 'Patrick', last_name: 'Muchiri', phone: '+254712345015',
  gender: 'M', county: 'Kiambu', sub_county: 'Thika', village: 'Juja',
  latitude: -1.1000, longitude: 37.0167,
  farm_size_ha: 2.0, primary_crop: 'avocado', year_registered: 2022,
  chama_member: true, sacco_member: true, has_mpesa_account: true,
  credit_score: 65.0, probability_default: 0.14, status: 'active',
  embedding: []
});

// ---- Relationships ----
// Connect farmers to counties, crops, SACCOS
// KCW-001 (Grace, Kiambu, maize, Kiambu Farmers SACCO)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-001'})
MATCH (c:County {name: 'Kiambu'})
MATCH (cr:Crop {name: 'maize'})
MATCH (s:SACCO {name: 'Kiambu Farmers SACCO'})
CREATE (f)-[:LOCATED_IN]->(c)
CREATE (f)-[:GROWS]->(cr)
CREATE (f)-[:MEMBER_OF]->(s);

// KCW-002 (Peter, Nakuru, maize)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-002'})
MATCH (c:County {name: 'Nakuru'})
MATCH (cr:Crop {name: 'maize'})
CREATE (f)-[:LOCATED_IN]->(c)
CREATE (f)-[:GROWS]->(cr);

// KCW-003 (Achieng, Kisumu, kale Kasumu Unity SACCO)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-003'})
MATCH (c:County {name: 'Kisumu'})
MATCH (cr:Crop {name: 'kale'})
MATCH (s:SACCO {name: 'Kisumu Unity SACCO'})
CREATE (f)-[:LOCATED_IN]->(c)
CREATE (f)-[:GROWS]->(cr)
CREATE (f)-[:MEMBER_OF]->(s);

// KCW-004 (Mwangi, Meru, coffee, Meru Central SACCO)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-004'})
MATCH (c:County {name: 'Meru'})
MATCH (cr:Crop {name: 'coffee'})
MATCH (s:SACCO {name: 'Meru Central SACCO'})
CREATE (f)-[:LOCATED_IN]->(c)
CREATE (f)-[:GROWS]->(cr)
CREATE (f)-[:MEMBER_OF]->(s);

// KCW-005 (Mary, Machakos, beans Machakos Green SACCO)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-005'})
MATCH (c:County {name: 'Machakos'})
MATCH (cr:Crop {name: 'beans'})
MATCH (s:SACCO {name: 'Machakos Green SACCO'})
CREATE (f)-[:LOCATED_IN]->(c)
CREATE (f)-[:GROWS]->(cr)
CREATE (f)-[:MEMBER_OF]->(s);

// KCW-006 (Jane, Uasin Gishu, maize, Nakuru North SACCO)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-006'})
MATCH (c:County {name: 'Uasin Gishu'})
MATCH (cr:Crop {name: 'maize'})
MATCH (s:SACCO {name: 'Nakuru North SACCO'})
CREATE (f)-[:LOCATED_IN]->(c)
CREATE (f)-[:GROWS]->(cr)
CREATE (f)-[:MEMBER_OF]->(s);

// KCW-007 (Benard, Homa Bay, banana)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-007'})
MATCH (c:County {name: 'Homa Bay'})
MATCH (cr:Crop {name: 'banana'})
CREATE (f)-[:LOCATED_IN]->(c)
CREATE (f)-[:GROWS]->(cr);

// KCW-008 (Sarah, Bungoma, sugarcane, Bungoma Farmers SACCO)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-008'})
MATCH (c:County {name: 'Bungoma'})
MATCH (cr:Crop {name: 'sugarcane'})
MATCH (s:SACCO {name: 'Bungoma Farmers SACCO'})
CREATE (f)-[:LOCATED_IN]->(c)
CREATE (f)-[:GROWS]->(cr)
CREATE (f)-[:MEMBER_OF]->(s);

// KCW-009 (Joseph, Meru, avocado)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-009'})
MATCH (c:County {name: 'Meru'})
MATCH (cr:Crop {name: 'avocado'})
CREATE (f)-[:LOCATED_IN]->(c)
CREATE (f)-[:GROWS]->(cr);

// KCW-010 (Faith, Nyeri, tea, Kiambu Farmers SACCO)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-010'})
MATCH (c:County {name: 'Nyeri'})
MATCH (cr:Crop {name: 'tea'})
MATCH (s:SACCO {name: 'Kiambu Farmers SACCO'})
CREATE (f)-[:LOCATED_IN]->(c)
CREATE (f)-[:GROWS]->(cr)
CREATE (f)-[:MEMBER_OF]->(s);

// KCW-011 (David, Nakuru, dairy, Nakuru North SACCO)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-011'})
MATCH (c:County {name: 'Nakuru'})
MATCH (cr:Crop {name: 'dairy'})
MATCH (s:SACCO {name: 'Nakuru North SACCO'})
CREATE (f)-[:LOCATED_IN]->(c)
CREATE (f)-[:GROWS]->(cr)
CREATE (f)-[:MEMBER_OF]->(s);

// KCW-012 (Agnes, Kilifi, tomato)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-012'})
MATCH (c:County {name: 'Kilifi'})
MATCH (cr:Crop {name: 'tomato'})
CREATE (f)-[:LOCATED_IN]->(c)
CREATE (f)-[:GROWS]->(cr);

// KCW-013 (Samuel, Uasin Gishu, maize, Meru Central SACCO)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-013'})
MATCH (c:County {name: 'Uasin Gishu'})
MATCH (cr:Crop {name: 'maize'})
MATCH (s:SACCO {name: 'Meru Central SACCO'})
CREATE (f)-[:LOCATED_IN]->(c)
CREATE (f)-[:GROWS]->(cr)
CREATE (f)-[:MEMBER_OF]->(s);

// KCW-014 (Beatrice, Kisumu, kale)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-014'})
MATCH (c:County {name: 'Kisumu'})
MATCH (cr:Crop {name: 'kale'})
CREATE (f)-[:LOCATED_IN]->(c)
CREATE (f)-[:GROWS]->(cr);

// KCW-015 (Patrick, Kiambu, avocado, Kiambu Farmers SACCO)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-015'})
MATCH (c:County {name: 'Kiambu'})
MATCH (cr:Crop {name: 'avocado'})
MATCH (s:SACCO {name: 'Kiambu Farmers SACCO'})
CREATE (f)-[:LOCATED_IN]->(c)
CREATE (f)-[:GROWS]->(cr)
CREATE (f)-[:MEMBER_OF]->(s);

// ---- Loans (avg ~KES 17,942 matching Apollo data) ----
// Grace Wanjiku - 2 loans
MATCH (f:FarmingHousehold {farmer_id: 'KCW-001'})
CREATE (l:Loan {
  loan_id: 'LN-001', farmer_id: 'KCW-001', amount_kes: 18000,
  purpose: 'seeds', term_months: 6, interest_rate_annual: 18.0,
  status: 'repaid', pd_at_origination: 0.12,
  disbursement_date: date('2024-01-15'), due_date: date('2024-07-15'),
  amount_repaid_kes: 18000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

MATCH (f:FarmingHousehold {farmer_id: 'KCW-001'})
CREATE (l:Loan {
  loan_id: 'LN-002', farmer_id: 'KCW-001', amount_kes: 25000,
  purpose: 'fertiliser', term_months: 6, interest_rate_annual: 18.0,
  status: 'active', pd_at_origination: 0.10,
  disbursement_date: date('2025-02-01'), due_date: date('2025-08-01'),
  amount_repaid_kes: 12500, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

// Peter Kiprop - 1 loan
MATCH (f:FarmingHousehold {farmer_id: 'KCW-002'})
CREATE (l:Loan {
  loan_id: 'LN-003', farmer_id: 'KCW-002', amount_kes: 30000,
  purpose: 'equipment', term_months: 12, interest_rate_annual: 22.0,
  status: 'active', pd_at_origination: 0.33,
  disbursement_date: date('2024-10-01'), due_date: date('2025-10-01'),
  amount_repaid_kes: 10000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

// Achieng Odhiambo - 1 loan
MATCH (f:FarmingHousehold {farmer_id: 'KCW-003'})
CREATE (l:Loan {
  loan_id: 'LN-004', farmer_id: 'KCW-003', amount_kes: 12000,
  purpose: 'seeds', term_months: 6, interest_rate_annual: 16.0,
  status: 'repaid', pd_at_origination: 0.08,
  disbursement_date: date('2024-06-01'), due_date: date('2024-12-01'),
  amount_repaid_kes: 12000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

// Mwangi Kimani - 2 loans
MATCH (f:FarmingHousehold {farmer_id: 'KCW-004'})
CREATE (l:Loan {
  loan_id: 'LN-005', farmer_id: 'KCW-004', amount_kes: 45000,
  purpose: 'equipment', term_months: 12, interest_rate_annual: 15.0,
  status: 'repaid', pd_at_origination: 0.05,
  disbursement_date: date('2023-03-01'), due_date: date('2024-03-01'),
  amount_repaid_kes: 45000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

MATCH (f:FarmingHousehold {farmer_id: 'KCW-004'})
CREATE (l:Loan {
  loan_id: 'LN-006', farmer_id: 'KCW-004', amount_kes: 60000,
  purpose: 'irrigation', term_months: 18, interest_rate_annual: 15.0,
  status: 'active', pd_at_origination: 0.04,
  disbursement_date: date('2025-01-10'), due_date: date('2026-07-10'),
  amount_repaid_kes: 20000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

// Mary Mutua - 1 loan
MATCH (f:FarmingHousehold {farmer_id: 'KCW-005'})
CREATE (l:Loan {
  loan_id: 'LN-007', farmer_id: 'KCW-005', amount_kes: 8000,
  purpose: 'seeds', term_months: 6, interest_rate_annual: 20.0,
  status: 'active', pd_at_origination: 0.22,
  disbursement_date: date('2025-03-15'), due_date: date('2025-09-15'),
  amount_repaid_kes: 3000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

// Jane Chebet - 1 loan
MATCH (f:FarmingHousehold {farmer_id: 'KCW-006'})
CREATE (l:Loan {
  loan_id: 'LN-008', farmer_id: 'KCW-006', amount_kes: 35000,
  purpose: 'equipment', term_months: 12, interest_rate_annual: 18.0,
  status: 'repaid', pd_at_origination: 0.09,
  disbursement_date: date('2024-02-01'), due_date: date('2025-02-01'),
  amount_repaid_kes: 35000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

// Benard Ochieng - 1 loan (delinquent)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-007'})
CREATE (l:Loan {
  loan_id: 'LN-009', farmer_id: 'KCW-007', amount_kes: 15000,
  purpose: 'seeds', term_months: 6, interest_rate_annual: 24.0,
  status: 'defaulted', pd_at_origination: 0.42,
  disbursement_date: date('2024-08-01'), due_date: date('2025-02-01'),
  amount_repaid_kes: 4000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

// Sarah Wekesa - 1 loan
MATCH (f:FarmingHousehold {farmer_id: 'KCW-008'})
CREATE (l:Loan {
  loan_id: 'LN-010', farmer_id: 'KCW-008', amount_kes: 20000,
  purpose: 'seeds', term_months: 6, interest_rate_annual: 18.0,
  status: 'active', pd_at_origination: 0.17,
  disbursement_date: date('2025-01-20'), due_date: date('2025-07-20'),
  amount_repaid_kes: 10000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

// Joseph Nyaga - 1 loan
MATCH (f:FarmingHousehold {farmer_id: 'KCW-009'})
CREATE (l:Loan {
  loan_id: 'LN-011', farmer_id: 'KCW-009', amount_kes: 7000,
  purpose: 'seeds', term_months: 6, interest_rate_annual: 22.0,
  status: 'active', pd_at_origination: 0.38,
  disbursement_date: date('2025-04-01'), due_date: date('2025-10-01'),
  amount_repaid_kes: 0, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

// Faith Njeri - 2 loans
MATCH (f:FarmingHousehold {farmer_id: 'KCW-010'})
CREATE (l:Loan {
  loan_id: 'LN-012', farmer_id: 'KCW-010', amount_kes: 22000,
  purpose: 'fertiliser', term_months: 6, interest_rate_annual: 15.0,
  status: 'repaid', pd_at_origination: 0.03,
  disbursement_date: date('2024-05-15'), due_date: date('2024-11-15'),
  amount_repaid_kes: 22000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

MATCH (f:FarmingHousehold {farmer_id: 'KCW-010'})
CREATE (l:Loan {
  loan_id: 'LN-013', farmer_id: 'KCW-010', amount_kes: 30000,
  purpose: 'equipment', term_months: 12, interest_rate_annual: 15.0,
  status: 'active', pd_at_origination: 0.02,
  disbursement_date: date('2025-02-15'), due_date: date('2026-02-15'),
  amount_repaid_kes: 15000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

// David Kiplagat - 1 loan
MATCH (f:FarmingHousehold {farmer_id: 'KCW-011'})
CREATE (l:Loan {
  loan_id: 'LN-014', farmer_id: 'KCW-011', amount_kes: 50000,
  purpose: 'livestock', term_months: 18, interest_rate_annual: 16.0,
  status: 'active', pd_at_origination: 0.10,
  disbursement_date: date('2024-11-01'), due_date: date('2026-05-01'),
  amount_repaid_kes: 15000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

// Agnes Mwikali - 1 loan (defaulted)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-012'})
CREATE (l:Loan {
  loan_id: 'LN-015', farmer_id: 'KCW-012', amount_kes: 5000,
  purpose: 'seeds', term_months: 6, interest_rate_annual: 25.0,
  status: 'defaulted', pd_at_origination: 0.48,
  disbursement_date: date('2024-04-01'), due_date: date('2024-10-01'),
  amount_repaid_kes: 1000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

// Samuel Kipruto - 2 loans (completed)
MATCH (f:FarmingHousehold {farmer_id: 'KCW-013'})
CREATE (l:Loan {
  loan_id: 'LN-016', farmer_id: 'KCW-013', amount_kes: 80000,
  purpose: 'equipment', term_months: 24, interest_rate_annual: 14.0,
  status: 'repaid', pd_at_origination: 0.02,
  disbursement_date: date('2022-06-01'), due_date: date('2024-06-01'),
  amount_repaid_kes: 80000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

MATCH (f:FarmingHousehold {farmer_id: 'KCW-013'})
CREATE (l:Loan {
  loan_id: 'LN-017', farmer_id: 'KCW-013', amount_kes: 100000,
  purpose: 'irrigation', term_months: 24, interest_rate_annual: 14.0,
  status: 'repaid', pd_at_origination: 0.01,
  disbursement_date: date('2023-01-10'), due_date: date('2025-01-10'),
  amount_repaid_kes: 100000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

// Beatrice Akinyi - 1 loan
MATCH (f:FarmingHousehold {farmer_id: 'KCW-014'})
CREATE (l:Loan {
  loan_id: 'LN-018', farmer_id: 'KCW-014', amount_kes: 10000,
  purpose: 'seeds', term_months: 6, interest_rate_annual: 20.0,
  status: 'active', pd_at_origination: 0.28,
  disbursement_date: date('2025-03-01'), due_date: date('2025-09-01'),
  amount_repaid_kes: 3000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);

// Patrick Muchiri - 1 loan
MATCH (f:FarmingHousehold {farmer_id: 'KCW-015'})
CREATE (l:Loan {
  loan_id: 'LN-019', farmer_id: 'KCW-015', amount_kes: 16000,
  purpose: 'seeds', term_months: 6, interest_rate_annual: 18.0,
  status: 'repaid', pd_at_origination: 0.14,
  disbursement_date: date('2024-09-01'), due_date: date('2025-03-01'),
  amount_repaid_kes: 16000, purpose_embedding: []
})
CREATE (f)-[:HAS_LOAN]->(l);
