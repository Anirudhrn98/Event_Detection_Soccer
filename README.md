
# Event Detection in Soccer/Football Games. 

This repository is a comprehensive collection housing the datasets applied within the project, alongside Python scripts for video extraction. It also encompasses Jupyter notebooks that articulate the methodologies for training and evaluating the models referenced in the associated paper. 

The paper explaining the testing results and the findings of this paper can be found in the documents folder.
#
The project involves creating a soccer match highlight video by detecting key and pivotal moments that occur in the game. These events include 
 
1. Free-kick   
2. Corner
3. Penalty
4. Red Card
5. Goal
6. Yellow Card




# Install packages

```bash
!pip install SoccerNet
```

# Download Dataset 
 Use download_dataset to download all necessary files.

# Extract Events
Use download_events to extract all necessary clips. Details provided in depth in code. 

# Training 

1. Use "Trainer_LSTM+LCRN.ipynb" to train the LSTM and LCRN models mentioned in the paper. 

2. Use "Trainer_Yolov8.ipynb" to train the Yolov8 model mentioned in paper. 

3. Use "Trainer_ImageClassifer.ipynb" to train the Image Classifier model mentioned in paper. 

4. Use "Trainer_VideoMAE.ipynb" to train the Video Classifier model mentioned in paper. 


# Testing

1. Run "Testing_ImageClassifier" to generate and extract "overview" video and in-game "replays". 

2. Run "Testing_Yolov8" to extract events which include 
a. Substitution 
b. Booking (Red Card and Yellow Card)
c. Goal

3. Run "Testing_VideoMAE" on the "overview" video extracted to identify events which include: 
a. Set-Piece (Corner and Free-Kick)
b. Penalty

# Roadmap

Create a more voluminous dataset for the Video Classifier and the Yolov8 Model. 

# Acknowledgment 

The author would like to thank Dr. Leon Reznik and Mr. Sergei Chuprov from Rochester Institute of Technology (RIT) for their help and guidance while working on the project. 




