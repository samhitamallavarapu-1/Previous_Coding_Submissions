The folder consists of 3 python files for Question 2['DataGeneration.py'] and Question 3['SeriesImageGeneration_CT.py','SeriesImageGeneration_all.py'], 3 folders with the CSV data['DicomCSVData'] and composite images['Series Images CT','Series Images All'], requirements.txt file to install the python dependencies required for this Exercise, and a readMe file to explain the code.

QUESTION 1:
For question 1, user needs to download and install NBIA Data Retriever in order to download the dicom files from the .tcia file. The .tcia file is downloaded from the website 'https://www.cancerimagingarchive.net/collection/lung-fused-ct-pathology/' as mentioned in the exercise.

QUESTION 2:
The python file, 'DataGeneration.py' contains the code to extract the header elements needed. I used the function 'extract_dicom_header' to extract the required header elements.
This function takes the dicom data as the input and outputs a dictionary where keys are the required header elements and values are the data associated with the header elements.
This function is called inside a loop; which loops through all the files that have the '.dcm' extension, and stores this data. Finally, this data is stored in a .csv format using pandas. The data is stored in 'DicomCSVData' folder.
I observed from the MetaData that the data for 'StudyDescription' was null and 'SeriesDate' is not included. Due to this, the data for these two fields is blank as written in the python code; as the default return for the dictionary 'get' attribute was set to an empty string.

QUESTION 3:
There are 2 python files for this question. The first python file, 'SeriesImageGeneration_CT.py' generates the images for only the dicom data that has 'CT' as the modality.
I observed from the pixel array data that for the data with modality other than 'CT', the pixel values predominantly had the same values, leading to a dark image with very minimal pixel variation. 
Hence, I made 2 python codes, where 'SeriesImageGeneration_CT.py' only works on the 'CT' modality data and 'SeriesImageGeneration_all.py' works on all the data. The images are also stored in different directories to avoid confusion. The name of the images is set to 'SeriesInstanceUID' as required by the question.
'Series Images CT' folder contains the images with only 'CT' modality.
'Series Images All' folder contains images with all the data.
The pixel values were also scaled between [0,255] to contain the values with the grayscale range for better representation of the image on a typical monitor with an average dynamic range.
The series was first sorted based on the slice location. Based on reviewing the dicom functionalities, I found that researchers typically use the z coordinates of the scanner with respect to patient-based coordinate system to sort the slices. Hence, I used 'ImagePositionPatient' parameter instead of 'SliceLocation' to sort the dicom data list.
The individual slices of a series were converted into a 48x48 thumbnail and all the thumbnails were appended to a list to generate the composite image in a square grid fashion.