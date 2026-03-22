import functools
import sys
import subprocess

def constrained_execution(max_retries: int = 3):
    """
    The Law of Loop Containment (law_001).
    Wraps execution blocks to physically prevent infinite LLM generation loops.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            errors = []
            for attempt in range(1, max_retries + 1):
                try:
                    print(f"   [CONSTRAINT CAGE] Attempt {attempt}/{max_retries}...")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"   [ERROR] Validation failed: {str(e)}")
                    errors.append(str(e))
            
            # The kill switch
            print("\n==================================================")
            print(f" [FATAL EVENT] MAX_RETRIES ({max_retries}) EXCEEDED.")
            print(" The AI has hallucinated itself into a death loop.")
            print("==================================================\n")
            print("Autonomously severing execution to preserve API budgets.")
            
            sys.exit(1)
        return wrapper
    return decorator
