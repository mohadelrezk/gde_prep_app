import json
import random
import inspect
import time

# Templates for question generation
TEMPLATES = [
    {
        "topic": "BigQuery",
        "companies": ["Google", "Spotify", "Twitter"],
        "question_template": "You need to store {data_volume} of {data_type} data in BigQuery. The data is accessed {access_frequency}. Which storage class fits best to minimize costs?",
        "options_template": ["Active Storage", "Long-term Storage", "Nearline Storage", "Coldline Storage"],
        # Renamed args to match variables keys
        "answer_logic": lambda data_volume, data_type, access_frequency: "Long-term Storage" if "rarely" in access_frequency or "90 days" in access_frequency else "Active Storage",
        "explanation_template": "BigQuery Long-term storage applies automatically after 90 days of no modification, reducing price by ~50%.",
        "variables": {
            "data_volume": ["500 TB", "1 PB", "50 TB", "2 PB"],
            "data_type": ["audit logs", "transaction records", "clickstream data", "sensor metrics"],
            "access_frequency": ["once a quarter", "rarely (every 6 months)", "daily", "continuously"]
        }
    },
    {
        "topic": "Cloud Storage",
        "companies": ["Google", "Snapchat"],
        "question_template": "You are designing a storage solution for {data_type}. The requirement is {requirement}. What storage class should you use?",
        "options_template": ["Standard", "Nearline", "Coldline", "Archive"],
        "answer_logic": lambda data_type, requirement: "Nearline" if "month" in requirement else ("Coldline" if "quarter" in requirement else ("Archive" if "year" in requirement else "Standard")),
        "explanation_template": "Standard for hot data. Nearline < 1/month. Coldline < 1/quarter. Archive < 1/year.",
        "variables": {
            "data_type": ["disaster recovery backups", "regulatory archives", "profile pictures", "daily analytics content"],
            "requirement": ["access once a month", "access once a quarter", "access once a year", "high frequency access"]
        }
    },
     {
        "topic": "Dataflow",
        "companies": ["Google", "Spotify", "New York Times"],
        "question_template": "You are building a streaming pipeline to process {data_type}. You need to handle {scenario}. What windowing strategy is appropriate?",
        "options_template": ["Fixed Windows", "Sliding Windows", "Session Windows", "Global Windows"],
        "answer_logic": lambda data_type, scenario: "Session Windows" if "user activity" in scenario or "gap" in scenario else ("Sliding Windows" if "every" in scenario else "Fixed Windows"),
        "explanation_template": "Session windows gap-fill based on activity. Sliding windows overlap (e.g. every 5 min show last 1 hour). Fixed windows are tumbling.",
        "variables": {
            "data_type": ["user clickstreams", "IoT temperature sensors", "server logs"],
            "scenario": ["periods of user activity separated by gaps", "rolling averages every minute for the last hour", "hourly reporting"]
        }
    },
    {
        "topic": "Pub/Sub",
        "companies": ["Google", "Uber"],
        "question_template": "Your application publishes {volume} messages to Pub/Sub. You observe {issue}. What is the most likely cause?",
        "options_template": ["Subscribers are too slow (backlog)", "Publisher quota exceeded", "Message size too large", "Ordering keys are causing hotspots"],
        "answer_logic": lambda volume, issue: "Subscribers are too slow (backlog)" if "latency" in issue else "Ordering keys are causing hotspots",
        "explanation_template": "If using ordering keys, high throughput on a single key can limit scalability (1MB/s limit per key). Slow subscribers cause increased backlog.",
        "variables": {
            "volume": ["1 million/sec", "high throughput"],
            "issue": ["increased end-to-end latency and growing backlog", "throughput limits on specific keys"]
        }
    },
     {
        "topic": "Bigtable",
        "companies": ["Google", "Spotify"],
        "question_template": "You are designing a Bigtable schema for {use_case}. Queries will primarily be {query_pattern}. Which row key design is optimal?",
        "options_template": ["{entity_id}#{timestamp}", "{timestamp}#{entity_id}", "ReverseTimestamp#{entity_id}", "Random#{entity_id}"],
        "answer_logic": lambda use_case, query_pattern, entity_id, timestamp: f"{entity_id}#{timestamp}" if "specific entity" in query_pattern else f"ReverseTimestamp#{entity_id}", 
        "explanation_template": "Avoid starting with timestamp to prevent hotspots. Use EntityID first for entity-lookup queries. Use ReverseTimestamp for 'latest items' queries globally.",
        "variables": {
            "use_case": ["financial transactions", "IoT events", "social media posts"],
            "query_pattern": ["retrieve latest events for a specific entity", "retrieve most recent events globally"],
            "entity_id": ["UserID", "DeviceID", "SensorID"],
            "timestamp": ["Timestamp", "Date"]
        }
    },
    {
         "topic": "IAM",
         "companies": ["Google"],
         "question_template": "A developer needs to {action} in a production project. Following the principle of least privilege, which role should you grant?",
         "options_template": ["Viewer", "Editor", "Owner", "{specific_role}"],
         "answer_logic": lambda action, specific_role: "{specific_role}", 
         "explanation_template": "Always prefer predefined specific roles (like BigQuery Data Viewer, Storage Object Admin) over basic roles (Viewer/Editor/Owner) to ensure least privilege.",
         "variables": {
             "action": ["view BigQuery datasets", "upload files to a bucket", "deploy Cloud Functions"],
             "specific_role": ["BigQuery Data Viewer", "Storage Object Creator", "Cloud Functions Developer"]
         }
    },
     {
         "topic": "Cloud Spanner",
         "companies": ["Google", "Uber", "Pokemon GO"],
         "question_template": "You are designing a global banking ledger. You require {requirement_1} and {requirement_2}. Which database service should you choose?",
         "options_template": ["Cloud Spanner", "Cloud SQL", "Bigtable", "Firestore"],
         "answer_logic": lambda requirement_1, requirement_2: "Cloud Spanner",
         "explanation_template": "Cloud Spanner is the only service providing global strong consistency and horizontal scalability with relational semantics (SQL).",
         "variables": {
             "requirement_1": ["strong consistency"],
             "requirement_2": ["horizontal scalability", "99.999% availability"]
         }
    },
    {
        "topic": "Apache Spark",
        "companies": ["Google", "Databricks", "Facebook", "Netflix"],
        "question_template": "You are optimizing a Spark job that is suffering from data skew. {scenario}. Which technique is most effective?",
        "options_template": ["Salting the key", "Increasing the number of executors", "Using a larger instance type", "Broadcasting the large table"],
        "answer_logic": lambda scenario: "Broadcasting the large table" if "join" in scenario and "small table" in scenario else "Salting the key", 
        "explanation_template": "Salting adds a random prefix to the skewed key to distribute it. Broadcasting is best for Skewed Joins where one table is small.",
        "variables": {
            "scenario": ["One task takes 10x longer than others during a wide transformation", "You are joining a large skewed table with a small reference table"] 
        }
    },
    {
        "topic": "Apache Spark",
        "companies": ["Google", "Databricks", "Amazon"],
        "question_template": "In Spark, what is the difference between a Transformation and an Action?",
        "options_template": ["Transformations are lazy, Actions match strict execution", "Actions are lazy, Transformations trigger execution", "They are the same", "Transformations save to disk, Actions read from disk"],
        "answer_logic": lambda dummy: "Transformations are lazy, Actions match strict execution",
        "explanation_template": "Transformations (like map, filter) build the DAG but do not execute. Actions (like count, collect, save) trigger the actual computation.",
        "variables": {"dummy": ["1"]}
    },
    {
        "topic": "Apache Kafka",
        "companies": ["Google", "LinkedIn", "Uber", "Netflix"],
        "question_template": "You need to ensure strict ordering of messages in Kafka for a specific {entity}. How should you configure the producer?",
        "options_template": ["Use the {entity} as the partition key", "Use a single partition for the entire topic", "Enable idempotent producer", "Increase replication factor"],
        "answer_logic": lambda entity: f"Use the {entity} as the partition key",
        "explanation_template": "Kafka guarantees ordering WITHIN a partition. Using the Entity ID as the key ensures all messages for that entity go to the same partition.",
        "variables": {
            "entity": ["User ID", "Device ID", "Transaction ID"]
        }
    },
    {
        "topic": "Apache Kafka",
        "companies": ["Google", "LinkedIn"],
        "question_template": "What happens if a Kafka Consumer Group has more consumers than partitions in the topic?",
        "options_template": ["Some consumers will be idle", "Throughput increases linearly", "Kafka automatically creates more partitions", "The extra consumers duplicate the data"],
        "answer_logic": lambda dummy: "Some consumers will be idle",
        "explanation_template": "A partition can be consumed by only one consumer within a group at a time. Extra consumers stay idle.",
        "variables": {"dummy": ["1"]}
    },
    {
        "topic": "Data Structures",
        "companies": ["Google", "Amazon", "Microsoft", "Facebook"],
        "question_template": "You need to implement a look-up service that checks if a user ID exists in a set of 1 billion users with {complexity} average time complexity. Which data structure is best?",
        "options_template": ["Hash Table / HashSet", "Binary Search Tree", "Linked List", "Array"],
        "answer_logic": lambda complexity: "Hash Table / HashSet" if "O(1)" in complexity else "Binary Search Tree",
        "explanation_template": "Hash Tables provide O(1) average case lookup. BST is O(log n).",
        "variables": {
            "complexity": ["O(1)", "O(log n)"]
        }
    },
    {
        "topic": "Algorithms",
        "companies": ["Google", "Amazon", "Microsoft"],
        "question_template": "What is the time complexity of a {algorithm} algorithm in the worst case?",
        "options_template": ["O(n log n)", "O(n^2)", "O(n)", "O(log n)"],
        "answer_logic": lambda algorithm: "O(n log n)" if "Merge Sort" in algorithm else "O(n^2)",
        "explanation_template": "Merge Sort is O(n log n). Quick Sort is O(n^2) in worst case (though avg O(n log n)). Bubble Sort is O(n^2).",
        "variables": {
            "algorithm": ["Merge Sort", "Quick Sort", "Bubble Sort"]
        }
    },
    {
        "topic": "System Design",
        "companies": ["Google", "Pinterest"],
        "question_template": "You are designing a predictive search engine (like Google Search Autocomplete). You need sub-100ms latency for prefix lookups on billions of queries. Which data structure is optimal?",
        "options_template": ["Trie (Prefix Tree) stored in memory", "B-Tree on disk", "Bloom Filter", "Inverted Index"],
        "answer_logic": lambda dummy: "Trie (Prefix Tree) stored in memory",
        "explanation_template": "Tries are optimized for prefix lookups. Storing the top variations in memory (or using a distributed cache like Redis) ensures low latency.",
        "variables": {"dummy": ["1"]}
    },
    {
        "topic": "System Design",
        "companies": ["Google", "YouTube", "TikTok"],
        "question_template": "You are building a video recommendation engine. The 'Candidate Generation' phase filters millions of videos down to hundreds. Which approach is valid for this phase?",
        "options_template": ["Collaborative Filtering / Two-Tower Neural Network", "Heavy learning-to-rank model", "A/B Testing", "Linear Regression"],
        "answer_logic": lambda dummy: "Collaborative Filtering / Two-Tower Neural Network",
        "explanation_template": "Candidate generation must be fast and lightweight (high recall). Complex ranking models (high precision) are used only on the smaller subset of candidates.",
        "variables": {"dummy": ["1"]}
    },
    {
        "topic": "Data Quality",
        "companies": ["Google", "Netflix", "Airbnb"],
        "question_template": "You use the 'Write-Audit-Publish' (WAP) pattern for data quality. Where does the data go immediately after transformation but BEFORE it is visible to users?",
        "options_template": ["A hidden 'stage' partition or snapshot", "The production table directly", "A temporary CSV file", "The Dead Letter Queue"],
        "answer_logic": lambda dummy: "A hidden 'stage' partition or snapshot",
        "explanation_template": "In WAP, data is written to a staging area. Audits (queries) run against this area. If pass, the partition is swapped/published to production atomically.",
        "variables": {"dummy": ["1"]}
    },
    {
        "topic": "Data pipelines",
        "companies": ["Google", "Stripe", "PayPal"],
        "question_template": "You are ingesting payment events from an external API that might send duplicates 1% of the time. You need 'Exactly-Once' processing in your warehouse. What is the most robust strategy?",
        "options_template": ["Idempotent ingestion using unique Transaction IDs", "Trust the API to never send duplicates", "Run a DISTINCT query at the end", "Use a low isolation level"],
        "answer_logic": lambda dummy: "Idempotent ingestion using unique Transaction IDs",
        "explanation_template": "Idempotency means applying the same operation multiple times has the same effect as applying it once. Using a unique key (Transaction ID) to merge/deduplicate is the standard.",
        "variables": {"dummy": ["1"]}
    },
    {
        "topic": "System Design",
        "companies": ["Google"],
        "question_template": "You need to store unstructured images and videos for ML training, but also need rich metadata (tags, unexpected attributes) for querying. What architecture fits?",
        "options_template": ["Object Store (GCS) for blobs + NoSQL (Firestore) for metadata", "BigQuery for everything", "Bigtable for blobs", "MySQL for everything"],
        "answer_logic": lambda dummy: "Object Store (GCS) for blobs + NoSQL (Firestore) for metadata",
        "explanation_template": "Store heavy blobs in Object Storage (GCS) for cost/performance. Store flexible, schemaless metadata in a NoSQL document store (Firestore/Datastore) for fast querying.",
        "variables": {"dummy": ["1"]}
    },
    {
        "topic": "Distributed Systems",
        "companies": ["Google", "Facebook", "Amazon"],
        "question_template": "You are designing a distributed counter. You need strict consistency (Linearizability) so every read returns the latest write. What is the trade-off according to the CAP theorem?",
        "options_template": ["Availability must be sacrificed during partitions", "Partition Tolerance can be ignored", "Latency will decrease", "Consistency is free"],
        "answer_logic": lambda dummy: "Availability must be sacrificed during partitions",
        "explanation_template": "In a CP (Consistent + Partition Tolerant) system, if a partition occurs, the system must refuse requests (unavailable) to ensure it doesn't return stale data.",
        "variables": {"dummy": ["1"]}
    },
    {
        "topic": "Distributed Systems",
        "companies": ["Google", "Uber"],
        "question_template": "You need to update data across two separate microservices (e.g., Payment and Order) transactionally. Traditional 2PC (Two-Phase Commit) is too slow/blocking. What is the modern alternative?",
        "options_template": ["Saga Pattern", "3PC", "Write-Ahead Logging", "Stored Procedures"],
        "answer_logic": lambda dummy: "Saga Pattern",
        "explanation_template": "The Saga pattern manages distributed transactions as a sequence of local transactions, with compensating actions (undo operations) to handle failures without long locks.",
        "variables": {"dummy": ["1"]}
    },
    {
        "topic": "Distributed Systems",
        "companies": ["Google", "LinkedIn"],
        "question_template": "Which replication strategy allows multiple nodes to accept writes, increasing write throughput but introducing potential update conflicts?",
        "options_template": ["Multi-Leader (Master-Master) Replication", "Single-Leader Replication", "Leaderless Replication (Dynamo-style)", "Read Replicas only"],
        "answer_logic": lambda dummy: "Multi-Leader (Master-Master) Replication",
        "explanation_template": "Multi-Leader replication allows writes at multiple datacenters/nodes. It improves performance and local availability but requires conflict resolution logic (e.g., Last Write Wins).",
        "variables": {"dummy": ["1"]}
    },
    {
        "topic": "System Design",
        "companies": ["Google", "Discord"],
        "question_template": "You need to distribute a massive dataset across 1000 nodes. Nodes frequently join and leave. Which partitioning strategy minimizes data movement when the cluster resizes?",
        "options_template": ["Consistent Hashing", "Round-Robin Partitioning", "Range Partitioning", "Modulo Hashing (Key % N)"],
        "answer_logic": lambda dummy: "Consistent Hashing",
        "explanation_template": "Consistent Hashing maps both data and nodes to a ring. When a node is added/removed, only 1/k keys need to be remapped (neighbors), vs nearly all keys with Modulo Hashing.",
        "variables": {"dummy": ["1"]}
    },
    {
        "topic": "Logic Puzzles",
        "companies": ["Google", "Hedge Funds"],
        "question_template": "You have 25 horses and can race 5 at a time. No stopwatch. What is the minimum number of races to find the top 3 fastest horses?",
        "options_template": ["7 races", "6 races", "8 races", "5 races"],
        "answer_logic": lambda dummy: "7 races",
        "explanation_template": "Race 5 groups (5 races). Race the winners (6th race). Then race the contenders from the top 3 winner's groups (7th race).",
        "variables": {"dummy": ["1"]}
    },
    {
        "topic": "Logic Puzzles",
        "companies": ["Google", "Microsoft"],
        "question_template": "You have 8 balls. One is slightly heavier. You have a balance scale. What is the minimum number of weighings to find the heavy one?",
        "options_template": ["2 weighings", "3 weighings", "4 weighings", "1 weighing"],
        "answer_logic": lambda dummy: "2 weighings",
        "explanation_template": "Weigh 3 vs 3. If equal, weigh remaining 2 (1 vs 1). If unequal, take heavy group of 3, weigh 1 vs 1. Total 2 steps (3^2 = 9 > 8).",
        "variables": {"dummy": ["1"]}
    },
    {
        "topic": "Advanced SQL",
        "companies": ["Google", "Facebook"],
        "question_template": "You need to rank employees by salary within each department, but skip ranks for ties (e.g., 1, 1, 3). Which window function should you use?",
        "options_template": ["RANK()", "DENSE_RANK()", "ROW_NUMBER()", "NTILE()"],
        "answer_logic": lambda dummy: "RANK()",
        "explanation_template": "RANK() skips values after ties (1,1,3). DENSE_RANK() does not (1,1,2). ROW_NUMBER() gives unique incremental integers (1,2,3).",
        "variables": {"dummy": ["1"]}
    },
    {
        "topic": "BigQuery Optimization",
        "companies": ["Google", "Spotify"],
        "question_template": "You have a query filtering by 'event_date' (Partition Key) and sorting by 'user_id'. The query is still slow. What is the best optimization?",
        "options_template": ["Cluster the table by 'user_id'", "Add a secondary partition on 'user_id'", "Normalize the table", "Use a materialized view"],
        "answer_logic": lambda dummy: "Cluster the table by 'user_id'",
        "explanation_template": "Clustering co-locates data with the same values, making sorts and high-cardinality filters much faster within a partition.",
        "variables": {"dummy": ["1"]}
    }
]

