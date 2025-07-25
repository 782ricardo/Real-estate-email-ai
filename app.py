import streamlit as st
import openai

st.title("Real Estate Email Generator")

openai.api_key = st.secrets["OPENAI_API_KEY"]

property_type = st.text_input("Property Type", "Condo")
location = st.text_input("Location", "Denver, CO")
price = st.text_input("Price (optional)", "$500,000")
features = st.text_area("Key Features", "3 bed, 2 bath, near downtown")
purpose = st.selectbox("Email Purpose", ["New Listing", "Follow-Up", "Open House", "Thank You", "Custom"])
tone = st.selectbox("Tone", ["Professional", "Friendly", "Luxury", "Casual"])

if st.button("Generate Email"):
    prompt = f"""Write a {tone.lower()} real estate email for the following:
- Type: {property_type}
- Location: {location}
- Price: {price}
- Features: {features}
- Purpose: {purpose}
"""

    client = openai.OpenAI()  # This is the NEW way to call the API

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    st.subheader("Generated Email:")
    st.write(response.choices[0].message.content)
