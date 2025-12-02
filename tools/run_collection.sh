#!/bin/bash
#
# Quick script to run enhanced UHI data collection
# Usage: bash run_collection.sh
#

echo "================================================"
echo "Urban Heat Island Data Collection"
echo "================================================"
echo ""

# Navigate to the data collection directory
cd "$(dirname "$0")/../src/data_collection" || exit 1

# Run the enhanced collector
python enhanced_collector.py

echo ""
echo "================================================"
echo "Data collection complete!"
echo "Check data/processed/ for the output dataset"
echo "================================================"

