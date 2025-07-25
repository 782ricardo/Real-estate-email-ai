import streamlit as st
import openai

# Set up API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Real Estate Email Generator")

# Input fields
property_type = st.text_input("Property Type", "Condo")
location = st.text_input("Location", "Denver, CO")
price = st.text_input("Price (optional)", "$500,000")
features = st.text_area("Key Features", "3 bed, 2 bath, near downtown")
purpose = st.selectbox("Email Purpose", ["New Listing", "Follow-Up", "Open House", "Thank You", "Custom"])
tone = st.selectbox("Tone", ["Professional", "Friendly", "Luxury", "Casual"])

# Generate button
if st.button("Generate Email"):
    prompt = f"""Write a {tone.lower()} real estate email for the following:
- Type: {property_type}
- Location: {location}
- Price: {price}
- Features: {features}
- Purpose: {purpose}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # fallback model if GPT-4 isn't available
            messages=[{"role": "user", "content": prompt}]
        )
        email = response.choices[0].message.content
        st.subheader("Generated Email:")
        st.write(email)

    except openai.error.InvalidRequestError as e:
        st.error("There was a problem with your OpenAI request.")
    except Exception as e:
        st.error(f"Something went wrong: {e}")
