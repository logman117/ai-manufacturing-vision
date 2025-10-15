# Manufacturing Part Analyzer - Complete Setup Guide

This guide will walk you through setting up the Manufacturing Part Analyzer from scratch, including Azure OpenAI configuration.

## Table of Contents
1. [Azure OpenAI Setup](#azure-openai-setup)
2. [Project Installation](#project-installation)
3. [Configuration](#configuration)
4. [Testing](#testing)
5. [Troubleshooting](#troubleshooting)

---

## Azure OpenAI Setup

### Step 1: Create Azure Account

If you don't have an Azure account:
1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Start Free" or sign in with existing account
3. Complete the registration process

### Step 2: Create Azure OpenAI Resource

1. **Navigate to Azure OpenAI Service**
   - In Azure Portal, click "Create a resource"
   - Search for "Azure OpenAI"
   - Click "Create"

2. **Configure the Resource**
   - **Subscription**: Select your subscription
   - **Resource Group**: Create new or select existing
   - **Region**: Choose a region (e.g., East US, West Europe)
   - **Name**: Give it a unique name (e.g., `my-openai-resource`)
   - **Pricing Tier**: Select appropriate tier (Standard S0)

3. **Review and Create**
   - Click "Review + Create"
   - Click "Create" and wait for deployment (2-5 minutes)

### Step 3: Deploy GPT-4 Vision Model

1. **Open Azure AI Studio**
   - Go to [Azure AI Studio](https://oai.azure.com/)
   - Sign in with your Azure account
   - Select your OpenAI resource

2. **Create Deployment**
   - Click "Deployments" in the left menu
   - Click "Create new deployment"
   - Select model: `gpt-4` or `gpt-4-vision-preview`
   - Give it a deployment name (e.g., `gpt-4-vision`)
   - Click "Create"

3. **Note Your Deployment Name**
   - Save the deployment name for later configuration

### Step 4: Get API Credentials

1. **Get Endpoint URL**
   - In Azure Portal, go to your OpenAI resource
   - Click "Keys and Endpoint" in the left menu
   - Copy the "Endpoint" URL
   - Example: `https://your-resource.openai.azure.com`

2. **Get API Key**
   - On the same page, copy "KEY 1" or "KEY 2"
   - Keep this secure - don't share it!

3. **Get API Version**
   - Current stable version: `2024-12-01-preview`
   - Check [Azure OpenAI docs](https://learn.microsoft.com/en-us/azure/ai-services/openai/) for latest

---

## Project Installation

### Step 1: Prerequisites

Ensure you have:
- Python 3.8 or higher
- pip package manager
- Git (optional, for cloning)

Check your Python version:
```bash
python --version
```

### Step 2: Download the Project

**Option A: Clone with Git**
```bash
git clone https://github.com/yourusername/manufacturing-part-analyzer.git
cd manufacturing-part-analyzer
```

**Option B: Download ZIP**
- Download the project ZIP from GitHub
- Extract to a folder
- Open terminal in that folder

### Step 3: Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Azure OpenAI SDK
- PDF processing libraries (PyMuPDF)
- Image processing (Pillow)
- Data handling (pandas, numpy)
- Other utilities

---

## Configuration

### Step 1: Create Environment File

Copy the example environment file:
```bash
cp .env.example .env
```

Or on Windows:
```bash
copy .env.example .env
```

### Step 2: Edit Environment File

Open `.env` in a text editor and fill in your credentials:

```env
# Your Azure OpenAI Endpoint (from Azure Portal)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com

# Your API Key (from Azure Portal - Keys and Endpoint)
AZURE_OPENAI_API_KEY=your-actual-api-key-here

# Your Deployment Name (from Azure AI Studio)
AZURE_OPENAI_DEPLOYMENT=gpt-4-vision

# API Version (use latest stable)
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Optional settings
ANALYSIS_TEMPERATURE=0.1
MAX_TOKENS=2000
```

### Step 3: Verify Configuration

Create a test script `test_config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

print("Configuration Check:")
print(f"Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
print(f"API Key: {'*' * 20}{os.getenv('AZURE_OPENAI_API_KEY')[-4:]}")
print(f"Deployment: {os.getenv('AZURE_OPENAI_DEPLOYMENT')}")
```

Run it:
```bash
python test_config.py
```

---

## Testing

### Quick Test - Single PDF

Create a test script `quick_test.py`:

```python
from manufacturing_part_analyzer import ManufacturingPartAnalyzer
import os
import json

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize analyzer
analyzer = ManufacturingPartAnalyzer(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

# Test with a sample PDF
pdf_path = "path/to/your/sample.pdf"  # Replace with actual path

try:
    print("Analyzing PDF...")
    result = analyzer.analyze_part(
        pdf_path=pdf_path,
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT")
    )

    print("\nResults:")
    print(json.dumps(result, indent=2))
    print("\nSuccess! The analyzer is working correctly.")

except Exception as e:
    print(f"Error: {e}")
    print("\nPlease check your configuration and try again.")
```

Run it:
```bash
python quick_test.py
```

### Expected Output

You should see:
```
Analyzing: sample.pdf
Extracting text from PDF...
Converting PDF to images...
Processing page 1...
Calling Azure OpenAI for analysis...

Results:
{
  "complexity_level": "Moderate",
  "type": "Bracket",
  "part_name": "Support Bracket",
  ...
}

Success! The analyzer is working correctly.
```

---

## Troubleshooting

### Common Issues

#### Issue: "Module not found"
**Solution**: Make sure virtual environment is activated and dependencies are installed
```bash
pip install -r requirements.txt
```

#### Issue: "Invalid API key"
**Possible causes:**
- API key copied incorrectly (check for extra spaces)
- Using wrong key from Azure Portal
- Endpoint URL doesn't match the key

**Solution**:
1. Go to Azure Portal
2. Navigate to your OpenAI resource
3. Click "Keys and Endpoint"
4. Copy KEY 1 again
5. Update `.env` file

#### Issue: "Deployment not found"
**Solution**: Verify deployment name in Azure AI Studio matches `.env`

#### Issue: "Rate limit exceeded"
**Solution**:
- Add delays between requests
- Check your quota in Azure Portal
- Upgrade your pricing tier if needed

#### Issue: "PDF processing error"
**Solutions**:
- Ensure PDF is not corrupted
- Check file permissions
- Try with a different PDF
- Reduce DPI if file is too large

#### Issue: "Import error for PyMuPDF"
**Solution**:
```bash
pip uninstall PyMuPDF
pip install PyMuPDF --upgrade
```

### Testing Connection to Azure

Create `test_azure_connection.py`:

```python
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

try:
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[{"role": "user", "content": "Hello!"}],
        max_tokens=10
    )
    print("Connection successful!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"Connection failed: {e}")
```

### Getting Help

If you're still having issues:

1. **Check Azure Status**
   - Visit [Azure Status Page](https://status.azure.com/)
   - Verify Azure OpenAI service is operational

2. **Review Logs**
   - Check error messages carefully
   - Look for specific error codes

3. **Consult Documentation**
   - [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
   - [Project GitHub Issues](https://github.com/yourusername/manufacturing-part-analyzer/issues)

4. **Create an Issue**
   - Provide error messages
   - Include your environment (OS, Python version)
   - Describe steps to reproduce

---

## Next Steps

Once setup is complete:

1. **Try batch processing** - Analyze multiple PDFs
2. **Customize prompts** - Adjust for your specific needs
3. **Integrate with your workflow** - Export results to database
4. **Explore advanced features** - Check the main README

## Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore` by default
2. **Rotate API keys regularly** - Generate new keys in Azure Portal
3. **Use separate keys** - Different keys for dev/prod
4. **Monitor usage** - Check Azure Portal for unexpected activity
5. **Set spending limits** - Configure cost alerts in Azure

---

Need more help? Open an issue on GitHub or consult the [main README](README.md).
