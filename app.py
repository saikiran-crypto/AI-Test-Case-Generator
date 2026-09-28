import streamlit as st
import pandas as pd
import os
import json
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
client = genai.Client(api_key=api_key)

# Streamlit page settings
st.set_page_config(
    page_title="AI Test Case Generator",
    page_icon="🧪",
    layout="wide"
)

# Title
st.title("🧪 AI Test Case Generator")

st.write(
    "Generate software test cases automatically "
    "from a software requirement using Artificial Intelligence."
)

# Requirement input
st.subheader("Enter Software Requirement")

requirement = st.text_area(
    "Software Requirement",
    placeholder="Example: User should be able to login using email and password."
)

# Generate button
if st.button("Generate Test Cases"):

    if requirement.strip() == "":
        st.warning("Please enter a software requirement.")

    else:

        # AI prompt
        prompt = f"""
You are a software testing expert.

Analyze the following software requirement and generate 8 useful test cases.

Software Requirement:
{requirement}

For each test case provide:

1. Test Case ID
2. Test Scenario
3. Test Type - Positive, Negative, or Boundary
4. Input
5. Expected Result
6. Priority - High, Medium, or Low

Include a mixture of positive, negative, and boundary/validation test cases when appropriate.

Keep the test cases clear and practical.

Return ONLY valid JSON in exactly this format:

[
  {{
    "Test Case ID": "TC01",
    "Test Scenario": "Description of the test scenario",
    "Test Type": "Positive",
    "Input": "Input details",
    "Expected Result": "Expected result",
    "Priority": "High"
  }}
]
"""

        try:

            # Generate test cases using Gemini
            with st.spinner("🤖 AI is generating test cases..."):

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )

            result = response.text

            # Remove markdown code blocks if AI adds them
            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

            # Convert AI response to Python
            test_cases = json.loads(result)

            # Convert to DataFrame
            df = pd.DataFrame(test_cases)

            # Success message
            st.success("✅ Test cases generated successfully!")

            # Display results
            st.subheader("Generated Test Cases")

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # Download CSV
            csv = df.to_csv(index=False)

            st.download_button(
                label="📥 Download Test Cases as CSV",
                data=csv,
                file_name="generated_test_cases.csv",
                mime="text/csv"
            )

        except Exception as e:

            st.error("❌ Something went wrong.")
            st.write(e)