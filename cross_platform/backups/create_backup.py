# cross_platform/backups/create_backup.py
import datetime
import shutil
from pathlib import Path

# --- Configuration ---
# The folder you want to back up.
SOURCE_DIR = Path.home() / "Documents" / "important_project"

# The folder where you want to store your backups.
DESTINATION_DIR = Path.home() / "Backups"


def create_backup(source: Path, destination: Path) -> None:
    """
    Creates a timestamped zip archive of a source directory.

    Args:
        source: The Path object of the directory to back up.
        destination: The Path object of the directory to store the backup in.
    """
    if not source.is_dir():
        print(f"Error: Source directory not found at {source}")
        return

    # Ensure the destination directory exists.
    destination.mkdir(parents=True, exist_ok=True)

    # Create a unique, timestamped filename for the backup.
    # e.g., "important_project_2025-06-24_17-30-05"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename_base = f"{source.name}_{timestamp}"

    # shutil.make_archive handles the zipping process elegantly.
    # It takes the base name for the new file, the format ('zip'), and the source directory.
    try:
        archive_path = shutil.make_archive(
            base_name=str(destination / backup_filename_base), format="zip", root_dir=str(source)
        )
        print(f"Successfully created backup: {archive_path}")
    except Exception as e:
        print(f"Error: Could not create backup. {e}")


if __name__ == "__main__":
    # It's good practice to create the directories if they don't exist for the example to run.
    (SOURCE_DIR).mkdir(exist_ok=True, parents=True)
    (DESTINATION_DIR).mkdir(exist_ok=True, parents=True)

    print("Creating a dummy file in the source directory for the backup...")
    (SOURCE_DIR / "my_important_file.txt").write_text("This is a test.")

    create_backup(SOURCE_DIR, DESTINATION_DIR)
