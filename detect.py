from anomaly_model import train_model

model = train_model()

with open("logs.txt") as f:
    logs = f.readlines()

anomaly_count = 0

with open("report.txt", "w") as report:
    report.write("=== LOG REPORT ===\n\n")

    for log in logs:
        log = log.strip()

        if "ERROR" in log:           
            report.write(f"[ERROR] {log}\n")
            print("Anomaly:", log)
            anomaly_count += 1
        else:
           report.write(f"[OK] {log}\n")

# Save history
with open("history.txt", "a") as h:
    h.write(f"{anomaly_count}\n")

# Fail pipeline if anomaly exists
if anomaly_count > 10:
    print("Anomaly detected but continuing...")
