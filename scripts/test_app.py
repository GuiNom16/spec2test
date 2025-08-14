#!/usr/bin/env python3
"""
Simple test script for Spec2Test Lite components
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.chunker import chunk_text
from core.parser import clean_text
from core.generator import parse_llm_csv_output
import pandas as pd

def test_chunker():
    """Test the text chunking functionality"""
    print("Testing chunker...")
    
    # Test with simple text
    text = "This is paragraph 1.\n\nThis is paragraph 2.\n\nThis is paragraph 3."
    chunks = chunk_text(text, max_chars=50)
    
    print(f"Input text length: {len(text)}")
    print(f"Number of chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1} ({len(chunk)} chars): {chunk[:30]}...")
    
    return len(chunks) > 0

def test_parser():
    """Test the text cleaning functionality"""
    print("\nTesting parser...")
    
    # Test with text containing intro content
    text = "Introduction\nTable of Contents\n\nRequirement 1: User login\nRequirement 2: User logout"
    cleaned = clean_text(text)
    
    print(f"Original text: {text[:50]}...")
    print(f"Cleaned text: {cleaned[:50]}...")
    
    return "Requirement" in cleaned

def test_csv_parser():
    """Test the CSV output parsing"""
    print("\nTesting CSV parser...")
    
    # Test with valid CSV
    valid_csv = """Title|Description
User Login|User can login with valid credentials
User Logout|User can logout successfully"""
    
    df = parse_llm_csv_output(valid_csv)
    print(f"Parsed DataFrame shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    if not df.empty:
        print("Sample data:")
        print(df.head())
    
    return not df.empty and "Title" in df.columns

def main():
    """Run all tests"""
    print("🧪 Running Spec2Test Lite Tests\n")
    
    tests = [
        ("Chunker", test_chunker),
        ("Parser", test_parser),
        ("CSV Parser", test_csv_parser)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
        except Exception as e:
            results.append((test_name, False))
            print(f"❌ ERROR - {test_name}: {str(e)}")
    
    print(f"\n📊 Results: {sum(1 for _, r in results if r)}/{len(results)} tests passed")
    
    if all(result for _, result in results):
        print("🎉 All tests passed! Your Spec2Test Lite is ready for launch.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main() 