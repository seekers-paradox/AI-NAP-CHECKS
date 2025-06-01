import re
import pandas as pd
from difflib import SequenceMatcher
from typing import Tuple

class TextMatcher:
    """Utility class for text matching and normalization."""
    
    @staticmethod
    def normalize_phone(phone) -> str:
        """Normalize phone number to digits only."""
        if not phone or pd.isna(phone):
            return ""
        digits_only = re.sub(r'\D', '', str(phone))
        if len(digits_only) > 10:
            digits_only = digits_only[-10:]
        return digits_only
    
    @staticmethod
    def similarity_ratio(a: str, b: str) -> float:
        """Calculate similarity ratio between two strings."""
        if not a or not b:
            return 0.0
        return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()
    
    @staticmethod
    def normalize_text_for_comparison(text) -> str:
        """Normalize text for comparison by removing special characters."""
        if not text or pd.isna(text):
            return ""
        normalized = re.sub(r'[^\w\s]', ' ', str(text).lower())
        normalized = ' '.join(normalized.split())
        return normalized
    
    @classmethod
    def check_name_match(cls, input_name: str, api_name: str, threshold: float = 0.8) -> Tuple[bool, float]:
        """Check if two business names match."""
        norm_input = cls.normalize_text_for_comparison(input_name)
        norm_api = cls.normalize_text_for_comparison(api_name)
        similarity = cls.similarity_ratio(norm_input, norm_api)
        contains_match = (norm_input in norm_api) or (norm_api in norm_input)
        return (similarity >= threshold) or contains_match, similarity
    
    @classmethod
    def check_address_match(cls, input_address: str, api_address: str, threshold: float = 0.85) -> Tuple[bool, float]:
        """Check if two addresses match."""
        norm_input = cls.normalize_text_for_comparison(input_address)
        norm_api = cls.normalize_text_for_comparison(api_address)
        similarity = cls.similarity_ratio(norm_input, norm_api)
        
        # Component-based matching
        input_parts = norm_input.split()
        api_parts = norm_api.split()
        key_matches = sum(1 for part in input_parts 
                         if len(part) > 2 and any(part in api_part for api_part in api_parts))
        
        component_match_ratio = key_matches / max(len(input_parts), 1) if input_parts else 0
        
        return (similarity >= threshold) or (component_match_ratio >= 0.7), max(similarity, component_match_ratio)
    
    @classmethod
    def check_phone_match(cls, input_phone: str, api_phone: str) -> Tuple[bool, float]:
        """Check if two phone numbers match."""
        norm_input = cls.normalize_phone(input_phone)
        norm_api = cls.normalize_phone(api_phone)
        
        if not norm_input or not norm_api:
            return False, 0.0
        
        if norm_input == norm_api:
            return True, 1.0
        
        if norm_input in norm_api or norm_api in norm_input:
            return True, 0.9
        
        return False, 0.0