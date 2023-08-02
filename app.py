import streamlit as st
import pandas as pd
import openai
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

img = Image.open('str.png')
st.set_page_config(page_title='Remarks Co-Pilot', page_icon=img)


# Set your OpenAI GPT-3 API key
gpt3_api_key = os.getenv("GPT3_API_KEY")

# Function to generate student remarks using GPT-3


def generate_remarks(student_name, gender, adjectives):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Assume the role of a teacher. Use '{student_name}' as student name, use '{gender}' as the gender pronoun and write qualitative remarks about the student for the student's report card in third person by using the following descriptors: {adjectives}.",
        max_tokens=100,
    )
    return response.choices[0].text


def main():
    st.image(img, width=100)
    st.title("Remarks Co-Pilot")

    # File upload
    st.write("Upload a CSV file with columns: 'student_name', 'gender', 'adjectives'")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)

        # Check if the required columns are present
        required_columns = ["student_name", "gender", "adjectives"]
        if not all(col in df.columns for col in required_columns):
            st.error(
                "The CSV file should contain 'student_name', 'gender', and 'adjectives' columns.")
            return

        # Generate student remarks using GPT-3 and add them to the DataFrame
        remarks = []
        for _, row in df.iterrows():
            generated_remarks = generate_remarks(
                row["student_name"], row["gender"], row["adjectives"])
            print(
                f"Generated remarks for {row['student_name']}: {generated_remarks}")
            remarks.append(generated_remarks)
            print(remarks)

        # Update the DataFrame with the 'student_remarks' column
        print("DataFrame Columns:", df.columns)
        df["student_remarks"] = remarks
        print(df["student_remarks"][0])

        # Show the DataFrame with the generated remarks
        st.write("DataFrame with Remarks:")
        st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

        # Download the new CSV file
        st.write("Click below to download the new CSV file:")
        st.download_button(label="Download CSV", data=df.to_csv(
            index=False), file_name="student_report_card_with_remarks.csv", mime="text/csv")


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """


st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.image(img, width=100)
        st.title("Remarks Co-Pilot")
        st.write("Beta access for Hwa Chong Users Demo")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return main()


if check_password():
    st.write("Here goes your normal Streamlit app...")
    st.button("Click me")


# add basic font styling
streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Roboto', sans-serif;
			}
			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)
