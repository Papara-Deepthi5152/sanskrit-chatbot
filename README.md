# वाग्देवी • Vāgdevī — Sanskrit Conversational AI Chatbot

> **संस्कृत-संभाषणम् • व्याकरणम् • सुभाषितानि • प्रश्नोत्तरी**
> An intelligent, multi-modal Sanskrit conversational companion, grammar tutor, and Vedic wisdom explorer.

---

## 🌟 Key Features

1. **Dual-Script Conversational AI**:
   - Chat in **Devanagari script** (e.g. `नमस्ते`, `कथम् अस्ति भवान्?`), **Roman transliteration / IAST** (e.g. `namaskarah`, `katham asti`), or **English** (e.g. `How do I say thank you?`).
   - Responses formatted with authentic Devanagari Sanskrit, Roman transliteration (IAST), and English explanation.

2. **Paninian Grammar Tutor (व्याकरणम्)**:
   - **Shabdarupa (Noun Declensions)**: Complete tables across all 8 Vibhaktis (cases) and 3 Vachanas (numbers) for `राम` (Rāma), `लता` (Latā), `फल` (Phala), `अस्मद्` (Asmad), `युष्मद्` (Yuṣmad), and more.
   - **Dhaturupa (Verb Conjugations)**: Conjugations across Lakaras (लट् Present, लङ् Past, लृट् Future, लोट् Imperative) for roots like `पठ्` (Paṭh), `गम्` (Gam), `कृ` (Kṛ), `भू` (Bhū).
   - **Morphological Word Analyzer**: Dissects arbitrary Sanskrit words into base root/stem, case/tense, person, number, and syntactic meaning (e.g. `पठामि` &rarr; Verb `पठ्`, Present Tense, 1st Person Singular).

3. **Sandhi Studio (सन्धि-शाला)**:
   - Interactive sandhi solver: join words like `विद्या + आलयः` &rarr; `विद्यालयः` with Paninian rule identification (`अकः सवर्णे दीर्घः`).
   - Comprehensive rulebook covering Dirgha, Guna, Vriddhi, Yan, Ayadi, and Visarga Sandhis.

4. **Bhagavad Gita & Subhashita Library (सुभाषितानि)**:
   - Classical verses with original Sanskrit, Roman IAST, word-by-word division (**पदच्छेदः**), prose sentence ordering (**अन्वयः**), and philosophical reflection.

5. **Gamified Practice Quiz (प्रश्नोत्तरी)**:
   - Interactive multiple-choice tests with real-time score tracking, immediate evaluation, and pedagogical explanations.

6. **Audio Speech Synthesis & Recognition**:
   - **Text-to-Speech (TTS)**: Listen to correct Sanskrit pronunciation for any reply using the Web Speech API.
   - **Speech-to-Text (STT)**: Speak directly into the microphone to chat hands-free.

7. **Devanagari Helper & Transliteration Preview**:
   - Virtual character and phrase toolbar for seamless typing of special Sanskrit diacritics (ः, ं, ँ, ऽ, etc.).
   - Real-time phonetic transliteration preview box.

---

## 🚀 Quick Start Guide

### 1. Run the Web Application
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### 2. Run in Terminal (CLI Mode)
```bash
python cli_chat.py
```
Enjoy an interactive, colorized terminal chat session with instant Devanagari output and helpful suggestions!

### 3. Run Automated Tests
```bash
python -m unittest tests/test_chatbot.py
```

---

## 📁 Project Architecture

```
sanskrit-chatbot/
├── app.py                      # Flask Web server & REST API
├── cli_chat.py                 # Colorized terminal chat interface
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── engine/                     # Sanskrit NLP & Linguistics Engine
│   ├── __init__.py
│   ├── transliteration.py      # Bidirectional Devanagari <-> IAST converter
│   ├── knowledge_base.py       # Curated dialogues, shlokas, grammar & dictionary
│   ├── grammar_engine.py       # Shabdarupa, Dhaturupa & morphological parser
│   ├── sandhi_engine.py        # Sandhi solver & Paninian rule matcher
│   ├── quiz_engine.py          # Interactive quiz question generator
│   └── dialogue_manager.py     # Intent router, memory & context manager
├── templates/
│   └── index.html              # Modern Vedic-themed responsive UI
├── static/
│   ├── css/
│   │   └── style.css           # Styling, typography & animations
│   └── js/
│       └── chat.js             # Chat client, Web Speech TTS/STT & tab controllers
└── tests/
    └── test_chatbot.py         # 21 unit & integration tests
```

---

## 🌐 REST API Endpoints

- `POST /api/chat`: Process message with session context (`{"message": "string"}`)
- `GET /api/shloka-of-the-day`: Returns a wisdom verse with padachheda and anvaya
- `GET /api/quiz/question`: Returns a random quiz question
- `POST /api/quiz/answer`: Evaluates quiz answer and updates score
- `POST /api/transliterate`: Converts English phonetic text to Devanagari and IAST
- `POST /api/sandhi`: Phonetically joins two Sanskrit words and identifies the rule
- `GET /api/grammar/shabda/<name>`: Retrieves full 8-case declension table
- `GET /api/grammar/dhatu/<name>`: Retrieves full conjugation table across Lakaras
- `GET /api/rules/sandhi`: Lists standard Sandhi rules with examples

---

*जयतु संस्कृतम्! जयतु भारतम्!*
