from PIL import Image
import os
import re


def natural_sort_key(s):
    """Extract numeric part after the last underscore and sort by that number"""
    match = re.search(r'_(\d+)\.', s)    # Look for the last number before the file extension
    if match:
        # Return a tuple with the filename and the number part after the last underscore as an integer for sorting
        return (s, int(match.group(1)))
    return (s, 0)    # If no number is found, return the filename and 0 (for safety)


def combine_images_row(images, output_path='combined_row.png'):
    # Sort images based on natural order (extracting number after the last '_')
    images.sort(key=natural_sort_key)

    # Open images
    opened_images = [Image.open(img) for img in images]

    # Get total width and max height
    widths, heights = zip(*(img.size for img in opened_images))
    total_width = sum(widths)
    max_height = max(heights)

    # Create a blank canvas with total width and max height
    combined_img = Image.new('RGB', (total_width, max_height), (255, 255, 255))

    # Paste images side by side
    x_offset = 0
    for img in opened_images:
        combined_img.paste(img, (x_offset, 0))
        x_offset += img.width

    # Save the combined image
    combined_img.save(output_path)
    print(f"Combined image saved as {output_path}")

if __name__ == '__main__':
    image_folder = './downloads/-DBiTRteSxcE'
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('png', 'jpg', 'jpeg'))]
    combine_images_row(image_files, output_path=os.path.join(image_folder, 'combined_row.png'))
