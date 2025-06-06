# Application
Color Detection from Images

# Color Detection from Images

## Overview
Color Detection from Images is a simple and interactive web application that allows designers, artists, and developers to upload an image and detect the color at any pixel coordinate. The application identifies the RGB color value at the selected point and finds the closest matching color name from a predefined dataset. It also provides a visual preview of the detected color.

This tool helps in selecting brand-consistent colors, analyzing visual content, and improving accessibility in digital design.

---

## Features
- Upload images in JPG, JPEG, or PNG formats.
- Detect color by specifying the pixel coordinates on the image.
- Retrieve the RGB values of the selected pixel.
- Find the closest matching color name from a comprehensive color dataset.
- Display a visual color box corresponding to the detected color.
- Clean and responsive user interface built with Streamlit.

---

## Technologies & Tools
- **Python** - programming language.
- **Streamlit** - for creating the interactive web interface.
- **OpenCV** - for image processing and pixel color extraction.
- **Pandas** - for handling the color dataset from CSV.
- **NumPy** - for efficient numeric computations.

---

## Installation

1. Clone the repository:
   
   git clone https://github.com/your-username/color-detection-app.git cd color-detection-app

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

3.Install required dependencies:

pip install -r requirements.txt

4.Ensure colors.csv is present in the project directory.

## Run the Streamlit app with the following command:
streamlit run app.py
