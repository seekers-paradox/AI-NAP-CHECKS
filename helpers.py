import pandas as pd
import re
from difflib import SequenceMatcher

def normalize_phone(phone):
    if not phone or pd.isna(phone):
        return ""
    digits_only = re.sub(r'\D', '', str(phone))
    if len(digits_only) > 10:
        digits_only = digits_only[-10:]
    return digits_only

def similarity_ratio(a, b):
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()

def normalize_text_for_comparison(text):
    if not text or pd.isna(text):
        return ""
    normalized = re.sub(r'[^\w\s]', ' ', str(text).lower())
    normalized = ' '.join(normalized.split())
    return normalized

def format_full_address(row):
    components = []
    for key in ["Address", "City", "ZipCode", "Country"]:
        val = str(row.get(key, "")).strip()
        if val and val.lower() != "nan":
            components.append(val)
    if not any(c.lower() == 'usa' for c in components):
        components.append("USA")  # default country
    return ", ".join(components)

def check_name_match(input_name, api_name, threshold=0.8):
    norm_input = normalize_text_for_comparison(input_name)
    norm_api = normalize_text_for_comparison(api_name)
    similarity = similarity_ratio(norm_input, norm_api)
    contains_match = (norm_input in norm_api) or (norm_api in norm_input)
    return (similarity >= threshold) or contains_match, similarity

def check_address_match(input_address, api_address, threshold=0.85):
    norm_input = normalize_text_for_comparison(input_address)
    norm_api = normalize_text_for_comparison(api_address)
    similarity = similarity_ratio(norm_input, norm_api)

    input_parts = norm_input.split()
    api_parts = norm_api.split()
    key_matches = 0
    total_parts = len(input_parts)
    for part in input_parts:
        if len(part) > 2 and any(part in api_part for api_part in api_parts):
            key_matches += 1
    component_match_ratio = key_matches / max(total_parts, 1) if total_parts > 0 else 0

    return (similarity >= threshold) or (component_match_ratio >= 0.7), max(similarity, component_match_ratio)

def check_phone_match(input_phone, api_phone):
    norm_input = normalize_phone(input_phone)
    norm_api = normalize_phone(api_phone)
    if not norm_input or not norm_api:
        return False, 0.0
    if norm_input == norm_api:
        return True, 1.0
    if norm_input in norm_api or norm_api in norm_input:
        return True, 0.9
    return False, 0.0