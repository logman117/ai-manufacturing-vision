"""
Manufacturing Part Analyzer
Uses Azure OpenAI (GPT-4 Vision) to analyze technical drawings and predict manufacturing characteristics
"""

import os
import json
import base64
from pathlib import Path
from typing import Dict, List, Optional
import fitz  # PyMuPDF
from openai import AzureOpenAI
from PIL import Image
import io


class ManufacturingPartAnalyzer:
    """
    Analyzes technical drawings (PDFs) to extract manufacturing characteristics
    """
    
    def __init__(self, azure_endpoint: str, api_key: str, api_version: str = "2024-12-01-preview"):
        """
        Initialize the analyzer with Azure OpenAI credentials

        Args:
            azure_endpoint: Azure OpenAI endpoint URL
            api_key: Azure OpenAI API key
            api_version: API version to use (defaults to latest for GPT-5)
        """
        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version=api_version
        )
        
        # Manufacturing characteristics to detect
        self.manufacturing_features = [
            "Laser Cut",
            "Saw/Shear", 
            "Break Press",
            "Fab",
            "Weld",
            "Painting",
            "Heat Treat",
            "Plating",
            "CNC Machining/Turning",
            "Metal Rolling",
            "Casting/Forging",
            "Tube Bending",
            "Metal Spinning",
            "Turret Punch/Metal Stamping",
            "Press",
            "Inserts"
        ]
    
    def pdf_to_images(self, pdf_path: str, dpi: int = 300) -> List[Image.Image]:
        """
        Convert PDF pages to images
        
        Args:
            pdf_path: Path to PDF file
            dpi: Resolution for conversion
            
        Returns:
            List of PIL Images
        """
        doc = fitz.open(pdf_path)
        images = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            # Render page to pixmap
            mat = fitz.Matrix(dpi/72, dpi/72)
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
        
        doc.close()
        return images
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract all text content from PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text as string
        """
        doc = fitz.open(pdf_path)
        text_content = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text_content.append(f"--- Page {page_num + 1} ---")
            text_content.append(page.get_text())
        
        doc.close()
        return "\n".join(text_content)
    
    def image_to_base64(self, image: Image.Image, format: str = "PNG") -> str:
        """
        Convert PIL Image to base64 string
        
        Args:
            image: PIL Image
            format: Image format
            
        Returns:
            Base64 encoded string
        """
        buffered = io.BytesIO()
        image.save(buffered, format=format)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/{format.lower()};base64,{img_str}"
    
    def create_analysis_prompt(self, extracted_text: str) -> str:
        """
        Create detailed prompt for manufacturing analysis
        
        Args:
            extracted_text: Text extracted from PDF
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an expert manufacturing engineer analyzing technical drawings and specifications using advanced GPT-5 vision and reasoning capabilities.

Based on the technical drawing image and the extracted text below, analyze this part and determine the following:

**Text Content from Drawing:**
{extracted_text[:3000]}  # Truncate if too long

**Your Task:**
Analyze the drawing and text to predict which manufacturing processes are required for this part.

**Return a JSON object with these fields:**

1. **complexity_level**: (string) Rate as "Simple", "Moderate", "Complex", or "Very Complex"
2. **type**: (string) Type of part (e.g., "Bracket", "Shaft", "Assembly", "Fastener", "Weldment")
3. **part_name**: (string) The name/description of the part from the drawing
4. **material**: (string) Material specification (e.g., "Steel", "Aluminum", "Stainless Steel")
5. **part_notes**: (string) Any important notes or special requirements

**Binary Manufacturing Process Indicators (0 or 1):**
For each process below, return 1 if the part requires it, 0 if not:

6. **laser_cut**: Does this part require laser cutting?
7. **saw_shear**: Does this part require saw or shear cutting?
8. **break_press**: Does this part require brake press/bending operations?
9. **fab**: Does this part require general fabrication operations?
10. **weld**: Does this part require welding? (look for weld symbols, weldment callouts)
11. **painting**: Does this part require painting/coating? (look for finish callouts)
12. **heat_treat**: Does this part require heat treatment?
13. **plating**: Does this part require plating? (look for "zinc plated", "chrome", etc.)
14. **cnc_machining_turning**: Does this part require CNC machining or turning? (look for tight tolerances, threaded holes, machined features)
15. **metal_rolling**: Does this part require metal rolling?
16. **casting_forging**: Is this a cast or forged part?
17. **tube_bending**: Does this part require tube bending?
18. **metal_spinning**: Does this part require metal spinning?
19. **turret_punch_stamping**: Does this part require turret punch or metal stamping?
20. **press**: Does this part require press operations?
21. **inserts**: Does this part require inserts? (look for threaded inserts, press-fit inserts)

