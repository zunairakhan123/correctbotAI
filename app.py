import streamlit as st
import requests
import os

# Backend API URL
API_URL = "http://localhost:8000/ask"

# Get the path to the current directory (where app.py is located)
BASE_DIR = os.path.dirname(__file__)
LOG_FILE = os.path.join(BASE_DIR, "flagged_responses.log")

# Badge Icons
BADGE_ICONS = {
    "Curiosity": "🔍",
    "Kindness": "💖",
    "Exploration": "🌍",
    "Reflection": "💭",
    "Problem Solving": "🧩",
    "Bravery": "🦸‍♂️",
    "Resilience": "💪",
    "Empathy": "🤝",
    "Teamwork": "🤗",
    "Creativity": "🎨",
}

# Educational Prompts
EDUCATIONAL_MODES = {
    "🧮 Homework Helper": "Can you help me understand this math problem?",
    "🔬 STEM Explorer": "Tell me something interesting about space or science!",
    "📚 Story Generator": "Can you tell me a fun bedtime story about animals?"
}
TEEN_MODES = {
    "🎓 Study Pro Tips": "What are some smart ways to prepare for exams?",
    "🌐 Digital Life": "How can I stay safe and positive on social media?",
    "💬 Open Conversations": "How can I stay confident and true to myself with my friends and peers?",
    "🧩 Mind Hacks": "Can you give me tips to improve my memory?",
    "🛠 Life Skills": "What are some important life skills every teen should know?"
}
MATURE_MODES = {
    "🌱 Daily Growth": "What are fun ways to stay on track with my goals?",
    "💼 Career Ideas": "How can I explore new ways to succeed in my work?",
    "📈 Skill Booster": "What are some fun ways to learn and grow professionally?",
    "🤝 Great Connections": "What can I do to build strong and friendly relationships?"
}



# Streamlit page settings
st.set_page_config(page_title="SafeMentor AI ", page_icon="🤖", layout="centered")
page = st.sidebar.selectbox("Select Page", ["Chat with Mentor✨", "Parent Review Panel📙"])

