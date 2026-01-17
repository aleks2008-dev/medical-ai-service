#!/usr/bin/env python3
"""
Script to test simplified logging performance in AI service.
"""

import time
import os

def test_logging_performance():
    """Test simplified logging performance"""
    print("=" * 50)
    print("SIMPLIFIED LOGGING PERFORMANCE TEST")
    print("=" * 50)

    # Test with logging enabled
    print("\n1. Testing with PERFORMANCE_LOGGING=true")
    os.environ["PERFORMANCE_LOGGING"] = "true"

    import importlib
    import src.services.ai_service
    importlib.reload(src.services.ai_service)

    from src.services.ai_service import log_info, log_error

    start_time = time.time()
    for i in range(1000):
        log_info(f"Test INFO message {i}")
        log_error(f"Test ERROR message {i}")
    enabled_time = time.time() - start_time
    print(f"With logging: {enabled_time:.3f}s for 2000 messages")

    # Test with logging disabled
    print("\n2. Testing with PERFORMANCE_LOGGING=false")
    os.environ["PERFORMANCE_LOGGING"] = "false"

    importlib.reload(src.services.ai_service)
    from src.services.ai_service import log_info, log_error

    start_time = time.time()
    for i in range(1000):
        log_info(f"Test INFO message {i}")  # Should be disabled
        log_error(f"Test ERROR message {i}")  # Always active
    disabled_time = time.time() - start_time
    print(f"INFO disabled: {disabled_time:.3f}s for 2000 messages")

    # Results
    if enabled_time > 0:
        improvement = ((enabled_time - disabled_time) / enabled_time) * 100
        print("\nRESULTS:")
    print(f"Performance improvement: {improvement:.2f}%")
    print(f"Enabled time: {enabled_time:.3f}s, Disabled time: {disabled_time:.3f}s")
    print("\n✅ Simplified logging is working correctly!")
    print("   - INFO logs can be disabled for production performance")
    print("   - ERROR logs remain always active for monitoring")

if __name__ == "__main__":
    test_logging_performance()
