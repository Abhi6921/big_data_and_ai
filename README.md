# Ludus Alliance Webapp

This README provides instructions on how to start and work with the web application built using the provided code.

## Prerequisites

Before starting with the web application, ensure that you have the following installed on your system:

- Python 3.x
- PyCharm
- Flask
- torch
- cv2 (OpenCV)

## Installation

1. Clone the repository or download the code files.
2. Open the terminal inside PyCharm.
3. There should be a virtual environment (you should see venv between parenthesis in your terminal), if not it is recommended to create one.
4. Activate the virtual environment (if needed).
5. Install the required Python packages using the `requirements.txt` file. Run the following command: `pip install -r requirements.txt`


## Starting the WebApp

To start the web application, follow these steps:

1. Open the terminal in PyCharm and navigate to the project directory (which you should already be in).
2. The virtual environment `(venv)` should be created and activated by now.
3. Run the following command: `python app.py`
4. The Flask development server will start running.
5. Open a web browser and visit `http://localhost:5000` to access the web application. Or select the url in the terminal
that will pop up `Running on http://127.0.0.1:5000`

## Working with the WebApp

### Prerequisites
1. Have a video of around 10-15 seconds (only 150 frames will be taken from the video).
2. Make sure the participant and paddle holder are standing at their position before recording (only two people in frame). 
3. Record horizontally with a mobile phone and make sure the people are in frame of the camera (feet till head) with the paddle.
4. Keep the camera steady during the recording.

#### Uploading a Video

1. On the home page, click on the "Choose File" button.
2. Select a video file from your local system.
3. Click the "Upload" button to submit the selected video file.
4. The web application will display the video with the object detection.

#### Viewing the Results

1. The video is done when there is no movement happening in the video.
2. Only press the `See Results` button when the video is done.
3. The results will be shown under the video, the average height, average distance to the paddle, and average distance to the participant.
4. These results are calculated based on the analysis of the video frames.


