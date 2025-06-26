import subprocess


def run_command(cmd, check_error=True):
    """
    Helper to run shell commands.
    Prints command, captures output, and optionally raises an error if the command fails.
    """
    print(f"Executing: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=check_error, encoding="utf-8"
        )
        if result.stderr:
            # Print stderr if it exists, even if command succeeded (e.g., warnings)
            print(f"Stderr: {result.stderr.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(cmd)}")
        print(f"Return Code: {e.returncode}")
        print(f"Stdout: {e.stdout.strip()}")
        print(f"Stderr: {e.stderr.strip()}")
        if check_error:
            raise
        return None  # Return None if check_error is False and command fails


def get_installed_formulae():
    """Get a set of all installed Homebrew formulae."""
    try:
        output = run_command(["brew", "list", "--formula"])
        if output is None:  # Handle case where run_command returned None due to error
            print("Warning: 'brew list --formula' command failed or returned no output.")
            return set()
        return set(output.splitlines())
    except Exception as e:
        print(f"Could not get installed formulae: {e}")
        return set()


def get_installed_casks():
    """Get a set of all installed Homebrew casks."""
    try:
        output = run_command(["brew", "list", "--cask"])
        if output is None:  # Handle case where run_command returned None due to error
            print("Warning: 'brew list --cask' command failed or returned no output.")
            return set()
        return set(output.splitlines())
    except Exception as e:
        print(f"Could not get installed casks: {e}")
        return set()


def get_formula_dependencies(formula_name):
    """
    Get all direct and transitive dependencies of a given formula using 'brew deps --union'.
    """
    dependencies = set()
    try:
        # --union provides a flat list of all recursive dependencies
        # Do not check_error=True here, as brew deps may fail if formula not found, etc.
        output = run_command(["brew", "deps", "--union", formula_name], check_error=False)
        if output:  # Only process if output is not None and not empty
            dependencies.update(output.splitlines())
    except Exception as e:
        print(f"Warning: Could not get dependencies for {formula_name}: {e}")
    return dependencies


