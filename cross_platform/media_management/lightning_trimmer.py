#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
import shutil
import subprocess
import sys

# --- CONFIGURATION ---
# Adjust these values to fine-tune the detection and trimming.

# BRIGHTNESS THRESHOLD (0-255). This is the most important setting.
# It defines how bright a frame's average luma must be to be considered part of a strike.
# - For dark, rural skies: 40-70 might be a good start.
# - For brighter, city skies: You may need a higher value like 80-120.
# Experiment to find the best value for your specific video.
BRIGHTNESS_THRESHOLD = 50

# Time in seconds to add before the lightning strike begins.
PRE_ROLL_SECONDS = 0.5

# Time in seconds to add after the lightning strike ends.
POST_ROLL_SECONDS = 1.0  # Increased slightly to better capture the fade-out
# --- END CONFIGURATION ---


def check_dependencies():
    """Checks if ffmpeg and ffprobe are in the system's PATH."""
    for tool in ["ffmpeg", "ffprobe"]:
        if not shutil.which(tool):
            print(f"Error: {tool} is not installed or not in your PATH.", file=sys.stderr)
            print(
                "Please install FFmpeg to use this script (it includes ffprobe).", file=sys.stderr
            )
            print("\nOn macOS, use: brew install ffmpeg", file=sys.stderr)
            print("On Windows, use: choco install ffmpeg", file=sys.stderr)
            print(
                "On Debian/Ubuntu, use: sudo apt update && sudo apt install ffmpeg\n",
                file=sys.stderr,
            )
            sys.exit(1)


def get_video_file_from_user():
    """Prompts the user to drag and drop a video file into the terminal."""
    while True:
        try:
            raw_path = input("Please drag and drop your video file here and press Enter: ")
            video_path = raw_path.strip().replace("\\ ", " ").strip("'\"")
            if os.path.isfile(video_path):
                print(f"✅ Video file accepted: {os.path.basename(video_path)}")
                return video_path
            else:
                print(
                    "Error: The path provided is not a valid file. Please try again.",
                    file=sys.stderr,
                )
        except (EOFError, KeyboardInterrupt):
            print("\nScript cancelled by user. Exiting.")
            sys.exit(0)


def get_video_framerate(video_path):
    """Uses ffprobe to get the video's framerate."""
    print("\n🔍 Step 1/5: Detecting video framerate...")
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=r_frame_rate",
        "-of",
        "json",
        video_path,
    ]
    try:
        process = subprocess.run(command, check=True, capture_output=True, text=True)
        data = json.loads(process.stdout)
        rate_str = data["streams"][0]["r_frame_rate"]
        num, den = map(int, rate_str.split("/"))
        fps = float(num) / den
        print(f"✅ Framerate detected: {fps:.2f} fps")
        return fps
    except (subprocess.CalledProcessError, KeyError, IndexError, ValueError) as e:
        print(f"Error: Could not determine framerate from video file. {e}", file=sys.stderr)
        sys.exit(1)


def detect_bright_frames(video_path):
    """
    Analyzes every frame's brightness and returns a list of timestamps for frames
    that exceed the BRIGHTNESS_THRESHOLD.
    """
    print(f"\n💡 Step 2/5: Analyzing frame brightness (Threshold = {BRIGHTNESS_THRESHOLD})...")
    print("(This may take a moment on long videos)")
    command = ["ffmpeg", "-i", video_path, "-vf", "signalstats,showinfo", "-f", "null", "-"]
    try:
        process = subprocess.run(command, stderr=subprocess.PIPE, text=True, check=False)
    except FileNotFoundError:
        print("FFmpeg command not found.", file=sys.stderr)
        sys.exit(1)

    bright_timestamps = []
    # Regex to capture both pts_time and the average luma (YAVG)
    regex = re.compile(r"pts_time:([\d.]+)\s.*lavfi\.signalstats\.YAVG=([\d.]+)")

    for line in process.stderr.splitlines():
        match = regex.search(line)
        if match:
            timestamp = float(match.group(1))
            brightness = float(match.group(2))
            if brightness > BRIGHTNESS_THRESHOLD:
                bright_timestamps.append(timestamp)

    if not bright_timestamps:
        print("No frames found above the brightness threshold.")
        return []

    print(f"Found {len(bright_timestamps)} frames that exceed the brightness threshold.")
    return bright_timestamps


