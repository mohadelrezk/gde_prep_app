import streamlit as st
from utils.styles import apply_custom_styles

apply_custom_styles()

st.title("📚 Study Resources")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Cheat Sheets",
    "Standard Resources",
    "Books & Deep Dives",
    "Design Patterns",
    "Video & Courses"
])

with tab1:
    st.subheader("Google Cloud Data Decision Cheatsheet")
    
    col1, col2 = st.columns(2)
    with col1:
        st.error("Wait! Do you need SQL?")
        st.markdown("- **Yes** → **BigQuery** (Analytics), **Cloud Spanner** (Global Transactional), **Cloud SQL** (Regional Transactional)")
        st.markdown("- **No** → **Bigtable** (High throughput/IoT), **Firestore** (Mobile/Web/Hierarchical)")
    
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

    st.markdown("---")
    st.subheader("Architecture Patterns Quick Reference")
    
    cols = st.columns(2)
    
    with cols[0]:
        st.markdown("**Lambda Architecture**")
        st.markdown("""
        - **Batch Layer**: Process historical data
        - **Speed Layer**: Real-time stream processing
        - **Serving Layer**: Merge batch + real-time views
        - *Use Case*: Need both accuracy and speed
        """)
        
        st.markdown("**Idempotency & Deduplication**")
        st.markdown("""
        - Handle "at-least-once" delivery
        - Track unique message IDs
        - Critical for payment/financial pipelines
        - Prevent duplicate records in warehouse
        """)
        
        st.markdown("**Replication Patterns**")
        st.markdown("""
        - **Leader-Follower**: Primary writes, replicas read
        - **Multi-leader**: Multiple write nodes
        - **Leaderless**: All nodes equal
        - Trade-offs: consistency vs availability
        """)
    
    with cols[1]:
        st.markdown("**Kappa Architecture**")
        st.markdown("""
        - Pure streaming, no batch layer
        - All data treated as event streams
        - Simpler than Lambda
        - *Use Case*: Real-time-first systems
        """)
        
        st.markdown("**Write-Audit-Publish (WAP)**")
        st.markdown("""
        - Write → Audit → Publish pattern
        - Data quality validation before serving
        - Netflix/Uber style data lakes
        - Ensures data reliability
        """)
        
        st.markdown("**Slowly Changing Dimensions (SCD)**")
        st.markdown("""
        - **Type 1**: Overwrite old values
        - **Type 2**: Keep history (new row)
        - **Type 3**: Keep limited history
        - Essential for warehouse modeling
        """)
    
    st.markdown("---")
    st.subheader("Distributed Systems Concepts")
    
    concept_cols = st.columns(3)
    
    with concept_cols[0]:
        st.markdown("**CAP Theorem**")
        st.markdown("""
        Choose 2 of 3:
        - **C**onsistency
        - **A**vailability
        - **P**artition tolerance
        """)
    
    with concept_cols[1]:
        st.markdown("**Consistent Hashing**")
        st.markdown("""
        - Load balancing for distributed keys
        - Minimal rehashing on node changes
        - Used in: Cassandra, DynamoDB
        """)
    
    with concept_cols[2]:
        st.markdown("**Data Mesh / Fabric**")
        st.markdown("""
        - Decentralized data ownership
        - Self-serve data platforms
        - Organizational shift in modern DE
        """)
    
    st.markdown("---")
    st.subheader("Dimensional Modeling (Kimball)")
    
    modeling_cols = st.columns(2)
    
    with modeling_cols[0]:
        st.markdown("**Star Schema**")
        st.markdown("""
        ```
        Fact Table (transactions)
        ├─ DIM_Customer
        ├─ DIM_Product
        └─ DIM_Date
        ```
        - Simple, performant
        - Common for analytics
        """)
    
    with modeling_cols[1]:
        st.markdown("**Snowflake Schema**")
        st.markdown("""
        ```
        Fact Table
        ├─ DIM_Customer
        │  └─ DIM_Region
        └─ DIM_Product
           └─ DIM_Category
        ```
        - Normalized, less storage
        - More joins, slower queries
        """)

