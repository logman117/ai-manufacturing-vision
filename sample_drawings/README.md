# Sample Drawings Directory

This directory is where you should place your technical drawing PDF files for analysis.

## Usage

Place your technical drawing PDFs in this directory to:
- Test the analyzer with real drawings
- Run batch processing on multiple files
- Try the example scripts

## Supported File Formats

- **PDF files** (.pdf) - Primary format
- Multi-page PDFs are supported
- Scanned drawings work best at 300 DPI or higher

## File Naming

You can use any naming convention you prefer. Examples:
- `part_001.pdf`
- `bracket_assembly.pdf`
- `drawing_sheet_1.pdf`

## PDF Quality Guidelines

For best results, ensure your PDFs:

### Text Quality
- Text should be searchable (OCR'd if scanned)
- Clear, legible text and dimensions
- Standard fonts that are readable

### Image Quality
- Minimum 300 DPI for scanned drawings
- Clear lines and symbols
- Good contrast between lines and background
- File size under 10MB per file (for faster processing)

### Drawing Content
- Include all pages if multi-page drawing
- Ensure weld symbols are visible
- Include title blocks with part information
- Show material callouts clearly
- Display finish specifications

## Example Directory Structure

```
sample_drawings/
├── mechanical_parts/
│   ├── bracket_001.pdf
│   ├── bracket_002.pdf
│   └── shaft_assembly.pdf
├── weldments/
│   ├── frame_assembly.pdf
│   └── support_structure.pdf
└── fasteners/
    ├── bolt_m12.pdf
    └── nut_specifications.pdf
```

## Getting Sample Drawings

If you don't have technical drawings to test with:

1. **Create Simple Drawings**
   - Use CAD software to create basic parts
   - Export as PDF

2. **Use Public Domain Resources**
   - Search for "technical drawing examples"
   - Ensure they are non-proprietary

3. **Generate Test Cases**
   - Simple bracket drawings
   - Basic shaft designs
   - Common fasteners

## Privacy and Security

**Important:**
- Never commit proprietary or confidential drawings to public repositories
- The `.gitignore` file is configured to ignore PDF files by default
- Review drawings before sharing to ensure no sensitive information

## Running Analysis

Once you have PDFs in this directory:

### Single File Analysis
```python
from manufacturing_part_analyzer import ManufacturingPartAnalyzer
import os

analyzer = ManufacturingPartAnalyzer(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

result = analyzer.analyze_part("sample_drawings/your_file.pdf")
```

### Batch Processing
```python
results = analyzer.analyze_batch(
    pdf_directory="sample_drawings/",
    output_file="results.json"
)
```

### Using Example Script
```bash
python example_usage.py
```

## Troubleshooting

### PDF Not Reading Correctly
- Check if PDF is password-protected (not supported)
- Verify file is not corrupted
- Try opening in a PDF reader to confirm it works

### Poor Analysis Results
- Increase scan quality to 300+ DPI
- Ensure drawing has clear, legible text
- Check that technical symbols are visible
- Verify drawing includes material and process callouts

### Large File Issues
- Reduce PDF file size using compression tools
- Lower DPI in the analyzer settings
- Split multi-page PDFs into smaller batches

## Need Help?

- See [SETUP.md](../SETUP.md) for configuration help
- Check [README.md](../README.md) for usage examples
- Review [troubleshooting section](../SETUP.md#troubleshooting)

---

**Note:** This directory should contain test drawings only. For production use, organize your drawings in a separate, secure location.
