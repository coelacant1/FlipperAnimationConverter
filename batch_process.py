import os
import cv2
import numpy as np
from PIL import Image, ImageChops, ImageOps

def process_images(base_input_folder, base_output_folder, animation_name, threshold_value, transform_x, transform_y, scale_factor):
    """
    Batch processes images by thresholding, transforming (moving), scaling, cropping, and exporting.
    Handles multiple input folders, saving outputs to structured asset folders, and generates meta.txt and manifest.txt files.

    Parameters:
        base_input_folder (str): Base folder containing input folders.
        base_output_folder (str): Base output folder for saving processed assets.
        animation_name (str): Name of the animation set.
        threshold_value (int): Threshold value (0-100 scale).
        transform_x (int): Number of pixels to move the image horizontally (positive or negative).
        transform_y (int): Number of pixels to move the image vertically (positive or negative).
        scale_factor (float): Scaling factor for resizing images.
    """
    # Validate input
    if not os.path.exists(base_input_folder):
        print(f"Base input folder {base_input_folder} does not exist.")
        return

    all_anim_folders = []

    # Iterate through subfolders in base input folder
    for subfolder in sorted(os.listdir(base_input_folder)):
        input_folder = os.path.join(base_input_folder, subfolder)
        if not os.path.isdir(input_folder):
            continue

        # Define output folder
        output_folder = os.path.join(base_output_folder, animation_name, "Anims", subfolder)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Created output folder: {output_folder}")

        print(f"Processing folder: {input_folder}")
        frame_files = []
        frame_count = 0

        # Process each image in the input folder
        for filename in sorted(os.listdir(input_folder)):
            input_path = os.path.join(input_folder, filename)

            # Only process image files
            if not filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tif', 'tiff')):
                continue

            try:
                # Read image using OpenCV
                image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
                if image is None:
                    print(f"Failed to load {filename}.")
                    continue

                # Handle transparency: convert alpha channel to white background
                if image.shape[-1] == 4:  # Image has alpha channel
                    alpha_channel = image[:, :, 3]
                    bgr_channels = image[:, :, :3]
                    white_background = np.ones_like(bgr_channels, dtype=np.uint8) * 255
                    alpha_factor = alpha_channel[:, :, np.newaxis] / 255.0
                    image = (bgr_channels * alpha_factor + white_background * (1 - alpha_factor)).astype(np.uint8)

                # Convert to grayscale for thresholding
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Apply threshold
                _, thresh_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)

                # Convert to PIL image for further processing
                pil_image = Image.fromarray(thresh_image)

                # Apply transformation (move image by x and y pixels)
                transformed_image = ImageChops.offset(pil_image, transform_x, transform_y)
                transformed_image = transformed_image.crop((0, 0, transformed_image.width, transformed_image.height))

                # Apply scaling
                width, height = transformed_image.size
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)
                scaled_image = transformed_image.resize((new_width, new_height), Image.LANCZOS)

                # Create a blank white image of 128x64
                final_image = Image.new("L", (128, 64), color=255)

                # Paste the scaled image centered onto the white background
                paste_x = (128 - scaled_image.width) // 2
                paste_y = (64 - scaled_image.height) // 2
                final_image.paste(scaled_image, (paste_x, paste_y))

                # Rename and save the processed image
                frame_name = f"frame_{frame_count}.png"
                output_path = os.path.join(output_folder, frame_name)
                final_image.save(output_path, "PNG")
                frame_files.append(frame_name)
                frame_count += 1

            except Exception as e:
                print(f"Error processing {filename}: {e}")

        # Generate meta.txt
        meta_path = os.path.join(output_folder, "meta.txt")
        with open(meta_path, "w") as meta_file:
            meta_file.write("Filetype: Flipper Animation\n")
            meta_file.write("Version: 1\n\n")
            meta_file.write("Width: 128\n")
            meta_file.write("Height: 64\n")
            meta_file.write("Passive frames: 0\n")
            meta_file.write(f"Active frames: {frame_count}\n")
            meta_file.write(f"Frames order: {' '.join(map(str, range(frame_count)))}\n")
            meta_file.write("Active cycles: 1\n")
            meta_file.write("Frame rate: 10\n")
            meta_file.write(f"Duration: 100\n")  # Assuming ~100ms per frame
            meta_file.write("Active cooldown: 3\n\n")
            meta_file.write("Bubble slots: 0\n")
        print(f"Generated meta.txt at {meta_path}")

        # Append animation folder for global manifest
        all_anim_folders.append((output_folder, subfolder))

    # Generate global manifest.txt
    manifest_path = os.path.join(base_output_folder, animation_name, "Anims/manifest.txt")
    with open(manifest_path, "w") as manifest_file:
        manifest_file.write("Filetype: Flipper Animation Manifest\n")
        manifest_file.write("Version: 1\n\n")
        for folder, name in all_anim_folders:
            manifest_file.write(f"Name: {name}\n")
            manifest_file.write("Min butthurt: 0\n")
            manifest_file.write("Max butthurt: 18\n")
            manifest_file.write("Min level: 1\n")
            manifest_file.write("Max level: 30\n")
            manifest_file.write("Weight: 3\n\n")
    print(f"Generated global manifest.txt at {manifest_path}")

# Example usage
if __name__ == "__main__":
    base_input_folder = "Inputs"  # Relative folder containing all subfolders
    base_output_folder = "Assets"  # Base output folder
    animation_name = "Coela"  # Custom variable name
    threshold_value = 200  # Range: 0-100
    transform_x = 0  # Move image 10 pixels to the right (negative to move left)
    transform_y = 0  # Move image 5 pixels up (positive to move down)
    scale_factor = 0.5  # Scale factor: 0.5 = 50% size, 2.0 = 200% size

    process_images(base_input_folder, base_output_folder, animation_name, threshold_value, transform_x, transform_y, scale_factor)
