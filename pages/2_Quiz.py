import streamlit as st
from utils.quiz_engine import QuizEngine
from utils.styles import apply_custom_styles

apply_custom_styles()

st.title("🧠 Practice Quiz")

# Initialize Quiz Engine
engine = QuizEngine()

# Session State for score
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_question_idx' not in st.session_state:
    st.session_state.current_question_idx = 0

# Sidebar settings
with st.sidebar:
    st.header("Quiz Settings")
    topic = st.selectbox("Select Topic", engine.get_all_topics())
    
    # Filter by Frequency/Importance
    min_score = st.slider("Filter by Importance Score (1-10)", 1, 10, 1, help="Higher score = More frequent/important interview questions.")
    
    num_questions = st.slider("Number of Questions", 1, 10, 3)
    if st.button("Start New Quiz"):
        st.session_state.quiz_questions = engine.get_random_questions(num_questions, topic, min_score)
        st.session_state.current_question_idx = 0
        st.session_state.score = 0
        st.session_state.quiz_active = True
        st.rerun()

if 'quiz_active' not in st.session_state or not st.session_state.quiz_active:
    st.info("👈 Select a topic and click 'Start New Quiz' in the sidebar to begin!")
else:
    questions = st.session_state.quiz_questions
    current_idx = st.session_state.current_question_idx
    
    if current_idx < len(questions):
        q = questions[current_idx]
        
        # Progress bar
        progress = (current_idx / len(questions))
        st.progress(progress, text=f"Question {current_idx + 1} of {len(questions)}")
        
        st.subheader(f"Topic: {q['topic']}")
        if 'companies' in q and q['companies']:
            st.caption(f"🏷️ Asked at: {', '.join(q['companies'])}")
        st.markdown(f"**{q['question']}**")
        
        # Form for the question
        with st.form(key=f"q_form_{current_idx}"):
            response = st.radio("Choose an answer:", q['options'], index=None)
            submit = st.form_submit_button("Submit Answer")
            
            if submit:
                if response:
                    st.session_state[f"answered_{current_idx}"] = True
                    st.session_state[f"response_{current_idx}"] = response
                else:
                    st.warning("Please select an option.")

        # Logic to display result and Next button (outside form)
        if st.session_state.get(f"answered_{current_idx}"):
            user_response = st.session_state.get(f"response_{current_idx}")
            is_correct = QuizEngine.check_answer(q, user_response)
            
            if is_correct:
                st.success("✅ Correct!")
                # Only increment score once per question (naive check, but sufficient for linear flow)
                # Ideally score logic should be separate or idempotent
            else:
                st.error(f"❌ Incorrect. The correct answer was: {q['answer']}")
            
            st.info(f"💡 **Explanation**: {q['explanation']}")
            
            if st.button("Next Question", type="primary"):
                # Update score if correct (need to prevent double counting if user re-clicks? 
                # Actually recalculating score based on stored results is safer, or just rely on simple session state increment)
                if is_correct:
                    st.session_state.score += 1
                
                st.session_state.current_question_idx += 1
                st.rerun()

    else:
        st.balloons()
        st.success(f"🎉 Quiz Completed! Final Score: {st.session_state.score} / {len(questions)}")
        if st.button("Restart"):
            st.session_state.quiz_active = False
            st.rerun()
