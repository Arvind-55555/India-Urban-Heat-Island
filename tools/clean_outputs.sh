#!/bin/bash
#
# Clean old output files
# Usage: bash clean_outputs.sh
#

echo "================================================"
echo "Cleaning old output files..."
echo "================================================"
echo ""

# Remove old visualizations (keeping the latest 5)
cd "$(dirname "$0")/../outputs/visualizations" || exit 1
ls -t *.png 2>/dev/null | tail -n +6 | xargs -r rm --
echo "✓ Cleaned old visualizations (kept latest 5)"

# Remove old reports (keeping the latest 5)
cd "../reports" || exit 1
ls -t *.txt 2>/dev/null | tail -n +6 | xargs -r rm --
echo "✓ Cleaned old reports (kept latest 5)"

# Remove old datasets (keeping the latest 3)
cd "../../data/processed" || exit 1
ls -t *.csv 2>/dev/null | tail -n +4 | xargs -r rm --
echo "✓ Cleaned old datasets (kept latest 3)"

echo ""
echo "================================================"
echo "Cleanup complete!"
echo "================================================"

