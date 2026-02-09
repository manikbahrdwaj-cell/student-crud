# patch_pyaudioop.py
import sys
import types

# Create a dummy module for pyaudioop
sys.modules['pyaudioop'] = types.ModuleType('pyaudioop')

# Provide dummy functions to avoid errors
def dummy_mul(*args, **kwargs):
    return b''

def dummy_ratecv(*args, **kwargs):
    return b'', 1

sys.modules['pyaudioop'].mul = dummy_mul
sys.modules['pyaudioop'].ratecv = dummy_ratecv
