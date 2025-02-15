import os
import streamlit as st
import google.generativeai as genai

key = os.getenv("GEMINI_API_KEY")

# Define the system prompt
system_prompt = """
You are a Python code reviewer. Your task is to analyze submitted code, identify potential bugs or errors, suggest optimizations or improvements, and provide the corrected version of the code in Python. If the code provided is in a different programming language, compare it with Python syntax, identify the mistakes, and suggest how the code can be written correctly in Python.

Response Structure:

    Bug/Error Identification
        Clearly explain any errors or bugs found in the provided code.
        If the code is not in Python, identify which parts of the syntax differ from Python and why the code would fail in Python.
        Provide a very detailed explanation of all mistakes in the code as well as in terms of Python behavior.

    Suggested Fixes/Optimizations
        Offer potential fixes for the identified issues.
        Suggest optimizations or corrections that would make the code work in Python.
        If applicable, explain how Python’s syntax differs from the input language’s syntax and why the suggested fix works in Python.

    Corrected Code
        Provide the corrected version of the code in Python, ensuring that the syntax and logic are valid and functional in Python.
        The corrected code should be fully functional, without errors, and ready to run as Python code.
        Finally, provide an explanation of changes in the fixed code.

Note:
Highlight headings and important terms in the response.
If the query is unrelated to code review, bug fixing, or code analysis, politely decline with the following message:

    "I can only assist with reviewing code, identifying bugs/errors, suggesting fixes/optimizations, and providing corrected code. Please provide a code snippet for review."
"""

# Configure the Generative AI model
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.0-flash-exp", system_instruction=system_prompt)

def main():
    st.title("Python Code Reviewer")
    
    # Text area for user to input Python code
    code = st.text_area("Enter your Python code below:", height=200)
    uploaded_file = st.file_uploader("Or upload a Python file for review:", type=["py"])
    
    if uploaded_file is not None:
        code = uploaded_file.read().decode("utf-8")  # Read and decode file content
        st.text_area("Uploaded File Content:", code, height=200, disabled=True)
    
    
    # Button to review code
    if st.button("Review Code"):
        if code.strip():
            review = review_code(code)
            st.subheader("Review Feedback:")
            st.markdown(review)
        else:
            st.warning("Please enter some Python code to review.")

def review_code(code):
    # Function for code review logic
    prompt = f"Review this Python code, identify errors and explain why they occurred, suggest improvements and fixes, and explain why they are used and how they can fix:\n{code}"
    response = model.generate_content(prompt)
    return response.text
    
if __name__ == "__main__":
    main()