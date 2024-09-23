import numpy as np
from ultralytics import YOLO
import cv2
import os

# Load the license plate detection model
license_plate_detector = YOLO('models/license_plate_detector.pt')

# Set input and output directories
input_directory = r'C:\\Users\\Administrator\\Downloads\\archive\\images'
output_directory = r'C:\\Users\\Administrator\\Downloads\\archive\\output'

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Process each image in the input directory
for filename in os.listdir(input_directory):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Read the image
        frame = cv2.imread(os.path.join(input_directory, filename))
        
        if frame is not None:
            # Detect license plates
            license_plates = license_plate_detector(frame)[0]
            for i, license_plate in enumerate(license_plates.boxes.data.tolist()):
                x1, y1, x2, y2, score, class_id = license_plate

                # Crop the license plate from the frame
                license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2)]

                # Save the cropped license plate image
                output_filename = os.path.join(output_directory, f'{filename.split(".")[0]}_plate_{i}.jpg')
                cv2.imwrite(output_filename, license_plate_crop)

                print(f"License plate saved: {output_filename}")
        else:
            print(f"Failed to read image: {filename}")