def group_continuous_frames(bright_timestamps, framerate):
    """Groups consecutive bright frames into continuous lightning events."""
    if not bright_timestamps:
        return []

    print("📊 Step 3/5: Grouping bright frames into continuous events...")
    # A gap larger than 1.5x the frame duration means the strike has ended.
    max_gap = 1.5 / framerate

    continuous_groups = []
    current_group_start = bright_timestamps[0]
    current_group_end = bright_timestamps[0]

    for i in range(1, len(bright_timestamps)):
        if bright_timestamps[i] - bright_timestamps[i - 1] <= max_gap:
            # This frame is part of the same continuous event
            current_group_end = bright_timestamps[i]
        else:
            # Gap detected, so the event ended. Finalize it and start a new one.
            continuous_groups.append((current_group_start, current_group_end))
            current_group_start = bright_timestamps[i]
            current_group_end = bright_timestamps[i]

    # Add the last event
    continuous_groups.append((current_group_start, current_group_end))
    print(f"Grouped into {len(continuous_groups)} distinct lightning event(s).")
    return continuous_groups


def calculate_and_merge_final_segments(event_groups):
    """Applies pre/post-roll to events and merges any resulting overlaps."""
    if not event_groups:
        return []

    print("🧩 Step 4/5: Applying buffers and merging final segments...")
    segments = [
        (max(0, start - PRE_ROLL_SECONDS), end + POST_ROLL_SECONDS) for start, end in event_groups
    ]
    segments.sort(key=lambda x: x[0])

    merged = []
    if not segments:
        return []

    current_start, current_end = segments[0]
    for next_start, next_end in segments[1:]:
        if next_start <= current_end:
            current_end = max(current_end, next_end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = next_start, next_end
    merged.append((current_start, current_end))

    print(f"Created {len(merged)} final video clips to render.")
    return merged


def generate_final_video(video_path, segments, final_output_path):
    """Generates the final video using hardware acceleration where possible."""
    print("\n✂️ Step 5/5: Building final video...")
    filter_complex = (
        f"[0:v]select='{'+'.join([f'between(t,{s},{e})' for s, e in segments])}',setpts=N/FRAME_RATE/TB[v];"
        f"[0:a]aselect='{'+'.join([f'between(t,{s},{e})' for s, e in segments])}',asetpts=N/SR/TB[a]"
    )
    base_cmd = [
        "ffmpeg",
        "-i",
        video_path,
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
        "-map",
        "[a]",
    ]

    encoder_settings = []
    if sys.platform == "darwin":
        print("✅ macOS detected. Using hardware-accelerated VideoToolbox encoder.")
        encoder_settings = ["-c:v", "hevc_videotoolbox", "-b:v", "30M", "-tag:v", "hvc1"]
    else:
        print("✅ Windows/Linux detected. Using CPU-based libx265 encoder.")
        encoder_settings = ["-c:v", "libx265", "-preset", "fast", "-crf", "22"]

    final_command = (
        base_cmd + encoder_settings + ["-c:a", "aac", "-b:a", "192k", "-y", final_output_path]
    )

    print("\n🚀 Starting final render. You will see live progress from FFmpeg.")
    print("-" * 50)
    try:
        subprocess.run(final_command, check=True)
        print("-" * 50)
        return True
    except subprocess.CalledProcessError:
        print("\n" + "-" * 50, file=sys.stderr)
        print("--- FFmpeg Re-encoding Error ---", file=sys.stderr)
        print(f"Failed Command: {' '.join(final_command)}", file=sys.stderr)
        return False
    except KeyboardInterrupt:
        print("\n" + "-" * 50 + "\nUser cancelled the encoding process.")
        return False


def main():
    """Main execution function."""
    print("--- Lightning Strike Video Trimmer (v6 - Brightness-State Detection) ---")
    check_dependencies()
    source_video_path = get_video_file_from_user()

    try:
        framerate = get_video_framerate(source_video_path)
        bright_frames = detect_bright_frames(source_video_path)
        if not bright_frames:
            print("\n✅ Process finished. No lightning activity found.")
            return

        event_groups = group_continuous_frames(bright_frames, framerate)
        final_segments = calculate_and_merge_final_segments(event_groups)
        if not final_segments:
            print("\n✅ Process finished. No final video clips could be created.")
            return

        directory, filename = os.path.split(source_video_path)
        name, ext = os.path.splitext(filename)
        output_filename = f"{name} - Lightning Trimmed.mp4"
        final_output_path = os.path.join(directory, output_filename)

        success = generate_final_video(source_video_path, final_segments, final_output_path)

        if success:
            print("\n🎉 --- Success! --- 🎉")
            print(f"Final video saved to: {final_output_path}")
        else:
            print("\n❌ --- Process Failed --- ❌")

    except Exception as e:
        print("\n--- An Unexpected Script Error Occurred ---", file=sys.stderr)
        print(str(e), file=sys.stderr)
    except KeyboardInterrupt:
        print("\nScript cancelled by user.")


if __name__ == "__main__":
    main()
