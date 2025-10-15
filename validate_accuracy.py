"""
Accuracy Validation Tool for Manufacturing Part Analyzer

This script compares AI predictions against ground truth data to visualize accuracy
for each manufacturing parameter.

Usage:
    python validate_accuracy.py [predictions.json] [ground_truth.xlsx]

Requirements:
    - Predictions JSON file (from analyzer)
    - Ground truth Excel file with actual values
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import json
import argparse
from pathlib import Path


def normalize_part_id(part_id):
    """
    Normalize part ID for matching between predictions and ground truth

    Args:
        part_id: Part identifier string

    Returns:
        Normalized part identifier
    """
    part_id = str(part_id)
    # Remove common suffixes
    for ext in ['_drw', '.pdf', ' (1)', ' (2)', '.PDF', '.DRW']:
        part_id = part_id.replace(ext, '')
    return part_id.strip()


def convert_excel_value(value):
    """
    Convert Excel value to binary 0 or 1

    Args:
        value: Value from Excel (bool, int, float, or NaN)

    Returns:
        0 or 1
    """
    if pd.isna(value):
        return 0
    if isinstance(value, (bool, np.bool_)):
        return 1 if value else 0
    if isinstance(value, (int, float, np.integer, np.floating)):
        return 1 if value > 0 else 0
    return 0


def load_predictions(predictions_file):
    """Load predictions from JSON file"""
    with open(predictions_file, 'r') as f:
        return json.load(f)


def load_ground_truth(excel_file):
    """Load ground truth data from Excel file"""
    return pd.read_excel(excel_file)


def create_process_map():
    """
    Define mapping between prediction keys and Excel column names

    CUSTOMIZE THIS: Modify these mappings to match your Excel column names
    """
    return {
        'laser_cut': 'Laser Cut',
        'saw_shear': 'Saw/Shear',
        'break_press': 'Break Press',
        'fab': 'Fab Weld',
        'weld': 'Fab Weld',
        'painting': 'Painting',
        'heat_treat': 'Heat Treat',
        'plating': 'Plating',
        'cnc_machining_turning': 'CNC Machining /Turning',
        'metal_rolling': 'Metal Rolling',
        'casting_forging': 'Casting / Forging',
        'tube_bending': 'Tube Bending',
        'metal_spinning': 'Metal Spinning',
        'turret_punch_stamping': 'Turret Punch /Metal Stamping',
        'press': 'Press Inserts',
        'inserts': 'Press Inserts',
    }


def initialize_parameters():
    """
    Initialize list of all parameters to track

    CUSTOMIZE THIS: Add or remove parameters based on your needs
    """
    return [
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


def calculate_accuracy(predictions, ground_truth_df, process_map):
    """
    Calculate accuracy for each parameter

    Args:
        predictions: List of prediction dictionaries
        ground_truth_df: DataFrame with ground truth values
        process_map: Mapping of prediction keys to Excel columns

    Returns:
        Dictionary with accuracy statistics for each parameter
    """
    all_params = initialize_parameters()
    parameter_stats = {param: {'correct': 0, 'total': 0} for param in all_params}

    # Analyze each prediction
    for pred in predictions:
        # Get part identifier (customize based on your data structure)
        part_id = normalize_part_id(
            pred.get('part_identifier') or
            pred.get('part_name') or
            pred.get('source_file', '')
        )

        # Find matching part in ground truth
        # CUSTOMIZE THIS: Adjust the column name and matching logic
        matches = ground_truth_df[
            ground_truth_df['Part ID'].astype(str).apply(normalize_part_id) == part_id
        ]

        if len(matches) == 0:
            continue

        actual = matches.iloc[0]

        # Check Complexity Level
        if 'complexity_level' in pred and 'Complexity Level' in actual:
            parameter_stats['Complexity Level']['total'] += 1
            pred_complexity = str(pred.get('complexity_level', '')).lower()
            actual_complexity = str(actual.get('Complexity Level', '')).lower()

            if pred_complexity == actual_complexity:
                parameter_stats['Complexity Level']['correct'] += 1

        # Check Type
        if 'type' in pred and 'Type' in actual:
            parameter_stats['Type']['total'] += 1
            pred_type = str(pred.get('type', '')).lower()
            actual_type = str(actual.get('Type', '')).lower()

            if pred_type == actual_type:
                parameter_stats['Type']['correct'] += 1

        # Check Material
        if 'material' in pred and 'Material' in actual:
            parameter_stats['Material']['total'] += 1
            pred_material = str(pred.get('material', '')).lower()
            actual_material = str(actual.get('Material', '')).lower()

            if pred_material in actual_material or actual_material in pred_material:
                parameter_stats['Material']['correct'] += 1

        # Check manufacturing processes
        for pred_key, excel_col in process_map.items():
            if pred_key not in pred or excel_col not in actual:
                continue

            # Handle combined columns (like Fab Weld = fab + weld)
            if excel_col == 'Fab Weld':
                if pred_key == 'fab':
                    parameter_stats[excel_col]['total'] += 1
                    fab_pred = pred.get('fab', 0)
                    weld_pred = pred.get('weld', 0)
                    combined_pred = max(fab_pred, weld_pred)
                    actual_val = convert_excel_value(actual[excel_col])

                    if combined_pred == actual_val:
                        parameter_stats[excel_col]['correct'] += 1

            elif excel_col == 'Press Inserts':
                if pred_key == 'press':
                    parameter_stats[excel_col]['total'] += 1
                    press_pred = pred.get('press', 0)
                    inserts_pred = pred.get('inserts', 0)
                    combined_pred = max(press_pred, inserts_pred)
                    actual_val = convert_excel_value(actual[excel_col])

                    if combined_pred == actual_val:
                        parameter_stats[excel_col]['correct'] += 1
            else:
                # Single process comparison
                if pred_key not in ['weld', 'inserts']:  # Skip duplicates
                    parameter_stats[excel_col]['total'] += 1
                    predicted = pred[pred_key]
                    actual_val = convert_excel_value(actual[excel_col])

                    if predicted == actual_val:
                        parameter_stats[excel_col]['correct'] += 1

    return parameter_stats


def create_visualization(parameter_stats, output_file='accuracy_report.png'):
    """
    Create accuracy visualization

    Args:
        parameter_stats: Dictionary with accuracy statistics
        output_file: Path to save the visualization
    """
    # Prepare data for plotting
    params = []
    correct_pct = []
    incorrect_pct = []
    totals = []

    for param, stats in parameter_stats.items():
        if stats['total'] == 0:
            continue

        total = stats['total']
        correct = stats['correct']
        incorrect = total - correct

        params.append(param)
        correct_pct.append((correct / total) * 100)
        incorrect_pct.append((incorrect / total) * 100)
        totals.append(total)

    if not params:
        print("No data to visualize. Check that part IDs match between predictions and ground truth.")
        return

    # Create the visualization
    fig, ax = plt.subplots(figsize=(14, 10))

    # Create horizontal bar chart
    y_pos = np.arange(len(params))
    bar_height = 0.6

    # Plot bars
    bars_correct = ax.barh(y_pos, correct_pct, bar_height,
                           label='Correct', color='#2ecc71', alpha=0.8)
    bars_incorrect = ax.barh(y_pos, incorrect_pct, bar_height,
                             left=correct_pct, label='Incorrect', color='#e74c3c', alpha=0.8)

    # Customize the plot
    ax.set_xlabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Parameters', fontsize=12, fontweight='bold')
    ax.set_title('Manufacturing Prediction Accuracy by Parameter',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(params, fontsize=10)
    ax.set_xlim(0, 100)

    # Add percentage labels on bars
    for i, (correct, incorrect, total) in enumerate(zip(correct_pct, incorrect_pct, totals)):
        # Correct percentage
        if correct > 5:  # Only show if bar is wide enough
            ax.text(correct/2, i, f'{correct:.0f}%',
                    ha='center', va='center', fontweight='bold', color='white', fontsize=9)

        # Incorrect percentage
        if incorrect > 5:  # Only show if bar is wide enough
            ax.text(correct + incorrect/2, i, f'{incorrect:.0f}%',
                    ha='center', va='center', fontweight='bold', color='white', fontsize=9)

        # Total count on the right
        ax.text(102, i, f'n={total}', ha='left', va='center', fontsize=8, color='gray')

    # Add grid
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Add legend
    ax.legend(loc='lower right', fontsize=10, framealpha=0.9)

    # Calculate overall accuracy
    overall_correct = sum([stats['correct'] for stats in parameter_stats.values()])
    overall_total = sum([stats['total'] for stats in parameter_stats.values()])
    overall_accuracy = (overall_correct / overall_total * 100) if overall_total > 0 else 0

    # Add overall accuracy text box
    textstr = f'Overall Accuracy: {overall_accuracy:.1f}%\n({overall_correct}/{overall_total} predictions)'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=props, fontweight='bold')

    plt.tight_layout()

    # Save the figure
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Accuracy visualization saved to: {output_file}")

    return overall_accuracy, overall_correct, overall_total


def print_summary_table(parameter_stats):
    """Print summary table of accuracy statistics"""
    print("\n" + "=" * 80)
    print("ACCURACY BY PARAMETER")
    print("=" * 80)
    print(f"{'Parameter':<35} {'Correct':<10} {'Total':<10} {'Accuracy':<10}")
    print("-" * 80)

    # Calculate overall stats
    overall_correct = 0
    overall_total = 0

    for param, stats in parameter_stats.items():
        if stats['total'] == 0:
            continue

        accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"{param:<35} {stats['correct']:<10} {stats['total']:<10} {accuracy:>6.1f}%")

        overall_correct += stats['correct']
        overall_total += stats['total']

    overall_accuracy = (overall_correct / overall_total * 100) if overall_total > 0 else 0

    print("-" * 80)
    print(f"{'OVERALL':<35} {overall_correct:<10} {overall_total:<10} {overall_accuracy:>6.1f}%")
    print("=" * 80)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Validate Manufacturing Part Analyzer accuracy',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_accuracy.py predictions.json ground_truth.xlsx
  python validate_accuracy.py --output accuracy.png

For more information, see: ACCURACY_VALIDATION.md
        """
    )

    parser.add_argument('predictions', nargs='?',
                        default='analysis_results.json',
                        help='Path to predictions JSON file (default: analysis_results.json)')
    parser.add_argument('ground_truth', nargs='?',
                        default='ground_truth.xlsx',
                        help='Path to ground truth Excel file (default: ground_truth.xlsx)')
    parser.add_argument('-o', '--output',
                        default='accuracy_report.png',
                        help='Output file for visualization (default: accuracy_report.png)')

    args = parser.parse_args()

    # Check if files exist
    if not Path(args.predictions).exists():
        print(f"Error: Predictions file not found: {args.predictions}")
        print("\nUsage: python validate_accuracy.py [predictions.json] [ground_truth.xlsx]")
        print("See ACCURACY_VALIDATION.md for setup instructions.")
        sys.exit(1)

    if not Path(args.ground_truth).exists():
        print(f"Error: Ground truth file not found: {args.ground_truth}")
        print("\nUsage: python validate_accuracy.py [predictions.json] [ground_truth.xlsx]")
        print("See ACCURACY_VALIDATION.md for setup instructions.")
        sys.exit(1)

    print("Loading data...")
    predictions = load_predictions(args.predictions)
    ground_truth = load_ground_truth(args.ground_truth)

    print(f"✓ Loaded {len(predictions)} predictions")
    print(f"✓ Loaded {len(ground_truth)} ground truth records")

    print("\nCalculating accuracy...")
    process_map = create_process_map()
    parameter_stats = calculate_accuracy(predictions, ground_truth, process_map)

    print("\nCreating visualization...")
    overall_accuracy, overall_correct, overall_total = create_visualization(
        parameter_stats,
        args.output
    )

    print_summary_table(parameter_stats)

    print(f"\n✓ Validation complete!")
    print(f"  Overall Accuracy: {overall_accuracy:.1f}% ({overall_correct}/{overall_total})")


if __name__ == "__main__":
    main()