def main():
    # Define the Homebrew formulae and casks you want to explicitly keep
    # Note: libssl is typically part of openssl@3 and not a separate formula in brew list
    KEEP_FORMULAE_EXPLICIT = {
        "ffmpeg",
        "git",
        "cmake",
        "meson",
        "ninja",
        "openssl@3",
        "curl",
        "wget",
        "htop",
        "yt-dlp",
    }
    # You stated all casks should be removed, so this set remains empty.
    KEEP_CASKS_EXPLICIT = set()

    print("--- Gathering Installed Homebrew Packages ---")
    all_installed_formulae = get_installed_formulae()
    all_installed_casks = get_installed_casks()

    print("\n--- Identifying Dependencies for Kept Formulae ---")
    kept_formulae_with_deps = set(KEEP_FORMULAE_EXPLICIT)

    for formula in KEEP_FORMULAE_EXPLICIT:
        print(f"  Calculating dependencies for: {formula}")
        deps = get_formula_dependencies(formula)
        # Add the formula itself and all its dependencies to the 'kept' set
        # Ensure the formula itself is marked to be kept
        kept_formulae_with_deps.add(formula)
        kept_formulae_with_deps.update(deps)

    print(f"\nExplicitly requested formulae to keep: {sorted(list(KEEP_FORMULAE_EXPLICIT))}")
    print(f"All formulae to keep (including dependencies): {sorted(list(kept_formulae_with_deps))}")
    print(f"Explicitly requested casks to keep: {sorted(list(KEEP_CASKS_EXPLICIT))}")

    # Determine formulae to uninstall
    formulae_to_uninstall = []
    for formula in all_installed_formulae:
        if formula not in kept_formulae_with_deps:
            formulae_to_uninstall.append(formula)

    # Determine casks to uninstall
    casks_to_uninstall = []
    for cask in all_installed_casks:
        if cask not in KEEP_CASKS_EXPLICIT:
            casks_to_uninstall.append(cask)

    # Specific handling for python@3.13 as requested
    python_formula = "python@3.13"
    if python_formula in all_installed_formulae:
        if python_formula in kept_formulae_with_deps:
            print(
                f"\nWARNING: '{python_formula}' is installed and is a dependency of one or more "
                "of the formulae you wish to keep. It will NOT be uninstalled automatically by this "
                "script to avoid breaking your kept applications. If you still wish to remove it, "
                "you may need to manually uninstall dependent formulae first or force remove it "
                "(use with caution and at your own risk)."
            )
            # Ensure it's not in the uninstall list if it's a kept dependency
            if python_formula in formulae_to_uninstall:
                formulae_to_uninstall.remove(python_formula)
        else:
            print(
                f"\n'{python_formula}' is installed via Homebrew and will be uninstalled as requested "
                "(not a dependency of kept items)."
            )
            # No action needed, it's already in formulae_to_uninstall if not a dependency
    else:
        print(f"\n'{python_formula}' is not currently installed via Homebrew.")

    print("\n--- Summary of Items to Uninstall (Dry Run) ---")
    print("The following packages WILL BE UNINSTALLED if you proceed:")

    if formulae_to_uninstall:
        print("\nFormulae to Uninstall:")
        for formula in sorted(formulae_to_uninstall):
            print(f"  - {formula}")
    else:
        print("\nNo Homebrew formulae targeted for uninstallation.")

    if casks_to_uninstall:
        print("\nCasks to Uninstall:")
        for cask in sorted(casks_to_uninstall):
            print(f"  - {cask}")
    else:
        print("\nNo Homebrew casks targeted for uninstallation.")

    if not formulae_to_uninstall and not casks_to_uninstall:
        print("\nNo Homebrew packages will be uninstalled based on your criteria. Exiting.")
        return

    # User confirmation before proceeding
    confirmation = (
        input("\nDo you want to proceed with the actual uninstallation? (type 'yes' to confirm): ")
        .lower()
        .strip()
    )
    if confirmation != "yes":
        print("Uninstallation cancelled by user.")
        return

    print("\n--- Starting Uninstallation Process ---")

    # Uninstall Casks first (less likely to have dependencies on formulae for uninstallation)
    print("\nAttempting to uninstall Casks...")
    for cask in casks_to_uninstall:
        print(f"Uninstalling cask: {cask}...")
        try:
            # Check for specific CalledProcessError to get more details
            result = subprocess.run(
                ["brew", "uninstall", "--cask", cask],
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
            )
            if result.stderr:
                print(f"Stderr during {cask} uninstall: {result.stderr.strip()}")
            print(f"Successfully uninstalled {cask}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to uninstall cask: {cask}.")
            print(f"Error details: {e.stderr.strip()}")
        except Exception as e:
            print(f"An unexpected error occurred trying to uninstall cask {cask}: {e}")
            print(f"Skipping {cask}.")

    # Uninstall Formulae
    print("\nAttempting to uninstall Formulae...")
    # It's generally better to let brew handle the order, iterating is fine.
    for formula in formulae_to_uninstall:
        print(f"Uninstalling formula: {formula}...")
        try:
            result = subprocess.run(
                ["brew", "uninstall", formula],
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
            )
            if result.stderr:
                print(f"Stderr during {formula} uninstall: {result.stderr.strip()}")
            print(f"Successfully uninstalled {formula}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to uninstall formula: {formula}.")
            print(f"Error details: {e.stderr.strip()}")
        except Exception as e:
            print(f"An unexpected error occurred trying to uninstall formula {formula}: {e}")
            print(f"Skipping {formula}.")

    print("\n--- Running Homebrew Cleanup ---")
    try:
        print("Running 'brew autoremove' to remove orphaned dependencies...")
        run_command(["brew", "autoremove"])
        print("Running 'brew cleanup' to remove old versions and downloads...")
        run_command(["brew", "cleanup"])
        print("Homebrew cleanup completed.")
    except Exception as e:
        print(f"Error during brew cleanup: {e}")

    print("\nUninstallation process completed.")
    print("It's a good idea to run 'brew doctor' now to check for any remaining issues.")
    print(
        "\nNOTE: Any remaining Homebrew packages are likely essential dependencies of the "
        "formulae you chose to keep (ffmpeg, git, cmake, etc.)."
    )
    print(
        "To confirm, you can use 'brew uses --installed <package>' for any remaining "
        "package to see which of your kept items depends on it."
    )


if __name__ == "__main__":
    main()
