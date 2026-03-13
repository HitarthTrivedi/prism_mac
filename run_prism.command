#!/bin/zsh
# ─────────────────────────────────────────────
#  Prism AI Agent Router — Double-click to run
# ─────────────────────────────────────────────

# Move to the folder where this script lives
cd "$(dirname "$0")"

echo "======================================"
echo "  🌈 Starting Prism AI Agent Router"
echo "======================================"

# Run the script
python3 prism.py

echo ""
echo "======================================"
echo "  ✅ Prism finished. Press any key to close."
echo "======================================"
read -r -k 1
