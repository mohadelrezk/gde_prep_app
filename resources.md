# Google Data Engineering Interview Resources

A compilation of resources used to gather and verify interview questions, ranging from standard platforms to niche engineering blogs and forums.

## 📚 Standard Resources
- **Glassdoor**: General interview experiences and frequent SQL/Python questions.
- **Reddit (r/dataengineering, r/google)**: Discussions on recent interview loops, team matching, and specific technical challenges.
- **LeetCode Discuss**: Detailed breakdown of coding rounds (SQL + Algo) and system design prompts.

## 🔗 Niche & "Unusual" Resources
- **Logic Puzzles**: Classic Google-style brain teasers (Horse Race, Balance Scale).

## 🕵️ Deep Search Findings (GitHub & Drive Patterns)
- **Tech Interview Handbook (Yangshun)**:
    - *Repo*: `github.com/yangshun/tech-interview-handbook`.
    - *Value*: Curated "Blind 75" style questions but for system design and behavioral.
- **"Elements of Programming Interviews" (EPI)**:
    - *Python Code Repos*: `github.com/gardncl/elements-of-programming-interviews`.
    - *Why*: Google DEs are often tested on "Pythonic" efficiency just like SWEs.
- **"Grokking the System Design Interview" (PDFs)**:
    - Often found in repo dumps named `system-design-primer`.
- **Google SRE Book**:
    - Free online. Essential for "Production Engineering" questions (SLO/SLA, Toil).
- **Team Blind**: aggregated discussions on "Google scale" problems, compensation-level expectations, and "Googlyness" behavioral questions.
- **Medium (Engineering Blogs)**:
    - *System Design*: Deep dives into "Designing a Predictive Search Engine like Google" (Prefix handling, Caching).
    - *Recommendation Systems*: "Design YouTube Video Recommendations" (Candidate Generation -> Ranking -> Serving).
    - *Data Pipelines*: Real-world scenarios like "Ingesting Stripe Payment Data" (Idempotency, Deduplication).
- **Google Cloud Blog**: Official architecture patterns (Smart Analytics, Data Mesh on GCP).
- **System Design Primer (GitHub)**: Foundational patterns relevant to data (Sharding, Consistent Hashing, CAP Theorem).
- **"Cracking the Data Engineering Interview" (Repo/Book snippets)**: Conceptual questions on ETL vs ELT, Data Modeling (SCDs), and big data frameworks (Spark/Kafka).

## 💡 Key Design Patterns Identified
1.  **Lambda vs Kappa Architecture**: Trade-offs between batch/speed layers vs pure streaming.
2.  **Slowly Changing Dimensions (SCD)**: specifically Type 2 (History preservation) for warehouse design.
3.  **Idempotency & Deduplication**: Handling "at-least-once" delivery in payment/critical pipelines.
4.  **Write-Audit-Publish (WAP)**: Data quality patterns for data lakes (Netlfix/Uber style).
5.  **Data Mesh / Data Fabic**: Organizational and architectural shifts in modern data engineering.

## 📺 Video & Courseware (Classic Resources)
- **Exponent (YouTube/Website)**: High-quality mock interviews (SQL + System Design). Key video: "Design a Data Pipeline" (Google style).
- **Coursera (GCP Data Engineering Professional Certificate)**: The standard theory track. Good for "old" foundational knowledge.
- **Data Engineering on GCP (YouTube)**: Official Google Cloud Tech playlists.

## 📚 Community-Sourced PDF & Book Suggestions (New/Niche)
- **"Ace the Data Engineering Interview" (Sean Coyne)**:
    - Frequently discussed on Reddit; focuses on practical implementations.
- **"Data Science / Engineering Interview" (Online Free Book)**:
    - Community-maintained guide covers probability, SQL, and ML system design.
- **"Google Cloud Data Decision Cheatsheet"**:
    - Essential 1-pager for choosing between Bigtable, Spanner, SQL, and BigQuery. (Integrated into this App).

## 📄 PDF Books & GitHub Guides
- **"Designing Data-Intensive Applications" (Martin Kleppmann)**:
    - *Summaries*: Found as [PDF summaries on GitHub/Shortform](https://github.com/search?q=designing+data+intensive+applications+summary).
    - *Key Concepts*: Replication (Leader-Follower), Partitioning (Consistent Hashing), Consistency Models (Linearizability vs Eventual), and Distributed Transactions (2PC).
- **"System Design Interview" (Alex Xu)**:
    - *Availability*: Widely circulated as PDF/GitHub summaries.
    - *Focus*: Rate Limiting, Consistent Hashing, Key-Value Store design—often adapted for DE interviews involved high-scale ingestion.
- **"The Data Warehouse Toolkit" (Ralph Kimball)**:
    - *Classic Text*: The "Bible" of dimensional modeling (Star Schema, Snowflakes, Facts/Dimensions). PDF versions are common references for SQL modeling rounds.
- **Google Professional Data Engineer Exam Guides**:
    - GitHub repositories often host "Exam Dumps" and "Study Guides" (search `site:github.com "google data engineer" guide`).
- **"Cracking the Data Engineering Interview"**:
    - Referenced as having a complementary PDF eBook. Covers end-to-end DE lifecycle.
