"""
Create a template Excel file for ground truth data

This script generates a template Excel file that users can fill in
with their actual/ground truth manufacturing data for accuracy validation.

Usage:
    python create_ground_truth_template.py [output_file.xlsx]
"""

import pandas as pd
import sys


def create_template(output_file='ground_truth_template.xlsx'):
    """
    Create ground truth template Excel file

    Args:
        output_file: Path to save the template file
    """

    # Define columns
    columns = [
        'Part ID',
        'Complexity Level',
        'Type',
        'Material',
        'Laser Cut',
        'Saw/Shear',
        'Break Press',
        'Fab Weld',
        'Painting',
        'Heat Treat',
        'Plating',
        'CNC Machining /Turning',
        'Metal Rolling',
        'Casting / Forging',
        'Tube Bending',
        'Metal Spinning',
        'Turret Punch /Metal Stamping',
        'Press Inserts'
    ]

    # Create example data with instructions
    example_data = [
        {
            'Part ID': 'example_bracket.pdf',
            'Complexity Level': 'Complex',
            'Type': 'Bracket',
            'Material': 'Steel',
            'Laser Cut': 0,
            'Saw/Shear': 1,
            'Break Press': 1,
            'Fab Weld': 1,
            'Painting': 1,
            'Heat Treat': 0,
            'Plating': 0,
            'CNC Machining /Turning': 1,
            'Metal Rolling': 0,
            'Casting / Forging': 0,
            'Tube Bending': 0,
            'Metal Spinning': 0,
            'Turret Punch /Metal Stamping': 0,
            'Press Inserts': 0
        },
        {
            'Part ID': 'example_shaft.pdf',
            'Complexity Level': 'Moderate',
            'Type': 'Shaft',
            'Material': 'Aluminum',
            'Laser Cut': 0,
            'Saw/Shear': 1,
            'Break Press': 0,
            'Fab Weld': 0,
            'Painting': 0,
            'Heat Treat': 0,
            'Plating': 1,
            'CNC Machining /Turning': 1,
            'Metal Rolling': 0,
            'Casting / Forging': 0,
            'Tube Bending': 0,
            'Metal Spinning': 0,
            'Turret Punch /Metal Stamping': 0,
            'Press Inserts': 0
        },
        {
            'Part ID': 'example_weldment.pdf',
            'Complexity Level': 'Very Complex',
            'Type': 'Weldment',
            'Material': 'Steel',
            'Laser Cut': 0,
            'Saw/Shear': 1,
            'Break Press': 1,
            'Fab Weld': 1,
            'Painting': 1,
            'Heat Treat': 0,
            'Plating': 0,
            'CNC Machining /Turning': 0,
            'Metal Rolling': 0,
            'Casting / Forging': 0,
            'Tube Bending': 0,
            'Metal Spinning': 0,
            'Turret Punch /Metal Stamping': 0,
            'Press Inserts': 0
        }
    ]

    # Create DataFrame
    df = pd.DataFrame(example_data, columns=columns)

    # Create Excel writer with formatting
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Write main sheet
        df.to_excel(writer, sheet_name='Ground Truth', index=False)

        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Ground Truth']

        # Add instructions sheet
        instructions = pd.DataFrame({
            'Instructions': [
                'GROUND TRUTH DATA TEMPLATE',
                '',
                'How to use this template:',
                '1. Delete the example rows (rows 2-4)',
                '2. Add your actual part data',
                '3. Fill in all columns for each part',
                '4. Save the file',
                '5. Run: python validate_accuracy.py predictions.json ground_truth.xlsx',
                '',
                'Column Descriptions:',
                '',
                'Part ID: Unique identifier matching your PDF filename (e.g., "bracket_001.pdf")',
                'Complexity Level: Choose from: Simple, Moderate, Complex, Very Complex',
                'Type: Part type (e.g., Bracket, Shaft, Assembly, Weldment, Fastener)',
                'Material: Material specification (e.g., Steel, Aluminum, Stainless Steel)',
                '',
                'Manufacturing Processes (enter 0 or 1):',
                'Laser Cut: 1 if part requires laser cutting, 0 if not',
                'Saw/Shear: 1 if part requires sawing or shearing, 0 if not',
                'Break Press: 1 if part requires brake press/bending, 0 if not',
                'Fab Weld: 1 if part requires fabrication or welding, 0 if not',
                'Painting: 1 if part requires painting/coating, 0 if not',
                'Heat Treat: 1 if part requires heat treatment, 0 if not',
                'Plating: 1 if part requires plating, 0 if not',
                'CNC Machining /Turning: 1 if part requires CNC machining or turning, 0 if not',
                'Metal Rolling: 1 if part requires metal rolling, 0 if not',
                'Casting / Forging: 1 if part is cast or forged, 0 if not',
                'Tube Bending: 1 if part requires tube bending, 0 if not',
                'Metal Spinning: 1 if part requires metal spinning, 0 if not',
                'Turret Punch /Metal Stamping: 1 if part requires turret punch or stamping, 0 if not',
                'Press Inserts: 1 if part requires press operations or inserts, 0 if not',
                '',
                'Important Notes:',
                '- Part ID must match the filename in your predictions (without path)',
                '- Use 0 or 1 for all process columns (not True/False or Yes/No)',
                '- Be consistent with complexity level and type naming',
                '- Verify all data carefully - this is your ground truth!',
                '',
                'For more help, see: ACCURACY_VALIDATION.md'
            ]
        })

        instructions.to_excel(writer, sheet_name='Instructions', index=False, header=False)

    print(f"✓ Ground truth template created: {output_file}")
    print(f"\nNext steps:")
    print(f"1. Open {output_file}")
    print(f"2. Read the Instructions sheet")
    print(f"3. Fill in the 'Ground Truth' sheet with your actual data")
    print(f"4. Save the file")
    print(f"5. Run: python validate_accuracy.py predictions.json {output_file}")


def main():
    """Main function"""
    output_file = 'ground_truth_template.xlsx'

    if len(sys.argv) > 1:
        output_file = sys.argv[1]

    try:
        create_template(output_file)
    except Exception as e:
        print(f"Error creating template: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
