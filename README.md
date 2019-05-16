# CSC545-GroupAzure
# If updating positive image detection:
- Add positive images to positive folder if needed
- Run objectmarker.exe in the positive folder
- Select positive objects with mouse, press spacebar to save
- can select multiple sections per image
- Press enter to move to next image
- run samples_creation.bat to produce vector file
# If only updating negative images:
- Add negative images to negative folder (JPG ONLY!)
- Delete any existing folders in cascade folder if they exist
- edit haartraining.bat and specify number of positive and negative images
- save, run haartraining.bat
- run convert.bat to create xml file
# Run program:
- python fireDetection.py
