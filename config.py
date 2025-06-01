import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """Configuration settings for the NAP audit system."""
    GOOGLE_PLACES_API_KEY: str = os.getenv("GOOGLE_PLACES_API_KEY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    INPUT_CSV: str = 'MT15_data_export.csv'
    OUTPUT_CSV: str = 'nap_audit_results_cleaned.csv'
    NAME_MATCH_THRESHOLD: float = 0.8
    ADDRESS_MATCH_THRESHOLD: float = 0.85
    REQUEST_DELAY: float = 1.0  # Seconds between API calls
    REQUEST_TIMEOUT: int = 10   # Request timeout in seconds