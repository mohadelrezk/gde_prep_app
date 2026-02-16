import streamlit as st
from utils.styles import apply_custom_styles

apply_custom_styles()

st.title("📚 Study Resources")

tab1, tab2 = st.tabs(["Cheat Sheets", "Flashcards"])

with tab1:
    st.subheader("Google Cloud Data Decision Cheatsheet")
    
    col1, col2 = st.columns(2)
    with col1:
        st.error("Wait! Do you need SQL?")
        st.markdown("- **Yes** -> **BigQuery** (Analytics), **Cloud Spanner** (Global Transactional), **Cloud SQL** (Regional Transactional)")
        st.markdown("- **No** -> **Bigtable** (High throughput/IoT), **Firestore** (Mobile/Web/Hierarchical)")
    
    with col2:
        st.info("Ingestion Needs")
        st.markdown("- **Pub/Sub**: Global, Async messaging.")
        st.markdown("- **Dataflow**: Transformation, Streaming/Batch.")
        st.markdown("- **Dataproc**: Lift & Shift Hadoop/Spark.")

    st.markdown("---")
    st.markdown("### Common Limits")
    st.code("""
    # Pub/Sub
    Message Size: 10MB
    Retention: 7 Days
    
    # Dataflow
    Streaming Engine: Auto-scaling
    """, language="yaml")

with tab2:
    st.subheader("Flashcards")
    st.warning("Flashcard feature coming soon! (Check 'Quiz' tab for practice)")
