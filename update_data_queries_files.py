#!/usr/bin/env python3
"""
Update all data-queries.md files in China-market skills to use the new query_tool.py approach.
"""

import os
import shutil
from pathlib import Path

def find_data_queries_files():
    """Find all data-queries.md files in China-market skills."""
    china_market_dir = Path("skills/China-market")
    files = list(china_market_dir.rglob("data-queries.md"))
    return sorted(files)

def backup_file(file_path):
    """Create a backup of the original file."""
    backup_path = file_path.with_suffix(".md.bak")
    shutil.copy2(file_path, backup_path)
    return backup_path

def update_file(file_path, template_path):
    """Update a data-queries.md file with the new template."""
    # Read the new template
    with open(template_path, 'r', encoding='utf-8') as f:
        new_content = f.read()
    
    # Backup the original file
    backup_path = backup_file(file_path)
    
    # Write the new content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return backup_path

def main():
    # Find all data-queries.md files
    files = find_data_queries_files()
    print(f"Found {len(files)} data-queries.md files")
    
    # Template path
    template_path = Path("skills/China-market/DATA_QUERIES_TEMPLATE_NEW.md")
    
    if not template_path.exists():
        print(f"Error: Template file not found: {template_path}")
        return
    
    # Update each file
    updated_files = []
    backup_files = []
    
    for file_path in files:
        try:
            backup_path = update_file(file_path, template_path)
            updated_files.append(file_path)
            backup_files.append(backup_path)
            print(f"✅ Updated: {file_path}")
            print(f"   Backup: {backup_path}")
        except Exception as e:
            print(f"❌ Error updating {file_path}: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total files found: {len(files)}")
    print(f"  Successfully updated: {len(updated_files)}")
    print(f"  Failed: {len(files) - len(updated_files)}")
    print(f"\nBackup files created with .bak extension")
    print(f"To restore a file: mv <file>.md.bak <file>.md")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
