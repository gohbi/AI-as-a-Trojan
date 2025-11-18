#!/bin/bash
# Quick Start Script for AI Content Scraper
# This script sets up and runs the scraper

set -e

echo "=========================================="
echo "AI-as-a-Trojan Content Scraper Quick Start"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.7 or higher and try again."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Navigate to scraper directory
cd "$(dirname "$0")"

# Check if dependencies are installed
echo "Checking dependencies..."
if ! python3 -c "import requests" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt --user
else
    echo "✓ Dependencies already installed"
fi

echo ""
echo "Starting scraper..."
echo "This will search multiple sources for AI-related content."
echo "The process may take several minutes depending on network speed."
echo ""

# Run the scraper
python3 ai_content_scraper.py

echo ""
echo "=========================================="
echo "Scraping complete!"
echo "=========================================="
echo ""
echo "Results saved to:"
echo "  - scraped_content.json (raw data)"
echo "  - SCRAPED_CONTENT.md (formatted report)"
echo ""
echo "You can now review the results and add relevant"
echo "articles to the repository structure."
