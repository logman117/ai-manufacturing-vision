# AI Manufacturing Part Analyzer

An AI-powered system that analyzes technical drawings (PDFs) to automatically predict manufacturing characteristics and processes using Azure OpenAI's GPT-4 Vision model.

## Features

- **Dual-mode PDF Analysis**: Extracts both text content and visual information from technical drawings
- **Manufacturing Process Prediction**: Identifies 16+ manufacturing processes required for each part
- **Batch Processing**: Analyze multiple drawings at once
- **Structured Output**: Returns JSON with all manufacturing characteristics
- **High Accuracy**: Uses GPT-4 Vision for superior drawing interpretation

## Manufacturing Characteristics Detected

### Metadata
- Complexity Level (Simple, Moderate, Complex, Very Complex)
- Part Type (Bracket, Shaft, Assembly, Fastener, Weldment, etc.)
- Part Name
- Material Specification
- Special Notes

### Manufacturing Processes (Binary 0/1)
1. **Laser Cut** - Laser cutting operations
2. **Saw/Shear** - Sawing or shearing operations
3. **Break Press** - Brake press/bending operations
4. **Fab** - General fabrication
5. **Weld** - Welding operations
6. **Painting** - Painting/coating
7. **Heat Treat** - Heat treatment
8. **Plating** - Electroplating (zinc, chrome, etc.)
9. **CNC Machining/Turning** - CNC machining or turning
10. **Metal Rolling** - Rolling operations
11. **Casting/Forging** - Cast or forged parts
12. **Tube Bending** - Tube bending operations
13. **Metal Spinning** - Metal spinning
14. **Turret Punch/Stamping** - Turret punch or stamping
15. **Press** - Press operations
16. **Inserts** - Threaded or press-fit inserts

## Prerequisites

### 1. Azure OpenAI Service
You need an Azure subscription with:
- Azure OpenAI Service deployed
- GPT-4 Vision model deployed
- API key and endpoint

### 2. Python Environment
- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/manufacturing-part-analyzer.git
cd manufacturing-part-analyzer
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Azure OpenAI Credentials

Copy the example environment file and fill in your credentials:
```bash
cp .env.example .env
```

Edit `.env` with your Azure OpenAI details:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=gpt-4-vision
```

## Usage

### Basic Usage - Single File

```python
from manufacturing_part_analyzer import ManufacturingPartAnalyzer
import os

