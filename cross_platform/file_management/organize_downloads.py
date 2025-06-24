# cross_platform/file_management/organize_downloads.py
import shutil
from pathlib import Path

# --- Configuration ---
# The path to your Downloads folder. Path.home() is a reliable way to get your user's home directory.
DOWNLOADS_DIR = Path.home() / "Downloads"

# A dictionary mapping category folder names to the file extensions they should contain.
# Note the use of tuples for extensions belonging to the same category.
FILE_EXT_MAPPINGS = {
    "Images": (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".heic"),
    "Documents": (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".rtf"),
    "Archives": (".zip", ".rar", ".7z", ".tar", ".gz"),
    "Audio": (".mp3", ".wav", ".aac", ".flac"),
    "Video": (".mp4", ".mov", ".avi", ".mkv"),
    "Installers": (".dmg", ".pkg", ".exe", ".msi"),
}


def organize_folder(target_dir: Path) -> None:
    """
    Organizes files in a directory by moving them into subfolders based on their extension.

    Args:
        target_dir: The Path object of the directory to organize.
    """
    if not target_dir.is_dir():
        print(f"Error: Directory not found at {target_dir}")
        return

    print(f"Scanning directory: {target_dir}...")

    # We iterate over every item in the target directory.
    for item in target_dir.iterdir():
        # We only care about files, not subdirectories.
        if item.is_file():
            # Find which category this file belongs to.
            destination_folder = None
            for category, extensions in FILE_EXT_MAPPINGS.items():
                if item.suffix.lower() in extensions:
                    destination_folder = target_dir / category
                    break  # Stop searching once we've found a match

            # If the file extension didn't match any category, we can either
            # leave it or move it to a generic 'Other' folder. Let's move it.
            if destination_folder is None:
                destination_folder = target_dir / "Other"

            # Create the destination folder if it doesn't already exist.
            # `exist_ok=True` prevents an error if the folder is already there.
            destination_folder.mkdir(parents=True, exist_ok=True)

            # Move the file to its new home.
            shutil.move(str(item), str(destination_folder))
            print(f"Moved: {item.name} -> {destination_folder.name}/")

    print("\nOrganization complete!")


if __name__ == "__main__":
    organize_folder(DOWNLOADS_DIR)
