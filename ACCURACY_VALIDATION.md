# Accuracy Validation Guide

This guide explains how to validate the accuracy of the Manufacturing Part Analyzer predictions against your ground truth data.

## Overview

The `validate_accuracy.py` script compares AI predictions against actual/ground truth data to:
- Calculate accuracy for each manufacturing parameter
- Generate visual accuracy reports
- Identify areas for improvement

## Quick Start

```bash
# 1. Run your predictions
python example_usage.py  # or use the analyzer directly

# 2. Prepare your ground truth Excel file
# (See "Ground Truth Format" section below)

# 3. Run validation
python validate_accuracy.py predictions.json ground_truth.xlsx
```

---

## Ground Truth Format

### Required Excel Structure

Your ground truth Excel file should have these columns:

| Column Name | Type | Description | Example |
|-------------|------|-------------|---------|
| Part ID | String | Unique part identifier | "bracket_001" |
| Complexity Level | String | Simple/Moderate/Complex/Very Complex | "Complex" |
| Type | String | Part type | "Bracket" |
| Material | String | Material specification | "Steel" |
| Laser Cut | Binary | 0 or 1 | 1 |
| Saw/Shear | Binary | 0 or 1 | 0 |
| Break Press | Binary | 0 or 1 | 1 |
| Fab Weld | Binary | 0 or 1 (combines fab + weld) | 1 |
| Painting | Binary | 0 or 1 | 1 |
| Heat Treat | Binary | 0 or 1 | 0 |
| Plating | Binary | 0 or 1 | 0 |
| CNC Machining /Turning | Binary | 0 or 1 | 1 |
| Metal Rolling | Binary | 0 or 1 | 0 |
| Casting / Forging | Binary | 0 or 1 | 0 |
| Tube Bending | Binary | 0 or 1 | 0 |
| Metal Spinning | Binary | 0 or 1 | 0 |
| Turret Punch /Metal Stamping | Binary | 0 or 1 | 0 |
| Press Inserts | Binary | 0 or 1 (combines press + inserts) | 0 |

### Example Ground Truth File

Create an Excel file `ground_truth.xlsx`:

| Part ID | Complexity Level | Type | Material | Laser Cut | Saw/Shear | Break Press | Fab Weld | ... |
|---------|-----------------|------|----------|-----------|-----------|-------------|----------|-----|
| bracket_front.pdf | Complex | Bracket | Steel | 0 | 1 | 1 | 1 | ... |
| shaft_001.pdf | Moderate | Shaft | Aluminum | 0 | 0 | 0 | 0 | ... |
| weldment_arm.pdf | Very Complex | Weldment | Steel | 0 | 1 | 0 | 1 | ... |

### Template File

A template Excel file is provided: `ground_truth_template.xlsx`

Download and fill it out with your actual values.

---

## Usage

### Basic Usage

```bash
python validate_accuracy.py predictions.json ground_truth.xlsx
```

### With Custom Output

```bash
python validate_accuracy.py predictions.json ground_truth.xlsx --output my_accuracy_report.png
```

### Using Default Files

If you name your files with defaults, you can just run:

```bash
python validate_accuracy.py
```

This looks for:
- `analysis_results.json` (predictions)
- `ground_truth.xlsx` (ground truth)

---

## Customization

### Custom Column Names

If your Excel has different column names, edit `validate_accuracy.py`:

```python
def create_process_map():
    """Customize these mappings to match your Excel columns"""
    return {
        'laser_cut': 'Your Column Name for Laser Cut',
        'saw_shear': 'Your Column Name for Saw/Shear',
        # ... add your column names here
    }
```

### Custom Part ID Matching

If your part identifiers need special handling, edit the `normalize_part_id()` function:

```python
def normalize_part_id(part_id):
    part_id = str(part_id)
    # Add your custom logic here
    part_id = part_id.replace('your_prefix_', '')
    return part_id.strip()
```

---

## Output

### Visual Report

The script generates a horizontal bar chart showing:
- **Green bars**: Correct predictions (%)
- **Red bars**: Incorrect predictions (%)
- **n=X labels**: Number of samples for each parameter
- **Overall accuracy box**: Total accuracy across all parameters

Example output: `accuracy_report.png`

### Console Output

```
================================================================================
ACCURACY BY PARAMETER
================================================================================
Parameter                           Correct    Total      Accuracy
--------------------------------------------------------------------------------
Complexity Level                    18         20         90.0%
Type                                15         20         75.0%
Laser Cut                           19         20         95.0%
Saw/Shear                           18         20         90.0%
Break Press                         17         20         85.0%
Fab Weld                            16         20         80.0%
...
--------------------------------------------------------------------------------
OVERALL                             150        180        83.3%
================================================================================
```

---

## Best Practices

### 1. Start Small

Test with 5-10 parts first:
- Easier to verify ground truth accuracy
- Faster iteration
- Good for identifying issues

### 2. Ensure Part ID Matching

The most common issue is mismatched Part IDs between predictions and ground truth.

