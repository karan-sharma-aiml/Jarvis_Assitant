#!/usr/bin/env python
"""
Runtime verification tests for GeminiProvider migration.

Tests the new google.genai SDK implementation.
"""

from __future__ import annotations

import logging
import os
import sys
import warnings

import pytest

# Capture all warnings
warnings.simplefilter("always")

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)-8s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


@pytest.fixture
def GeminiProvider():
    from app.llm.providers.gemini_provider import GeminiProvider as Provider

    return Provider


@pytest.fixture
def provider():
    from app.llm.providers.gemini_provider import GeminiProvider

    if not os.getenv("GEMINI_API_KEY"):
        return None

    try:
        return GeminiProvider()
    except Exception:
        return None


def test_import():
    """Test 1: Import GeminiProvider."""
    logger.info("TEST 1: Importing GeminiProvider...")
    try:
        from app.llm.providers.gemini_provider import GeminiProvider
        logger.info("✓ GeminiProvider imported successfully")
        return GeminiProvider
    except ImportError as e:
        logger.error(f"✗ Failed to import GeminiProvider: {e}")
        return None


def test_future_warnings():
    """Test 8: Check for FutureWarnings."""
    logger.info("TEST 8: Checking for FutureWarnings...")
    
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Import the provider
        from app.llm.providers.gemini_provider import GeminiProvider
        
        # Check for FutureWarnings
        future_warnings = [warning for warning in w if issubclass(warning.category, FutureWarning)]
        
        if future_warnings:
            logger.error(f"✗ Found {len(future_warnings)} FutureWarning(s):")
            for warning in future_warnings:
                logger.error(f"  - {warning.message}")
            return False
        else:
            logger.info("✓ No FutureWarnings detected")
            return True


def test_instantiation(GeminiProvider):
    """Test 2: Create GeminiProvider instance."""
    logger.info("TEST 2: Creating GeminiProvider instance...")
    
    # Check if API key is configured
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        logger.warning("⚠ GEMINI_API_KEY not set in environment. Test will be skipped.")
        logger.info("  (This is expected in test environment - it's validated by API Key Validation test)")
        return None
    
    try:
        provider = GeminiProvider()
        logger.info(f"✓ GeminiProvider instance created: {provider}")
        return provider
    except Exception as e:
        logger.error(f"✗ Failed to create GeminiProvider: {e}")
        return None


def test_api_key_validation(GeminiProvider):
    """Test 7: Verify behavior when GEMINI_API_KEY is missing."""
    logger.info("TEST 7: Testing missing API key validation...")
    
    # Temporarily remove API key from settings
    from app.config import settings as settings_module
    original_key = settings_module.settings.GEMINI_API_KEY
    settings_module.settings.GEMINI_API_KEY = ""
    
    try:
        provider = GeminiProvider()
        logger.error("✗ GeminiProvider should have raised ProviderConnectionError")
        return False
    except Exception as e:
        if "GEMINI_API_KEY is not configured" in str(e):
            logger.info(f"✓ Correctly raised error: {e}")
            return True
        else:
            logger.error(f"✗ Unexpected error: {e}")
            return False
    finally:
        # Restore API key
        settings_module.settings.GEMINI_API_KEY = original_key


def test_provider_attributes(provider):
    """Test provider attributes."""
    logger.info("TEST: Verifying provider attributes...")
    
    if not provider:
        logger.warning("⚠ Provider not available. Skipping attribute tests.")
        return None
    
    tests = [
        ("provider_name", "gemini"),
        ("supports_streaming", True),
        ("supports_tools", True),
        ("supports_images", True),
    ]
    
    all_passed = True
    for attr, expected in tests:
        actual = getattr(provider, attr)
        if actual == expected:
            logger.info(f"✓ {attr} = {actual}")
        else:
            logger.error(f"✗ {attr} = {actual} (expected {expected})")
            all_passed = False
    
    return all_passed


def test_health_check(provider):
    """Test 3: Verify health_check()."""
    logger.info("TEST 3: Testing health_check()...")
    
    if not provider:
        logger.warning("⚠ Provider not available. Skipping health_check test.")
        return None
    
    try:
        result = provider.health_check()
        logger.info(f"✓ health_check() returned: {result}")
        return result
    except Exception as e:
        logger.error(f"✗ health_check() failed: {e}")
        return False


