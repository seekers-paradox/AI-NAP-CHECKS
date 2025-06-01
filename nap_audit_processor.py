import pandas as pd
import time
from typing import List
from models import BusinessData, MatchResult
from google_places_client import GooglePlacesClient
from nap_matcher import NAPMatcher
from ai_matcher import AIBusinessMatcher
from config import Config

class NAPAuditProcessor:
    """Main processor for NAP audit operations."""
    
    def __init__(self, config: Config):
        self.config = config
        self.google_client = GooglePlacesClient(config)
        self.nap_matcher = NAPMatcher(config)
        self.ai_matcher = AIBusinessMatcher(config)
    
    def process_csv(self) -> List[MatchResult]:
        """Process the input CSV and return match results."""
        df = pd.read_csv(self.config.INPUT_CSV)
        df.columns = [col.strip() for col in df.columns]
        results = []
        
        print(f"Processing {len(df)} records...")
        
        for index, row in df.iterrows():
            business = BusinessData.from_csv_row(row)
            print(f"Searching for: {business.name} ({index+1}/{len(df)})")
            
            try:
                result = self._process_single_business(business)
                results.append(result)
                print(f"   {result.overall_status}")
                
                # Rate limiting
                time.sleep(self.config.REQUEST_DELAY)
                
            except Exception as e:
                error_result = self._create_error_result(business, str(e))
                results.append(error_result)
                print(f"Error processing {business.name}: {str(e)}")
        
        return results
    
    def _process_single_business(self, business: BusinessData) -> MatchResult:
        """Process a single business record."""
        query = f"{business.name} {business.address}"
        place = self.google_client.search_and_get_details(query)
        
        if not place:
            return self._create_no_results_result(business)
        
        result = self.nap_matcher.match_business_to_place(business, place)
        
        # Optional AI verification for ambiguous cases
        if result.overall_status.startswith("PARTIAL") or result.overall_status.startswith("FAIL"):
            ai_match = self.ai_matcher.is_match(
                business.name, business.address, place.name, place.address
            )
            if ai_match:
                print("   ✅ AI confirmed match!")
            else:
                print("   ❌ AI confirmed no match")
        
        return result
    
    def _create_no_results_result(self, business: BusinessData) -> MatchResult:
        """Create a result for when no Google Places results are found."""
        from models import PlaceData
        empty_place = PlaceData(name="", phone="", address="")
        
        return MatchResult(
            input_business=business,
            api_place=empty_place,
            name_match=False,
            address_match=False,
            phone_match=False,
            name_similarity=0.0,
            address_similarity=0.0,
            phone_similarity=0.0,
            overall_status="FAIL - No results found"
        )
    
    def _create_error_result(self, business: BusinessData, error_msg: str) -> MatchResult:
        """Create a result for when an error occurs during processing."""
        from models import PlaceData
        empty_place = PlaceData(name="", phone="", address="")
        
        return MatchResult(
            input_business=business,
            api_place=empty_place,
            name_match=False,
            address_match=False,
            phone_match=False,
            name_similarity=0.0,
            address_similarity=0.0,
            phone_similarity=0.0,
            overall_status=f"ERROR - {error_msg}"
        )
    
    def save_results(self, results: List[MatchResult]) -> None:
        """Save results to CSV file."""
        results_data = [result.to_dict() for result in results]
        output_df = pd.DataFrame(results_data)
        output_df.to_csv(self.config.OUTPUT_CSV, index=False)
        print(f"Results written to {self.config.OUTPUT_CSV}")