<h1 align="center">Stereo to 5.1 Audio Upmixer for macOS</h1>

<p align="center">
  A command-line Python script to upmix stereo audio files to 5.1 surround sound on macOS using FFmpeg.
  <br />
  It provides an easy-to-use interface for processing multiple files at once and is designed to run in the macOS Terminal.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Platform-macOS-lightgrey.svg" alt="macOS">
  <img src="https://img.shields.io/badge/Tool-FFmpeg-green.svg" alt="FFmpeg">
  <a href="https://github.com/dunamismax/golang/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/dunamismax/golang/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome"></a>
  <a href="https://github.com/dunamismax/golang/stargazers"><img src="https://img.shields.io/github/stars/dunamismax/golang?style=social" alt="GitHub Stars"></a>
</p>

---

## ✨ Guiding Philosophy

This Stereo to 5.1 Audio Upmixer is built on a few core principles:

- **Simplicity & Efficiency**: The script focuses on a single, clear purpose: upmixing stereo audio. It leverages the powerful FFmpeg tool for audio processing, ensuring efficiency without unnecessary complexity.
- **macOS Integration**: Designed specifically for macOS users, the script provides clear instructions for setup using Homebrew and integrates seamlessly with the macOS Terminal for drag-and-drop file processing.
- **Quality Upmixing**: While not using AI, the script employs a carefully constructed FFmpeg filtergraph to create a balanced and immersive 5.1 mix, with optimized default settings for common use cases.
- **User-Friendly Experience**: Utilizing the `rich` Python library, the command-line interface offers enhanced readability with colored output, progress indicators, and clear summaries.

---

##  Getting Started

This project requires Python 3 and FFmpeg. All commands should be run from the project's root directory.

First, navigate to the script's directory:

```sh
# Example:
cd path/to/your/project/folder
```

### Prerequisites

Before you begin, you need to install a few tools using the Terminal.

1.  **Homebrew:** The standard package manager for macOS. If you don't have it, open Terminal and run this command:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2.  **Python & FFmpeg:** Use Homebrew to install Python 3 and the FFmpeg tool.

    ```bash
    brew install python ffmpeg
    ```

### Setup and Installation

Follow these steps to set up a dedicated environment for the script.

1.  **Create a Python Virtual Environment:**
    This isolates the script's dependencies from your main system.

    ```bash
    python3 -m venv venv
    ```

2.  **Activate the Virtual Environment:**
    You must do this every time you want to run the script in a new terminal session.

    ```bash
    source venv/bin/activate
    ```

    Your terminal prompt should now start with `(venv)`.

3.  **Install Required Libraries:**
    Install the necessary Python package (`rich` for styled output) from the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

### How to Run the Script

1.  **Activate the Virtual Environment**
    If your terminal prompt doesn't show `(venv)`, run `source venv/bin/activate` inside the script's directory.

2.  **Run the Script with Your Audio Files**
    Type `python3 upmix_audio.py` followed by a space. Then, **drag one or more stereo audio files** from a Finder window and drop them onto the Terminal window. The file paths will be pasted automatically.

3.  **Press Enter**
    The script will show you a list of the files it is about to process and then begin the upmixing. The script will always use the ideal default settings for upmixing to FLAC.

    **Example Command:**

    ```bash
    (venv) python3 upmix_audio.py "/Users/sawyer/Music/track1.mp3" "/Users/sawyer/Downloads/soundtrack.wav"
    ```

### Output Files

-   The new 5.1 surround sound files are saved in the **same folder** as the original source files.
-   The output files will have the suffix `_5.1_upmixed.flac`. For example, `track1.mp3` becomes `track1_5.1_upmixed.flac`.

### Listening to the 5.1 Audio

To properly play back the 6-channel audio files, you will need:

1.  A media player that supports multi-channel FLAC, such as **VLC** or **IINA**.
2.  An audio system capable of playing 5.1 surround sound, like an A/V receiver or compatible headphones.

---

## ️ Project Structure

The `upmix_audio` project is organized as follows:

```sh
upmix_audio/
├── upmix_audio.py          # Main script for audio upmixing.
├── requirements.txt        # Python dependencies.
└── README.md               # This documentation file.
```

---

##  Contribute

**This project is built by the community, for the community. We need your help!**

Whether you're a seasoned Python developer or just starting, there are many ways to contribute:

-   **Report Bugs:** Find something broken? [Open an issue](https://github.com/dunamismax/golang/issues) and provide as much detail as possible.
-   **Suggest Features:** Have a great idea for a new feature (e.g., support for more output formats, advanced filter options)? [Start a discussion](https://github.com/dunamismax/golang/discussions) or open a feature request issue.
-   **Write Code:** Grab an open issue, fix a bug, or implement a new system. [Submit a Pull Request](https://github.com/dunamismax/golang/pulls) and we'll review it together.
-   **Improve Documentation:** Great documentation is as important as great code. Help us make our guides and examples clearer and more comprehensive.

If this project excites you, please **give it a star!** ⭐ It helps us gain visibility and attract more talented contributors like you.

### Connect

Connect with the author, **dunamismax**, on:

-   **Twitter:** [@dunamismax](https://twitter.com/dunamismax)
-   **Bluesky:** [@dunamismax.bsky.social](https://bsky.app/profile/dunamismax.bsky.social)
-   **Reddit:** [u/dunamismax](https://www.reddit.com/user/dunamismax)
-   **Discord:** `dunamismax`
-   **Signal:** `dunamismax.66`

##  License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.