if page == "Chat with Mentor✨":
    st.markdown("""
        <h1 style='text-align: center;'>🤖 SafeMentor AI </h1>
        <p style='text-align: center; font-size: 18px;'>
            Ask a fun, creative, or kind question—and earn badges while you learn! 🌟
        </p>
    """, unsafe_allow_html=True)

    role = st.radio("👤 Select your role:", ["child", "teen", "mature"], horizontal=True)

    default_text = ""
    if role == "child":
        st.markdown("### 🌟 Explore Fun Learning Ideas!")

        mode_labels = ["None"] + [f"{emoji} {mode}" for emoji, mode in [item.split(" ", 1) for item in EDUCATIONAL_MODES.keys()]]
        mode_mapping = dict(zip(mode_labels[1:], EDUCATIONAL_MODES.keys()))  # maps back to original

        selected_label = st.selectbox("Choose a mode:", mode_labels)

        if selected_label != "None":
            selected_mode_key = mode_mapping.get(selected_label, "")
            default_text = EDUCATIONAL_MODES[selected_mode_key]
            st.info(f"💡 **Prompt Idea:** {default_text}")

    elif role == "teen":
        st.markdown("### 🔥 Explore Cool Topics Just for You!")

        # Define modes for teens
        teen_mode_labels = ["None"] + [f"{emoji} {mode}" for emoji, mode in [item.split(" ", 1) for item in TEEN_MODES.keys()]]
        teen_mode_mapping = dict(zip(teen_mode_labels[1:], TEEN_MODES.keys()))  # maps back to original

        selected_label_teen = st.selectbox("Choose a mode:", teen_mode_labels)

        if selected_label_teen != "None":
            selected_mode_key_teen = teen_mode_mapping.get(selected_label_teen, "")
            default_text = TEEN_MODES[selected_mode_key_teen]
            st.info(f"💡 **Prompt Idea:** {default_text}")
    
    elif role == "mature":
        st.markdown("### 🎯 Empower Your Future with Positive Choices!")
        
        mode_labels = ["None"] + [f"{emoji} {mode}" for emoji, mode in [item.split(" ", 1) for item in MATURE_MODES.keys()]]
        mode_mapping = dict(zip(mode_labels[1:], MATURE_MODES.keys()))  # maps back to original
        
        selected_label = st.selectbox("Choose a mode:", mode_labels)
        
        if selected_label != "None":
            selected_mode_key = mode_mapping.get(selected_label, "")
            default_text = MATURE_MODES[selected_mode_key]
            st.info(f"💡 **Prompt Idea:** {default_text}")

    user_input = st.text_area("💬 What would you like to ask your mentor?", value=default_text, height=120)

    if "last_input" not in st.session_state:
        st.session_state.last_input = ""
    if "last_response" not in st.session_state:
        st.session_state.last_response = ""
    if "last_role" not in st.session_state:
        st.session_state.last_role = ""
    if "auto_flagged" not in st.session_state:
        st.session_state.auto_flagged = False

    if st.button("🧠 Ask Mentor"):
        if not user_input.strip():
            st.warning("Please type a question to continue.")
        else:
            with st.spinner("Thinking positive thoughts... 🤔✨"):
                try:
                    response = requests.post(API_URL, json={"user_input": user_input, "role": role})
                    if response.status_code == 200:
                        result = response.json()
                        reply = result["reply"]

                        st.session_state.last_input = user_input
                        st.session_state.last_response = reply
                        st.session_state.last_role = role
                        st.session_state.auto_flagged = False

                        st.success("✨ Here's your mentor's response:")
                        st.markdown(
                            f"<div style='padding:10px; background-color:#f0f2f6; border-radius:10px; color: black;'>{reply}</div>",
                            unsafe_allow_html=True
                        )

                        if result["badge"]:
                            icon = BADGE_ICONS.get(result["badge"], "🏅")
                            badge_name = result["badge"]

                            st.markdown(f"""
                                <div style="
                                    background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
                                    border-radius: 15px;
                                    padding: 20px;
                                    margin-top: 20px;
                                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                    text-align: center;
                                ">
                                    <h3 style='margin-bottom: 10px;'>{icon} <span style='color:#2c3e50;'>{badge_name}</span> Badge Earned!</h3>
                                    <p style='font-size: 16px; color: #34495e;'>Awesome! You demonstrated {badge_name.lower()} in your question or thinking. Keep it up! 💡</p>
                                </div>
                        

                            """, unsafe_allow_html=True)
                    else:
                        error_msg = response.json().get("detail", "Something went wrong.")
                        st.error(f"🚫 {error_msg}")

                        if error_msg in ["That question may not be safe to ask.", "Sorry, the response could not be shown."]:
                            with open(LOG_FILE, "a", encoding="utf-8") as f:
                                f.write(
                                    f"Role: {role}\n"
                                    f"Input: {user_input}\n"
                                    f"Response:\n{error_msg}\n"
                                    f"---END-FLAG---\n"
                                )
                            st.session_state.auto_flagged = True
                            st.warning("⚠️ The response has been automatically flagged for review.")
                except requests.exceptions.RequestException:
                    st.error("⚠️ Failed to connect to the mentor API. Please try again later.")

    if st.session_state.last_response and not st.session_state.auto_flagged:
        if st.button("🚩 Flag this response"):
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(
                    f"Role: {st.session_state.last_role}\n"
                    f"Input: {st.session_state.last_input}\n"
                    f"Response:\n{st.session_state.last_response}\n"
                    f"---END-FLAG---\n"
                )
            st.warning("⚠️ The response has been flagged for review. Thank you for your feedback.")

elif page == "Parent Review Panel📙":
    st.title("👀 Parent Review Panel")
    st.markdown("Review all flagged responses submitted by users.")

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = f.read().strip().split("---END-FLAG---\n")

        logs = [log.strip() for log in logs if log.strip()]

        if logs:
            updated_logs = []
            for i, entry in enumerate(logs):
                if entry:
                    with st.expander(f"🚩 Flag #{i + 1}", expanded=False):
                        lines = entry.strip().split("\n")
                        for line in lines:
                            st.markdown(f"<div style='color:white;'>{line}</div>", unsafe_allow_html=True)

                        if st.button(f"🗑️ Delete This Flag", key=f"delete_flag_{i}"):
                            continue
                        else:
                            updated_logs.append(entry)

            with open(LOG_FILE, "w", encoding="utf-8") as f:
                for flag in updated_logs:
                    f.write(flag + "\n---END-FLAG---\n")

            if st.button("🧹 Clear All Flags"):
                open(LOG_FILE, "w", encoding="utf-8").close()
                st.success("All flagged responses cleared.")
                st.rerun()
        else:
            st.info("✅ No flagged responses yet.")
    else:
        st.info("✅ No flagged responses found.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px;'>Made with ❤️ for safe and positive learning experiences.</p>", unsafe_allow_html=True)