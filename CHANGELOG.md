# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Support for DXF and DWG file formats
- Web interface for easier access
- Cost estimation features
- Multi-language support
- Integration with popular CAD systems

---

## [1.0.0] - 2024-10-15

### Added
- Initial release of Manufacturing Part Analyzer
- Azure OpenAI GPT-4 Vision integration
- PDF text extraction using PyMuPDF
- Image-based analysis of technical drawings
- Detection of 16 manufacturing processes:
  - Laser Cut
  - Saw/Shear
  - Break Press
  - Fab
  - Weld
  - Painting
  - Heat Treat
  - Plating
  - CNC Machining/Turning
  - Metal Rolling
  - Casting/Forging
  - Tube Bending
  - Metal Spinning
  - Turret Punch/Stamping
  - Press
  - Inserts
- Metadata extraction:
  - Complexity level
  - Part type
  - Part name
  - Material specification
  - Special notes
- Batch processing capability
- JSON output format
- Structured output with type hints
- Error handling and logging
- Environment variable configuration via .env
- Example usage scripts
- Comprehensive documentation:
  - README.md
  - SETUP.md
  - CONTRIBUTING.md
  - Example scripts

### Features
- Single PDF analysis
- Batch processing multiple PDFs
- Export results to JSON
- Compatibility with pandas for data analysis
- Support for multi-page technical drawings
- Configurable DPI for image processing
- Adjustable temperature for AI consistency

### Documentation
- Complete setup guide for Azure OpenAI
- Usage examples for common scenarios
- Troubleshooting guide
- API reference in docstrings
- Contributing guidelines

### Security
- .gitignore configured to exclude .env files
- .env.example template for safe credential management
- No hardcoded credentials in source code

---

## Release Notes

### Version 1.0.0 - Initial Release

This is the first public release of the Manufacturing Part Analyzer. The tool provides automated analysis of technical drawings using Azure OpenAI's GPT-4 Vision model to predict required manufacturing processes.

**Key Features:**
- AI-powered analysis of technical drawings
- Identification of 16+ manufacturing processes
- Batch processing support
- Structured JSON output
- Easy Azure OpenAI integration

**Getting Started:**
1. Set up Azure OpenAI account
2. Deploy GPT-4 Vision model
3. Configure credentials in .env file
4. Run the analyzer on your technical drawings

For detailed setup instructions, see [SETUP.md](SETUP.md).

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to contribute to this project.

## Questions or Issues?

- Open an issue on GitHub
- Check existing issues for solutions
- Review the [SETUP.md](SETUP.md) guide

---

[Unreleased]: https://github.com/yourusername/manufacturing-part-analyzer/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/manufacturing-part-analyzer/releases/tag/v1.0.0
