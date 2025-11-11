# src/feedback/retrain.py
from ultralytics import YOLO
import os

def retrain_model():
    """
    Retrains the YOLOv8 model using existing dataset and new feedback data.
    """
    # Path to your model
    model_path = "experiments/yolov8/best.pt"
    data_config = "data/dataset.yaml"

    if not os.path.exists(model_path):
        print("❌ Model not found! Train your base model first.")
        return

    print("🔄 Starting adaptive retraining using feedback data...")

    model = YOLO(model_path)
    model.train(data=data_config, epochs=10, resume=True)

    print("✅ Retraining complete! New weights saved in runs/detect/train/weights/best.pt")

if __name__ == "__main__":
    retrain_model()
