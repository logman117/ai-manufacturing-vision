"""
Example Usage Script for Manufacturing Part Analyzer

This script demonstrates how to use the analyzer for both single and batch processing.
"""

import os
import json
from manufacturing_part_analyzer import ManufacturingPartAnalyzer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def example_single_file():
    """
    Example 1: Analyze a single PDF file
    """
    print("=" * 60)
    print("Example 1: Analyzing a Single PDF")
    print("=" * 60)

    # Initialize the analyzer
    analyzer = ManufacturingPartAnalyzer(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
    )

    # Path to your PDF file
    pdf_path = "sample_drawings/example_part.pdf"

    # Analyze the part
    try:
        result = analyzer.analyze_part(
            pdf_path=pdf_path,
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5-chat")
        )

        # Display results
        print("\nAnalysis Results:")
        print(f"Part Name: {result.get('part_name', 'N/A')}")
        print(f"Type: {result.get('type', 'N/A')}")
        print(f"Complexity: {result.get('complexity_level', 'N/A')}")
        print(f"Material: {result.get('material', 'N/A')}")

        print("\nManufacturing Processes Required:")
        processes = [
            ("Laser Cut", result.get('laser_cut', 0)),
            ("Saw/Shear", result.get('saw_shear', 0)),
            ("Break Press", result.get('break_press', 0)),
            ("Fabrication", result.get('fab', 0)),
            ("Welding", result.get('weld', 0)),
            ("Painting", result.get('painting', 0)),
            ("Heat Treatment", result.get('heat_treat', 0)),
            ("Plating", result.get('plating', 0)),
            ("CNC Machining", result.get('cnc_machining_turning', 0)),
        ]

        for process, required in processes:
            status = "✓ Yes" if required else "✗ No"
            print(f"  {process}: {status}")

        # Save results to file
        output_file = "single_analysis_result.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nFull results saved to: {output_file}")

    except FileNotFoundError:
        print(f"\nError: PDF file not found at {pdf_path}")
        print("Please update the pdf_path variable with a valid file path.")
    except Exception as e:
        print(f"\nError during analysis: {e}")


def example_batch_processing():
    """
    Example 2: Analyze multiple PDF files in a directory
    """
    print("\n" + "=" * 60)
    print("Example 2: Batch Processing Multiple PDFs")
    print("=" * 60)

    # Initialize the analyzer
    analyzer = ManufacturingPartAnalyzer(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
    )

    # Directory containing PDF files
    pdf_directory = "sample_drawings/"
    output_file = "batch_analysis_results.json"

    try:
        # Analyze all PDFs in the directory
        results = analyzer.analyze_batch(
            pdf_directory=pdf_directory,
            output_file=output_file
        )

        # Display summary
        print(f"\nAnalyzed {len(results)} drawings")
        print(f"Results saved to: {output_file}")

        # Show summary statistics
        print("\nSummary:")
        complexity_counts = {}
        type_counts = {}

        for result in results:
            if 'error' not in result:
                complexity = result.get('complexity_level', 'Unknown')
                part_type = result.get('type', 'Unknown')

                complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1
                type_counts[part_type] = type_counts.get(part_type, 0) + 1

        print("\nComplexity Distribution:")
        for complexity, count in complexity_counts.items():
            print(f"  {complexity}: {count}")

        print("\nPart Type Distribution:")
        for part_type, count in type_counts.items():
            print(f"  {part_type}: {count}")

    except FileNotFoundError:
        print(f"\nError: Directory not found at {pdf_directory}")
        print("Please create a 'sample_drawings' directory with PDF files.")
    except Exception as e:
        print(f"\nError during batch processing: {e}")


def example_export_to_excel():
    """
    Example 3: Export batch results to Excel
    """
    print("\n" + "=" * 60)
    print("Example 3: Export Results to Excel")
    print("=" * 60)

    try:
        import pandas as pd

        # Load results from batch processing
        with open("batch_analysis_results.json", 'r') as f:
            results = json.load(f)

        # Convert to DataFrame
        df = pd.DataFrame(results)

        # Remove error entries
        df = df[~df['source_file'].str.contains('error', na=False)]

        # Export to Excel
        excel_file = "manufacturing_analysis.xlsx"
        df.to_excel(excel_file, index=False)
        print(f"\nResults exported to: {excel_file}")

        # Display preview
        print("\nPreview (first 5 rows):")
        print(df.head().to_string())

    except FileNotFoundError:
        print("\nError: batch_analysis_results.json not found")
        print("Run example_batch_processing() first to generate results.")
    except ImportError:
        print("\nError: pandas and openpyxl are required for Excel export")
        print("Install with: pip install pandas openpyxl")
    except Exception as e:
        print(f"\nError during export: {e}")


def check_configuration():
    """
    Check if Azure OpenAI configuration is set up correctly
    """
    print("=" * 60)
    print("Checking Configuration")
    print("=" * 60)

    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_DEPLOYMENT"
    ]

    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask API key for security
            if "KEY" in var:
                display_value = "*" * 20 + value[-4:] if len(value) > 4 else "****"
            else:
                display_value = value
            print(f"✓ {var}: {display_value}")
        else:
            print(f"✗ {var}: Not set")
            all_set = False

    if all_set:
        print("\nConfiguration looks good!")
    else:
        print("\nPlease set missing variables in your .env file")

    return all_set


def main():
    """
    Main function to run all examples
    """
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║  Manufacturing Part Analyzer - Example Usage Script      ║")
    print("╚" + "═" * 58 + "╝")
    print()

    # Check configuration first
    if not check_configuration():
        print("\nPlease configure your .env file before running examples.")
        print("See SETUP.md for detailed instructions.")
        return

    # Run examples
    print("\n" + "─" * 60)
    print("Choose an example to run:")
    print("─" * 60)
    print("1. Analyze a single PDF file")
    print("2. Batch process multiple PDFs")
    print("3. Export results to Excel")
    print("4. Run all examples")
    print("0. Exit")
    print("─" * 60)

    choice = input("\nEnter your choice (0-4): ").strip()

    if choice == "1":
        example_single_file()
    elif choice == "2":
        example_batch_processing()
    elif choice == "3":
        example_export_to_excel()
    elif choice == "4":
        example_single_file()
        example_batch_processing()
        example_export_to_excel()
    elif choice == "0":
        print("Exiting...")
    else:
        print("Invalid choice. Please run again and select 0-4.")

    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
