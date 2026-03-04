import os
from pathlib import Path
from PIL import Image

TARGET_SIZE = 256


def convert_png_to_jpg(png_root: str, jpg_root: str) -> None:
    for dirpath, _, filenames in os.walk(png_root):
        for filename in filenames:
            if not filename.lower().endswith(".png"):
                continue

            png_path = os.path.join(dirpath, filename)

            # Preserve relative directory structure
            rel_path = os.path.relpath(dirpath, png_root)
            jpg_dir = os.path.join(jpg_root, rel_path)
            os.makedirs(jpg_dir, exist_ok=True)

            jpg_path = os.path.join(
                jpg_dir,
                os.path.splitext(filename)[0] + ".jpg"
            )

            if Path(jpg_path).exists():
                continue

            try:
                with Image.open(png_path) as img:
                    img = img.convert("RGB")

                    width, height = img.size

                    if width == height:
                        new_size = (TARGET_SIZE, TARGET_SIZE)
                    else:
                        new_height = int((TARGET_SIZE / width) * height)
                        new_size = (TARGET_SIZE, new_height)

                    img = img.resize(new_size, Image.LANCZOS)
                    img.save(jpg_path, "JPEG", quality=100, method=6)

                    print(f"Converted: {png_path} → {jpg_path}")

            except Exception as e:
                print(f"Failed to convert {png_path}: {e}")


if __name__ == "__main__":
    # scripts/ → project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    png_dir = os.path.join(project_root, "png")
    jpg_dir = os.path.join(project_root, "jpg")

    os.makedirs(jpg_dir, exist_ok=True)

    convert_png_to_jpg(png_dir, jpg_dir)
