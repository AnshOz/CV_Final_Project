import streamlit as st
import cv2
import time

# Function to display a frame in Streamlit
def display_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    st.image(frame, channels="RGB")

# Initialize Streamlit app
st.title("Webcam Recorder with Drowsiness Alerts")

'''
# Button state
if "recording" not in st.session_state:
    st.session_state.recording = False
# Start/Stop Button
if st.button("Start/Stop"):
    st.session_state.recording = not st.session_state.recording
'''
# Status display
status_placeholder = st.empty()

# Webcam stream handling
video_placeholder = st.empty()

if st.session_state.recording:
    cap = cv2.VideoCapture(0)  # Initialize webcam
    if not cap.isOpened():
        st.error("Unable to access the camera. Please check your webcam.")
    else:
        start_time = time.time()
        drowsy_warning_triggered = False
        final_warning_triggered = False

        while st.session_state.recording:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to capture frame. Stopping recording.")
                break

            # Display live stream
            video_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
            elapsed_time = time.time() - start_time

            # Update status based on elapsed time
            if elapsed_time < 1:
                status_placeholder.markdown("### Status: **Live Recording...**")
            elif elapsed_time < 7:
                status_placeholder.markdown("### Status: **Non-Drowsy**")
            elif elapsed_time < 11:  # 7 + 4 seconds
                if not drowsy_warning_triggered:
                    drowsy_warning_triggered = True
                status_placeholder.markdown("### Status: **Warning! Drowsy**")
            else:
                if not final_warning_triggered:
                    final_warning_triggered = True
                status_placeholder.markdown("## **You have been drowsy for the last 5 seconds. Please consider taking a break!**")
                video_placeholder.empty()

            # Allow Streamlit to refresh UI
            time.sleep(0.01)  # Approx. 30 FPS

        cap.release()
