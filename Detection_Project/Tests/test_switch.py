import os
import time

print("I am going to switch to your Notes app in 3 seconds...")
time.sleep(3)

# This version uses different quotes to make sure 'Notes' is seen as an app name
os.system("osascript -e 'tell application \"Notes\" to activate'")

print("Did it work?")