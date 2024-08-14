# IceLakesBot

This Python-based bot automates fishing in the game IceLakes. It controls your fishing rod, detects bites, and manages the fishing process automatically.

## Features
- **Automated Fishing**: Automatically handles the fishing rod based on pixel detection and game screen analysis.
- **Customizable Duration**: Set the duration of the fishing session in minutes.
- **Adjustable Rod Movement**: Configure the pixel width for rod movement across the screen.
- **Image Saving**: Optionally save images of successful catches and regular intervals for analysis.

## Requirements
`Python 3.9+`
`OpenCV (opencv-python)`
`NumPy (numpy)`
`PyAutoGUI (pyautogui)`
`Pillow (Pillow)`
`Keyboard (keyboard)`

## Installation

1. Clone this repository.
2. Install the required Python packages by running the following command in your terminal:
    ```bash
    pip install -r requirements.txt
    ```
    This will install all the necessary dependencies listed in the requirements.txt file, ensuring that the bot will 
    function correctly.

## Usage
Run the script main.py with optional command-line arguments:
```bash
python main.py [-t TIME] [-p PIXELS] [--save-img]
    -t, --time: Duration for the bot to run in minutes (default: 10.0 minutes).
    -p, --pixels: Number of pixels the rod should move from left to right from the center of the screen (default: 50 pixels).
    --save-img: Enable this flag to save images of frames when a fish is caught and every 150 seconds when the rod is straight.
```
## Hotkeys
- `X`: Pause the bot.
- `Z`: Resume the bot.

## Example
To run the bot for 20 minutes, moving the rod 60 pixels wide, and saving images:

```bash
python main.py -t 20 -p 60 --save-img
```
