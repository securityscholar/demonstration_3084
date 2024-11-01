# -*- coding: utf-8 -*-
import streamlit as st
import cv2
import numpy as np

# Function to extract the dominant color from an image
def get_dominant_color(image_path):
    # Read the image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Reshape the image to be a list of pixels
    pixels = img.reshape(-1, 3)
    
    # Convert to float
    pixels = np.float32(pixels)

    # Define criteria and apply k-means clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    k = 3  # Number of colors
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert centers to uint8
    centers = np.uint8(centers)
    
    # Get the most dominant color
    dominant_color = centers[0]  # For simplicity, take the first color

    return tuple(dominant_color)

# Function to check if two colors match based on simple rules
def colors_match(color1, color2):
    # Convert RGB to a basic color category (you can enhance this logic)
    categories = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'brown': (165, 42, 42),
        # Add more color categories as needed
    }
    
    # Example logic for matching colors
    # You can expand this logic based on your matching criteria
    if (color1[0] in range(200, 256) and color1[1] < 100 and color1[2] < 100):  # Red
        return color2 == categories['brown']  # e.g., Red shirt with Brown pants
    
    return False

# Streamlit app
st.title("Clothing Match Checker")
st.write("Upload two images of clothing to see if they match!")

# Upload images
uploaded_file1 = st.file_uploader("Upload first clothing image", type=["jpg", "jpeg", "png"])
uploaded_file2 = st.file_uploader("Upload second clothing image", type=["jpg", "jpeg", "png"])

if uploaded_file1 and uploaded_file2:
    # Save uploaded files temporarily
    with open("image1.jpg", "wb") as f:
        f.write(uploaded_file1.getbuffer())
    with open("image2.jpg", "wb") as f:
        f.write(uploaded_file2.getbuffer())

    # Get dominant colors
    color1 = get_dominant_color("image1.jpg")
    color2 = get_dominant_color("image2.jpg")

    # Check if colors match
    if colors_match(color1, color2):
        st.image(uploaded_file1, caption='First Clothing Image', use_column_width=True)
        st.image(uploaded_file2, caption='Second Clothing Image', use_column_width=True)
        st.success("👍 The clothes match!")
    else:
        st.image(uploaded_file1, caption='First Clothing Image', use_column_width=True)
        st.image(uploaded_file2, caption='Second Clothing Image', use_column_width=True)
        st.error("👎 The clothes do not match.")