with tab2:
    st.subheader("Standard Platforms")
    
    resources = [
        ("Glassdoor", "General interview experiences and frequent SQL/Python questions."),
        ("Reddit (r/dataengineering, r/google)", "Discussions on recent interview loops, team matching, and specific technical challenges."),
        ("LeetCode Discuss", "Detailed breakdown of coding rounds (SQL + Algo) and system design prompts."),
        ("Team Blind", "Aggregated discussions on 'Google scale' problems, compensation expectations, and 'Googlyness' behavioral questions."),
    ]
    
    for idx, (resource, description) in enumerate(resources):
        st.markdown(f"**{resource}**")
        st.markdown(f"_{description}_")
        st.divider()
    
    st.subheader("Niche Resources")
    st.markdown("- **Logic Puzzles**: Classic Google-style brain teasers (Horse Race, Balance Scale, etc.)")
    
    st.subheader("Deep Search Findings")
    findings = [
        ("Tech Interview Handbook (Yangshun)", "github.com/yangshun/tech-interview-handbook - Curated questions for system design and behavioral."),
        ("Elements of Programming Interviews (EPI)", "github.com/gardncl/elements-of-programming-interviews - Python code repos for coding interview prep."),
        ("System Design Primer", "github.com - Foundational patterns relevant to data (Sharding, Consistent Hashing, CAP Theorem)."),
        ("Google SRE Book", "Free online. Essential for 'Production Engineering' questions (SLO/SLA, Toil)."),
    ]
    
    for resource, description in findings:
        st.markdown(f"**{resource}**")
        st.markdown(f"_{description}_")
        st.divider()

with tab3:
    st.subheader("Essential Books & References")
    
    books = [
        ("Designing Data-Intensive Applications", "Martin Kleppmann", ["Replication (Leader-Follower)", "Partitioning (Consistent Hashing)", "Consistency Models", "Distributed Transactions (2PC)"]),
        ("System Design Interview", "Alex Xu", ["Rate Limiting", "Consistent Hashing", "Key-Value Store Design", "High-scale ingestion patterns"]),
        ("The Data Warehouse Toolkit", "Ralph Kimball", ["Dimensional Modeling (Star Schema, Snowflakes)", "Facts/Dimensions", "The 'Bible' of data warehouse design"]),
        ("Cracking the Data Engineering Interview", "Various", ["ETL vs ELT", "Data Modeling (SCDs)", "Big data frameworks (Spark/Kafka)", "End-to-end DE lifecycle"]),
        ("Ace the Data Engineering Interview", "Sean Coyne", ["Practical implementations", "Community-discussed, Reddit-recommended"]),
        ("Grokking the System Design Interview", "Various", ["System design patterns", "Often found in repo dumps as 'system-design-primer'"]),
    ]
    
    for title, author, topics in books:
        st.markdown(f"**{title}** by {author}")
        for topic in topics:
            st.markdown(f"- {topic}")
        st.divider()
    
    st.subheader("Additional Resources")
    st.markdown("- **Google Cloud Blog**: Official architecture patterns (Smart Analytics, Data Mesh on GCP)")
    st.markdown("- **Google Professional Data Engineer Exam Guides**: GitHub repositories with study guides and exam patterns")

with tab4:
    st.subheader("Key Design Patterns Identified")
    
    patterns = [
        ("Lambda vs Kappa Architecture", "Trade-offs between batch/speed layers vs pure streaming."),
        ("Slowly Changing Dimensions (SCD) Type 2", "History preservation for warehouse design."),
        ("Idempotency & Deduplication", "Handling 'at-least-once' delivery in payment/critical pipelines."),
        ("Write-Audit-Publish (WAP)", "Data quality patterns for data lakes (Netflix/Uber style)."),
        ("Data Mesh / Data Fabric", "Organizational and architectural shifts in modern data engineering."),
    ]
    
    for idx, (pattern, description) in enumerate(patterns, 1):
        st.markdown(f"**{idx}. {pattern}**")
        st.markdown(f"_{description}_")
        st.divider()

with tab5:
    st.subheader("Video Courseware & Learning Platforms")
    
    courses = [
        ("Exponent (YouTube/Website)", ["High-quality mock interviews (SQL + System Design)", "Key video: 'Design a Data Pipeline' (Google style)"]),
        ("Coursera - GCP Data Engineering Professional Certificate", ["Standard theory track", "Foundational knowledge", "Official Google-backed curriculum"]),
        ("Data Engineering on GCP (YouTube)", ["Official Google Cloud Tech playlists", "Hands-on tutorials and architecture walkthroughs"]),
        ("Medium (Engineering Blogs)", ["System Design: Designing a Predictive Search Engine", "Recommendation Systems: YouTube Video Recommendations", "Data Pipelines: Ingesting Stripe Payment Data"]),
    ]
    
    for platform, topics in courses:
        st.markdown(f"**{platform}**")
        for topic in topics:
            st.markdown(f"- {topic}")
        st.divider()
