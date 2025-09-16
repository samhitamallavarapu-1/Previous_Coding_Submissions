import os
import pydicom
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math
from pydicom.pixel_data_handlers.util import apply_modality_lut
from pydicom.pixel_data_handlers import apply_windowing

''' Question 3: Read the pixel data for each image in a DICOM series and generate a composite image composed
of 48 x 48 thumbnails of each slice. Save the composite image as PNG with the SeriesInstanceUID
as the filename.'''

def load_dicom_series(folder_path):
    """
    Load all DICOM files from a folder and group them by series.
    
    Parameters:
        folder_path (str): Path to the folder containing DICOM files.
        
    Returns:
        dict: A dictionary where keys are series instance UID and values are lists of DICOM datasets belonging to each series.
    """
    dicom_series = {} # Initialize an empty dictionary to store the SeriesInstanceUID as keys and the corresponding data as values in a list
    for root, _, files in os.walk(folder_path): # Check all subdirectories
        for file in files:
            if(file.endswith('.dcm')):
                file_path = os.path.join(root, file) # Get the file location for the file that ends with .dcm
                dicom_data = pydicom.dcmread(file_path) # Read the file and store the data
                series_uid = dicom_data.SeriesInstanceUID # Store SeriesInstanceUID from the dicom data
                modality = dicom_data.Modality # Store Modality from the dicom data
                if series_uid not in dicom_series:
                    dicom_series[series_uid] = []  # If this is the first entry generate the key and an empty list
                dicom_series[series_uid].append(dicom_data) # Append the dicom data to the list
    return dicom_series

def sort_dicom_series_by_slice_location(dicom_series):
    """
    Sort DICOM series based on slice location.
    
    Parameters:
        dicom_series (dict): Dictionary containing DICOM datasets grouped by series.
        
    Returns:
        dict: Sorted DICOM series.
    """
    sorted_dicom_series = {}
    for series_uid, dicom_list in dicom_series.items(): # Iterate over the dictionary
        dicom_list.sort(key=lambda x: float(x.ImagePositionPatient[2])) # Sort based z coordinates of the scanner with respect to patient-based coordinate system (Provides better accuracy than SliceLocation parameter)
        sorted_dicom_series[series_uid] = dicom_list # Store the sorted list in dictionary with the series instance uid as the key
    return sorted_dicom_series

def generate_thumbnail_images(dicom_series):
    """
    Generate thumbnail images for all slices in a DICOM series.
    
    Parameters:
        dicom_series (list): List of DICOM datasets belonging to the same series.
        
    Returns:
        list: List of PIL.Image objects representing the thumbnail images.
    """
    thumbnail_images = [] # Initialize an empty list to store all the thumbnail images to plot later
    for dicom_data in dicom_series: # Iterate over all the data in a series
        dcm_pixel_data = dicom_data.pixel_array.astype(float) # Convert to floating point for higher precision
        dcm_pixel_data_scaled = ((np.maximum(dcm_pixel_data,0))/dcm_pixel_data.max())*255.0 # Normalizing the pixel data between [0,1] and scaling to [0,255]
        # ddtt = np.uint8(ddtt)
        img = Image.fromarray(dcm_pixel_data_scaled) # Convert DICOM pixel array to PIL Image
        img = img.convert('L') # Convert to grayscale        
        img.thumbnail((48, 48)) # Resize image to 48x48 thumbnail
        thumbnail_images.append(img) # Append the 48x48 thumbnail to the list for a series data
    return thumbnail_images

folder_path = "./Data/Lung-Fused-CT-Pathology/" # Root Directory to access dicom data
dicom_series = load_dicom_series(folder_path) # Get the dicom series
sorted_dicom_series = sort_dicom_series_by_slice_location(dicom_series) # Sort the dicom series based on the slice location

image_dir = './Series Images All' # Folder where images are stored
if not os.path.exists(image_dir): # Make a new folder if the folder does not exist
    os.makedirs(image_dir)

for series_uid, dicom_list in sorted_dicom_series.items():
    thumbnail_images = generate_thumbnail_images(dicom_list) # Get all thumbnails for a series
    num_thumbnails = len(thumbnail_images) # Total number of thumbnails
    rows = cols = int(math.ceil(math.sqrt(num_thumbnails)))  # Calculate the number of rows and columns to get the composite image with square grid
    if(rows>1 and cols>1):
        fig, axes = plt.subplots(rows, cols, figsize=(rows, cols)) # Generate subplots
        used_ax=0 # Used as a counter to keep a track of number of subplots actually used in the grid
        for ax, img in zip(axes.flatten(), thumbnail_images):
            ax.imshow(img, cmap='gray')
            ax.axis('off') 
            used_ax+=1
        for u in range(used_ax,len(axes.flatten())):
            axes.flat[u].set_visible(False) # Set all the unused subplots as not visible
        fig.patch.set_facecolor('black') # Set the plot background as black
        plt.savefig(f"{image_dir}/{series_uid}.png", bbox_inches='tight') # Save the figure in Series Images All folder
    else:
        fig, axes = plt.subplots(1, num_thumbnails, figsize=(num_thumbnails, 1)) # For the edge case when there is only one thumbnail
        axes.imshow(img, cmap='gray')
        fig.patch.set_facecolor('black')
        plt.savefig(f"{image_dir}/{series_uid}.png", bbox_inches='tight') # Save the figure in Series Images All folder