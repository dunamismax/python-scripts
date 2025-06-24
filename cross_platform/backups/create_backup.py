# cross_platform/backups/create_backup_v2.py

import datetime
import shutil
from pathlib import Path
from typing import Any, Dict, List

# --- Main Configuration ---
# Define all your backup tasks in this list.
# You can add as many dictionaries (jobs) as you like.
# This makes the script incredibly easy to configure and maintain.
BACKUP_JOBS: List[Dict[str, Any]] = [
    {
        "name": "Important Project",
        "source": Path.home() / "Documents" / "important_project",
        "destination": Path.home() / "Backups",
        "retention_days": 7,  # Keep backups for 7 days
    },
    {
        "name": "Photos Archive",
        "source": Path.home() / "Pictures",
        "destination": Path.home() / "Backups" / "Photos",
        "retention_days": 30,  # Keep photo backups for 30 days
    },
]


def create_backup(source: Path, destination: Path) -> bool:
    """
    Creates a timestamped zip archive of a source directory.

    Args:
        source: The Path object of the directory to back up.
        destination: The Path object of the directory to store the backup in.

    Returns:
        True if the backup was created successfully, False otherwise.
    """
    if not source.is_dir():
        print(f"  [ERROR] Source directory not found: {source}")
        return False

    # Ensure the destination directory exists.
    destination.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # A cleaner filename, e.g., "important_project--2025-06-24_17-30-05.zip"
    backup_filename_base = f"{source.name}--{timestamp}"

    try:
        archive_path = shutil.make_archive(
            base_name=str(destination / backup_filename_base), format="zip", root_dir=str(source)
        )
        print(f"  [SUCCESS] Created backup: {Path(archive_path).name}")
        return True
    except Exception as e:
        print(f"  [ERROR] Could not create backup. {e}")
        return False


def cleanup_old_backups(destination: Path, retention_days: int) -> None:
    """
    Deletes backups in the destination folder older than the retention period.

    Args:
        destination: The Path object of the backup directory to clean.
        retention_days: The maximum number of days to keep backups.
    """
    print(f"  [INFO] Cleaning up backups older than {retention_days} days in {destination}...")

    # This is the key to our logic: the cutoff date.
    # Any file older than this date will be deleted.
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=retention_days)

    if not destination.is_dir():
        return  # Nothing to clean if the directory doesn't exist.

    deleted_count = 0
    # We use .glob('*.zip') to safely iterate over only our zip archives.
    for item in destination.glob("*.zip"):
        if item.is_file():
            # Get the file's modification time. path.stat().st_mtime returns a timestamp.
            file_mod_time_ts = item.stat().st_mtime
            file_mod_time = datetime.datetime.fromtimestamp(file_mod_time_ts)

            if file_mod_time < cutoff_date:
                try:
                    item.unlink()  # The pathlib way to delete a file.
                    print(f"    - Deleted old backup: {item.name}")
                    deleted_count += 1
                except Exception as e:
                    print(f"    - [ERROR] Could not delete {item.name}. {e}")

    if deleted_count == 0:
        print("  [INFO] No old backups to delete.")


def setup_test_environment():
    """A helper function to create dummy directories for testing."""
    print("--- Setting up test environment ---")
    for job in BACKUP_JOBS:
        job["source"].mkdir(parents=True, exist_ok=True)
        job["destination"].mkdir(parents=True, exist_ok=True)
        # Create a dummy file in the source to ensure the backup is not empty.
        (job["source"] / f"dummy_file_for_{job['name']}.txt").write_text(
            f"Test content for {job['name']}."
        )
    print("--- Test environment setup complete ---\n")


def main():
    """The main function to orchestrate the backup process."""
    print("--- Starting Backup Script ---")
    if not BACKUP_JOBS:
        print("No backup jobs configured. Exiting.")
        return

    for job in BACKUP_JOBS:
        print(f"\nProcessing job: '{job['name']}'")
        print(f"  Source: {job['source']}")
        print(f"  Destination: {job['destination']}")

        # Step 1: Create the new backup
        backup_successful = create_backup(job["source"], job["destination"])

        # Step 2: Clean up old backups, but only if the new backup was made successfully.
        if backup_successful:
            cleanup_old_backups(job["destination"], job["retention_days"])

    print("\n--- Backup Script Finished ---")


if __name__ == "__main__":
    # To run this for the first time, you might need to create the folders.
    # This helper function does that for you based on your config.
    setup_test_environment()
    main()
