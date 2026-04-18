import random
import time

logs = [
    "INFO User login",
    "INFO File uploaded",
    "INFO Service started",
    "INFO Connection established",

    "WARNING Disk usage high",
    "WARNING Memory usage high",
    "WARNING CPU temperature high",

    "ERROR Database failed",
    "ERROR Timeout occurred",
    "ERROR API request failed",
    "ERROR Disk read failure"
]

for _ in range(50):   # runs only 50 times
    with open("logs.txt", "a") as f:
        f.write(random.choice(logs) + "\n")

    time.sleep(1)

print("Log generation completed")