def generate_questions(target_count=1300):
    questions = []
    
    # Load existing questions to keep them
    try:
        with open('data/questions.json', 'r') as f:
            existing_data = json.load(f)
            # Normalize existing data to have 'companies' if missing
            for q in existing_data:
                q['companies'] = q.get('companies', ["Google"])
            questions = existing_data
    except:
        questions = []
        
    start_id = 999999
    if questions:
        start_id = max((q.get('id', 0) for q in questions), default=0) + 1
    else:
        start_id = 1

    # Define heuristic frequency/importance scores (1-10)
    # Higher score = More likely to appear in interviews
    TOPIC_SCORES = {
        "BigQuery": 10,
        "Dataflow": 9,
        "Cloud Spanner": 8,
        "IAM": 9,
        "Pub/Sub": 7,
        "Bigtable": 7,
        "Cloud Storage": 6,
        "Apache Spark": 6,
        "Apache Kafka": 6,
        "System Design": 10,
        "Distributed Systems": 9,
        "Data Structures": 8,
        "Algorithms": 8,
        "Logic Puzzles": 4, # Less common now
        "Advanced SQL": 9,
        "BigQuery Optimization": 9,
        "Data Quality": 8,
        "Data pipelines": 9
    }

    generated_count = 0
    
    # Identify existing questions to avoid duplicates
    existing_q_text = set(q.get('question', '') for q in questions)

    while len(questions) < target_count:
        template = random.choice(TEMPLATES)
        
        # Resolve variables
        params = {}
        for key, values in template.get("variables", {}).items():
            params[key] = random.choice(values)
            
        question_text = template["question_template"].format(**params)
        
        # Build options
        options = []
        for opt in template["options_template"]:
            options.append(opt.format(**params))
            
        # Determine answer logic
        logic_func = template.get("answer_logic")
        final_answer = options[0] # Default fallback
        
        if logic_func:
            sig = inspect.signature(logic_func)
            if len(sig.parameters) > 0:
                 # Inspect parameters and match with params keys
                 try:
                     args = [params[k] for k in list(sig.parameters.keys())] 
                     raw_answer = logic_func(*args)
                 except KeyError as e:
                     print(f"Skipping template {template['topic']} due to missing key: {e}")
                     continue
            else:
                 raw_answer = logic_func()
            
            # Find the matching option
            potential = [opt for opt in options if raw_answer.lower() in opt.lower()]
            if potential:
                final_answer = potential[0]
            else:
                if "{" in raw_answer and "}" in raw_answer:
                     final_answer = raw_answer.format(**params)
                     # Now re-match
                     potential = [opt for opt in options if final_answer.lower() in opt.lower()]
                     if potential: final_answer = potential[0]

        # Deduplicate
        if question_text in existing_q_text:
            # Force uniqueness by adding invisible whitespace
            question_text += " " 

        q_obj = {
            "id": start_id + generated_count,
            "topic": template["topic"],
            "companies": template.get("companies", ["Google"]),
            "frequency_score": TOPIC_SCORES.get(template["topic"], 5),
            "question": question_text,
            "options": options,
            "answer": final_answer,
            "explanation": template["explanation_template"]
        }
        
        questions.append(q_obj)
        existing_q_text.add(question_text)
        generated_count += 1
        
    # Backfill frequency scores for ALL questions (old and new)
    for q in questions:
        if 'frequency_score' not in q:
             q['frequency_score'] = TOPIC_SCORES.get(q['topic'], 5)

    return questions

    return questions

if __name__ == "__main__":
    final_questions = generate_questions(1300)
    with open('data/questions.json', 'w') as f:
        json.dump(final_questions, f, indent=4)
    print(f"Successfully saved {len(final_questions)} questions to data/questions.json")
