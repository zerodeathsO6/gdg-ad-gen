import streamlit as st
import google.generativeai as genai
import dotenv

config = dotenv.dotenv_values(".env")

genai.configure(api_key=config["API_KEY"])

# Used AI to write the prompt to give to the AI which then uses AI and generates
GUWAHATI_MARKETING_EXPERT_TEXT = (
    "You are a brilliant, highly sarcastic, and witty marketing executive living in Guwahati, Assam. "
    "Your job is to create a hyper-local social media advertisement for the business name provided by the user.\n\n"
    "CRITICAL RULES:\n"
    "1. You must heavily use local context, inside jokes, and landmarks (e.g., traffic at Ganeshguri or Paltan Bazar, "
    "hanging out at Dighalipukhuri or GS Road, typical local college stereotypes, vs. Fancy Bazar bargain hunters).\n"
    "2. The advertisement must match the specific tone requested by the user.\n"
    "3. Keep the output punchy, under 120 words, structured for a social media post, and use emojis naturally.\n"
    "4. Blend English with standard local phrasing or slang seamlessly if it elevates the humor."
)

GUWAHATI_MARKETING_EXPERT_IMAGE = (
    "You are a brilliant, highly sarcastic, and witty marketing executive living in Guwahati, Assam. "
    "Your job is to create a hyper-local social media advertisement for the business name provided by the user.\n\n"
    "CRITICAL RULES:\n"
    "1. You must use local context, inside jokes, and landmarks (e.g., traffic at Ganeshguri or Paltan Bazar, "
    "hanging out at Dighalipukhuri or GS Road, typical local college stereotypes, vs. Fancy Bazar bargain hunters).\n"
    "2. The advertisement must match the specific tone requested by the user.\n"
    "3. Keep the output vibrant and related to the actual context of the user prompt, what the user provides as the brand name\n"
    "4. Add in some local humour in a corner with an example brand punchline related to the brand provided."
)

text_model = genai.GenerativeModel(
    system_instruction=GUWAHATI_MARKETING_EXPERT_TEXT,
    model_name="gemini-3.1-flash-lite"
)

# I dont have a paid tier goddamit
# image_model = genai.GenerativeModel(
#     model_name="gemini-2.5-flash-image",
#     system_instruction=GUWAHATI_MARKETING_EXPERT_IMAGE
# )

st.set_page_config(page_title="Generate a witty image based on a custom business in Guwahati", page_icon="💡", layout="centered")

st.title("💡 The 'Brand Hijack' Agency")
st.write("Generate hilarious, hyper-local ads for local brands.")

brand_name = st.text_input("What local brand or shop are we hijacking?", placeholder="e.g., JB's, Central Mall, a local corner momo stall...")

tone = st.selectbox(
    "Choose the advertising strategy:",
    ["Pure Sarcasm / Roasting", "Overly Dramatic / Cinematic", "Chaotic Local Slang", "Wholesome Nostalgia"]
)

if st.button("Generate Campaign 🚀"):
    if not brand_name:
        st.warning("Please enter a brand name first!")
    else:
        with st.spinner("Brewing a strong cup of Assam tea and writing copy..."):
            try:
                # Structure the final user prompt
                user_prompt = f"Write a social media ad for the brand: '{brand_name}' using the following strategy: {tone}."
                
                # Call the API
                response = text_model.generate_content(user_prompt).text
                
                st.subheader("📋 Your Generated Campaign:")
                st.info(response)


                # Need the paid tier goddamit
                # image_prompt= f"Make a social media ad for the brand: '{brand_name}' using the following strategy: {tone}"
                # img_res = image_model.generate_content(image_prompt)

                # for part in img_res.candidates[0].content.parts:
                #     if part.inline_data:
                #         st.image(part.inline_data.data, caption=f"AI Generated Ad Concept for {brand_name}", use_column_width=True)
            except Exception as e:
                st.error(f"Something went sideways with the API: {e}")