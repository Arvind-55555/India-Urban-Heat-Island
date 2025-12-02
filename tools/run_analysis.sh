#!/bin/bash
#
# Quick script to run UHI data analysis
# Usage: bash run_analysis.sh
#

echo "================================================"
echo "Urban Heat Island Data Analysis"
echo "================================================"
echo ""

# Navigate to the analysis directory
cd "$(dirname "$0")/../src/analysis" || exit 1

# Run the analyzer
python analyzer.py

echo ""
echo "================================================"
echo "Analysis complete!"
echo "Check outputs/ for visualizations and reports"
echo "================================================"

