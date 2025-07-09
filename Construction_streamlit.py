import streamlit as st
from ultralytics import YOLO
import os
import tempfile
import shutil

# Load your custom YOLOv8 model
model = YOLO("custom_yolo_model.pt")  # Leave unchanged if using default

st.set_page_config(page_title="YOLOv8 Object Detection", layout="centered")
st.title("🧠 YOLOv8 Object Detection App")
st.markdown("Upload an image or video and run YOLOv8 object detection.")

# Upload file
uploaded_file = st.file_uploader("Choose an image or video...", type=["jpg", "jpeg", "png", "mp4", "mov", "avi"])

st.write("For video files, result will be stored in runs folder...")

if uploaded_file:
    is_image = uploaded_file.type.startswith("image")
    suffix = ".jpg" if is_image else ".mp4"

    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    # Display original media
    if is_image:
        st.image(tmp_path, caption="Uploaded Image", use_container_width=True)
    else:
        st.video(tmp_path)

    st.write("⏳ Running YOLOv8 detection...")

    # Run detection
    results = model.predict(source=tmp_path, save=True, conf=0.25)

    # Find output file path
    result_dir = results[0].save_dir
    result_file = os.path.join(result_dir, os.path.basename(tmp_path))
    result_file = result_file.replace("\\", "/")

    st.success("✅ Detection complete!")

    # Display result media

    if is_image and os.path.exists(result_file):
        st.image(result_file, caption="Detected Image", use_container_width=True)
    elif not is_image and os.path.exists(result_file):
        st.video(result_file)

