import openai
from typing import Optional
from config import Config

class AIBusinessMatcher:
    """AI-powered business matching using OpenAI."""
    
    def __init__(self, config: Config):
        openai.api_key = config.OPENAI_API_KEY
    
    def is_match(self, local_name: str, local_address: str, 
                google_name: str, google_address: str) -> bool:
        """Use AI to determine if two businesses are the same."""
        prompt = f"""
Compare the following two places and determine if they are likely the same business:

Local Business:
Name: {local_name}
Address: {local_address}

Google Places Result:
Name: {google_name}
Address: {google_address}

Consider variations in business names, abbreviations, and address formatting.
Respond with 'Yes' if they match, 'No' if they are clearly different businesses.
"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            
            reply = response["choices"][0]["message"]["content"].strip().lower()
            return reply.startswith("yes")
        
        except Exception as e:
            # Fallback to False if AI matching fails
            return False