import streamlit as st
from utils.styles import apply_custom_styles

st.set_page_config(
    page_title="Knowledgebase DE | Data Engineering",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global styles
apply_custom_styles()

st.title("Data Engineering Knowledgebase")
st.markdown("""
### Welcome to your study companion! 
Master the concepts for data engineering interviews.

#### 🚀 Start Here
Select a module from the sidebar to begin:
- **📊 Dashboard**: Track your progress and streaks.
- **🧠 Quiz Mode**: Practice with realistic exam questions.
- **📚 Resources**: Cheat sheets and flashcards.

---
""")

# Quick Stats or "Continue where you left off" could go here
# For now, just a placeholder
st.info("💡 Tip: Consistency is key. Try to do at least 5 questions a day!")
