#!/usr/bin/env python3

def print_hello():
    try:
        request = str("hello its working")
        return request
    except Exception as e:
        print(f"operation failed: {e}")
        return None

if __name__ == "__main__":
    print(print_hello())
