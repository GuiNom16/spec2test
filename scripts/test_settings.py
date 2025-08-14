#!/usr/bin/env python3
"""
Test script to verify settings integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_settings_import():
    """Test that settings can be imported and used"""
    try:
        import config.settings as settings
        print("✅ Settings imported successfully")
        
        # Test that all expected variables exist
        expected_vars = [
            'DEFAULT_MODEL', 'CHUNK_SIZE', 'TIMEOUT_SECONDS',
            'SUPPORTED_FORMATS', 'TEMP_FILE_PREFIX',
            'CSV_SEPARATOR', 'CSV_FILENAME',
            'APP_TITLE', 'UPLOAD_LABEL'
        ]
        
        for var in expected_vars:
            if hasattr(settings, var):
                print(f"✅ {var} = {getattr(settings, var)}")
            else:
                print(f"❌ {var} not found")
                return False
        
        return True
    except ImportError as e:
        print(f"❌ Failed to import settings: {e}")
        return False

def test_prompt_integration():
    """Test that prompt uses CSV_SEPARATOR"""
    try:
        from config.settings import CSV_SEPARATOR
        from core.prompt import get_prompt
        
        prompt = get_prompt("Test requirements")
        if CSV_SEPARATOR in prompt:
            print(f"✅ Prompt uses CSV_SEPARATOR ({CSV_SEPARATOR})")
            return True
        else:
            print(f"❌ Prompt doesn't use CSV_SEPARATOR")
            return False
    except Exception as e:
        print(f"❌ Prompt test failed: {e}")
        return False

def main():
    """Run settings tests"""
    print("🧪 Testing Settings Integration\n")
    
    tests = [
        ("Settings Import", test_settings_import),
        ("Prompt Integration", test_prompt_integration)
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
        print("🎉 Settings integration is working correctly!")
    else:
        print("⚠️  Some settings tests failed.")

if __name__ == "__main__":
    main() 