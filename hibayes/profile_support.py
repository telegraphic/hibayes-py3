"""
# profile_support.py

Tools/decorator for code profiling
"""

import builtins

try:
    profile = builtins.profile
except AttributeError:
    # No line profiler, provide a pass-through version
    def profile(func):
        return func
