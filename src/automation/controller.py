# src/automation/controller.py

def handle_automation(detections):
    for det in detections:
        obj = det["class"]
        if obj == "box":
            print("🟢 Sent to Left Conveyor")
        elif obj == "bottle":
            print("🔵 Sent to Right Conveyor")
        else:
            print(f"🟡 Sent {obj} to Center Conveyor")
