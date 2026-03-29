#!/bin/bash

cd /Users/hitarthtrivedi/Documents/PythonProgram/prism_mac

echo "$(date): run_prism.command started, waiting for network..."

# Wait for internet connectivity before proceeding
while ! ping -c 1 -W 1 8.8.8.8 >/dev/null 2>&1; do
    echo "$(date): Network not reachable, waiting 5 seconds..."
    sleep 5
done

echo "$(date): Network connected! Starting prism watcher loop..."

while true; do
    echo "$(date): Checking for notes updates..."
    /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 prism.py
    sleep 10
done
