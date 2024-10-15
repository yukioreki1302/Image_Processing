from PIL import Image
import numpy as np

# 1. Biến đổi ảnh sang âm bản
def negative_transformation(image):
    image_array = np.array(image)
    return Image.fromarray(255 - image_array)

# 2. Biến đổi logarit
def logarithmic_transformation(image):
    image_array = np.array(image)
    c = 255 / np.log(1 + np.max(image_array))
    log_image = c * (np.log(image_array + 1))
    log_image = np.array(log_image, dtype=np.uint8)
    return Image.fromarray(log_image)

# 3. Biến đổi Power Law (Gamma Correction)
def power_law_transformation(image, gamma):
    image_array = np.array(image)
    c = 255 / (np.max(image_array) ** gamma)
    power_law_image = c * (image_array ** gamma)
    power_law_image = np.array(power_law_image, dtype=np.uint8)
    return Image.fromarray(power_law_image)

# 4. Biến đổi tuyến tính từng đoạn
def piecewise_linear_transformation(image, r1, s1, r2, s2):
    def pixel_val(p, r1, s1, r2, s2):
        if p < r1:
            return (s1 / r1) * p
        elif r1 <= p <= r2:
            return ((s2 - s1) / (r2 - r1)) * (p - r1) + s1
        else:
            return ((255 - s2) / (255 - r2)) * (p - r2) + s2

    image_array = np.array(image)
    pixel_val_vec = np.vectorize(pixel_val)
    piecewise_image = pixel_val_vec(image_array, r1, s1, r2, s2)
    piecewise_image = np.array(piecewise_image, dtype=np.uint8)
    return Image.fromarray(piecewise_image)

# 5. Biến đổi Bit Plane Slicing
def bit_plane_slicing(image, bit):
    image_array = np.array(image)
    bit_plane_image = (image_array & (1 << bit)) >> bit
    bit_plane_image = np.array(bit_plane_image * 255, dtype=np.uint8)
    return Image.fromarray(bit_plane_image)

# 6. Biến đổi Thresholding (Ngưỡng)
def threshold_transformation(image, threshold_value):
    image_array = np.array(image)
    threshold_image = np.where(image_array > threshold_value, 255, 0)  # Binary threshold
    threshold_image = np.array(threshold_image, dtype=np.uint8)
    return Image.fromarray(threshold_image)

# Lưu ảnh đã xử lý
def save_image(image, path):
    image.save(path)
