# Fixes relative import error with the api script being at the same directory level as other scripts
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))