import pandas as pd
import time
from config import API_KEY, INPUT_CSV, OUTPUT_CSV, NAME_MATCH_THRESHOLD, ADDRESS_MATCH_THRESHOLD
from helpers import (
    format_full_address, check_name_match, check_address_match, check_phone_match
)
from google_api import search_place, get_place_details

def main():
    df = pd.read_csv(INPUT_CSV)
    df.columns = [col.strip() for col in df.columns]
    results = []

    print(f"Processing {len(df)} records...")

    for index, row in df.iterrows():
        business_name = str(row.get("CompanyName", "")).strip()
        phone = str(row.get("WorkNumber", "")).strip()
        full_address = format_full_address(row)

        query = f"{business_name} {full_address}"
        print(f"Searching for: {business_name} ({index+1}/{len(df)})")

        try:
            places_result = search_place(query, API_KEY)
            time.sleep(1)  # To respect rate limits

            if not places_result.get('results'):
                results.append({
                    "Input Business Name": business_name,
                    "Input Phone": phone,
                    "Input Address": full_address,
                    "API Name": "",
                    "API Phone": "",
                    "API Address": "",
                    "Name Match": "No",
                    "Address Match": "No",
                    "Phone Match": "No",
                    "Name Similarity": 0.0,
                    "Address Similarity": 0.0,
                    "Phone Similarity": 0.0,
                    "Overall NAP Status": "FAIL - No results found"
                })
                continue

            top_result = places_result['results'][0]
            place_id = top_result['place_id']
            place_details = get_place_details(place_id, API_KEY).get('result', {})

            api_name = top_result.get("name", "")
            api_address = place_details.get("formatted_address", "")
            api_phone = place_details.get("formatted_phone_number", "")

            name_match, name_sim = check_name_match(business_name, api_name, NAME_MATCH_THRESHOLD)
            address_match, address_sim = check_address_match(full_address, api_address, ADDRESS_MATCH_THRESHOLD)
            phone_match, phone_sim = check_phone_match(phone, api_phone)

            if name_match and address_match and phone_match:
                status = "SUCCESS - All NAP data matches"
            elif name_match and address_match:
                status = "SUCCESS - Name & Address match (Phone missing/different)"
            elif name_match and phone_match:
                status = "PARTIAL - Name & Phone match (Address different)"
            elif address_match and phone_match:
                status = "PARTIAL - Address & Phone match (Name different)"
            elif name_match:
                status = "PARTIAL - Only Name matches"
            elif (name_sim >= 0.95 and address_sim >= 0.95) or (name_sim >= 0.95 and phone_sim >= 0.95):
                status = "SUCCESS - 95%+ similarity match"
            else:
                status = "FAIL - Significant NAP inconsistencies"

            results.append({
                "Input Business Name": business_name,
                "Input Phone": phone,
                "Input Address": full_address,
                "API Name": api_name,
                "API Phone": api_phone,
                "API Address": api_address,
                "Name Match": "Yes" if name_match else "No",
                "Address Match": "Yes" if address_match else "No",
                "Phone Match": "Yes" if phone_match else "No",
                "Name Similarity": round(name_sim, 3),
                "Address Similarity": round(address_sim, 3),
                "Phone Similarity": round(phone_sim, 3),
                "Overall NAP Status": status
            })

            print(f"   {status}")

        except Exception as e:
            print(f"Error: {str(e)}")
            results.append({
                "Input Business Name": business_name,
                "Input Phone": phone,
                "Input Address": full_address,
                "API Name": "",
                "API Phone": "",
                "API Address": "",
                "Name Match": "Error",
                "Address Match": "Error",
                "Phone Match": "Error",
                "Name Similarity": 0.0,
                "Address Similarity": 0.0,
                "Phone Similarity": 0.0,
                "Overall NAP Status": f"ERROR - {str(e)}"
            })

    output_df = pd.DataFrame(results)
    output_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Results written to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()