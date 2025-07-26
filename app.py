import streamlit as st 
import streamlit_authenticator as stauth

# --- LOGIN SETUP ---

# Hashed password for abc123
hashed_passwords = [
    'pbkdf2:sha256:600000$2VoZGbLpZYIBGFZf$354a6bcb5a0bc71d2c8d55286d221ca8ed8e63f3e1b196c27cc8db9f5bdf9a49'
]

credentials = {
    "usernames": {
        "demo_user": {
            "name": "Demo User",
            "password": hashed_passwords[0]
        }
    }
}

authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="realestate_email_tool",
    key="abc123",
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", "main")

# 🚫 Step 1: Check for banned users
banned_users = ["badguy@email.com", "testuser"]
if username in banned_users:
    st.error("Access denied. Please contact support.")
    st.stop()

# ✅ Step 2: Handle login status
if authentication_status is False:
    st.error("Username or password is incorrect.")
elif authentication_status is None:
    st.warning("Please enter your username and password.")
elif authentication_status:
    authenticator.logout("Logout")
    st.sidebar.success(f"Welcome, {name}! 👋")

    # ✅ Your tool starts here

    # 🧠 Your real estate email generator starts below this line
import openai

# Set up OpenAI client (new format for v1.0+)
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
