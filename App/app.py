import streamlit as st
import cv2
import numpy as np
from collections import deque
import time
from PIL import Image


# Function to display a frame in Streamlit
def display_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    st.image(frame, channels="RGB")

# Initialize Streamlit app
st.title("Webcam Recorder with Frame Buffer")

# Button state
if "recording" not in st.session_state:
    st.session_state.recording = False

# Circular buffer to store the last 128 frames
FRAME_BUFFER_SIZE = 128
if "frame_buffer" not in st.session_state:
    st.session_state.frame_buffer = deque(maxlen=FRAME_BUFFER_SIZE)

# Status display
status_placeholder = st.empty()
if st.session_state.recording:
    status_placeholder.markdown("### Status: **Live Recording...**")
else:
    status_placeholder.markdown("### Status: **Playback**")

# Start/Stop Button
if st.button("Start/Stop"):
    st.session_state.recording = not st.session_state.recording

# Webcam stream handling
video_placeholder = st.empty()
if st.session_state.recording:
    cap = cv2.VideoCapture(0)  # Initialize webcam
    if not cap.isOpened():
        st.error("Unable to access the camera. Please check your webcam.")
    else:
        while st.session_state.recording:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to capture frame. Stopping recording.")
                break

            # Display live stream and store frame in the buffer
            video_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
            st.session_state.frame_buffer.append(frame)

            # Update the status
            status_placeholder.markdown("### Status: **Live Recording...**")

            # Allow Streamlit to refresh UI
            time.sleep(0.03)  # Approx. 30 FPS

        cap.release()

# Stop recording: Loop the buffered frames
if not st.session_state.recording and st.session_state.frame_buffer:
    while True:
        for frame in list(st.session_state.frame_buffer):
            video_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
            status_placeholder.markdown("### Status: **Processing**")
            #images = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))]
            time.sleep(0.03)  # Display at 30 FPS
