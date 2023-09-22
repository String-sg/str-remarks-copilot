import streamlit as st
import pandas as pd
import openai
from PIL import Image
import webbrowser

img = Image.open('str.png')
st.set_page_config(page_title='Remarks Co-Pilot', page_icon=img)
print(st.secrets.get("global", {}).get("disable_password_check"))


def get_credentials():
    value = st.text_input(
        "Enter your OpenAI API Key or Password", type="password", key="api_key_input")
    if value == st.secrets["password"]:
        return st.secrets["GPT_API_KEY"], True
    elif validate_api_key(value):
        return value, True
    else:
        return None, False


def validate_api_key(value):
    try:
        # Set the API key for this specific request
        openai.api_key = value
        # Make a test call to the OpenAI API to the "davinci" model
        openai.Completion.create(
            engine="text-davinci-003",
            prompt="Test",
            max_tokens=5
        )
        return True  # If the call was successful, the API key is valid
    except openai.error.AuthenticationError:
        # If there's an authentication error, the API key is not valid
        return False
    except Exception as e:
        # You may also handle other exceptions if needed
        print("An unexpected error occurred. The API key seems invalid", str(e))
        return False


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
    if not check_password():
        st.warning("Password validation failed.")
        return

    api_key, is_valid = get_credentials()  # Call this once

    if api_key is None or not is_valid:
        st.warning("Please enter a valid API key or password to proceed.")
        return

    openai.api_key = api_key
    # Prompt templates
    prompt_templates = {
        "For AC Vetting": "Write a single paragraph of 80 words commenting on a student for their termly report book which would be shared with them and their parents. Use the[as the name; male as the gender pronoun and hardworking to describe the student. Write in 3rd person. Adopt a formal but positive tone when expressing comments. If specific examples are lacking, include a question to prompt the end user to write more specific remarks. If the following string is found in the input above, use the exact substitutions: instead of using 'pupil', use 'student'. Instead of 'tables', use 'desks'. Instead of 'well-mannered' use 'well-behaved'. Instead of 'ICT Captain' use 'ICT Champion'. Instead of 'co-operative' use 'cooperative'. Instead of 'for displaying Loyalty', use 'for displaying loyalty'. Instead of 'sweet disposition/ sweet-natured', use 'gentle disposition/ good-natured'. Instead of 'best of his abilities', use 'best of his ability'. Instead of 'as the English Captain', use 'as the English Language Captain'. If direct and concrete steps to take for student in terms of academic and/or character and/or social emotional' does not exist in the input, raise it as a question in the output 'No direct and concrete steps for the student to improve'. Use positive adjectives to encourage student in pursuing passion/goals and recognise effort and improvement. When there is a change in the character traits or moving to another point, we should use {student_name} again.",
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
    st.text("")
    st.write(
        "Upload a CSV file with columns: 'student_name', 'gender', 'adjectives'. Need a template?")
    url = 'https://go.gov.sg/remarks-dummy-student'

    if st.button('Download template'):
        webbrowser.open_new_tab(url)
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
    # Skip password check if developing on local
    if st.secrets.get("global", {}).get("disable_password_check"):
        return True

    # Check if the password has been entered in the session state
    if "password" in st.session_state:
        # Verify the entered password with the one stored in st.secrets
        if st.session_state["password"] == st.secrets["password"]:
            return True
        else:
            st.error("😕 Password incorrect")
            return False


def password_entered():
    """Checks whether a password entered by the user is correct."""
    if "password" in st.session_state:
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False
    else:
        st.session_state["password"] = st.text_input(
            "Password", type="password", key="password_input")

    if "password_correct" not in st.session_state or "password" not in st.session_state:
        # First run, show input for password.
        st.image(img, width=100)
        st.title("Remarks Co-Pilot")
        st.write("Beta access - limited demo as proof of concept")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password_input")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password_input")
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():
    main()

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
