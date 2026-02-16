import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* General Theme Adjustments */
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #262730;
        }
        
        /* Headers */
        h1, h2, h3 {
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 600;
        }
        
        h1 {
            background: -webkit-linear-gradient(45deg, #4285F4, #34A853, #FBBC05, #EA4335);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Card-like containers using st.info/success/warning as base or custom divs */
        div.stButton > button {
            width: 100%;
            border-radius: 8px;
            font-weight: bold;
            border: none;
            background-color: #4285F4;
            color: white;
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #357abd;
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }
        
        /* Radio buttons for Quiz */
        .stRadio label {
            font-size: 1.1rem;
            padding: 10px;
            border-radius: 5px;
            transition: background 0.2s;
        }
        .stRadio label:hover {
            background-color: #ffffff10;
        }
        </style>
    """, unsafe_allow_html=True)
