import streamlit as st # pyright: ignore[reportMissingImports]
import google.generativeai as genai # type: ignore
import json
import re

# Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Page config
st.set_page_config(page_title="AI Copy Generator", layout="wide")

# Title
st.title("📚 AI Website Copy Generator (Coaching Institute)")
st.markdown("Create high-converting, SEO-optimized website copy 🚀")
st.markdown("---")

# Sidebar Inputs
st.sidebar.header("📌 Institute Details")

name = st.sidebar.text_input("Institute Name")
location = st.sidebar.text_input("Location")
courses = st.sidebar.text_area("Courses Offered")
audience = st.sidebar.text_input("Target Audience")
usp = st.sidebar.text_area("Unique Selling Points")

tone = st.sidebar.selectbox("Tone", ["Professional", "Friendly", "Motivational"])
goal = st.sidebar.selectbox("Goal", ["Enrollments", "Leads", "Calls"])

# SEO Keywords
keywords = st.sidebar.text_area(
    "SEO Keywords (comma separated)",
    placeholder="e.g. best coaching institute in Noida, JEE coaching near me"
)

# Generate Button
if st.sidebar.button("✨ Generate Copy"):

    if not name or not courses:
        st.warning("⚠️ Please fill required fields")
    else:
        with st.spinner("Generating premium copy... 🚀"):

            prompt = f"""
            You are an expert conversion copywriter + SEO strategist.

            Generate HIGH-CONVERTING website copy for a coaching institute.

            Follow rules:
            - Focus on student pain points & results
            - Use simple persuasive language
            - Avoid generic phrases
            - Naturally include SEO keywords: {keywords}
            - Do NOT overstuff keywords

            Return STRICT JSON only.
            No explanation, no markdown, no extra text.

            Format:
            {{
              "hero": {{
                "headline": "",
                "subheadline": "",
                "cta": ""
              }},
              "about": "",
              "courses": "",
              "why_choose_us": ["", "", "", "", ""],
              "testimonials": [
                {{"name": "", "review": ""}},
                {{"name": "", "review": ""}},
                {{"name": "", "review": ""}}
              ],
              "cta": ["", "", ""]
            }}

            Business Info:
            Name: {name}
            Location: {location}
            Courses: {courses}
            Audience: {audience}
            USP: {usp}
            Tone: {tone}
            Goal: {goal}
            """

            # Use working model
            model = genai.GenerativeModel("gemini-2.5-flash")

            response = model.generate_content(prompt)
            raw_output = response.text

            # 🔥 FIXED JSON PARSING
            match = re.search(r"\{.*\}", raw_output, re.DOTALL)

            if match:
                json_text = match.group(0)
                try:
                    data = json.loads(json_text)
                except:
                    st.error("⚠️ JSON parsing failed. Showing raw output.")
                    st.code(raw_output)
                    st.stop()
            else:
                st.error("⚠️ No valid JSON found.")
                st.code(raw_output)
                st.stop()

        st.success("✅ Copy Generated Successfully!")

        # HERO
        st.markdown("## 🏠 Hero Section")
        st.markdown(f"### {data['hero']['headline']}")
        st.write(data['hero']['subheadline'])
        st.success(data['hero']['cta'])

        st.markdown("---")

        # ABOUT
        st.markdown("## 👤 About")
        st.info(data["about"])

        st.markdown("---")

        # COURSES
        st.markdown("## 📚 Courses")
        st.write(data["courses"])

        st.markdown("---")

        # WHY CHOOSE US
        st.markdown("## ⭐ Why Choose Us")
        for point in data["why_choose_us"]:
            st.markdown(f"✅ {point}")

        st.markdown("---")

        # TESTIMONIALS
        st.markdown("## 💬 Testimonials")
        for t in data["testimonials"]:
            st.markdown(f"**{t['name']}**: {t['review']}")

        st.markdown("---")

        # CTA
        st.markdown("## 📢 Call To Action")
        for c in data["cta"]:
            st.success(c)

        st.markdown("---")

        # DOWNLOAD BUTTON
        st.download_button(
            label="📥 Download Copy",
            data=json.dumps(data, indent=2),
            file_name="website_copy.json",
            mime="application/json"
        )