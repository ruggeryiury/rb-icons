import os
from pathlib import Path
from PIL import Image

TARGET_SIZE = 256


def convert_png_to_webp(png_root: str, webp_root: str) -> None:
    for dirpath, _, filenames in os.walk(png_root):
        for filename in filenames:
            if not filename.lower().endswith(".png"):
                continue

            png_path = os.path.join(dirpath, filename)

            # Preserve relative directory structure
            rel_path = os.path.relpath(dirpath, png_root)
            webp_dir = os.path.join(webp_root, rel_path)
            os.makedirs(webp_dir, exist_ok=True)

            webp_path = os.path.join(
                webp_dir,
                os.path.splitext(filename)[0] + ".webp"
            )

            if Path(webp_path).exists():
                continue

            try:
                with Image.open(png_path) as img:
                    img = img.convert("RGBA")

                    width, height = img.size

                    if width == height:
                        new_size = (TARGET_SIZE, TARGET_SIZE)
                    else:
                        new_height = int((TARGET_SIZE / width) * height)
                        new_size = (TARGET_SIZE, new_height)

                    img = img.resize(new_size, Image.LANCZOS)
                    img.save(webp_path, "WEBP", quality=100, method=6)

                    print(f"Converted: {png_path} → {webp_path}")

            except Exception as e:
                print(f"Failed to convert {png_path}: {e}")


if __name__ == "__main__":
    # scripts/ → project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    png_dir = os.path.join(project_root, "png")
    webp_dir = os.path.join(project_root, "webp")

    os.makedirs(webp_dir, exist_ok=True)

    convert_png_to_webp(png_dir, webp_dir)
