import cv2
import numpy as np
from collections import deque
import sys
import subprocess
import os

def main():
    if len(sys.argv) < 2:
        print("ERROR: Please provide video file path")
        sys.exit(1)
    
    VIDEO_PATH = sys.argv[1]
    
    if not os.path.exists(VIDEO_PATH):
        print(f"ERROR: Video file not found: {VIDEO_PATH}")
        sys.exit(1)

    # Changed to use .mp4 extension directly
    TEMP_OUTPUT = "temp_motion.mp4"
    OUTPUT_VIDEO = "all_motion_events.mp4"

    FPS = 30
    PRE_EVENT_SECONDS = 7
    POST_EVENT_SECONDS = 7

    MIN_CONTOUR_AREA = 400
    MOTION_WINDOW = 20
    MOTION_THRESHOLD = 5

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("ERROR: Cannot open video")
        sys.exit(1)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    if original_fps > 0:
        FPS = int(original_fps)

    # Streamlit requires MP4 with proper codec for browser playback
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(TEMP_OUTPUT, fourcc, FPS, (width, height))

    frame_buffer = deque(maxlen=FPS * PRE_EVENT_SECONDS)
    motion_window = deque(maxlen=MOTION_WINDOW)

    prev_gray = None
    recording = False
    post_event_counter = 0
    frame_count = 0

    print(f"Processing video: {VIDEO_PATH}")
    print(f"Resolution: {width}x{height}, FPS: {FPS}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_buffer.append(frame.copy())

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_gray is None:
            prev_gray = gray
            continue

        frame_delta = cv2.absdiff(prev_gray, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        motion_area = sum(
            cv2.contourArea(c)
            for c in contours
            if cv2.contourArea(c) >= MIN_CONTOUR_AREA
        )

        motion_window.append(1 if motion_area > 0 else 0)

        if sum(motion_window) >= MOTION_THRESHOLD and not recording:
            recording = True
            post_event_counter = FPS * POST_EVENT_SECONDS
            print(f"Motion detected at frame {frame_count}")
            for bf in frame_buffer:
                out.write(bf)

        if recording:
            out.write(frame)
            post_event_counter -= 1
            if post_event_counter <= 0:
                recording = False
                motion_window.clear()

        prev_gray = gray
        frame_count += 1
        
        # Progress indicator
        if frame_count % 100 == 0:
            print(f"Processed {frame_count} frames...")

    cap.release()
    out.release()
    
    print(f"Total frames processed: {frame_count}")
    print(f"Temporary output created: {TEMP_OUTPUT}")

    # Check if temporary file was created and has content
    if os.path.exists(TEMP_OUTPUT) and os.path.getsize(TEMP_OUTPUT) > 0:
        # Ensure proper MP4 format for browser playback
        print("Converting to browser-compatible format...")
        
        # First check if ffmpeg is available
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            ffmpeg_available = True
        except:
            ffmpeg_available = False
            print("FFmpeg not found, using OpenCV output directly")
        
        if ffmpeg_available:
            try:
                subprocess.run(
                    [
                        "ffmpeg", "-y",
                        "-i", TEMP_OUTPUT,
                        "-c:v", "libx264",
                        "-pix_fmt", "yuv420p",
                        "-preset", "fast",
                        "-movflags", "+faststart",
                        OUTPUT_VIDEO
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )
                print(f"Conversion successful: {OUTPUT_VIDEO}")
            except subprocess.CalledProcessError as e:
                print(f"FFmpeg conversion failed: {e}")
                # Fall back to just copying the temp file
                import shutil
                shutil.copy(TEMP_OUTPUT, OUTPUT_VIDEO)
        else:
            # FFmpeg not available, just rename the temp file
            os.rename(TEMP_OUTPUT, OUTPUT_VIDEO)
        
        # Clean up temporary file
        if os.path.exists(TEMP_OUTPUT):
            os.remove(TEMP_OUTPUT)
            
        print(f"DONE: {OUTPUT_VIDEO}")
        print(f"Output size: {os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024):.2f} MB")
    else:
        print("ERROR: No motion detected or processing failed")
        sys.exit(1)

if __name__ == "__main__":
    main()