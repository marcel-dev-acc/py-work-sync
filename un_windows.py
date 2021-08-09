"""
Windows in all its glory likes doing some weird and wonderful things
This file provides a space to remove windows mannerisms
"""

# Installs dos2unix Linux
# sudo apt-get install -y dos2unix 

# recursively removes windows related stuff
# find . -type f -exec dos2unix {} \; # The . denotes the current folder (instead provide a folder path)