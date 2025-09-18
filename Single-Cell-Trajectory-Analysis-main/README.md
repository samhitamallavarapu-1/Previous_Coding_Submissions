# Single-Cell-Trajectory-Analysis

This private repository contains the R programming file as well as the nextflow file needed to perform the single-cell trajectory analysis.

To start the process, we used preprocessed Seurat-based data. I have also written the preprocessing code in R(Preprocessing.Rmd) that is not needed to run the SingleCell.Rmd and perform evaluation and visualization and is just provided as an optional file.

The nextflow files contains three parameters: nfeatures to parametrize the number of features in FindVariableFeatures function; npcs to parametrize the total number of principal components to generate in RunPCA function and rootparentnode to parametrize the root parent node in the graph plot to visualize the trajectories starting from the parent node.

To run the nextflow file on the terminal I used the following code:
nextflow run trajectory_analysis.nf     

All the code in this repository should be stored in the same directory to avoid errors. 

SingleCell.Rmd file requires the preprocessed Seurat data file 'data.RDS' file that can be obtained through this Google Drive link: 
https://drive.google.com/drive/folders/1cfNrAgRghBHiXFiEAFLlkP_ChD9Dxs8-

The compressed raw data 'Data.tar' is also included in this Google Drive link. This file will be needed to run the 'Preprocessing.Rmd' file to preprocess the raw data. The 'Data.tar' file should be extracted in the same directory as the code and this should make the preprocessing code work and generate the 'data.RDS' file.

The report is generated as an HTML file after running the nextflow script. 

The analysis is performed on a preprocessed Seurat based dataset. I performed PCA and UMAP for feature extraction and clustering of the data to obtain more meaningful insight. After the analysis, I plotted the UMAP clusters and generated tree graph to check the trajectory of the cells. In the first output of the analysis report, we can see the number of days that it took for the cells to reach the final point of their trajectory. The second output converts that first data set into an integer format on a scale in gradient form to make the data clearer in terms of the length of time it takes to get to certain positions. The third and fourth outputs are preparing the data to include a trajectory pathway map with labels. The final graph combines all of the outputs to show a color gradient version of the trajectory map with an overlay of the pathways that the cell trajectories take.