# Initialize analyzer
analyzer = ManufacturingPartAnalyzer(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

# Analyze a single PDF
result = analyzer.analyze_part(
    pdf_path="drawings/part_drawing.pdf",
    deployment_name="gpt-4-vision"
)

# Print results
import json
print(json.dumps(result, indent=2))
```

### Batch Processing - Multiple Files

```python
from manufacturing_part_analyzer import ManufacturingPartAnalyzer
import os

# Initialize analyzer
analyzer = ManufacturingPartAnalyzer(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

# Analyze all PDFs in a directory
results = analyzer.analyze_batch(
    pdf_directory="drawings/",
    output_file="analysis_results.json"
)

print(f"Analyzed {len(results)} drawings")
```

### Example Output

```json
{
  "complexity_level": "Complex",
  "type": "Weldment",
  "part_name": "Support Bracket Assembly",
  "material": "Steel",
  "part_notes": "Weldment assembly with powder coat finish",
  "laser_cut": 0,
  "saw_shear": 1,
  "break_press": 0,
  "fab": 1,
  "weld": 1,
  "painting": 1,
  "heat_treat": 0,
  "plating": 0,
  "cnc_machining_turning": 1,
  "metal_rolling": 0,
  "casting_forging": 0,
  "tube_bending": 0,
  "metal_spinning": 0,
  "turret_punch_stamping": 0,
  "press": 0,
  "inserts": 0,
  "source_file": "support_bracket.pdf",
  "extracted_text_preview": "MATERIAL: STEEL..."
}
```

## Azure OpenAI Setup

### 1. Create an Azure OpenAI Resource
- Go to [Azure Portal](https://portal.azure.com)
- Create "Azure OpenAI" resource
- Note the endpoint and keys

### 2. Deploy GPT-4 Vision Model
- In Azure AI Studio, go to Deployments
- Deploy `gpt-4` or `gpt-4-vision-preview`
- Note the deployment name

### 3. Get Credentials
- **Endpoint**: Found in "Keys and Endpoint" section
- **API Key**: Found in "Keys and Endpoint" section
- **Deployment Name**: The name you gave your deployment

For detailed setup instructions, see [SETUP.md](SETUP.md)

## Advanced Features

### Accuracy Validation

Validate the analyzer's accuracy against your ground truth data:

```bash
# 1. Create ground truth template
python create_ground_truth_template.py

# 2. Fill in the template with actual values
# Edit ground_truth_template.xlsx

# 3. Run validation
python validate_accuracy.py analysis_results.json ground_truth_template.xlsx
```

This generates:
- Visual accuracy report (bar chart)
- Detailed accuracy statistics per parameter
- Overall accuracy metrics

For detailed instructions, see [ACCURACY_VALIDATION.md](ACCURACY_VALIDATION.md)

### Custom Prompts

You can modify the analysis prompt in the `create_analysis_prompt()` method to:
- Add industry-specific requirements
- Adjust sensitivity for certain processes
- Include additional metadata fields

### Export to Database

```python
import pandas as pd

# Analyze batch
results = analyzer.analyze_batch("drawings/")

# Convert to DataFrame
df = pd.DataFrame(results)

# Export to Excel
df.to_excel("manufacturing_analysis.xlsx", index=False)

# Or export to CSV
df.to_csv("manufacturing_analysis.csv", index=False)
```

## Troubleshooting

### Common Issues

**Issue**: "Invalid API key or endpoint"
- **Solution**: Double-check your Azure OpenAI credentials in `.env` file

**Issue**: "Model deployment not found"
- **Solution**: Verify your deployment name matches what's in Azure Portal

**Issue**: "Rate limit exceeded"
- **Solution**: Add delays between batch processing or increase quotas in Azure

**Issue**: "Image too large"
- **Solution**: Reduce DPI in `pdf_to_images()` method (default is 300)

### PDF Quality Tips

For best results:
- Use high-quality PDF scans (300 DPI minimum)
- Ensure text is searchable (not just images)
- Keep file sizes reasonable (<10MB per file)
- Multi-page drawings are supported

## Performance Considerations

- **Processing Time**: ~5-15 seconds per page depending on complexity
- **Cost**: Each analysis uses GPT-4 Vision tokens (image + text)
- **Batch Processing**: Use delays between requests to avoid rate limits

## API Rate Limits

Azure OpenAI has rate limits. For batch processing:
- Add delays: `time.sleep(1)` between requests
- Monitor usage in Azure Portal
- Consider upgrading quota for large batches

## Project Structure

```
manufacturing-part-analyzer/
├── manufacturing_part_analyzer.py  # Main analyzer class
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── SETUP.md                        # Detailed setup guide
├── CONTRIBUTING.md                 # Contribution guidelines
└── LICENSE                         # MIT License
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Azure OpenAI GPT-4 Vision
- Uses PyMuPDF for PDF processing
- Inspired by the need to automate manufacturing process planning

## Support

For issues and questions:
- Create an issue in the GitHub repository
- Check existing issues for solutions
- Refer to Azure OpenAI documentation

## Disclaimer

This tool uses AI and should be validated by engineering experts for production use. Always verify critical manufacturing decisions with qualified personnel.

## Roadmap

- [ ] Support for DXF/DWG file formats
- [ ] Integration with CAD systems
- [ ] Cost estimation features
- [ ] Multi-language support
- [ ] Web interface

---

**Star this repo if you find it useful!**
