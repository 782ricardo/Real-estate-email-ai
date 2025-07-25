import streamlit as st 
import streamlit_authenticator as stauth

# --- LOGIN SETUP ---

# Hashed password for 'abc123'
hashed_passwords = stauth.Hasher(['abc123']).generate()

credentials = {
    "usernames": {
        "demo_user": {
            "name": "Demo User",
            "password": hashed_passwords[0]
        }
    }
}

authenticator = stauth.Authenticate(credentials, "my_app", "abcdef", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username or password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.write(f"Welcome, {name} 👋")

    # 🧠 Your real estate email generator starts below this line
import openai

# Set up OpenAI client (new format for v1.0+)
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # use GPT-4 if your account has access
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        email = response.choices[0].message.content
        st.subheader("Generated Email:")
        st.write(email)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