**Tips:**
- Use consistent naming (e.g., always include `.pdf` or never include it)
- Check for extra spaces or special characters
- Use the `normalize_part_id()` function to handle variations

### 3. Verify Ground Truth

Double-check your ground truth data:
- Have a domain expert review
- Ensure binary values are truly 0 or 1
- Check for typos in part names

### 4. Handle Edge Cases

Some parts might be ambiguous:
- Document assumptions
- Be consistent across similar parts
- Note uncertain cases

---

## Troubleshooting

### Issue: "No data to visualize"

**Cause**: Part IDs don't match between predictions and ground truth

**Solution**:
1. Print part IDs from both files:
   ```python
   # Add this to validate_accuracy.py temporarily
   print("Prediction IDs:", [normalize_part_id(p.get('source_file')) for p in predictions])
   print("Ground truth IDs:", [normalize_part_id(str(id)) for id in ground_truth['Part ID']])
   ```
2. Adjust the `normalize_part_id()` function to handle differences

### Issue: "KeyError: 'Part ID'"

**Cause**: Excel column name doesn't match expected name

**Solution**:
- Ensure your Excel has a column named "Part ID"
- Or modify the script to use your column name:
  ```python
  matches = ground_truth_df[
      ground_truth_df['YOUR_COLUMN_NAME'].astype(str).apply(normalize_part_id) == part_id
  ]
  ```

### Issue: Low accuracy for specific parameter

**Possible causes**:
1. **Prompt needs adjustment**: The AI prompt may not emphasize this parameter enough
2. **Ambiguous drawings**: Some drawings may not clearly show this feature
3. **Ground truth error**: Double-check your ground truth values
4. **Model limitation**: Some features may be harder for the model to detect

**Solutions**:
- Review misclassified examples
- Adjust the analysis prompt in `manufacturing_part_analyzer.py`
- Add more context or examples to the prompt
- Consider fine-tuning if using custom models

---

## Advanced Usage

### Batch Validation Across Datasets

```bash
# Validate multiple datasets
for dataset in dataset1 dataset2 dataset3; do
    python validate_accuracy.py \
        predictions_${dataset}.json \
        ground_truth_${dataset}.xlsx \
        --output accuracy_${dataset}.png
done
```

### Export Results to CSV

Modify the script to save results:

```python
# Add at the end of main()
import csv

with open('accuracy_results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Parameter', 'Correct', 'Total', 'Accuracy'])
    for param, stats in parameter_stats.items():
        if stats['total'] > 0:
            accuracy = (stats['correct'] / stats['total'] * 100)
            writer.writerow([param, stats['correct'], stats['total'], f"{accuracy:.1f}%"])
```

### Compare Multiple Models

Run predictions with different models/prompts and compare:

```bash
python validate_accuracy.py predictions_model_v1.json ground_truth.xlsx -o v1_accuracy.png
python validate_accuracy.py predictions_model_v2.json ground_truth.xlsx -o v2_accuracy.png
```

---

## Integration with CI/CD

### Automated Testing

Add to your CI pipeline:

```yaml
# .github/workflows/accuracy_test.yml
name: Accuracy Test

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run accuracy validation
        run: |
          python validate_accuracy.py
          # Fail if accuracy drops below threshold
          python -c "
          import json
          with open('accuracy_results.json') as f:
              accuracy = json.load(f)['overall_accuracy']
          assert accuracy >= 80.0, f'Accuracy {accuracy}% below threshold'
          "
```

---

## Tips for High Accuracy

1. **High-quality PDFs**: Use 300+ DPI scans
2. **Clear drawings**: Ensure text and symbols are legible
3. **Consistent ground truth**: Use same criteria across all parts
4. **Prompt engineering**: Adjust prompts based on validation results
5. **Iterative improvement**: Review errors and adjust
6. **Domain expertise**: Have experts validate both predictions and ground truth

---

## Example Workflow

```bash
# 1. Analyze parts
python example_usage.py
# Output: analysis_results.json

# 2. Create ground truth file
# - Open ground_truth_template.xlsx
# - Fill in actual values for your parts
# - Save as ground_truth.xlsx

# 3. Validate accuracy
python validate_accuracy.py analysis_results.json ground_truth.xlsx

# 4. Review results
# - Check accuracy_report.png
# - Review console output
# - Identify low-accuracy parameters

# 5. Improve (if needed)
# - Adjust prompts in manufacturing_part_analyzer.py
# - Re-run analysis
# - Validate again
```

---

## Support

For help with accuracy validation:
1. Check this guide thoroughly
2. Review ground truth format
3. Ensure Part ID matching works
4. Open an issue on GitHub with:
   - Sample of your predictions JSON
   - Sample of your ground truth Excel
   - Error messages or output

---

## Related Documentation

- [README.md](README.md) - Main project documentation
- [SETUP.md](SETUP.md) - Setup instructions
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command reference

---

**Remember**: Accuracy validation is iterative. Start small, verify carefully, and improve gradually.