**Analysis Guidelines:**
- Look for weld symbols (triangles, specific weld callouts) to identify welding
- Check material callouts and notes for plating requirements
- Examine dimensions and tolerances - tight tolerances suggest CNC machining
- Look for bend lines, brake symbols for brake press operations
- Check for threaded holes, inserts in the drawing
- Look at the complexity of the geometry to assess the part type
- Check notes section for special processes like heat treatment
- For assemblies, consider the main fabrication process

Return ONLY a valid JSON object with all fields. Do not include any other text."""

        return prompt
    
    def analyze_part(self, pdf_path: str, deployment_name: str = "gpt-5-chat") -> Dict:
        """
        Analyze a technical drawing PDF and predict manufacturing characteristics

        Args:
            pdf_path: Path to PDF file
            deployment_name: Azure OpenAI deployment name (defaults to gpt-5-chat)
            
        Returns:
            Dictionary with analysis results
        """
        print(f"Analyzing: {pdf_path}")
        
        # Extract text
        print("Extracting text from PDF...")
        extracted_text = self.extract_text_from_pdf(pdf_path)
        
        # Convert PDF to images
        print("Converting PDF to images...")
        images = self.pdf_to_images(pdf_path)
        
        # Create prompt
        prompt = self.create_analysis_prompt(extracted_text)
        
        # Prepare messages with images
        messages = [
            {
                "role": "system",
                "content": "You are an expert manufacturing engineer who analyzes technical drawings."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}
                ]
            }
        ]
        
        # Add all page images
        for idx, img in enumerate(images):
            print(f"Processing page {idx + 1}...")
            base64_image = self.image_to_base64(img)
            messages[1]["content"].append({
                "type": "image_url",
                "image_url": {"url": base64_image}
            })
        
        # Call Azure OpenAI
        print("Calling Azure OpenAI for analysis...")
        try:
            response = self.client.chat.completions.create(
                model=deployment_name,
                messages=messages,
                max_tokens=2000,
                temperature=0.1  # Low temperature for consistent analysis
            )
            
            result_text = response.choices[0].message.content
            
            # Extract JSON from response
            # Sometimes the model wraps JSON in markdown code blocks
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            result = json.loads(result_text.strip())
            
            # Add metadata
            result["source_file"] = os.path.basename(pdf_path)
            result["extracted_text_preview"] = extracted_text[:500]
            
            return result
            
        except Exception as e:
            print(f"Error during analysis: {e}")
            return {
                "error": str(e),
                "source_file": os.path.basename(pdf_path)
            }
    
    def analyze_batch(self, pdf_directory: str, output_file: str = "analysis_results.json") -> List[Dict]:
        """
        Analyze multiple PDF files in a directory
        
        Args:
            pdf_directory: Directory containing PDF files
            output_file: Output JSON file path
            
        Returns:
            List of analysis results
        """
        pdf_files = list(Path(pdf_directory).glob("*.pdf"))
        results = []
        
        print(f"Found {len(pdf_files)} PDF files to analyze")
        
        for pdf_file in pdf_files:
            result = self.analyze_part(str(pdf_file))
            results.append(result)
            print(f"Completed: {pdf_file.name}\n")
        
        # Save results
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to: {output_file}")
        return results


def main():
    """
    Example usage
    """
    # Configure Azure OpenAI credentials
    # You'll need to set these as environment variables or pass them directly
    AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5-chat")

    if not AZURE_ENDPOINT or not API_KEY:
        print("ERROR: Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY environment variables")
        print("\nExample:")
        print("export AZURE_OPENAI_ENDPOINT='https://your-resource.openai.azure.com/'")
        print("export AZURE_OPENAI_API_KEY='your-api-key'")
        print("export AZURE_OPENAI_DEPLOYMENT='gpt-5-chat'")
        return
    
    # Initialize analyzer
    analyzer = ManufacturingPartAnalyzer(
        azure_endpoint=AZURE_ENDPOINT,
        api_key=API_KEY
    )
    
    # Example: Analyze a single PDF
    # result = analyzer.analyze_part("path/to/drawing.pdf", deployment_name=DEPLOYMENT_NAME)
    # print(json.dumps(result, indent=2))
    
    # Example: Analyze all PDFs in a directory
    # results = analyzer.analyze_batch("path/to/pdf/directory", "results.json")
    
    print("Setup complete! Use the analyzer object to process your PDFs.")
    print("\nExample usage:")
    print("  result = analyzer.analyze_part('drawing.pdf')")
    print("  results = analyzer.analyze_batch('pdf_directory/', 'output.json')")


if __name__ == "__main__":
    main()
