import requests
import logging
from typing import Optional, Dict, Any
from models import PlaceData
from config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class GooglePlacesClient:
    """Client for interacting with Google Places API."""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def search_place(self, query: str) -> Optional[Dict[str, Any]]:
        """Search for a place using Google Places Text Search API."""
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': query,
            'key': self.config.GOOGLE_PLACES_API_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=self.config.REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to search place '{query}': {e}")
            return None
    
    def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a place."""
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_address,formatted_phone_number',
            'key': self.config.GOOGLE_PLACES_API_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=self.config.REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to get place details for '{place_id}': {e}")
            return None
    
    def search_and_get_details(self, query: str) -> Optional[PlaceData]:
        """Search for a place and return detailed information."""
        search_result = self.search_place(query)
        
        if not search_result or not search_result.get('results'):
            return None
        
        top_result = search_result['results'][0]
        place_id = top_result['place_id']
        
        details_result = self.get_place_details(place_id)
        if not details_result or 'result' not in details_result:
            return None
        
        details = details_result['result']
        
        return PlaceData(
            name=top_result.get("name", ""),
            address=details.get("formatted_address", ""),
            phone=details.get("formatted_phone_number", ""),
            place_id=place_id
        )