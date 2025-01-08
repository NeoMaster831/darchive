"""
subpapi.py - Subprocess API
"""

import subprocess

def run_cmd(*args):
    """
    Run a command in the shell and return the output.
    """
    result = subprocess.run(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert(result.returncode == 0)
    return result.stdout, result.stderr

if __name__ == "__main__":
    print(run_cmd("ls -al"))