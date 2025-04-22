import cv2
import numpy as np


def apply_rotational_blur(image_path, output_path, kernel_size=25):
    # Load the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Image not found or invalid path.")

    # Create a circular motion blur kernel
    kernel = np.zeros((kernel_size, kernel_size), dtype=np.float32)
    center = kernel_size // 2

    # Draw a circular blur pattern
    for i in range(kernel_size):
        for j in range(kernel_size):
            dist = np.sqrt((i - center) ** 2 + (j - center) ** 2)
            if center - 1 <= dist <= center:  # Thin circular band
                kernel[i, j] = 1

    # Normalize the kernel
    kernel /= np.sum(kernel)

    # Apply the filter to the image
    blurred_img = cv2.filter2D(img, -1, kernel)

    # Save the output image
    cv2.imwrite(output_path, blurred_img)
    print(f"Rotational blur applied and saved to {output_path}")


# Example usage
apply_rotational_blur(
    "assets/data/person1000_bacteria_2931.jpeg",
    "rotational_blurred.jpg",
    kernel_size=25,
)
