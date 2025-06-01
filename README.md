# NAP Audit System

A comprehensive Name, Address, Phone (NAP) data validation system that compares business information from CSV files against Google Places API data, with optional AI-powered verification for ambiguous matches.

## 🚀 Features

- **Automated NAP Validation**: Compare business data against Google Places API
- **Intelligent Matching**: Multiple matching algorithms including similarity scoring and component-based matching
- **AI-Powered Verification**: Optional OpenAI integration for ambiguous cases
- **Comprehensive Reporting**: Detailed CSV output with match scores and status
- **Rate Limiting**: Built-in API rate limiting to respect service limits
- **Error Handling**: Robust error handling with detailed logging
- **Configurable Thresholds**: Easily adjust matching sensitivity

## 📋 Prerequisites

- Python 3.7+
- Google Places API key
- OpenAI API key (optional, for AI-powered matching)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd nap-audit-system
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_PLACES_API_KEY=your_google_places_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 📁 Project Structure

```
nap-audit-system/
├── main.py                    # Main entry point
├── config.py                  # Configuration settings
├── models.py                  # Data models and classes
├── text_utils.py             # Text matching utilities
├── google_places_client.py   # Google Places API client
├── ai_matcher.py             # OpenAI-powered matching
├── nap_matcher.py            # NAP matching logic
├── nap_audit_processor.py    # Main processing engine
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
└── README.md                 # This file
```

## 📊 Input CSV Format

Your input CSV file should contain the following columns:

| Column Name | Description | Required |
|-------------|-------------|----------|
| `CompanyName` | Business name | Yes |
| `WorkNumber` | Phone number | No |
| `Address` | Street address | No |
| `City` | City name | No |
| `ZipCode` | ZIP/Postal code | No |
| `Country` | Country (defaults to USA) | No |

### Example Input CSV:
```csv
CompanyName,WorkNumber,Address,City,ZipCode,Country
"Joe's Pizza","(555) 123-4567","123 Main St","New York","10001","USA"
"Smith & Associates","555-987-6543","456 Oak Ave","Los Angeles","90210","USA"
```

## ⚙️ Configuration

Edit `config.py` to customize settings:

```python
@dataclass
class Config:
    INPUT_CSV: str = 'your_input_file.csv'           # Input CSV filename
    OUTPUT_CSV: str = 'nap_audit_results.csv'       # Output CSV filename
    NAME_MATCH_THRESHOLD: float = 0.8                # Name similarity threshold (0-1)
    ADDRESS_MATCH_THRESHOLD: float = 0.85            # Address similarity threshold (0-1)
    REQUEST_DELAY: float = 1.0                       # Delay between API calls (seconds)
    REQUEST_TIMEOUT: int = 10                        # API request timeout (seconds)
```

## 🚀 Usage

### Basic Usage

1. **Prepare your CSV file** with business data
2. **Update the configuration** in `config.py` if needed
3. **Run the audit**:
   ```bash
   python main.py
   ```

### Command Line Output

```
Processing 100 records...
Searching for: Joe's Pizza (1/100)
   SUCCESS - All NAP data matches
Searching for: Smith & Associates (2/100)
   PARTIAL - Name & Address match (Phone missing/different)
   ✅ AI confirmed match!
...

=== NAP Audit Summary ===
Total Records: 100
Successful Matches: 75
Partial Matches: 15
Failed Matches: 8
Errors: 2

Results written to nap_audit_results.csv
```

## 📈 Output CSV Format

The output CSV contains detailed matching results:

| Column | Description |
|--------|-------------|
| `Input Business Name` | Original business name |
| `Input Phone` | Original phone number |
| `Input Address` | Original full address |
| `API Name` | Google Places business name |
| `API Phone` | Google Places phone number |
| `API Address` | Google Places formatted address |
| `Name Match` | Yes/No name match result |
| `Address Match` | Yes/No address match result |
| `Phone Match` | Yes/No phone match result |
| `Name Similarity` | Name similarity score (0-1) |
| `Address Similarity` | Address similarity score (0-1) |
| `Phone Similarity` | Phone similarity score (0-1) |
| `Overall NAP Status` | Final matching status |

### Status Values

- **SUCCESS - All NAP data matches**: Perfect match across all fields
- **SUCCESS - Name & Address match**: Good match, phone may be missing
- **SUCCESS - 95%+ similarity match**: Very high similarity scores
- **PARTIAL - Name & Phone match**: Address differs significantly
- **PARTIAL - Address & Phone match**: Business name differs
- **PARTIAL - Only Name matches**: Only name is similar
- **FAIL - Significant NAP inconsistencies**: Poor match across fields
- **FAIL - No results found**: No Google Places results
- **ERROR - [message]**: Processing error occurred

## 🤖 AI-Powered Matching

The system uses OpenAI's GPT-4 for intelligent verification of ambiguous matches. AI matching is triggered when:

- Initial matching results are `PARTIAL` or `FAIL`
- Rule-based algorithms are uncertain

### AI Matching Benefits:
- Handles business name variations and abbreviations
- Understands address formatting differences
- Provides human-like judgment for edge cases
- Cost-effective (only used when needed)

## 🔧 Advanced Configuration

### Custom Matching Thresholds

Adjust sensitivity by modifying thresholds in `config.py`:

```python
# More strict matching
NAME_MATCH_THRESHOLD: float = 0.9
ADDRESS_MATCH_THRESHOLD: float = 0.9

# More lenient matching  
NAME_MATCH_THRESHOLD: float = 0.7
ADDRESS_MATCH_THRESHOLD: float = 0.75
```

### Rate Limiting

Control API call frequency:

```python
REQUEST_DELAY: float = 2.0  # 2 seconds between calls (slower, safer)
REQUEST_DELAY: float = 0.5  # 0.5 seconds between calls (faster, higher risk)
```

## 🐛 Troubleshooting

### Common Issues

**1. API Key Errors**
```
Error: GOOGLE_PLACES_API_KEY not found in environment variables
```
- Ensure `.env` file exists with valid API keys
- Check API key permissions and quotas

**2. Rate Limiting**
```
Failed to search place: 429 Too Many Requests
```
- Increase `REQUEST_DELAY` in config
- Check your Google Places API quota

**3. CSV Format Issues**
```
KeyError: 'CompanyName'
```
- Verify CSV column names match expected format
- Check for extra spaces in column headers

**4. No Results Found**
```
FAIL - No results found
```
- Business may not exist in Google Places
- Try more specific search terms
- Check address formatting

### Debug Mode

Enable detailed logging by modifying the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 📝 API Costs

### Google Places API
- **Text Search**: ~$32 per 1,000 requests
- **Place Details**: ~$17 per 1,000 requests
- **Total**: ~$49 per 1,000 business records

### OpenAI API (Optional)
- **GPT-4**: ~$0.03 per 1,000 tokens
- **Estimated**: ~$5-10 per 1,000 business records (partial usage)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review [Google Places API documentation](https://developers.google.com/places/web-service/overview)
3. Check [OpenAI API documentation](https://platform.openai.com/docs)
4. Open an issue on GitHub

## 🔄 Version History

- **v1.0.0** - Initial release with basic NAP matching
- **v1.1.0** - Added AI-powered verification
- **v1.2.0** - Improved error handling and logging
- **v2.0.0** - Complete refactor with modular architecture

---

## 📋 Requirements.txt

```txt
pandas>=1.3.0
requests>=2.25.0
python-dotenv>=0.19.0
openai>=0.27.0
```

Save this as `requirements.txt` in your project root.

---

*Built with ❤️ for accurate business data validation*