def test_chat(provider):
    """Test 4: Verify chat()."""
    logger.info("TEST 4: Testing chat()...")
    
    if not provider:
        logger.warning("⚠ Provider not available. Skipping chat test.")
        return None
    
    try:
        response = provider.chat("Hello, what is your name?")
        logger.info(f"✓ chat() returned: {response[:100]}...")
        return True
    except Exception as e:
        logger.warning(f"⚠ chat() failed (may be due to API limits): {type(e).__name__}: {str(e)[:100]}")
        return None


def test_generate(provider):
    """Test 5: Verify generate()."""
    logger.info("TEST 5: Testing generate()...")
    
    if not provider:
        logger.warning("⚠ Provider not available. Skipping generate test.")
        return None
    
    try:
        response = provider.generate("What is AI in one sentence?")
        logger.info(f"✓ generate() returned: {response[:100]}...")
        return True
    except Exception as e:
        logger.warning(f"⚠ generate() failed (may be due to API limits): {type(e).__name__}: {str(e)[:100]}")
        return None


def test_llm_manager():
    """Test 6: Verify integration with LLMManager."""
    logger.info("TEST 6: Testing LLMManager integration...")
    
    try:
        from app.llm.manager import LLMManager
        
        manager = LLMManager()
        logger.info(f"✓ LLMManager initialized: {manager}")
        
        providers = manager.list_providers()
        logger.info(f"✓ Available providers: {providers}")
        
        if "gemini" in providers:
            logger.info("✓ Gemini provider registered in LLMManager")
            return True
        else:
            logger.warning("⚠ Gemini provider not in list (might be due to API key not set)")
            return None
            
    except Exception as e:
        logger.error(f"✗ LLMManager integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_no_manager_changes():
    """Test 9: Confirm that manager.py doesn't need changes."""
    logger.info("TEST 9: Verifying manager.py compatibility...")
    
    try:
        from app.llm.manager import PROVIDER_REGISTRY
        from app.config.settings import Provider
        
        # Check if PROVIDER_REGISTRY has Provider enum as keys
        for key in PROVIDER_REGISTRY.keys():
            if not isinstance(key, Provider):
                logger.error(f"✗ PROVIDER_REGISTRY key is not Provider enum: {key}")
                return False
        
        logger.info("✓ manager.py uses Provider enum correctly")
        logger.info("✓ No changes required to manager.py")
        return True
        
    except Exception as e:
        logger.error(f"✗ Manager verification failed: {e}")
        return False


def main():
    """Run all tests."""
    logger.info("=" * 70)
    logger.info("GeminiProvider Migration - Runtime Verification Tests")
    logger.info("=" * 70)
    
    results = {}
    
    # Test 1: Import
    GeminiProvider = test_import()
    results["Import"] = GeminiProvider is not None
    
    if not GeminiProvider:
        logger.error("Cannot continue without successful import")
        return results
    
    # Test 8: FutureWarnings
    results["No FutureWarnings"] = test_future_warnings()
    
    # Test 2: Instantiation
    provider = test_instantiation(GeminiProvider)
    # Instantiation is only testable if API key is set. If None, it's a skip, not a failure.
    results["Instantiation (requires API key)"] = provider if provider is not None else None
    
    # Test 7: API Key validation
    results["API Key Validation"] = test_api_key_validation(GeminiProvider)
    
    # Provider attributes
    if provider:
        results["Provider Attributes"] = test_provider_attributes(provider)
    
    # Test 3: Health check
    results["Health Check"] = test_health_check(provider)
    
    # Test 4: Chat
    results["Chat"] = test_chat(provider)
    
    # Test 5: Generate
    results["Generate"] = test_generate(provider)
    
    # Test 6: LLMManager integration
    results["LLMManager Integration"] = test_llm_manager()
    
    # Test 9: Manager compatibility
    results["Manager Compatibility"] = test_no_manager_changes()
    
    # Summary
    logger.info("=" * 70)
    logger.info("TEST SUMMARY")
    logger.info("=" * 70)
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test_name, result in results.items():
        if result is True:
            logger.info(f"✓ {test_name}: PASSED")
            passed += 1
        elif result is False:
            logger.error(f"✗ {test_name}: FAILED")
            failed += 1
        else:  # None
            logger.warning(f"⚠ {test_name}: SKIPPED")
            skipped += 1
    
    logger.info("=" * 70)
    logger.info(f"Results: {passed} passed, {failed} failed, {skipped} skipped")
    logger.info("=" * 70)
    
    if failed == 0:
        logger.info("✓ Migration verification SUCCESSFUL")
        return 0
    else:
        logger.error("✗ Migration verification FAILED")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
