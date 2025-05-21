import streamlit as st
import pandas as pd
import numpy as np
import cv2
from io import BytesIO

st.set_page_config(
    page_title="Color Detection from Images",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("🎨 Color Detection from Images")
st.write(
    "Upload an image, then click anywhere on the image to detect the color at that pixel. "
    "The closest color name and its RGB values will be displayed."
)

# Load colors.csv dataset with color names and rgb values
@st.cache_data
def load_colors_data():
    df = pd.read_csv("colors.csv", header=None, names=["color", "color_name", "hex", "R", "G", "B"])
    return df

colors_df = load_colors_data()

# Function to calculate the closest color from the dataset
def get_closest_color_name(R, G, B):
    # Euclidean distance between clicked color and dataset colors
    distances = np.sqrt((colors_df["R"] - R) ** 2 + (colors_df["G"] - G) ** 2 + (colors_df["B"] - B) ** 2)
    idx = distances.idxmin()
    return colors_df.loc[idx, "color_name"], colors_df.loc[idx, "R"], colors_df.loc[idx, "G"], colors_df.loc[idx, "B"]

# Image upload
uploaded_file = st.file_uploader("Upload Image (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read image as OpenCV image
    image_bytes = uploaded_file.read()
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)  # BGR format

    # Convert to RGB for display and interaction
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img_rgb.shape

    st.write("Click on the image to detect the color!")

    # Use Streamlit to display image and capture click coordinates
    # Streamlit doesn't natively support capturing mouse position on images.
    # We'll use HTML + JS canvas to achieve click detection with st.components.
    import streamlit.components.v1 as components

    # Convert image to base64 to embed in HTML
    import base64

    _, im_buf_arr = cv2.imencode(".png", img_rgb)
    im_bytes = im_buf_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes).decode()

    # HTML and JS for click event on image canvas that returns coordinates
    html_code = f"""
    <canvas id="canvas" width="{w}" height="{h}" style="border:1px solid #d3d3d3;"></canvas>
    <script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    // Load image
    const image = new Image();
    image.src = "data:image/png;base64,{im_b64}";
    image.onload = function() {{
        ctx.drawImage(image,0,0);
    }};

    // Function to send coords to Streamlit
    function sendCoords(x, y) {{
        const coords = {{x: x, y: y}};
        window.parent.postMessage({{isStreamlitMessage: true, type: "streamlit:message", event: "click", data: coords}}, "*");
    }}

    // Add click listener
    canvas.addEventListener('click', function(event) {{
        const rect = canvas.getBoundingClientRect();
        const x = Math.floor(event.clientX - rect.left);
        const y = Math.floor(event.clientY - rect.top);
        sendCoords(x, y);
    }});
    </script>
    """

    # Component to render canvas and receive click data
    # Using Streamlit's experimental features to receive messages from iframe
    message = components.html(html_code, height=h + 10, scrolling=False)

    # A hack: We simulate a small text input that receives click coordinates from JS
    # Since Streamlit does not natively support JS event messaging easily,
    # We will rely on a workaround with st.experimental_get_query_params or session state.
    # Instead, we use streamlit's experimental features for a simpler implementation here:
    # Alternatively, fallback to file upload + manual coordinate input.

    # Since direct communication from JS to Streamlit isn't straightforward without a separate server,
    # we simplify: Let user input click coordinates manually below after viewing the image.

    st.markdown("**Note:** Due to Streamlit limitations, click coordinates input is manual in this demo. "
                "View the image above and enter the coordinates of the pixel to detect the color.")

    col1, col2 = st.columns(2)
    x_coord = col1.number_input("X Coordinate", min_value=0, max_value=w-1, step=1, value=w//2)
    y_coord = col2.number_input("Y Coordinate", min_value=0, max_value=h-1, step=1, value=h//2)

    if st.button("Detect Color"):
        r, g, b = img_rgb[y_coord, x_coord]
        color_name, cR, cG, cB = get_closest_color_name(r, g, b)

        st.markdown(f"### Detected Color at ({x_coord}, {y_coord})")
        st.markdown(f"**RGB Value:** ({r}, {g}, {b})")
        st.markdown(f"**Closest Color Name:** {color_name} (Dataset RGB: {cR}, {cG}, {cB})")
        st.markdown(
            f'<div style="width:100px; height:100px; background-color: rgb({r},{g},{b}); border: 1px solid #000;"></div>',
            unsafe_allow_html=True,
        )
else:
    st.info("Please upload an image to get started.")

