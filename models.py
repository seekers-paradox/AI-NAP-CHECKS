from dataclasses import dataclass
from typing import Optional

@dataclass
class BusinessData:
    """Represents business information from input CSV."""
    name: str
    phone: str
    address: str
    
    @classmethod
    def from_csv_row(cls, row) -> 'BusinessData':
        """Create BusinessData from a pandas DataFrame row."""
        return cls(
            name=str(row.get("CompanyName", "")).strip(),
            phone=str(row.get("WorkNumber", "")).strip(),
            address=cls._format_address(row)
        )
    
    @staticmethod
    def _format_address(row) -> str:
        """Format address components into a full address string."""
        components = []
        for key in ["Address", "City", "ZipCode", "Country"]:
            val = str(row.get(key, "")).strip()
            if val and val.lower() != "nan":
                components.append(val)
        
        if not any(c.lower() == 'usa' for c in components):
            components.append("USA")
        
        return ", ".join(components)

@dataclass
class PlaceData:
    """Represents place information from Google Places API."""
    name: str
    phone: str
    address: str
    place_id: Optional[str] = None

@dataclass
class MatchResult:
    """Represents the result of matching business data with place data."""
    input_business: BusinessData
    api_place: PlaceData
    name_match: bool
    address_match: bool
    phone_match: bool
    name_similarity: float
    address_similarity: float
    phone_similarity: float
    overall_status: str
    
    def to_dict(self) -> dict:
        """Convert match result to dictionary for CSV export."""
        return {
            "Input Business Name": self.input_business.name,
            "Input Phone": self.input_business.phone,
            "Input Address": self.input_business.address,
            "API Name": self.api_place.name,
            "API Phone": self.api_place.phone,
            "API Address": self.api_place.address,
            "Name Match": "Yes" if self.name_match else "No",
            "Address Match": "Yes" if self.address_match else "No",
            "Phone Match": "Yes" if self.phone_match else "No",
            "Name Similarity": round(self.name_similarity, 3),
            "Address Similarity": round(self.address_similarity, 3),
            "Phone Similarity": round(self.phone_similarity, 3),
            "Overall NAP Status": self.overall_status
        }