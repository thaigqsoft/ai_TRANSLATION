#!/usr/bin/env python3
"""
structure_validator.py — Validate HTML structure after translation/polish

USAGE:
    python structure_validator.py --original /path/to/original --translated /path/to/translated

FEATURES:
- Compares HTML structure between original and translated files
- Checks <p> tag count preservation
- Validates tag hierarchy
- Reports mismatches
"""

import os
import re
import sys
import argparse
from pathlib import Path
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────────────────────────────────────
# FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def get_tag_structure(html):
    """Extract tag structure as a list of tag names."""
    soup = BeautifulSoup(html, 'html.parser')
    tags = []
    for tag in soup.find_all():
        tags.append(tag.name)
    return tags


def get_p_count(html):
    """Count <p> tags in HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    return len(soup.find_all('p'))


def get_text_length(html):
    """Get total text length (excluding tags)."""
    soup = BeautifulSoup(html, 'html.parser')
    return len(soup.get_text())


def validate_structure(original_html, translated_html, filename):
    """
    Validate that translated HTML preserves structure of original.
    Returns: (is_valid, issues_list)
    """
    issues = []
    
    # Check <p> count
    orig_p = get_p_count(original_html)
    trans_p = get_p_count(translated_html)
    
    if orig_p != trans_p:
        issues.append(f"Paragraph count mismatch: original={orig_p}, translated={trans_p}")
    
    # Check tag structure (simplified)
    orig_tags = get_tag_structure(original_html)
    trans_tags = get_tag_structure(translated_html)
    
    if orig_tags != trans_tags:
        # Find first difference
        for i, (o, t) in enumerate(zip(orig_tags, trans_tags)):
            if o != t:
                issues.append(f"Tag structure differs at position {i}: expected '{o}', got '{t}'")
                break
        
        if len(orig_tags) != len(trans_tags):
            issues.append(f"Tag count differs: original={len(orig_tags)}, translated={len(trans_tags)}")
    
    # Check text length (translated should be similar or longer due to Thai)
    orig_len = get_text_length(original_html)
    trans_len = get_text_length(translated_html)
    
    if trans_len < orig_len * 0.5:  # Translated should not be less than 50% of original
        issues.append(f"Text length suspicious: original={orig_len}, translated={trans_len}")
    
    return len(issues) == 0, issues


def compare_files(original_dir, translated_dir):
    """Compare all HTML files between two directories."""
    # Get file lists
    orig_files = set(f for f in os.listdir(original_dir) if f.endswith('.html'))
    trans_files = set(f for f in os.listdir(translated_dir) if f.endswith('.html'))
    
    # Check for missing files
    missing_in_trans = orig_files - trans_files
    missing_in_orig = trans_files - orig_files
    
    if missing_in_trans:
        print(f"Missing in translated: {len(missing_in_trans)} files")
        for f in list(missing_in_trans)[:5]:
            print(f"  - {f}")
    
    if missing_in_orig:
        print(f"Extra in translated: {len(missing_in_orig)} files")
        for f in list(missing_in_orig)[:5]:
            print(f"  - {f}")
    
    # Compare common files
    common_files = orig_files & trans_files
    valid_count = 0
    invalid_files = []
    
    for fname in sorted(common_files):
        orig_path = os.path.join(original_dir, fname)
        trans_path = os.path.join(translated_dir, fname)
        
        with open(orig_path, 'r', encoding='utf-8') as f:
            orig_html = f.read()
        
        with open(trans_path, 'r', encoding='utf-8') as f:
            trans_html = f.read()
        
        is_valid, issues = validate_structure(orig_html, trans_html, fname)
        
        if is_valid:
            valid_count += 1
        else:
            invalid_files.append((fname, issues))
    
    return valid_count, len(common_files), invalid_files


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Validate HTML structure after translation')
    parser.add_argument('--original', required=True, help='Directory with original HTML files')
    parser.add_argument('--translated', required=True, help='Directory with translated HTML files')
    parser.add_argument('--verbose', action='store_true', help='Show detailed issues')
    
    args = parser.parse_args()
    
    # Validate directories exist
    if not os.path.isdir(args.original):
        print(f"Error: Original directory not found: {args.original}")
        sys.exit(1)
    
    if not os.path.isdir(args.translated):
        print(f"Error: Translated directory not found: {args.translated}")
        sys.exit(1)
    
    print(f"Comparing:")
    print(f"  Original:   {args.original}")
    print(f"  Translated: {args.translated}")
    print()
    
    # Compare
    valid_count, total_files, invalid_files = compare_files(args.original, args.translated)
    
    # Summary
    print(f"\n{'=' * 50}")
    print(f"Total files compared: {total_files}")
    print(f"Valid:   {valid_count} ({valid_count/total_files*100:.1f}%)")
    print(f"Invalid: {len(invalid_files)} ({len(invalid_files)/total_files*100:.1f}%)")
    
    if invalid_files and args.verbose:
        print(f"\nInvalid files:")
        for fname, issues in invalid_files[:10]:
            print(f"\n  {fname}:")
            for issue in issues:
                print(f"    - {issue}")
        
        if len(invalid_files) > 10:
            print(f"  ... and {len(invalid_files) - 10} more")
    
    # Exit with error if any invalid
    sys.exit(0 if len(invalid_files) == 0 else 1)


if __name__ == "__main__":
    main()
