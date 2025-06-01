# nap_matcher.py
from typing import List
from models import BusinessData, PlaceData, MatchResult
from text_utils import TextMatcher
from config import Config

class NAPMatcher:
    """Handles Name, Address, Phone (NAP) matching logic."""
    
    def __init__(self, config: Config):
        self.config = config
        self.text_matcher = TextMatcher()
    
    def match_business_to_place(self, business: BusinessData, place: PlaceData) -> MatchResult:
        """Match a business to a place and return detailed results."""
        name_match, name_sim = self.text_matcher.check_name_match(
            business.name, place.name, self.config.NAME_MATCH_THRESHOLD
        )
        
        address_match, address_sim = self.text_matcher.check_address_match(
            business.address, place.address, self.config.ADDRESS_MATCH_THRESHOLD
        )
        
        phone_match, phone_sim = self.text_matcher.check_phone_match(
            business.phone, place.phone
        )
        
        overall_status = self._determine_overall_status(
            name_match, address_match, phone_match, name_sim, address_sim, phone_sim
        )
        
        return MatchResult(
            input_business=business,
            api_place=place,
            name_match=name_match,
            address_match=address_match,
            phone_match=phone_match,
            name_similarity=name_sim,
            address_similarity=address_sim,
            phone_similarity=phone_sim,
            overall_status=overall_status
        )
    
    def _determine_overall_status(self, name_match: bool, address_match: bool, phone_match: bool,
                                name_sim: float, address_sim: float, phone_sim: float) -> str:
        """Determine the overall matching status based on individual matches."""
        if name_match and address_match and phone_match:
            return "SUCCESS - All NAP data matches"
        elif name_match and address_match:
            return "SUCCESS - Name & Address match (Phone missing/different)"
        elif name_match and phone_match:
            return "PARTIAL - Name & Phone match (Address different)"
        elif address_match and phone_match:
            return "PARTIAL - Address & Phone match (Name different)"
        elif name_match:
            return "PARTIAL - Only Name matches"
        elif (name_sim >= 0.95 and address_sim >= 0.95) or (name_sim >= 0.95 and phone_sim >= 0.95):
            return "SUCCESS - 95%+ similarity match"
        else:
            return "FAIL - Significant NAP inconsistencies"