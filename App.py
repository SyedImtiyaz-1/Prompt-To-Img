# import base64
# import streamlit as st
# import openai
# import os


# openai.api_key = "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"

# st.set_page_config(
#     page_title="Text to Image Generator",
#     page_icon="🎨",
#     layout="wide",
# )
# # Custom CSS styles
# st.markdown(
#     """
#     <style>
#     .download-button {
#         background-color: #221e5b;
#         color: #ffffff;
#         padding: 10px 15px;
#         border: 25px;
#         border-radius: 5px;
#         cursor: pointer;
#         text-decoration: none;
#         font-weight: bold;
#     }

#     .download-button:hover {
#         background-color: #ff5588;
#         color: #ffffff;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.title("Text to Image Generator")

# # Prompt input
# prompt = st.text_area("Enter the prompt : 👇", height=5)

# # Size selection
# size_options = ["256x256", "512x512", "1024x1024"]
# selected_size = st.selectbox("Select image size:", size_options)

# if st.button("Generate🪄"):
#     # Generate image
#     try:
#         response = openai.Image.create(
#             prompt=prompt,
#             n=1,
#             size=selected_size,
#             response_format="b64_json",
#         )

#         # Display image

#         if response["data"]:
#             image_data = base64.b64decode(response["data"][0]["b64_json"])
#             st.image(image_data, use_column_width=True)

#             # Download button
#             b64_image = base64.b64encode(image_data).decode()
#             href = f'<a class="download-button" href="data:image/png;base64,{b64_image}" download="generated_image.png">Download</a>'
#             st.markdown(href, unsafe_allow_html=True)
#         else:
#             st.warning("No image generated.")
#     except Exception as e:
#         st.error(e)
#         print(e)

        
import base64
import streamlit as st
import openai
import sqlite3
import re

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Initialize SQLite database connection
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Create a table to store user data if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        email TEXT
    )
''')
conn.commit()

# Function to validate email format
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) and email.endswith("@gmail.com")

# Function to simulate user authentication
def authenticate(name, age, gender, email):
    if not name or not age or not gender or not email:
        return False

    if not is_valid_email(email):
        return False

    # Save user data in session state
    st.session_state.user = {"name": name, "age": age, "gender": gender, "email": email}
    return True

# Function to check if the user is authenticated
def is_authenticated():
    return st.session_state.get("authenticated", False)

# Set your OpenAI API key
openai.api_key = "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"

# Streamlit configuration
st.set_page_config(
    page_title="Text to Image Generator",
    page_icon="🎨",
    layout="wide",
)

# Custom CSS styles
st.markdown(
    """
    <style>
    .download-button {
        background-color: #221e5b;
        color: #ffffff;
        padding: 10px 15px;
        border: 25px;
        border-radius: 5px;
        cursor: pointer;
        text-decoration: none;
        font-weight: bold;
    }

    .download-button:hover {
        background-color: #ff5588;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Text to Image Generator")

# User information in the sidebar
name = st.sidebar.text_input("Name")
age = st.sidebar.number_input("Age", min_value=0, max_value=150, value=30)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
email = st.sidebar.text_input("Email")

# Login button
login_button = st.sidebar.button("Login")

# Authentication logic
if login_button:
    if authenticate(name, age, gender, email):
        st.session_state.authenticated = True
    else:
        st.warning("Invalid or incomplete information. Please check your input and try again.")

# Check if the user is authenticated before showing the generator
if is_authenticated():
    # Generator section
    # Prompt input
    prompt = st.text_area("Enter the prompt : 👇", height=5)

    # Size selection
    size_options = ["256x256", "512x512", "1024x1024"]
    selected_size = st.selectbox("Select image size:", size_options)

    if st.button("Generate🪄"):
        # Generate image
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size=selected_size,
                response_format="b64_json",
            )

            # Display image
            if response["data"]:
                image_data = base64.b64decode(response["data"][0]["b64_json"])
                st.image(image_data, use_column_width=True)

                # Download button
                b64_image = base64.b64encode(image_data).decode()
                href = f'<a class="download-button" href="data:image/png;base64,{b64_image}" download="generated_image.png">Download</a>'
                st.markdown(href, unsafe_allow_html=True)

                cursor.execute('''
                     INSERT INTO user (name, age, gender, email)
                     VALUES (?, ?, ?, ?)
                    ''', (st.session_state.user["name"], st.session_state.user["age"], st.session_state.user["gender"], st.session_state.user["email"]))

            else:
                st.warning("No image generated.")
        except Exception as e:
            st.error(e)
            print(e)
else:
    st.info("Please log in to access the Text to Image Generator.")
