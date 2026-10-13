"""
Sanskrit Interactive Quiz Engine (प्रश्नोत्तरी-विभागः)
Generates varied multiple-choice questions across:
- Vocabulary (शब्दार्थः)
- Shabdarupa (विभक्ति-ज्ञानम्)
- Dhaturupa (लकार-ज्ञानम्)
- Sandhi (सन्धि-ज्ञानम्)
- Subhashita (सुभाषित-ज्ञानम्)
"""

import random
from typing import Dict, List, Any, Optional

QUIZ_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "q1",
        "category": "शब्दार्थः (Vocabulary)",
        "question_sa": "'गृहम्' शब्दस्य आङ्ग्लभाषायाम् अर्थः कः?",
        "question_en": "What is the meaning of the Sanskrit word 'गृहम्' (Gṛham)?",
        "options": ["House / Home", "Book", "Tree", "Water"],
        "correct_index": 0,
        "explanation": "'गृहम्' (Gṛham) denotes house or home (नपुंसकलिङ्गम्)."
    },
    {
        "id": "q2",
        "category": "विभक्ति-ज्ञानम् (Noun Cases)",
        "question_sa": "'राम' शब्दस्य षष्ठी-विभक्ति-एकवचनं किम्?",
        "question_en": "What is the 6th case singular (षष्ठी विभक्तिः एकवचनम् - Genitive) of 'राम' (Rāma)?",
        "options": ["रामेण", "रामस्य", "रामात्", "रामाय"],
        "correct_index": 1,
        "explanation": "'रामस्य' means 'of Rama' or 'Rama's' (षष्ठी एकवचनम्). रामेण is 3rd, रामाय is 4th, रामात् is 5th case."
    },
    {
        "id": "q3",
        "category": "लकार-ज्ञानम् (Verb Conjugation)",
        "question_sa": "'अहम् पुस्तकं ______।' (पठ् - लट् लकारः उत्तमपुरुषः एकवचनम्)",
        "question_en": "Complete with the correct present tense form of पठ् for 'अहम्' (I):",
        "options": ["पठति", "पठसि", "पठामि", "पठन्ति"],
        "correct_index": 2,
        "explanation": "With First Person 'अहम्' (I), the verb takes 'आमि' suffix in present tense (लट्) -> 'पठामि' (I read)."
    },
    {
        "id": "q4",
        "category": "सन्धि-ज्ञानम् (Sandhi)",
        "question_sa": "'विद्या + आलयः' इत्यनयोः सन्धौ किं पदं भवति?",
        "question_en": "What word is formed by joining 'विद्या + आलयः' (Vidyā + Ālayaḥ)?",
        "options": ["विद्योदयः", "विद्यालयः", "विद्यैलयः", "विद्यलयः"],
        "correct_index": 1,
        "explanation": "According to दीर्घसन्धिः (अकः सवर्णे दीर्घः), ā + ā merges into long ā -> 'विद्यालयः'."
    },
    {
        "id": "q5",
        "category": "सुभाषित-ज्ञानम् (Wisdom Verses)",
        "question_sa": "श्लोकं पूरयतु: 'उद्यमेन हि सिध्यन्ति कार्याणि न _______।'",
        "question_en": "Complete the verse: 'Udyamena hi sidhyanti kāryāṇi na _______'",
        "options": ["मनोरथैः", "अलसैः", "वचनैः", "धनैः"],
        "correct_index": 0,
        "explanation": "'मनोरथैः' (by mere wishes). The full line is: 'उद्यमेन हि सिध्यन्ति कार्याणि न मनोरथैः' (Tasks succeed through diligence, not mere daydreaming)."
    },
    {
        "id": "q6",
        "category": "शब्दार्थः (Vocabulary)",
        "question_sa": "'सूर्यः' शब्दस्य पर्यायपदं किम्?",
        "question_en": "Which of these is a synonym for 'सूर्यः' (Sūryaḥ - Sun)?",
        "options": ["चन्द्रः", "भास्करः", "वारि", "पर्वतः"],
        "correct_index": 1,
        "explanation": "'भास्करः' (Bhāskaraḥ - Creator of radiance) is an ancient and well-known name for the Sun."
    },
    {
        "id": "q7",
        "category": "सम्भाषणम् (Conversation)",
        "question_sa": "How do you politely say 'Thank You' in Sanskrit?",
        "question_en": "Which Sanskrit phrase translates to 'Thank you'?",
        "options": ["क्षम्यताम् (Kṣamyatām)", "स्वागतम् (Svāgatam)", "धन्यवादः (Dhanyavādaḥ)", "कृपया (Kṛpayā)"],
        "correct_index": 2,
        "explanation": "'धन्यवादः' (Dhanyavādaḥ) means 'Thank you'. 'क्षम्यताम्' means excuse me, 'स्वागतम्' means welcome, 'कृपया' means please."
    },
    {
        "id": "q8",
        "category": "सन्धि-ज्ञानम् (Sandhi)",
        "question_sa": "'नमः + ते' इत्यनयोः सन्धौ किं भवति?",
        "question_en": "What does 'नमः + ते' (Namaḥ + te) join to form?",
        "options": ["नमोते", "नमस्ते", "नमस्तेः", "नमते"],
        "correct_index": 1,
        "explanation": "By विसर्जनीयस्य सः rule (Visarga Sandhi), before 't', visarga transforms into 's' -> 'नमस्ते' (Namaste)."
    },
    {
        "id": "q9",
        "category": "सर्वनाम (Pronouns)",
        "question_sa": "संस्कृते 'वयम्' शब्दस्य अर्थः कः?",
        "question_en": "What does the Sanskrit pronoun 'वयम्' (Vayam) mean?",
        "options": ["I", "You all", "We all", "They"],
        "correct_index": 2,
        "explanation": "'वयम्' is the plural nominative form of 'अस्मद्' meaning 'We all'."
    },
    {
        "id": "q10",
        "category": "संख्याः (Numbers)",
        "question_sa": "संस्कृते 'पञ्च' संख्यायाः आङ्ग्ले अर्थः कः?",
        "question_en": "What number does 'पञ्च' (Pañca) represent?",
        "options": ["Three", "Four", "Five", "Seven"],
        "correct_index": 2,
        "explanation": "'पञ्च' (Pañca) stands for the numeral 5."
    }
]

class QuizEngine:
    def __init__(self):
        self.questions = QUIZ_QUESTIONS

    def get_random_question(self, exclude_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Fetch a random question, avoiding already presented IDs if possible."""
        avail = [q for q in self.questions if not exclude_ids or q["id"] not in exclude_ids]
        if not avail:
            avail = self.questions
        return random.choice(avail)

    def get_question_by_id(self, qid: str) -> Optional[Dict[str, Any]]:
        for q in self.questions:
            if q["id"] == qid:
                return q
        return None

    def evaluate_answer(self, qid: str, selected_index: int) -> Dict[str, Any]:
        q = self.get_question_by_id(qid)
        if not q:
            return {"error": "Question not found"}

        is_correct = (selected_index == q["correct_index"])
        return {
            "question_id": qid,
            "is_correct": is_correct,
            "selected_index": selected_index,
            "correct_index": q["correct_index"],
            "correct_answer": q["options"][q["correct_index"]],
            "explanation": q["explanation"]
        }
