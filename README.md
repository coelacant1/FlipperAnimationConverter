# Flipper Zero Batch Image Processor

## Overview
This script batch processes folders of images, prepares them for use as animations on the **Flipper Zero** device, and generates the required **meta.txt** and **manifest.txt** files. 

The script processes all folders within a relative `Inputs/` directory, applies specified transformations, and saves the output in an organized directory structure under `Assets/{VariableName}/{InputFolderName}/Anims`.

## Features
- Thresholding images (black/white conversion)
- Translating images horizontally and vertically
- Resizing and centering images on a white 128x64 canvas
- Batch processing all folders under the `Inputs` directory
- Generating **meta.txt** files for individual animations
- Creating a global **manifest.txt** file for all animations

## Notes
- Images should be in a similar formatting between sequences
- Images should work with the same threshold value/be similar in exposure/lighting

## Installation
1. Install the required Python libraries:
   ```bash
   pip install opencv-python-headless pillow numpy
   ```
   asset_packer from the Momentum repository requires the following Python libraries:
   ```bash
   pip install pillow heatshrink2
   ```
2. Save the script to your project directory.
3. Prepare your input folders under a relative path: `Inputs/`.

## Usage
Run the script as follows:

```bash
python batch_process.py
```

### Parameters
The script can be customized using the following parameters:

| Parameter         | Description                                 | Default Value |
|-------------------|---------------------------------------------|---------------|
| `base_input_folder` | Base folder containing all input subfolders | `Inputs`      |
| `base_output_folder`| Output folder for generated animations     | `Assets`      |
| `animation_name`   | Animation name for output folder structure   | `Coela`  |
| `threshold_value` | Threshold value for image binarization (0-255) | `200`          |
| `transform_x`     | Horizontal pixel shift (positive or negative) | `10`          |
| `transform_y`     | Vertical pixel shift (positive or negative) | `-5`          |
| `scale_factor`    | Image scaling factor (e.g., `0.5` = 50%)    | `0.5`         |

### Output Directory Structure
The output will be organized as follows:
```
Assets/
  Animations/
    InputFolder1/
      Anims/
        frame_0.png
        frame_1.png
        ...
        meta.txt
    InputFolder2/
      Anims/
        frame_0.png
        frame_1.png
        ...
        meta.txt
    manifest.txt
```

### Example meta.txt
Each folder will have a `meta.txt`:
```
Filetype: Flipper Animation
Version: 1

Width: 128
Height: 64
Passive frames: 0
Active frames: 5
Frames order: 0 1 2 3 4
Active cycles: 1
Frame rate: 10
Duration: 100
Active cooldown: 3

Bubble slots: 0
```

### Example manifest.txt
A global `manifest.txt` file will be generated under `Assets/{VariableName}`:
```
Filetype: Flipper Animation Manifest
Version: 1

Name: InputFolder1
Min butthurt: 0
Max butthurt: 18
Min level: 1
Max level: 30
Weight: 3

Name: InputFolder2
Min butthurt: 0
Max butthurt: 18
Min level: 1
Max level: 30
Weight: 3
```

## How It Works
1. **Input Processing**: The script reads all image files from each subfolder in `Inputs/`.
2. **Image Transformation**:
   - Converts to black-and-white using a threshold value.
   - Shifts images horizontally (`transform_x`) and vertically (`transform_y`).
   - Resizes the image using `scale_factor` and centers it on a 128x64 white canvas.
3. **Output**: The processed frames are saved as `frame_X.png` files.
4. **Metadata Generation**:
   - `meta.txt` is generated for each animation folder.
   - A global `manifest.txt` is generated to catalog all animations.

## Notes
- Ensure input images are in `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tif`, or `.tiff` formats.
- Input images with transparency will have their transparent areas filled with white.
- Frames are resized and centered to fit the Flipper Zero's 128x64 resolution.

## Future Changes
- Allow threshold, scaling, and transformation per sequence

## Requirements
- Python 3.8+
- Libraries:
  - OpenCV (`opencv-python-headless`)
  - Pillow (`PIL`)
  - NumPy
  - Heatshrink2
