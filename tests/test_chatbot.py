"""
Comprehensive Unit & Integration Test Suite for Sanskrit Chatbot
"""

import unittest
import json
from engine.transliteration import to_devanagari, to_iast, is_devanagari, normalize_sanskrit
from engine.grammar_engine import GrammarEngine
from engine.sandhi_engine import SandhiEngine
from engine.quiz_engine import QuizEngine
from engine.dialogue_manager import DialogueManager
from app import app

class TestSanskritTransliteration(unittest.TestCase):
    def test_devanagari_detection(self):
        self.assertTrue(is_devanagari("नमस्ते"))
        self.assertTrue(is_devanagari("रामः"))
        self.assertFalse(is_devanagari("namaste"))
        self.assertFalse(is_devanagari("hello world"))

    def test_phonetic_to_devanagari(self):
        self.assertEqual(to_devanagari("namaste"), "नमस्ते")
        self.assertEqual(to_devanagari("shubhadinam"), "शुभदिनम्")
        self.assertEqual(to_devanagari("aham"), "अहम्")
        self.assertTrue(len(to_devanagari("vidya")) > 0)

    def test_devanagari_to_iast(self):
        self.assertEqual(to_iast("नमस्ते"), "namaste")
        self.assertEqual(to_iast("विद्या"), "vidyā")

    def test_normalize_sanskrit(self):
        norm = normalize_sanskrit("Śubhaprabhātam!")
        self.assertIn("shubhaprabhatam", norm)


class TestGrammarEngine(unittest.TestCase):
    def setUp(self):
        self.grammar = GrammarEngine()

    def test_lookup_shabda_rama(self):
        res = self.grammar.lookup_shabda("rama")
        self.assertIsNotNone(res)
        self.assertEqual(res["word"], "राम")
        self.assertEqual(len(res["table"]), 8)

    def test_lookup_dhatu_path(self):
        res = self.grammar.lookup_dhatu("path")
        self.assertIsNotNone(res)
        self.assertIn("lat", res["lakaras"])

    def test_morphological_analysis(self):
        # पठामि should identify as path dhatu lat lakara 1st person singular
        morphs = self.grammar.analyze_word("पठामि")
        self.assertTrue(len(morphs) > 0)
        first = morphs[0]
        self.assertEqual(first["type"], "dhatu")
        self.assertEqual(first["base"], "पठ्")


class TestSandhiEngine(unittest.TestCase):
    def setUp(self):
        self.sandhi = SandhiEngine()

    def test_dirgha_sandhi_join(self):
        res = self.sandhi.join_words("विद्या", "आलयः")
        self.assertEqual(res["joined"], "विद्यालयः")
        self.assertIn("दीर्घसन्धिः", res["rule_name"])

    def test_guna_sandhi_join(self):
        res = self.sandhi.join_words("नर", "ईशः")
        self.assertEqual(res["joined"], "नरेशः")

    def test_visarga_sandhi_join(self):
        res = self.sandhi.join_words("नमः", "ते")
        self.assertEqual(res["joined"], "नमस्ते")


class TestQuizEngine(unittest.TestCase):
    def setUp(self):
        self.quiz = QuizEngine()

    def test_get_random_question(self):
        q = self.quiz.get_random_question()
        self.assertIn("id", q)
        self.assertIn("options", q)
        self.assertEqual(len(q["options"]), 4)

    def test_evaluate_answer(self):
        q = self.quiz.get_random_question()
        res_correct = self.quiz.evaluate_answer(q["id"], q["correct_index"])
        self.assertTrue(res_correct["is_correct"])

        wrong_idx = (q["correct_index"] + 1) % 4
        res_wrong = self.quiz.evaluate_answer(q["id"], wrong_idx)
        self.assertFalse(res_wrong["is_correct"])


class TestDialogueManager(unittest.TestCase):
    def setUp(self):
        self.dm = DialogueManager()

    def test_greeting_intent(self):
        resp = self.dm.process_message("namaste")
        self.assertIn("नमस्कारः", resp["text_sa"])

    def test_user_name_memory(self):
        resp = self.dm.process_message("My name is Arjun")
        self.assertEqual(self.dm.context["user_name"], "Arjun")
        self.assertIn("Arjun", resp["text_en"])

    def test_shloka_intent(self):
        resp = self.dm.process_message("Tell me a Gita shloka")
        self.assertIsNotNone(resp["text_sa"])
        self.assertIn("Gita", resp["text_en"])

    def test_sandhi_message_join(self):
        resp = self.dm.process_message("विद्या + आलयः")
        self.assertIn("विद्यालयः", resp["text_sa"])


class TestFlaskAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'V\xc4\x81gdev\xc4\xab', res.data)

    def test_api_chat(self):
        res = self.client.post('/api/chat', json={"message": "namaste"})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn("text_sa", data)

    def test_api_shloka_of_day(self):
        res = self.client.get('/api/shloka-of-the-day')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn("shloka_sa", data)

    def test_api_transliterate(self):
        res = self.client.post('/api/transliterate', json={"text": "namaste"})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["devanagari"], "नमस्ते")

    def test_api_sandhi(self):
        res = self.client.post('/api/sandhi', json={"word1": "विद्या", "word2": "आलयः"})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["joined"], "विद्यालयः")

if __name__ == '__main__':
    unittest.main()
