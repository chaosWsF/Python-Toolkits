import json
import os
import sys
from pathlib import Path
from PIL import Image


def get_image_folder() -> Path:
    """Return the image folder path from ENV or config file."""
    env_path = os.getenv('IMAGE_FOLDER')
    if env_path:
        return Path(env_path)

    config_path = Path(__file__).resolve().parent / 'img2pdf_config.json'
    if config_path.exists():
        try:
            with config_path.open('r', encoding='utf-8') as f:
                config = json.load(f)
        except (json.JSONDecodeError, OSError) as exc:
            raise RuntimeError(f'Failed to read config file {config_path}: {exc}') from exc

        platform_key = 'windows' if sys.platform.startswith('win') else 'darwin' if sys.platform == 'darwin' else 'linux'
        if platform_key in config:
            return Path(config[platform_key])
        if 'default' in config:
            return Path(config['default'])

        raise RuntimeError(
            'Config file found but no path for current platform. '
            'Use IMAGE_FOLDER env var or add a platform key in img2pdf_config.json.'
        )

    raise RuntimeError(
        'No IMAGE_FOLDER environment variable set and no img2pdf_config.json file found. '
        'Create img2pdf_config.json or set IMAGE_FOLDER.'
    )


image_folder = get_image_folder()
if not image_folder.exists():
    raise FileNotFoundError(f'Image folder does not exist: {image_folder}')

filenames = os.listdir(image_folder)
image_format = ('.webp', 'WEBP', '.jpg', 'JPG', '.jpeg', 'JPEG', '.png', 'PNG')

# Convert and collect images
for f in filenames:
    subdir = image_folder / f
    if subdir.is_dir():
        image_files = sorted([subdir / file for file in os.listdir(subdir) if file.endswith(image_format)])
        if image_files:
            images = [Image.open(image_f).convert('RGB') for image_f in image_files]
            save_loc = image_folder / f'{f}.pdf'
            images[0].save(save_loc, save_all=True, append_images=images[1:], format='PDF')
            print(f"Converted {len(images)} images in {f} to PDF: {save_loc}")
        else:
            print(f"No images found in {f}.")
    else:
        print(f"Skipping {f}, not a directory.")
