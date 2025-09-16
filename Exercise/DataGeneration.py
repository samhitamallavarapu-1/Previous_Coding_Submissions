import os
import pydicom
import pandas as pd

'''Question 2: Extract a subset of DICOM header elements from the entire set of files in the collection and save
them into a text file in comma-separated values (CSV) format. Please extract the following elements: PatientID, StudyDate, StudyInstanceUID, StudyDescription,
Modality, BodyPartExamined, SeriesDate, SeriesInstanceUID, SeriesDescription.'''

# Function to extract DICOM header elements
def extract_dicom_header(ds):
    """
    Extract the header elements from the input DICOM file object.
    
    Parameters:
        ds: DICOM file object.
        
    Returns:
        dict: A dictionary where keys are the required header elements and values are the data associated with the header elements.
    """
    study_date = ds.get('StudyDate', '')
    study_date=study_date[4:6]+"-"+study_date[6:]+"-"+study_date[:4] # To get the date in the same format as the metadata

    return {
        'PatientID': ds.get('PatientID', ''),
        'StudyDate': study_date,
        'StudyInstanceUID': ds.get('StudyInstanceUID', ''),
        'StudyDescription': ds.get('StudyDescription', ''),
        'Modality': ds.get('Modality', ''),
        'BodyPartExamined': ds.get('BodyPartExamined', ''),
        'SeriesDate': ds.get('SeriesDate', ''),
        'SeriesInstanceUID': ds.get('SeriesInstanceUID', ''),
        'SeriesDescription': ds.get('SeriesDescription', '')
    }

dicom_dir = './Data/' # Directory containing DICOM files

dicom_data = [] # List to store extracted DICOM header elements and data
for root, dirs, files in os.walk(dicom_dir):
    for file in files:
        if file.endswith('.dcm'):
            dicom_file = os.path.join(root, file)      
            ds = pydicom.dcmread(dicom_file)  # Read DICOM file
            dicom_data.append(extract_dicom_header(ds))


df = pd.DataFrame(dicom_data) # Convert extracted data to DataFrame
csv_dir = './DicomCSVData'
output_csv = csv_dir + '/dicom_header_elements.csv' 
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)
df.to_csv(output_csv, index=False) # Save DataFrame to CSV
print(f"DICOM header elements extracted and saved to '{output_csv}'")