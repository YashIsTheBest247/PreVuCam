# 🎥 PreVuCam – AI-Enhanced Motion Detection Extension

PreVuCam is a Streamlit-based AI extension for traditional camera systems. It enables intelligent motion-based video trimming using frame differencing, reducing storage usage, power consumption, and manual review time.

This system works as an add-on layer over an existing camera module. Users upload recorded footage, and the system automatically extracts motion events into a single compiled video.

---

## 🚀 Features

- 📤 Upload recorded video files
- 🎯 Automatic motion detection using frame differencing
- ⏱️ 7-second pre-event buffer
- ⏱️ 7-second post-event buffer
- ✂️ Automatic trimming of motion clips
- 📦 Compilation of all detected events into a single MP4 file
- 📥 Download processed output
- 📊 Processing logs for debugging

---

## 🧠 How It Works

PreVuCam enhances a traditional camera system by:

1. Accepting a recorded video file
2. Running motion detection using frame differencing
3. Identifying motion events
4. Extracting:
   - 7 seconds before the event
   - The motion event itself
   - 7 seconds after the event
5. Combining all event clips into one final video file

This ensures:
- Reduced storage usage
- Lower power consumption
- Faster video review
- Cleaner event-based surveillance

---

## 📂 Project Structure

```bash
PreVuCam/
│
├── app.py # Streamlit frontend (main UI)
├── try.py # Motion detection processing script
├── uploads/ # Temporary uploaded videos
├── all_motion_events.mp4 # Final compiled output
└── README.md
```



---

## 🛠️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YashIsTheBest247/PreVuCam
cd PreVuCam
```

2️⃣ Install Dependencies
``` bash
pip install streamlit opencv-python numpy
```
3️⃣ Run the Application
```bash
streamlit run app.py
``` 
🖥️ Usage

Open the Streamlit interface.
Upload a supported video file:
.mp4,
.avi,
.mov,
.mkv,
.webm

Click "Run Motion Detection" >
Wait for processing >
View detected motion events >
Download the compiled output video.

⚙️ Default Settings

1. Pre-event buffer: 7 seconds
2. Post-event buffer: 7 seconds
3. Motion detection method: Frame 
4. Differencing

Output format: MP4 (browser compatible)

🧩 Code Overview
app.py
1. Handles file uploads
2. Displays original video
3. Executes motion detection script using subprocess
4. Displays logs and output
5. Provides download button

🧩try.py
1. Performs frame differencing
2. Detects motion events
3. Extracts buffered clips
4. Merges clips into a single output file

🔬 Technical Concept
1. This project serves as an AI-powered extension layer to traditional CCTV systems.
2. Instead of continuously storing raw footage, 
PreVuCam:
1. Identifies meaningful motion
2. Stores only relevant segments
3. Eliminates idle recording time

This makes surveillance systems:
1. More efficient
2. More scalable
3. More intelligent
