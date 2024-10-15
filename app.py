import streamlit as st
import os
from processing import *
from PIL import Image

# Cấu hình thư mục tải lên và lưu ảnh
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Giao diện chính của ứng dụng
st.title("Image Processing App")

# Người dùng upload ảnh
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

# Chọn phương pháp xử lý ảnh
method = st.selectbox(
    "Select processing method",
    ("Negative", "Logarithmic", "Power Law", "Piecewise Linear", "Bit Plane Slicing", "Thresholding")
)

# Nhập các tham số bổ sung cho các phương pháp
if method == "Power Law":
    gamma = st.slider("Gamma", min_value=0.1, max_value=5.0, value=1.0)
elif method == "Piecewise Linear":
    r1 = st.slider("r1", min_value=0, max_value=255, value=50)
    s1 = st.slider("s1", min_value=0, max_value=255, value=100)
    r2 = st.slider("r2", min_value=0, max_value=255, value=200)
    s2 = st.slider("s2", min_value=0, max_value=255, value=250)
elif method == "Bit Plane Slicing":
    bit = st.slider("Bit", min_value=0, max_value=7, value=0)
elif method == "Thresholding":
    threshold_value = st.slider("Threshold Value", min_value=0, max_value=255, value=128)

# Khi người dùng nhấn nút xử lý
if st.button("Process Image"):
    if uploaded_file is not None:
        # Lưu file tải lên
        image = Image.open(uploaded_file).convert('L')  # Chuyển sang ảnh grayscale
        filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        image.save(filepath)

        # Xử lý ảnh theo phương pháp đã chọn
        if method == "Negative":
            processed_image = negative_transformation(image)
        elif method == "Logarithmic":
            processed_image = logarithmic_transformation(image)
        elif method == "Power Law":
            processed_image = power_law_transformation(image, gamma)
        elif method == "Piecewise Linear":
            processed_image = piecewise_linear_transformation(image, r1, s1, r2, s2)
        elif method == "Bit Plane Slicing":
            processed_image = bit_plane_slicing(image, bit)
        elif method == "Thresholding":
            processed_image = threshold_transformation(image, threshold_value)

        # Lưu ảnh đã xử lý
        output_path = os.path.join(OUTPUT_FOLDER, uploaded_file.name)
        save_image(processed_image, output_path)

        # Hiển thị ảnh đã xử lý
        st.image(processed_image, caption='Processed Image', use_column_width=True)
        st.success(f"Image processed and saved to {output_path}")
