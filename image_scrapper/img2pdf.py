import os
from PIL import Image


# List your .webp files
image_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
filenames = os.listdir(image_folder)
image_format = ('.webp', 'WEBP', '.jpg', 'JPG', '.jpeg', 'JPEG', '.png', 'PNG')

# Convert and collect images
for f in filenames:
    subdir = os.path.join(image_folder, f)
    if os.path.isdir(subdir):
        image_files = sorted([os.path.join(subdir, file) for file in os.listdir(subdir) if file.endswith(image_format)])
        if image_files:
            images = [Image.open(image_f).convert('RGB') for image_f in image_files]
            save_loc = os.path.join(image_folder, f + '.pdf')
            images[0].save(save_loc, save_all=True, append_images=images[1:])
            print(f"Converted {len(images)} images in {f} to PDF: {save_loc}")
    else:
        print(f"Skipping {f}, not a directory.")
