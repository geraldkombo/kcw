"""Model catalogue for Featherless API access.
All models verified available as of May 2026.
"""

MODEL_CATALOGUE = {
    "deepseek-v4-pro": {
        "id": "deepseek/deepseek-v4-pro",
        "params": "862B",
        "added": "April 2026",
        "context": 32768,
        "use_case": "Primary credit risk reasoning, graph traversal planning",
    },
    "gemma-4-27b": {
        "id": "google/gemma-4-27b-it",
        "params": "31B",
        "added": "March 2026",
        "context": 8192,
        "use_case": "Multilingual farmer intake (Swahili, Sheng, English), UI generation",
    },
    "minimax-m2.5": {
        "id": "minimax/minimax-m2.5",
        "params": "unknown",
        "added": "2026",
        "context": 16384,
        "use_case": "Geo-spatial analysis, climate stress assessment, default fallback",
    },
}
