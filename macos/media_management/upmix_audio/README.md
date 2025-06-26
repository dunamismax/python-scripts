# 5.1 Audio Upmixer for macOS

A command-line script that uses FFmpeg to upmix stereo (2-channel) audio files into 5.1 surround sound.

It provides an easy-to-use interface for processing multiple files at once and is designed to run in the macOS Terminal.

## How It Works

The script does not use any AI. Instead, it uses a carefully constructed set of audio filters within FFmpeg to create a 5.1 mix from a stereo source.

- **Front Left/Right:** The original stereo channels, with a slight delay for a wider soundstage.
- **Center:** A mono mix of the original channels, with high frequencies reduced to keep it from sounding "flat."
- **LFE (Subwoofer):** A dedicated channel created by filtering out only the low bass frequencies from the source.
- **Surround Left/Right:** A delayed and filtered version of the audio to create an ambient, atmospheric rear sound field.

## Prerequisites

Before you begin, you need to install a few tools using the Terminal.

1. **Homebrew:** The standard package manager for macOS. If you don't have it, open Terminal and run this command:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Python & FFmpeg:** Use Homebrew to install Python 3 and the FFmpeg tool.

   ```bash
   brew install python ffmpeg
   ```

## Setup and Installation

Follow these steps to set up a dedicated environment for the script.

1. **Navigate to the Script's Directory:**
   Open the Terminal app and use the `cd` command to go to the folder where this script is located.

   ```bash
   # Example:
   cd path/to/your/project/folder
   ```

2. **Create a Python Virtual Environment:**
   This isolates the script's dependencies from your main system.

   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment:**
   You must do this every time you want to run the script in a new terminal session.

   ```bash
   source venv/bin/activate
   ```

   Your terminal prompt should now start with `(venv)`.

4. **Install Required Libraries:**
   Install the necessary Python package (`rich` for styled output) from the `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Script

1. **Activate the Virtual Environment**
   If your terminal prompt doesn't show `(venv)`, run `source venv/bin/activate` inside the script's directory.

2. **Run the Script with Your Audio Files**
   Type `python3 advanced_upmixer.py` followed by a space. Then, **drag one or more stereo audio files** from a Finder window and drop them onto the Terminal window. The file paths will be pasted automatically.

3. **Press Enter**
   The script will show you a list of the files it is about to process and then begin the upmixing.

   **Example Command:**

   ```bash
   (venv) python3 advanced_upmixer.py "/Users/sawyer/Music/track1.mp3" "/Users/sawyer/Downloads/soundtrack.wav"
   ```

## Output Files

- The new 5.1 surround sound files are saved in the **same folder** as the original source files.
- The output files will have the suffix `_5.1_upmixed.flac` (or `.ac3` if you choose that option). For example, `track1.mp3` becomes `track1_5.1_upmixed.flac`.

## Listening to the 5.1 Audio

To properly play back the 6-channel audio files, you will need:

1. A media player that supports multi-channel FLAC, such as **VLC** or **IINA**.
2. An audio system capable of playing 5.1 surround sound, like an A/V receiver or compatible headphones.
