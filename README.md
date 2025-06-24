<h1 align="center">DunamisMax's Python Scripts</h1>

<p align="center">
  <img src="https://www.unixmen.com/wp-content/uploads/2017/02/Python-Programming-Language.png" alt="Python image" width="400">
</p>

<p align="center">
  A personal and well-organized collection of Python utility scripts for automation, data processing, and general purpose tasks.
  <br />
  This repository serves as a version-controlled toolbox, with scripts sorted by target OS and category.
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Language-Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Language: Python"></a>
  <a href="https://github.com/stephenvsawyer/python-scripts/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="License: MIT"></a>
  <a href="#"><img src="https://img.shields.io/badge/Maintained-Yes-brightgreen.svg?style=flat-square" alt="Maintained: Yes"></a>
</p>

---

## ✨ Purpose & Philosophy

This repository is my personal, organized toolbox for reusable Python scripts. It is founded on a few key principles:

- **Organized, Not Random**: To avoid a "junk drawer" of files, all scripts are logically sorted by the operating system they target and their functional category.
- **Practical & Reusable**: Every script should solve a real-world problem, be well-documented, and be written clearly enough to be adapted for future tasks.
- **Pythonic & Readable**: Code should follow best practices (PEP 8) and prioritize clarity and simplicity. The "how" is as important as the "what."
- **Version Controlled**: By living in Git, every script's history is preserved, preventing accidental loss and tracking improvements over time.

---

## 🏗️ Understanding the Structure

The repository is organized first by the target operating system, and then by category. This makes it easy to find a script that fits a specific need.

- **`cross_platform/`**: Scripts that are OS-agnostic and written to work on macOS, Windows, and Linux without modification.
- **`macos/`**: Scripts that are written specifically for macOS, likely using macOS-specific file paths or command-line tools.
- **`windows/`**: Scripts tailored for the Windows operating system.
- **`linux/`**: Scripts designed for Linux environments.

Within each of these directories, you'll find scripts sorted into the following categories:

```sh
python-scripts/
├── cross_platform/
│ ├── backups/
│ ├── data_processing/
│ ├── dev_tools/
│ ├── file_management/
│ ├── media_management/
│ ├── system_automation/
│ ├── text_processing/
│ └── web_scraping/
├── macos/
│ ├── ... (same categories as above)
├── windows/
│ ├── ...
└── linux/
└── ...
```

---

## 🚀 How to Use a Script

1. **Find the Script**: Navigate through the directory structure to find the script you need.
2. **Check Dependencies**: Some scripts may require third-party libraries. It's best practice to create a dedicated virtual environment to avoid cluttering your global Python installation.

   ```sh
   # Navigate to the repo folder
   cd path/to/python-scripts

   # Create a virtual environment (do this only once)
   python3 -m venv .venv

   # Activate the environment (do this every time you work in a new terminal)
   source .venv/bin/activate
   ```

3. **Install Libraries**: If the script's directory contains a `requirements.txt` file, install the necessary libraries.

   ```sh
   pip install -r web_scraping/requirements.txt
   ```

4. **Run the Script**: Execute the script from your terminal.

   ```sh
   python3 macos/file_management/my_cool_script.py
   ```

---

## 🤝 Guidelines for Adding New Scripts

To maintain the quality and organization of this toolbox, new scripts should adhere to the following guidelines:

- **Choose the Right Home**: Place the script in the correct OS and category folder. If it can work anywhere, it belongs in `cross_platform`.
- **Write Clean Code**: Follow PEP 8 style guidelines. Use clear variable names and functions.
- **Avoid Hardcoded Paths**: Use relative paths or environment variables. Don't hardcode a path like `/Users/sawyer/Downloads/`.
- **Document Your Work**: Add comments to explain complex logic. For bigger scripts, consider adding a small `README.md` in the same folder.

### Connect

Connect with the author, **dunamismax**, on:

- **Twitter:** [@dunamismax](https://twitter.com/dunamismax)
- **Bluesky:** [@dunamismax.bsky.social](https://bsky.app/profile/dunamismax.bsky.social)
- **Reddit:** [u/dunamismax](https://www.reddit.com/user/dunamismax)
- **Discord:** `dunamismax`
- **Signal:** `dunamismax.66`

### 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.
