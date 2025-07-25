prompt = f"""Write a {tone.lower()} real estate email for the following:
- Type: {property_type}
- Location: {location}
- Price: {price}
- Features: {features}
- Purpose: {purpose}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # safer fallback
            messages=[{"role": "user", "content": prompt}]
        )
        email = response.choices[0].message.content
        st.subheader("Generated Email:")
        st.write(email)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
