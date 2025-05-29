import os

API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
INPUT_CSV = 'MT15_data_export.csv'
OUTPUT_CSV = 'nap_audit_results_cleaned.csv'

# Matching thresholds
NAME_MATCH_THRESHOLD = 0.8
ADDRESS_MATCH_THRESHOLD = 0.85