from config import Config
from nap_audit_processor import NAPAuditProcessor

def main():
    """Main entry point for the NAP audit system."""
    config = Config()
    processor = NAPAuditProcessor(config)
    
    # Validate configuration
    if not config.GOOGLE_PLACES_API_KEY:
        print("Error: GOOGLE_PLACES_API_KEY not found in environment variables")
        return
    
    if not config.OPENAI_API_KEY:
        print("Warning: OPENAI_API_KEY not found - AI matching will be disabled")
    
    # Process the CSV file
    results = processor.process_csv()
    
    # Save results
    processor.save_results(results)
    
    # Print summary
    total_records = len(results)
    successful_matches = sum(1 for r in results if r.overall_status.startswith("SUCCESS"))
    partial_matches = sum(1 for r in results if r.overall_status.startswith("PARTIAL"))
    failed_matches = sum(1 for r in results if r.overall_status.startswith("FAIL"))
    errors = sum(1 for r in results if r.overall_status.startswith("ERROR"))
    
    print(f"\n=== NAP Audit Summary ===")
    print(f"Total Records: {total_records}")
    print(f"Successful Matches: {successful_matches}")
    print(f"Partial Matches: {partial_matches}")
    print(f"Failed Matches: {failed_matches}")
    print(f"Errors: {errors}")

if __name__ == "__main__":
    main()