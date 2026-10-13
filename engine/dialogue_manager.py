"""
Sanskrit Dialogue Manager (संभाषण-प्रबन्धकः)
Coordinates:
- Multi-turn conversation and context memory
- Dual-script understanding (Devanagari & Latin transliteration)
- Grammar queries, Shloka retrieval, Sandhi resolution, and Dictionary lookups
- TF-IDF semantic matching and rule-based intent recognition
"""

import re
import random
from typing import Dict, List, Any, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .transliteration import to_devanagari, to_iast, is_devanagari, normalize_sanskrit
from .knowledge_base import (
    GREETINGS_DATA, SUBHASHITA_COLLECTION, DICTIONARY_WORDS,
    SHABDARUPA_DATA, DHATURUPA_DATA, SANDHI_RULES
)
from .grammar_engine import GrammarEngine
from .sandhi_engine import SandhiEngine
from .quiz_engine import QuizEngine

class DialogueManager:
    def __init__(self):
        self.grammar = GrammarEngine()
        self.sandhi = SandhiEngine()
        self.quiz = QuizEngine()

        # Session memory
        self.context: Dict[str, Any] = {
            "user_name": None,
            "turn_count": 0,
            "last_intent": None,
            "active_quiz": None,
            "quiz_score": {"correct": 0, "total": 0}
        }

        # Initialize TF-IDF index for semantic intent matching
        self._init_intent_vectorizer()

    def _init_intent_vectorizer(self):
        self.intent_corpus = []
        self.intent_labels = []

        # Index greetings and FAQ patterns
        for item in GREETINGS_DATA:
            for pat in item["patterns"]:
                norm = normalize_sanskrit(pat)
                self.intent_corpus.append(norm)
                self.intent_labels.append(("greeting", item))

        # Index subhashitas by title, theme, and first lines
        for sh in SUBHASHITA_COLLECTION:
            self.intent_corpus.append(normalize_sanskrit(sh["title"]))
            self.intent_labels.append(("shloka_direct", sh))
            self.intent_corpus.append(normalize_sanskrit(sh["meaning_en"]))
            self.intent_labels.append(("shloka_direct", sh))
            self.intent_corpus.append(normalize_sanskrit(sh["shloka_sa"]))
            self.intent_labels.append(("shloka_direct", sh))

        # Build vectorizer
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.intent_corpus)

    def process_message(self, message: str) -> Dict[str, Any]:
        """
        Main entry point for incoming user messages.
        Returns rich structured response dictionary.
        """
        raw_msg = message.strip()
        if not raw_msg:
            return self._format_response(
                text_sa="कृपया किमपि वदतु!",
                text_iast="Kṛpayā kimapi vadatu!",
                text_en="Please say something! You can type in Sanskrit (Devanagari/English) or ask in English.",
                follow_ups=["नमस्ते", "Tell me a shloka", "Start quiz", "Rama shabda"]
            )

        self.context["turn_count"] += 1
        msg_norm = normalize_sanskrit(raw_msg)
        msg_lower = raw_msg.lower()

        # Check if an active quiz answer is being submitted
        if self.context.get("active_quiz"):
            # Check for digit 1-4 or option letter A-D
            answer_idx = self._parse_quiz_answer(msg_lower)
            if answer_idx is not None:
                return self._handle_quiz_submission(answer_idx)

        # Check for user introducing their name
        name_extracted = self._extract_user_name(raw_msg)
        if name_extracted:
            self.context["user_name"] = name_extracted
            name_deva = to_devanagari(name_extracted)
            return self._format_response(
                text_sa=f"साधु! स्वागतम् अस्ति भवतां {name_deva}-महोदय/महोदये!",
                text_iast=f"Sādhu! Svāgatam asti bhavatāṃ {to_iast(name_deva)}-mahodya/mahodaye!",
                text_en=f"Wonderful to meet you, {name_extracted}! How can I assist you on your Sanskrit journey today?",
                follow_ups=["Teach me Sanskrit", "Tell me a Gita shloka", "Start a quiz", "Explain grammar"]
            )

        # 1. Check for Quiz triggers
        if any(w in msg_lower for w in ["quiz", "test me", "question", "प्रश्नोत्तरी", "pariksha", "परीक्षा"]):
            return self._handle_new_quiz()

        # 2. Check for Sandhi queries
        sandhi_resp = self._check_sandhi_query(raw_msg, msg_norm)
        if sandhi_resp:
            return sandhi_resp

        # 3. Check for Shabdarupa (Noun declensions)
        shabda_resp = self._check_shabdarupa_query(raw_msg, msg_norm)
        if shabda_resp:
            return shabda_resp

        # 4. Check for Dhaturupa (Verb conjugations)
        dhatu_resp = self._check_dhaturupa_query(raw_msg, msg_norm)
        if dhatu_resp:
            return dhatu_resp

        # 5. Check for Morphological analysis
        morph_resp = self._check_morphology_query(raw_msg, msg_norm)
        if morph_resp:
            return morph_resp

        # 6. Check for Shloka / Subhashita / Gita
        if any(w in msg_lower for w in ["shloka", "sloka", "subhashita", "subhashitam", "gita", "verse", "श्लोक", "सुभाषित", "गीता"]):
            return self._handle_shloka_query(raw_msg, msg_lower)

        # 7. Check Dictionary / Translation lookup
        dict_resp = self._check_dictionary_query(raw_msg, msg_norm)
        if dict_resp:
            return dict_resp

        # 8. Check semantic match against knowledge base & greetings
        kb_resp = self._semantic_match(raw_msg, msg_norm)
        if kb_resp:
            return kb_resp

        # 9. Conversational fallback
        return self._handle_fallback(raw_msg)

    def _extract_user_name(self, text: str) -> Optional[str]:
        # Sanskrit patterns: mama nama [name] asti
        m = re.search(r'(?:मम\s+नाम|mama\s+nama|my\s+name\s+is|i\s+am)\s+([A-Za-z\u0900-\u097F]+)', text, re.IGNORECASE)
        if m:
            candidate = m.group(1).strip()
            if candidate.lower() not in ["kim", "what", "asti", "अस्ति"]:
                return candidate
        return None

    def _parse_quiz_answer(self, text: str) -> Optional[int]:
        t = text.strip()
        # Direct numbers 1, 2, 3, 4
        if t in ["1", "2", "3", "4"]:
            return int(t) - 1
        # Letters a, b, c, d
        mapping = {"a": 0, "b": 1, "c": 2, "d": 3, "option 1": 0, "option 2": 1, "option 3": 2, "option 4": 3}
        if t in mapping:
            return mapping[t]
        return None

    def _handle_new_quiz(self) -> Dict[str, Any]:
        q = self.quiz.get_random_question()
        self.context["active_quiz"] = q["id"]

        options_text = "\n".join([f"**{i+1}.** {opt}" for i, opt in enumerate(q["options"])])

        html_card = f"""
        <div class="quiz-box card">
            <div class="quiz-category">🏷️ {q['category']}</div>
            <div class="quiz-question-sa">{q['question_sa']}</div>
            <div class="quiz-question-en">{q['question_en']}</div>
            <div class="quiz-options">
                {''.join([f'<button class="btn-quiz-option" onclick="sendQuizAnswer({i+1})"><span class="opt-num">{i+1}</span> {opt}</button>' for i, opt in enumerate(q["options"])])}
            </div>
        </div>
        """

        return self._format_response(
            text_sa=f"प्रश्नोत्तरी आरब्धा! {q['question_sa']}",
            text_iast=f"Praśnottarī ārabdhā! {to_iast(q['question_sa'])}",
            text_en=f"{q['question_en']}\n\n{options_text}\n\n*(Type 1, 2, 3, or 4 or click an option above)*",
            html_content=html_card,
            follow_ups=["1", "2", "3", "4"],
            intent="quiz_question"
        )

    def _handle_quiz_submission(self, answer_idx: int) -> Dict[str, Any]:
        qid = self.context["active_quiz"]
        result = self.quiz.evaluate_answer(qid, answer_idx)
        self.context["active_quiz"] = None  # clear active question

        self.context["quiz_score"]["total"] += 1
        if result["is_correct"]:
            self.context["quiz_score"]["correct"] += 1
            status_sa = "साधु! समीचीनम् उत्तरम्! (Correct!) 🎉"
            status_en = f"Splendid! That's correct! Answer: **{result['correct_answer']}**"
        else:
            status_sa = "अहो! उत्तरं न समीचीनम्। (Incorrect) 💡"
            status_en = f"Not quite. The correct answer was **{result['correct_answer']}**."

        total = self.context["quiz_score"]["total"]
        corr = self.context["quiz_score"]["correct"]
        score_summary = f"\n\n**Your Current Score:** {corr}/{total} ({int(corr/total*100)}%)"

        html_card = f"""
        <div class="quiz-result-box {'success' if result['is_correct'] else 'notice'}">
            <h4>{'✅ साधु! समीचीनम्!' if result['is_correct'] else '❌ प्रयत्नः उत्तमः!'}</h4>
            <p><strong>Correct Answer:</strong> {result['correct_answer']}</p>
            <p><strong>विवरणम् (Explanation):</strong> {result['explanation']}</p>
            <div class="score-badge">Total Score: {corr} / {total}</div>
        </div>
        """

        return self._format_response(
            text_sa=status_sa,
            text_iast=to_iast(status_sa),
            text_en=f"{status_en}\n\n**विवरणम् (Explanation):** {result['explanation']}{score_summary}",
            html_content=html_card,
            follow_ups=["Next Quiz Question", "Teach me grammar", "Tell me a shloka"],
            intent="quiz_result"
        )

    def _check_sandhi_query(self, raw: str, norm: str) -> Optional[Dict[str, Any]]:
        # Check if user typed "word1 + word2"
        if "+" in raw:
            parts = [p.strip() for p in raw.split("+")]
            if len(parts) == 2 and parts[0] and parts[1]:
                res = self.sandhi.join_words(parts[0], parts[1])
                html_card = f"""
                <div class="sandhi-result card">
                    <div class="sandhi-formula"><strong>{parts[0]}</strong> + <strong>{parts[1]}</strong> = <span class="highlight-result">{res['joined']}</span> ({res['joined_iast']})</div>
                    <div class="sandhi-rule"><strong>नियमः (Rule):</strong> {res['rule_name']} — <em>{res['sutra']}</em></div>
                    <p class="sandhi-expl">{res['explanation']}</p>
                </div>
                """
                return self._format_response(
                    text_sa=f"{parts[0]} + {parts[1]} = {res['joined']}। (सन्धिः: {res['rule_name']})",
                    text_iast=f"{to_iast(parts[0])} + {to_iast(parts[1])} = {res['joined_iast']} ({to_iast(res['rule_name'])})",
                    text_en=f"Sandhi Result: **{res['joined']}** ({res['joined_iast']})\nRule: **{res['rule_name']}** ({res['sutra']})\n{res['explanation']}",
                    html_content=html_card,
                    follow_ups=["Explain Dirgha Sandhi", "Explain Guna Sandhi", "Join vidya + alaya"],
                    intent="sandhi_join"
                )

        # Check for sandhi rule explanation queries
        for r in SANDHI_RULES:
            rule_key = normalize_sanskrit(r["name"])
            sutra_key = normalize_sanskrit(r["sutra"])
            if (rule_key in norm or sutra_key in norm or
                ("sandhi" in norm and any(k in norm for k in rule_key.split()))):
                ex_text = "\n".join([f"- **{ex['split']}** = **{ex['joined']}** ({ex['meaning']})" for ex in r["examples"]])
                html_card = f"""
                <div class="sandhi-card card">
                    <h3>{r['name']}</h3>
                    <div class="sutra-badge">सूत्रम्: {r['sutra']}</div>
                    <p><strong>Rule:</strong> {r['rule']}</p>
                    <h5>उदाहरणानि (Examples):</h5>
                    <ul>
                        {''.join([f"<li><code>{ex['split']}</code> &rarr; <strong>{ex['joined']}</strong> ({ex['meaning']})</li>" for ex in r['examples']])}
                    </ul>
                </div>
                """
                return self._format_response(
                    text_sa=f"सन्धि-नियमः: {r['name']}। सूत्रम्: {r['sutra']}।",
                    text_iast=to_iast(f"{r['name']} | {r['sutra']}"),
                    text_en=f"### {r['name']}\n**सूत्रम् (Sutra):** {r['sutra']}\n**Explanation:** {r['rule']}\n\n**Examples:**\n{ex_text}",
                    html_content=html_card,
                    follow_ups=["विद्या + आलयः", "नर + ईशः", "नमः + ते"],
                    intent="sandhi_explanation"
                )

        return None

    def _check_shabdarupa_query(self, raw: str, norm: str) -> Optional[Dict[str, Any]]:
        if any(w in norm for w in ["shabda", "shabdarupa", "declension", "noun table", "विभक्ति", "शब्दरूप"]):
            # Find target noun
            for key, data in SHABDARUPA_DATA.items():
                if key in norm or data["word"] in raw or normalize_sanskrit(data["transliteration"]) in norm:
                    md_table = self.grammar.format_shabda_markdown(data)
                    rows_html = "".join([
                        f"<tr><td>{r['vibhakti']}</td><td><strong>{r['singular']}</strong></td><td>{r['dual']}</td><td>{r['plural']}</td><td>{r['usage']}</td></tr>"
                        for r in data["table"]
                    ])
                    html_card = f"""
                    <div class="table-card card">
                        <h3>शब्दरूपम्: {data['word']} ({data['transliteration']})</h3>
                        <p class="subtitle">{data['type']} &bull; {data['meaning']}</p>
                        <div class="table-wrapper">
                            <table class="sanskrit-table">
                                <thead>
                                    <tr><th>विभक्तिः</th><th>एकवचनम्</th><th>द्विवचनम्</th><th>बहुवचनम्</th><th>Usage</th></tr>
                                </thead>
                                <tbody>
                                    {rows_html}
                                </tbody>
                            </table>
                        </div>
                    </div>
                    """
                    return self._format_response(
                        text_sa=f"अत्र '{data['word']}' शब्दस्य रूपाणि सन्ति।",
                        text_iast=f"Atra '{data['transliteration']}' śabdasya rūpāṇi santi.",
                        text_en=md_table,
                        html_content=html_card,
                        follow_ups=["Lata shabda", "Phala shabda", "Asmad declension", "Path dhatu"],
                        intent="shabdarupa_lookup"
                    )

        # Direct search by noun name alone if followed by shabda
        for key, data in SHABDARUPA_DATA.items():
            if f"{key} table" in norm or f"{key} declension" in norm or f"{data['word']} रूप" in raw:
                md_table = self.grammar.format_shabda_markdown(data)
                return self._format_response(
                    text_sa=f"अत्र '{data['word']}' शब्दस्य रूपाणि सन्ति।",
                    text_iast=f"Atra '{data['transliteration']}' śabdasya rūpāṇi santi.",
                    text_en=md_table,
                    follow_ups=["Rama shabda", "Asmad declension", "Path dhatu"],
                    intent="shabdarupa_lookup"
                )

        return None

    def _check_dhaturupa_query(self, raw: str, norm: str) -> Optional[Dict[str, Any]]:
        if any(w in norm for w in ["dhatu", "dhaturupa", "conjugate", "conjugation", "verb", "धातु", "लकार"]):
            for key, data in DHATURUPA_DATA.items():
                if key in norm or data["dhatu"] in raw or normalize_sanskrit(data["transliteration"]) in norm:
                    md_table = self.grammar.format_dhatu_markdown(data)
                    return self._format_response(
                        text_sa=f"अत्र '{data['dhatu']}' धातोः रूपाणि सन्ति।",
                        text_iast=f"Atra '{data['transliteration']}' dhātoḥ rūpāṇi santi.",
                        text_en=md_table,
                        follow_ups=["Gam dhatu", "Kri dhatu", "Rama shabda", "Start quiz"],
                        intent="dhaturupa_lookup"
                    )
        return None

    def _check_morphology_query(self, raw: str, norm: str) -> Optional[Dict[str, Any]]:
        # Single Sanskrit word analysis or "analyze [word]"
        tokens = raw.replace("?", "").replace("!", "").split()
        target_token = None
        if len(tokens) == 1 and (is_devanagari(tokens[0]) or len(tokens[0]) > 3):
            target_token = tokens[0]
        elif len(tokens) in [2, 3] and any(w in norm for w in ["meaning", "what is", "analyze", "पदपरिचयः", "पदपरिचय"]):
            target_token = tokens[-1]

        if target_token:
            morphs = self.grammar.analyze_word(target_token)
            if morphs:
                m_details = []
                for m in morphs:
                    if m["type"] == "shabda":
                        m_details.append(f"- **शब्दः**: {m['base']} ({m['transliteration']}) | **विभक्तिः**: {m['vibhakti']} | **वचनम्**: {m['vachana']} | **अर्थः**: {m['usage']}")
                    elif m["type"] == "dhatu":
                        m_details.append(f"- **धातुः**: {m['base']} ({m['transliteration']}) | **लकारः**: {m['lakara']} | **पुरुषः**: {m['purusha']} | **वचनम्**: {m['vachana']} | **अर्थः**: {m['meaning']}")

                return self._format_response(
                    text_sa=f"पदपरिचयः: '{target_token}'",
                    text_iast=f"Padaparicayaḥ: '{to_iast(target_token)}'",
                    text_en=f"### Morphological Analysis for **{target_token}**:\n" + "\n".join(m_details),
                    follow_ups=["Conjugate पठ्", "Rama shabda", "Start quiz"],
                    intent="morphology_analysis"
                )

        return None

    def _handle_shloka_query(self, raw: str, lower: str) -> Dict[str, Any]:
        # Check if user mentioned a specific shloka topic (gita, karmanye, vidya, udyamena, vasudhaiva, sarve)
        matched = None
        for s in SUBHASHITA_COLLECTION:
            if s["id"] in lower or any(word in lower for word in s["id"].split("_")):
                matched = s
                break

        if not matched:
            matched = random.choice(SUBHASHITA_COLLECTION)

        html_card = f"""
        <div class="shloka-card card">
            <div class="shloka-source">📜 {matched['source']}</div>
            <div class="shloka-sanskrit">{matched['shloka_sa'].replace(chr(10), '<br>')}</div>
            <div class="shloka-iast">{matched['shloka_iast'].replace(chr(10), '<br>')}</div>
            <hr/>
            <div class="shloka-breakdown">
                <p><strong>पदच्छेदः (Word division):</strong> {matched['padachheda']}</p>
                <p><strong>अन्वयः (Prose order):</strong> {matched['anvaya']}</p>
            </div>
            <div class="shloka-meaning">
                <p><strong>English Meaning:</strong> {matched['meaning_en']}</p>
                <p><strong>💡 Philosophical Lesson:</strong> <em>{matched['lesson']}</em></p>
            </div>
        </div>
        """

        return self._format_response(
            text_sa=matched["shloka_sa"],
            text_iast=matched["shloka_iast"],
            text_en=f"### {matched['title']}\n**Source:** {matched['source']}\n\n**पदच्छेदः (Word division):** {matched['padachheda']}\n\n**अन्वयः (Prose order):** {matched['anvaya']}\n\n**Meaning:** {matched['meaning_en']}\n\n**💡 Lesson:** {matched['lesson']}",
            html_content=html_card,
            follow_ups=["Another Shloka", "Gita 2.47", "Vasudhaiva Kutumbakam", "Quiz on this Shloka"],
            intent="shloka_verse"
        )

    def _check_dictionary_query(self, raw: str, norm: str) -> Optional[Dict[str, Any]]:
        for entry in DICTIONARY_WORDS:
            sa_norm = normalize_sanskrit(entry["sa"])
            iast_norm = normalize_sanskrit(entry["iast"])
            en_words = [w.strip() for w in entry["en"].lower().split("/")]

            # If user queried the Sanskrit word
            if sa_norm == norm or iast_norm == norm or entry["sa"] in raw:
                return self._format_response(
                    text_sa=f"{entry['sa']} ({entry['iast']}) = {entry['en']} [{entry['type']}].",
                    text_iast=f"{entry['iast']} = {entry['en']}.",
                    text_en=f"### शब्दार्थः (Dictionary):\n- **संस्कृतम्**: {entry['sa']} ({entry['iast']})\n- **English**: {entry['en']}\n- **Type**: {entry['type']}",
                    follow_ups=["Another word", "Shabdarupa table", "Start quiz"],
                    intent="dictionary_lookup"
                )

            # If user asked "how to say [word] in sanskrit" or asked the English word
            if any(ew in norm for ew in en_words) and ("sanskrit" in norm or "say" in norm or "meaning" in norm or len(norm.split()) <= 2):
                return self._format_response(
                    text_sa=f"आङ्ग्लपदस्य '{entry['en']}' संस्कृतम् अस्ति: **{entry['sa']}** ({entry['iast']})।",
                    text_iast=f"Āṅglapadasya '{entry['en']}' saṃskṛtam asti: {entry['iast']}.",
                    text_en=f"In Sanskrit, **'{entry['en']}'** is expressed as:\n- **{entry['sa']}** ({entry['iast']})\n- Part of speech: {entry['type']}",
                    follow_ups=[f"Use {entry['sa']} in sentence", "Another vocabulary word", "Start quiz"],
                    intent="translation_lookup"
                )

        return None

    def _semantic_match(self, raw: str, norm: str) -> Optional[Dict[str, Any]]:
        try:
            vec = self.vectorizer.transform([norm])
            scores = cosine_similarity(vec, self.tfidf_matrix)[0]
            best_idx = scores.argmax()
            best_score = scores[best_idx]

            if best_score > 0.45:
                label_type, item = self.intent_labels[best_idx]
                if label_type == "greeting":
                    return self._format_response(
                        text_sa=item["response_sa"],
                        text_iast=item["response_iast"],
                        text_en=item["response_en"],
                        follow_ups=item.get("follow_ups", []),
                        intent=item["intent"]
                    )
                elif label_type == "shloka_direct":
                    return self._handle_shloka_query(raw, item["id"])
        except Exception:
            pass

        return None

    def _handle_fallback(self, raw: str) -> Dict[str, Any]:
        """Graceful, culturally authentic fallback for unclassified inputs."""
        # Check if typed in Sanskrit or Romanized
        if is_devanagari(raw):
            return self._format_response(
                text_sa="भवतः वचनं मया ज्ञातम्। कृपया अग्रे वदतु अथवा व्याकरण-श्लोक-प्रश्नोत्तरी-विषये पृच्छतु।",
                text_iast="Bhavataḥ vacanaṃ mayā jñātam. Kṛpayā agre vadatu athavā vyākaraṇa-śloka-praśnottarī-viṣaye pṛcchatu.",
                text_en="I hear and understand your Sanskrit expression! You can ask me to conjugate verbs, decline nouns, explain sandhi, recite shlokas, or launch an interactive quiz.",
                follow_ups=["सुभाषितम् श्रावयतु (Tell a shloka)", "पठ् धातुरूपम् (Conjugate path)", "प्रश्नोत्तरी (Start quiz)", "कथम् अस्ति भवान्?"]
            )
        else:
            return self._format_response(
                text_sa="अहं भवतां वचनम् अवगन्तुं यते। कृपया अन्यत् किमपि पृच्छतु।",
                text_iast="Ahaṃ bhavatāṃ vacanam avagantuṃ yate. Kṛpayā anyat kimapi pṛcchatu.",
                text_en="I am your dedicated Sanskrit companion! You can ask me to:\n- **Conjugate verbs** (e.g. *Conjugate path / gam*)\n- **Decline nouns** (e.g. *Rama / Lata shabda*)\n- **Analyze words** (e.g. *What is पठामि?*)\n- **Solve Sandhi** (e.g. *vidya + alaya*)\n- **Explore Gita & Subhashita** (e.g. *Tell me a shloka*)\n- **Test your knowledge** (e.g. *Start Sanskrit quiz*)",
                follow_ups=["Tell me a Gita shloka", "Rama shabda rupa", "vidya + alaya", "Start quiz"],
                intent="general_fallback"
            )

    def _format_response(
        self,
        text_sa: str,
        text_iast: str,
        text_en: str,
        html_content: Optional[str] = None,
        follow_ups: Optional[List[str]] = None,
        intent: str = "general"
    ) -> Dict[str, Any]:
        self.context["last_intent"] = intent

        # Audio text: clean Sanskrit for TTS
        audio_text = re.sub(r'[\*\#\_\|\[\]\(\)]', '', text_sa).strip()

        return {
            "text_sa": text_sa,
            "text_iast": text_iast,
            "text_en": text_en,
            "html_content": html_content,
            "audio_text": audio_text,
            "follow_ups": follow_ups or ["नमस्ते", "Subhashita", "Grammar", "Quiz"],
            "intent": intent,
            "turn_count": self.context["turn_count"]
        }
