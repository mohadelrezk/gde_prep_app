import json
import os
import streamlit as st
import random

class QuizEngine:
    def __init__(self, data_path="data/questions.json"):
        self.data_path = data_path
        self.questions = self._load_questions()

    def _load_questions(self):
        try:
            with open(self.data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading questions: {e}")
            return []

    def get_questions_by_topic(self, topic=None, min_score=0):
        pool = self.questions
        if topic and topic != "All":
            pool = [q for q in pool if q['topic'] == topic]
        
        if min_score > 0:
            pool = [q for q in pool if q.get('frequency_score', 0) >= min_score]
            
        return pool

    def get_random_questions(self, count=5, topic=None, min_score=0):
        pool = self.get_questions_by_topic(topic, min_score)
        if not pool:
            return []
        return random.sample(pool, min(count, len(pool)))

    def get_all_topics(self):
        topics = set(q['topic'] for q in self.questions)
        return ["All"] + sorted(list(topics))

    @staticmethod
    def check_answer(question, selected_option):
        return question['answer'] == selected_option
