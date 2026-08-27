from pathlib import Path

# filename prefix → correct class ID (must match dataset.yaml order)
CLASS_MAP = {
    "person": 0,
    "box": 1,
    "bottle": 2,
    "equipment": 3,
}

BASE_DIR = Path(r"D:\visionpack\visionpack-ai\data\labels")

def fix_dir(split: str):
    dir_path = BASE_DIR / split
    for txt_file in dir_path.glob("*.txt"):
        prefix = txt_file.stem.split("_")[0]
        if prefix not in CLASS_MAP:
            print(f"⚠️  Skipping unknown: {txt_file.name}")
            continue

        correct_id = CLASS_MAP[prefix]
        lines = txt_file.read_text().strip().split("\n")
        new_lines = []

        for line in lines:
            if not line.strip():
                continue
            parts = line.split()
            parts[0] = str(correct_id)
            new_lines.append(" ".join(parts))

        txt_file.write_text("\n".join(new_lines) + "\n")
        print(f"✅ {split}/{txt_file.name} → class {correct_id} ({prefix})")

fix_dir("train")
fix_dir("val")
print("\n🎉 Done! Now delete .cache files and retrain.")