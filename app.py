import streamlit as st
import os
import subprocess
import time
import sys

st.set_page_config(page_title="Motion Detection", layout="wide")

st.title("🎥 PreVuCam")
st.markdown("Upload a video to detect motion events")

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
try_script_path = os.path.join(current_dir, "try.py")

# Check if try.py exists
if not os.path.exists(try_script_path):
    st.error(f"❌ Motion detection script not found at: {try_script_path}")
    st.stop()

uploaded_file = st.file_uploader(
    "Upload a video file",
    type=["mp4", "avi", "mov", "mkv", "webm"]
)

if uploaded_file:
    os.makedirs("uploads", exist_ok=True)
    
    # Create unique filename to avoid conflicts
    timestamp = str(int(time.time()))
    input_filename = f"upload_{timestamp}_{uploaded_file.name}"
    input_path = os.path.join("uploads", input_filename)
    
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"✅ Video uploaded successfully: {uploaded_file.name}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Video")
        # Reset file pointer to beginning
        uploaded_file.seek(0)
        st.video(uploaded_file.read())
    
    with col2:
        st.subheader("Processing")
        if st.button("🚀 Run Motion Detection", type="primary"):
            # Clear any previous output
            output_path = os.path.join(current_dir, "all_motion_events.mp4")
            if os.path.exists(output_path):
                os.remove(output_path)
            
            with st.spinner("Detecting motion events... This may take a while ⏳"):
                # Create a placeholder for output
                output_placeholder = st.empty()
                
                # Run motion detection
                try:
                    # Use full paths
                    python_executable = sys.executable
                    
                    st.info(f"Processing: {uploaded_file.name}")
                    
                    # Run the script and capture output
                    result = subprocess.run(
                        [python_executable, try_script_path, input_path],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    
                    # Display output
                    if result.stdout:
                        output_placeholder.text_area("Processing Log", result.stdout, height=200)
                    
                    st.success("🎉 Processing complete!")
                    
                    # Check for output file
                    if os.path.exists(output_path):
                        st.subheader("Detected Motion Events")
                        
                        # Get file size
                        file_size = os.path.getsize(output_path) / (1024 * 1024)
                        st.info(f"Output file size: {file_size:.2f} MB")
                        
                        # Show video
                        with open(output_path, "rb") as video_file:
                            video_bytes = video_file.read()
                            st.video(video_bytes)
                        
                        # Add download button
                        st.download_button(
                            label="📥 Download Processed Video",
                            data=video_bytes,
                            file_name="motion_events.mp4",
                            mime="video/mp4"
                        )
                    else:
                        st.error("❌ Output video was not created")
                        
                except subprocess.CalledProcessError as e:
                    st.error(f"❌ Processing failed with exit code {e.returncode}")
                    
                    # Display error details
                    with st.expander("Error Details"):
                        if e.stdout:
                            st.text("STDOUT:")
                            st.code(e.stdout)
                        if e.stderr:
                            st.text("STDERR:")
                            st.code(e.stderr)
                            
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
                    import traceback
                    with st.expander("Traceback"):
                        st.code(traceback.format_exc())

# Add instructions
with st.sidebar:
    st.markdown("""
    ### 📋 Instructions:
    1. Upload a video file
    2. Click "Run Motion Detection"
    3. View detected motion events
    4. Download the processed video

    ### ⚙️ Settings:
    - Pre-event buffer: 7 seconds
    - Post-event buffer: 7 seconds
    - Motion sensitivity: Medium
    - Output format: MP4 (browser compatible)
    """)
    
    # Show system info
    st.markdown("---")
    st.markdown("### System Information")
    st.text(f"Python: {sys.version.split()[0]}")
    st.text(f"Current directory: {current_dir}")
    st.text(f"try.py path: {try_script_path}")

# Cleanup message
st.markdown("---")
st.caption("Uploaded files are stored in the 'uploads' folder")