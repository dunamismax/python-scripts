#!/usr/bin/env python3
import shutil
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table

# --- Configuration ---
OUTPUT_SUFFIX = "_5.1_upmixed"
DEFAULT_LFE_CROSSOVER = 120
DEFAULT_FRONT_DELAY = 1.5
DEFAULT_REAR_DELAY = 20
DEFAULT_OUTPUT_FORMAT = ".flac"

# Initialize Rich Console for beautiful output
console = Console()


def check_dependencies():
    """Checks if FFmpeg and ffprobe are available."""
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        console.print(
            "[bold red]Error: FFmpeg and ffprobe are required but not found in your system's PATH.[/bold red]"
        )
        console.print(
            "Please install them. On macOS with Homebrew, you can run: [cyan]brew install ffmpeg[/cyan]"
        )
        return False
    return True


def get_audio_info(file_path: Path) -> dict:
    """Uses ffprobe to get audio stream information in a robust key-value format."""
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "a:0",
        "-show_entries",
        "stream=channels,channel_layout,sample_rate",
        "-of",
        "default=noprint_wrappers=1:nokey=0",
        str(file_path),
    ]
    try:
        result = subprocess.check_output(command, text=True, stderr=subprocess.PIPE).strip()
        info_dict = dict(line.split("=", 1) for line in result.split("\n") if "=" in line)

        return {
            "channels": int(info_dict.get("channels", 0)),
            "layout": info_dict.get("channel_layout", "unknown"),
            "sample_rate": int(info_dict.get("sample_rate", 0)),
        }
    except (subprocess.CalledProcessError, ValueError) as e:
        console.print(f"[bold red]Could not probe file: {file_path.name}[/bold red]")
        if isinstance(e, subprocess.CalledProcessError):
            console.print(f"[dim]ffprobe error:\n{e.stderr}[/dim]")
        else:
            console.print(f"[dim]{e}[/dim]")
        return {}


def upmix_file_to_5_1(file_path: Path):
    """
    Upmixes a stereo audio file to 5.1 surround sound using a sophisticated FFmpeg filtergraph.
    """
    console.rule(f"[bold blue]Processing: {file_path.name}", style="blue")

    audio_info = get_audio_info(file_path)
    if not audio_info or audio_info.get("channels") != 2:
        console.print(
            f"[yellow]Warning:[/yellow] '{file_path.name}' is not a valid stereo file (channels={audio_info.get('channels', 'N/A')}). Skipping."
        )
        return False

    output_file = file_path.with_name(f"{file_path.stem}{OUTPUT_SUFFIX}{DEFAULT_OUTPUT_FORMAT}")

    # --- Corrected and Simplified FFmpeg Filtergraph ---
    # This version uses the correct `adelay` syntax for mono streams and removes the
    # problematic `map` parameter from the `join` filter.
    ffmpeg_filter = (
        f"[0:a]channelsplit=channel_layout=stereo[L][R];"
        f"[L][R]amerge=inputs=2,pan=mono|c0=0.5*FL+0.5*FR,highshelf=f=2000:g=-6[FC];"
        f"[L][R]amerge=inputs=2,pan=mono|c0=0.5*FL+0.5*FR,lowpass=f={DEFAULT_LFE_CROSSOVER}[LFE];"
        f"[L]adelay={DEFAULT_FRONT_DELAY}[FLd];"
        f"[R]adelay={DEFAULT_FRONT_DELAY}[FRd];"
        f"[L]adelay={DEFAULT_REAR_DELAY},lowpass=f=7000[SL];"
        f"[R]adelay={DEFAULT_REAR_DELAY},lowpass=f=7000[SR];"
        f"[FLd][FRd][FC][LFE][SL][SR]join=inputs=6:channel_layout=5.1[a]"
    )

    ffmpeg_command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(file_path),
        "-filter_complex",
        ffmpeg_filter,
        "-map",
        "[a]",
        "-y",
        "-c:a",
        "flac" if DEFAULT_OUTPUT_FORMAT == ".flac" else "ac3",
        *(["-b:a", "640k"] if DEFAULT_OUTPUT_FORMAT == ".ac3" else []),
        str(output_file),
    ]

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task(f"[cyan]Upmixing to {output_file.name}", total=None)
            process = subprocess.run(
                ffmpeg_command,
                check=True,
                capture_output=True,
                text=True,
            )

        console.print("  [bold green]✓ Upmix complete![/bold green]")
        console.print(f"    [dim]Saved to:[/dim] [cyan]{output_file.name}[/cyan]\n")
        return True

    except subprocess.CalledProcessError as e:
        console.print("[bold red]An error occurred during FFmpeg processing.[/bold red]")
        # Create a more readable version of the command for printing
        printable_command = " ".join(f'"{arg}"' if " " in arg else arg for arg in e.cmd)
        console.print("[yellow]FFmpeg Command:[/yellow]")
        console.print(f"[dim]{printable_command}[/dim]")
        console.print("[yellow]FFmpeg Error Log:[/yellow]")
        console.print(f"[dim]{e.stderr}[/dim]")
        console.print(f"[bold red]✗ Failed to process:[/bold red] [cyan]{file_path.name}[/cyan]\n")
        return False


def main():
    """Main function to handle arguments and processing loop."""
    console.print(
        Panel(
            "[bold magenta]Advanced 5.1 FFmpeg Upmixer[/bold magenta] 🎶",
            title="[bold]v2.2[/bold]",
            border_style="magenta",
            expand=False,
        )
    )

    if not check_dependencies():
        sys.exit(1)

    if len(sys.argv) < 2:
        console.print("[bold red]Error: No audio files provided.[/bold red]")
        console.print("Usage: python3 upmix_audio.py <file1> [file2 ...]")
        sys.exit(1)

    valid_files = []
    for f in sys.argv[1:]:
        p = Path(f)
        if p.is_file():
            valid_files.append(p)
        else:
            console.print(
                f"\n[bold red]Error:[/bold red] '{f}' is not a valid file path and will be skipped."
            )

    if not valid_files:
        console.print("[yellow]No valid files were provided to process.[/yellow]")
        return

    table = Table(title="Files to Process", show_header=True, header_style="bold cyan")
    table.add_column("Index", style="dim", width=5, justify="right")
    table.add_column("Filename", style="cyan")
    for i, f in enumerate(valid_files, 1):
        table.add_row(str(i), f.name)
    console.print(table)

    success_count = 0
    fail_count = 0
    for file_path in valid_files:
        if upmix_file_to_5_1(file_path):
            success_count += 1
        else:
            fail_count += 1

    console.rule("[bold green]Processing Summary", style="green")
    console.print(f"Successfully processed: [bold green]{success_count}[/bold green] file(s).")
    if fail_count > 0:
        console.print(f"Failed to process: [bold red]{fail_count}[/bold red] file(s).")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold yellow]Process cancelled by user. Exiting.[/bold yellow]")
        sys.exit(0)
