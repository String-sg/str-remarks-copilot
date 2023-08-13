import streamlit as st
import pandas as pd
import openai
from PIL import Image


img = Image.open('str.png')
st.set_page_config(page_title='Remarks Co-Pilot', page_icon=img)


# Set your OpenAI GPT-3 API key
openai.api_key = st.secrets["GPT_API_KEY"]

# Function to generate student remarks using GPT-3


def generate_remarks(prompt_template_edited, student_name, gender, adjectives):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt_template_edited.format(
                student_name=student_name, gender=gender, adjectives=adjectives)}
        ],
        max_tokens=200,
        temperature=0
    )
    return completion.choices[0].message


def main():
    st.image(img, width=100)
    st.title("Remarks Co-Pilot")

    # Prompt templates
    prompt_templates = {
        "For AC Demo": "Assume the role of a teacher. Use '{student_name}' as student name, use '{gender}' as the gender pronoun and write qualitative remarks of no more than 80 words about the student for the student's report card in third person by using the following descriptors: {adjectives}. Remarks given should be speciifc, objective, acitonable and positive. Link to character traits: integrity, love and loyalty and learning dispositions: curiosity, collaboration and excellence.",
        "For HCI Demo": "Assume the role of a teacher. Use '{student_name}' as student name, use '{gender}' as the gender pronoun and write a brief summary of no more than 80 words the student's performance in class by using the following descriptors: {adjectives}.",
        "For NJC Demo": "Assume the role of a teacher. Use '{student_name}' as student name, use '{gender}' as the gender pronoun and write a paragraph of no more than 80 words  about the student's strengths and areas for improvement by using the following descriptors: {adjectives}."
    }

    # Prompt template selection
    prompt_template = st.selectbox(
        "Select a prompt template", list(prompt_templates.keys()))

    # Prompt template editing
    prompt_template_edited = st.text_area(
        "Edit the prompt template", value=prompt_templates[prompt_template])

    # Read the uploaded CSV file
    st.write("Upload a CSV file with columns: 'student_name', 'gender', 'adjectives'")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file:
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
                prompt_template_edited, row["student_name"], row["gender"], row["adjectives"])
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
        st.write("Beta access - limited demo as proof of concept")
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
