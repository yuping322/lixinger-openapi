#!/bin/bash
# Risk Monitor Rules Schema Validation Script
# Usage: ./scripts/validate-rules.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(dirname "$SCRIPT_DIR")"
RULES_DIR="$PLUGIN_ROOT/skills/risk-signal-engine/rules"
SCHEMA_FILE="$PLUGIN_ROOT/templates/rules-schema.json"

TOTAL=0
PASSED=0
FAILED=0
FAILED_FILES=()

if [[ ! -f "$SCHEMA_FILE" ]]; then
    echo "ERROR: Schema file not found: $SCHEMA_FILE"
    exit 1
fi

if [[ ! -d "$RULES_DIR" ]]; then
    echo "ERROR: Rules directory not found: $RULES_DIR"
    exit 1
fi

echo "=== Risk Monitor Rules Schema Validation ==="
echo "Schema: $SCHEMA_FILE"
echo "Rules directory: $RULES_DIR"
echo ""

for rule_file in "$RULES_DIR"/*.json; do
    if [[ -f "$rule_file" ]]; then
        TOTAL=$((TOTAL + 1))
        filename=$(basename "$rule_file")
        
        if jsonschema -i "$rule_file" "$SCHEMA_FILE" > /dev/null 2>&1; then
            PASSED=$((PASSED + 1))
            echo "[PASS] $filename"
        else
            FAILED=$((FAILED + 1))
            FAILED_FILES+=("$filename")
            echo "[FAIL] $filename"
            jsonschema -i "$rule_file" "$SCHEMA_FILE" 2>&1 | head -5
            echo ""
        fi
    fi
done

echo ""
echo "=== Validation Summary ==="
echo "Total:   $TOTAL"
echo "Passed:  $PASSED"
echo "Failed:  $FAILED"

if [[ $FAILED -gt 0 ]]; then
    echo ""
    echo "Failed files:"
    for f in "${FAILED_FILES[@]}"; do
        echo "  - $f"
    done
    exit 1
fi

echo ""
echo "All rules validated successfully."
exit 0