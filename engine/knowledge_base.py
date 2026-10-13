"""
Sanskrit Chatbot Knowledge Base
Contains conversational patterns, Gita & Subhashita verses,
Vyakarana (Grammar) tables, Sandhi rules, and bilingual vocabulary.
"""

from typing import Dict, List, Any, Optional

GREETINGS_DATA = [
    {
        "intent": "greeting_general",
        "patterns": [
            "namaste", "namaskarah", "namaskaram", "namaskar", "namaste ji",
            "नमस्कारः", "नमस्ते", "हरि ॐ", "hari om", "pranam", "प्रणामः"
        ],
        "response_sa": "नमो नमः! भवते/भवत्यै नमस्कारः। अद्य अहं भवतां कथं साहाय्यं कर्तुं शक्नोमि?",
        "response_iast": "Namo namaḥ! Bhavate/Bhavatyai namaskāraḥ. Adya ahaṃ bhavatāṃ kathaṃ sāhāyyaṃ kartuṃ śaknomi?",
        "response_en": "Salutations! Greetings to you. How may I assist you today in the world of Sanskrit?",
        "follow_ups": ["कथम् अस्ति भवान्?", "Tell me a shloka", "Explain Rama shabda", "Translate something"]
    },
    {
        "intent": "greeting_morning",
        "patterns": [
            "suprabhatam", "shubhaprabhatam", "good morning", "subhaprabhatam",
            "सुप्रभातम्", "शुभप्रभातम्"
        ],
        "response_sa": "शुभप्रभातम्! भवताम् अयं दिवसः मङ्गलमयः, सुखदः, ज्ञानवर्धकः च भवतु।",
        "response_iast": "Śubhaprabhātam! Bhavatām ayaṃ divasaḥ maṅgalamayaḥ, sukhadaḥ, jñānavardhakaḥ ca bhavatu.",
        "response_en": "Good morning! May this day be auspicious, joyous, and filled with learning for you.",
        "follow_ups": ["अद्यतन सुभाषितम् (Shloka of the day)", "कथम् अस्ति भवान्?", "Sanskrit quiz"]
    },
    {
        "intent": "greeting_evening_night",
        "patterns": [
            "shubharatrih", "shubharatri", "good night", "shubhasandhya", "good evening",
            "शुभरात्रिः", "शुभसन्ध्या", "शुभदिनम्"
        ],
        "response_sa": "शुभसन्ध्या / शुभरात्रिः! शान्तिमयं सुखदं च शयनं भवतु। पुनर्मिलामः!",
        "response_iast": "Śubhasandhyā / Śubharātriḥ! Śāntimayaṃ sukhadaṃ ca śayanaṃ bhavatu. Punarmilāmaḥ!",
        "response_en": "Good evening / Good night! May you have peaceful and restorative rest. Until we meet again!",
        "follow_ups": ["पुनर्मिलामः (See you again)", "Peace prayer (शान्तिमन्त्रः)"]
    },
    {
        "intent": "how_are_you",
        "patterns": [
            "katham asti bhavan", "katham asti", "how are you", "katham asi",
            "कथम् अस्ति भवान्", "कथम् अस्ति भवती", "कथमस्ति", "कथम् अस्ति", "kushalam va", "कुशलं वा"
        ],
        "response_sa": "अहं कुशली अस्मि! सर्वं कुशलम्। भवान् (भवती) कथम् अस्ति? भवतां संस्कृत-अध्ययनं कथं प्रचलति?",
        "response_iast": "Ahaṃ kuśalī asmi! Sarvaṃ kuśalam. Bhavān (Bhavatī) katham asti? Bhavatāṃ saṃskṛta-adhyayanam kathaṃ pracalati?",
        "response_en": "I am well! All is well with me. How are you? How is your Sanskrit journey going?",
        "follow_ups": ["अहम् अपि कुशली (I am also well)", "Teach me Sanskrit", "Give me a quiz"]
    },
    {
        "intent": "user_fine",
        "patterns": [
            "aham kushali", "aham api kushali", "kushali asmi", "i am good", "i am fine", "all good",
            "अहं कुशली अस्मि", "कुशली", "उत्तमम्", "uttamam", "sarvam kushalam"
        ],
        "response_sa": "साधु! एतत् श्रुत्वा अतीव आनन्दः जातः। अद्य वयं किम् अध्येष्यामहे?",
        "response_iast": "Sādhu! Etat śrutvā atīva ānandaḥ jātaḥ. Adya vayaṃ kim adhyeṣyāmahe?",
        "response_en": "Splendid! So glad to hear that. What shall we learn or discuss today?",
        "follow_ups": ["व्याकरणम् (Grammar)", "सुभाषितानि (Wisdom verses)", "सम्भाषणम् (Conversation)"]
    },
    {
        "intent": "bot_identity",
        "patterns": [
            "bhavatah nama kim", "who are you", "what is your name", "your name",
            "भवतः नाम किम्", "भवत्याः नाम किम्", "का त्वम्", "कः त्वम्", "introduce yourself"
        ],
        "response_sa": "मम नाम 'वाग्देवी' (संस्कृत-मित्रम्) अस्ति! अहं भवतां संस्कृत-संभाषण-सहायकः, व्याकरण-मार्गदर्शकः च अस्मि।",
        "response_iast": "Mama nāma 'Vāgdevī' (Saṃskṛta-Mitram) asti! Ahaṃ bhavatāṃ saṃskṛta-sambhāṣaṇa-sahāyakaḥ, vyākaraṇa-mārgadarśakaḥ ca asmi.",
        "response_en": "My name is 'Vagdevi' (Sanskrit Friend)! I am your Sanskrit conversational companion and grammar guide.",
        "follow_ups": ["What can you do?", "Teach me basic phrases", "Test my Sanskrit"]
    },
    {
        "intent": "capabilities",
        "patterns": [
            "what can you do", "help", "features", "options", "commands",
            "साहाय्यम्", "भवतः सामर्थ्यं किम्", "how to use"
        ],
        "response_sa": "अहं विविधानि कार्याणि कर्तुं शक्नोमि:\n१. संस्कृत-सम्भाषणम् (Sanskrit conversation in Devanagari & English)\n२. व्याकरण-जिज्ञासा (Noun Shabdarupa, Verb Dhaturupa, Sandhi)\n३. गीता-श्लोकाः सुभाषितानि च (Verses with word breakdown & meaning)\n४. शब्दकोशः अनुवादः च (Sanskrit-English vocabulary & translation)\n५. प्रश्नोत्तरी (Interactive Sanskrit practice quiz)!",
        "response_iast": "Ahaṃ vividhāni kāryāṇi kartuṃ śaknomi:\n1. Saṃskṛta-sambhāṣaṇam\n2. Vyākaraṇa-jijñāsā\n3. Gītā-ślokāḥ subhāṣitāni ca\n4. Śabdakośaḥ anuvādaḥ ca\n5. Praśnottarī!",
        "response_en": "Here is what I can do:\n1. Conversational Sanskrit: Chat in Sanskrit or English\n2. Grammar Guru: Shabdarupa declensions, Dhatu conjugations, Sandhi rules\n3. Gita & Subhashita: Famous verses with word-by-word meanings\n4. Dictionary & Translation: High-frequency Sanskrit terms & sentences\n5. Interactive Quiz: Test your vocabulary and grammar!",
        "follow_ups": ["Tell me a Gita shloka", "Conjugate पठ् (path)", "Declension of राम (Rama)", "Start quiz"]
    },
    {
        "intent": "thank_you",
        "patterns": [
            "dhanyavadah", "dhanyavada", "thank you", "thanks", "dhanyavaad",
            "धन्यवादः", "धन्यवादाः", "आभारः"
        ],
        "response_sa": "स्वागतम्! भवते भूयो भूयः धन्यवादः। यदि अन्यत् किमपि पृच्छितुम् इच्छति, अवश्यं वदतु।",
        "response_iast": "Svāgatam! Bhavate bhūyo bhūyaḥ dhanyavādaḥ. Yadi anyat kimapi pṛcchitum icchati, avaśyaṃ vadatu.",
        "response_en": "You are welcome! Thank you as well. If there is anything else you'd like to ask, please do!",
        "follow_ups": ["पुनर्मिलामः", "One more shloka", "Grammar question"]
    },
    {
        "intent": "farewell",
        "patterns": [
            "punah milamah", "punarmilamah", "bye", "goodbye", "see you", "alvida",
            "पुनः मिलामः", "पुनर्मिलामः", "जयतु संस्कृतम्", "jayatu samskritam"
        ],
        "response_sa": "पुनर्मिलामः! भवतां दिवसः शुभः भूयात्। जयतु संस्कृतम्! जयतु भारतम्!",
        "response_iast": "Punarmilāmaḥ! Bhavatāṃ divasaḥ śubhaḥ bhūyāt. Jayatu Saṃskṛtam! Jayatu Bhāratam!",
        "response_en": "See you again! May your day be blessed. Victory to Sanskrit! Victory to Bharat!",
        "follow_ups": ["जयतु संस्कृतम्!"]
    }
]

SUBHASHITA_COLLECTION = [
    {
        "id": "gita_2_47",
        "title": "कर्मण्येवाधिकारस्ते (Karmanyevadhikaraste) - Bhagavad Gita 2.47",
        "shloka_sa": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।\nमा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि॥",
        "shloka_iast": "Karmaṇyevādhikāraste mā phaleṣu kadācana |\nMā karmaphalaheturbhūrmā te saṅgo'stvakarmaṇi ||",
        "source": "भगवद्गीता २.४७ (Bhagavad Gita 2.47)",
        "padachheda": "कर्मणि एव अधिकारः ते, मा फलेषु कदाचन। मा कर्म-फल-हेतुः भूः, मा ते सङ्गः अस्तु अकर्मणि॥",
        "anvaya": "ते अधिकारः कर्मणि एव, फलेषु कदाचन मा। कर्मफलहेतुः मा भूः, अकर्मणि ते सङ्गः मा अस्तु।",
        "meaning_en": "You have a right only to perform your duties, but never to the fruits of action. Let not the fruit of action be your motive, nor let there be any attachment to inaction.",
        "lesson": "Focus completely on the quality and integrity of your effort, free from anxiety about outcomes or paralysis of inaction."
    },
    {
        "id": "vidya_dadati_vinayam",
        "title": "विद्या ददाति विनयम् (Vidya Dadati Vinayam) - Hitopadesha",
        "shloka_sa": "विद्या ददाति विनयं विनयाद्याति पात्रताम्।\nपात्रत्वाद्धनमाप्नोति धनाद्धर्मं ततः सुखम्॥",
        "shloka_iast": "Vidyā dadāti vinayaṃ vinayādyāti pātratām |\nPātratvāddhanamāpnoti dhanāddharmaṃ tataḥ sukham ||",
        "source": "हितोपदेशः (Hitopadesha)",
        "padachheda": "विद्या ददाति विनयम्, विनयात् याति पात्रताम्। पात्रत्वात् धनम् आप्नोति, धनात् धर्मम्, ततः सुखम्॥",
        "anvaya": "विद्या विनयं ददाति, विनयात् पात्रतां याति, पात्रत्वात् धनम् आप्नोति, धनात् धर्मं (करोति), ततः सुखम् (भवति)।",
        "meaning_en": "True knowledge bestows humility; from humility comes worthiness/competence; from worthiness one attains wealth; from wealth one performs righteous duty (Dharma); and from Dharma comes genuine joy and peace.",
        "lesson": "Education begins with humility and culminates in righteous, peaceful living."
    },
    {
        "id": "udyamena_hi_sidhyanti",
        "title": "उद्यमेन हि सिध्यन्ति (Effort Alone Brings Success)",
        "shloka_sa": "उद्यमेन हि सिध्यन्ति कार्याणि न मनोरथैः।\nन हि सुप्तस्य सिंहस्य प्रविशन्ति मुखे मृगाः॥",
        "shloka_iast": "Udyamena hi sidhyanti kāryāṇi na manorathaiḥ |\nNa hi suptasya siṃhasya praviśanti mukhe mṛgāḥ ||",
        "source": "पञ्चतन्त्रम् (Panchatantra)",
        "padachheda": "उद्यमेन हि सिध्यन्ति कार्याणि न मनोरथैः। न हि सुप्तस्य सिंहस्य प्रविशन्ति मुखे मृगाः॥",
        "anvaya": "कार्याणि उद्यमेन हि सिध्यन्ति, मनोरथैः न। सुप्तस्य सिंहस्य मुखे मृगाः न हि प्रविशन्ति।",
        "meaning_en": "Tasks are accomplished only through diligence and active effort, never by mere daydreaming or wishing. Deer do not enter into the mouth of a sleeping lion on their own!",
        "lesson": "Action and persevering work are indispensable; even the king of beasts must hunt."
    },
    {
        "id": "vasudhaiva_kutumbakam",
        "title": "वसुधैव कुटुम्बकम् (The World is One Family) - Maha Upanishad",
        "shloka_sa": "अयं निजः परो वेति गणना लघुचेतसाम्।\nउदारचरितानां तु वसुधैव कुटुम्बकम्॥",
        "shloka_iast": "Ayaṃ nijaḥ paro veti gaṇanā laghucetasām |\nUdāracaritānāṃ tu vasudhaiva kuṭumbakam ||",
        "source": "महोपनिषद् ६.७१ (Maha Upanishad 6.71)",
        "padachheda": "अयम् निजः परः वा इति गणना लघु-चेतसाम्। उदार-चरितानाम् तु वसुधा एव कुटुम्बकम्॥",
        "anvaya": "अयम् निजः परः वा इति गणना लघुचेतसां (भवति)। उदारचरितानां तु वसुधा एव कुटुम्बकं (भवति)।",
        "meaning_en": "'This person is mine, that person is a stranger' is the narrow calculation of petty minds. For the noble and generous-hearted, the entire earth itself is one beloved family.",
        "lesson": "Universal empathy and global kinship transcend small-minded borders and prejudices."
    },
    {
        "id": "sarve_bhavantu_sukhinah",
        "title": "सर्वे भवन्तु सुखिनः (Universal Well-Being Mantra)",
        "shloka_sa": "सर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः।\nसर्वे भद्राणि पश्यन्तु मा कश्चिद्दुःखभाग्भवेत्॥",
        "shloka_iast": "Sarve bhavantu sukhinaḥ sarve santu nirāmayāḥ |\nSarve bhadrāṇi paśyantu mā kaścidduḥkhabhāgbhavet ||",
        "source": "बृहदारण्यकोपनिषद् / शान्तिमन्त्रः (Brihadaranyaka Upanishad)",
        "padachheda": "सर्वे भवन्तु सुखिनः, सर्वे सन्तु निरामयाः। सर्वे भद्राणि पश्यन्तु, मा कश्चित् दुःख-भाग् भवेत्॥",
        "anvaya": "सर्वे सुखिनः भवन्तु, सर्वे निरामयाः सन्तु, सर्वे भद्राणि पश्यन्तु, कश्चित् अपि दुःखभाग् मा भवेत्।",
        "meaning_en": "May all beings be happy. May all beings be free from illness and distress. May all behold what is good and auspicious. May no one suffer sorrow.",
        "lesson": "The pinnacle of Vedic prayer: wishing good health, peace, and delight to all of existence without exception."
    },
    {
        "id": "asato_ma_sadgamaya",
        "title": "असतो मा सद्गमय (Lead Me from Untruth to Truth)",
        "shloka_sa": "असतो मा सद्गमय।\nतमसो मा ज्योतिर्गमय।\nमृत्योर्मा अमृतं गमय॥\nॐ शान्तिः शान्तिः शान्तिः॥",
        "shloka_iast": "Asato mā sadgamaya |\nTamaso mā jyotirgamaya |\nMṛtyormā amṛtaṃ gamaya ||\nOṃ śāntiḥ śāntiḥ śāntiḥ ||",
        "source": "बृहदारण्यकोपनिषद् १.३.२८ (Brihadaranyaka Upanishad 1.3.28)",
        "padachheda": "असतः मा सत् गमय। तमसः मा ज्योतिः गमय। मृत्योः मा अमृतम् गमय॥",
        "anvaya": "मा असतः सत् गमय, तमसः ज्योतिः गमय, मृत्योः अमृतं गमय।",
        "meaning_en": "Lead me from the unreal/false to the Real/Truth. Lead me from darkness/ignorance to Light/Wisdom. Lead me from mortality to Immortality. Om Peace, Peace, Peace.",
        "lesson": "The eternal human prayer for spiritual awakening and clarity."
    },
    {
        "id": "gita_4_7",
        "title": "यदा यदा हि धर्मस्य (Descent of Dharma) - Bhagavad Gita 4.7",
        "shloka_sa": "यदा यदा हि धर्मस्य ग्लानिर्भवति भारत।\nअभ्युत्थानमधर्मस्य तदात्मानं सृजाम्यहम्॥",
        "shloka_iast": "Yadā yadā hi dharmasya glānirbhavati bhārata |\nAbhyutthānamadharmasya tadātmānaṃ sṛjāmyaham ||",
        "source": "भगवद्गीता ४.७ (Bhagavad Gita 4.7)",
        "padachheda": "यदा यदा हि धर्मस्य ग्लानिः भवति, भारत। अभ्युत्थानम् अधर्मस्य, तदा आत्मानम् सृजामि अहम्॥",
        "anvaya": "हे भारत! यदा यदा हि धर्मस्य ग्लानिः, अधर्मस्य च अभ्युत्थानं भवति, तदा अहम् आत्मानं सृजामि।",
        "meaning_en": "Whenever and wherever there is a decline of righteousness (Dharma), O Bharata, and a predominant rise of unrighteousness (Adharma), at that time I manifest Myself.",
        "lesson": "Righteousness is an eternal cosmological principle that restores balance against oppression."
    },
    {
        "id": "na_chora_haaryam",
        "title": "न चोरहार्यं न च राजहार्यं (The Incomparable Wealth of Knowledge)",
        "shloka_sa": "न चोरहार्यं न च राजहार्यं न भ्रातृभाज्यं न च भारकारि।\nव्यये कृते वर्धत एव नित्यं विद्याधनं सर्वधनप्रधानम्॥",
        "shloka_iast": "Na corahāryaṃ na ca rājahāryaṃ na bhrātṛbhājyaṃ na ca bhārakāri |\nVyaye kṛte vardhata eva nityaṃ vidyādhanaṃ sarvadhanapradhānam ||",
        "source": "सुभाषितरत्नभाण्डागारम् (Subhashita Ratnabhandagaram)",
        "padachheda": "न चोर-हार्यम् न च राज-हार्यम्, न भ्रातृ-भाज्यम् न च भार-कारि। व्यये कृते वर्धते एव नित्यम्, विद्या-धनम् सर्व-धन-प्रधानम्॥",
        "anvaya": "विद्याधनं न चोरहार्यं, न च राजहार्यं, न भ्रातृभाज्यं, न च भारकारि। व्यये कृते नित्यं वर्धते एव। अतः विद्याधनं सर्वधनप्रधानम्।",
        "meaning_en": "Knowledge is a treasure that cannot be stolen by thieves, confiscated by kings, divided among brothers, nor is it a heavy burden to carry. The more it is spent and shared, the more it perpetually grows. Truly, the wealth of knowledge is supreme among all wealth!",
        "lesson": "Knowledge is the only possession that multiplies when shared and cannot be depleted or robbed."
    }
]

SHABDARUPA_DATA = {
    "rama": {
        "word": "राम",
        "transliteration": "Rāma",
        "type": "अकारान्तः पुंल्लिङ्गः (Akārāntaḥ Puṃlliṅgaḥ - Masculine ending in 'a')",
        "meaning": "Lord Rama / Delight / Beautiful",
        "table": [
            {"vibhakti": "प्रथमा (Nominative)", "singular": "रामः", "dual": "रामौ", "plural": "रामाः", "usage": "Subject (Rama)"},
            {"vibhakti": "द्वितीया (Accusative)", "singular": "रामम्", "dual": "रामौ", "plural": "रामान्", "usage": "Object (to Rama)"},
            {"vibhakti": "तृतीया (Instrumental)", "singular": "रामेण", "dual": "रामाभ्याम्", "plural": "रामैः", "usage": "By / with Rama"},
            {"vibhakti": "चतुर्थी (Dative)", "singular": "रामाय", "dual": "रामाभ्याम्", "plural": "रामेभ्यः", "usage": "For / to Rama"},
            {"vibhakti": "पञ्चमी (Ablative)", "singular": "रामात्", "dual": "रामाभ्याम्", "plural": "रामेभ्यः", "usage": "From Rama"},
            {"vibhakti": "षष्ठी (Genitive)", "singular": "रामस्य", "dual": "रामयोः", "plural": "रामाणाम्", "usage": "Of Rama's"},
            {"vibhakti": "सप्तमी (Locative)", "singular": "रामे", "dual": "रामयोः", "plural": "रामेषु", "usage": "In / on Rama"},
            {"vibhakti": "सम्बोधनम् (Vocative)", "singular": "हे राम!", "dual": "हे रामौ!", "plural": "हे रामाः!", "usage": "O Rama!"}
        ]
    },
    "lata": {
        "word": "लता",
        "transliteration": "Latā",
        "type": "आकारान्तः स्त्रीलिङ्गः (Ākārāntaḥ Strīliṅgaḥ - Feminine ending in 'ā')",
        "meaning": "Creeper / Vine",
        "table": [
            {"vibhakti": "प्रथमा", "singular": "लता", "dual": "लते", "plural": "लताः", "usage": "Creeper"},
            {"vibhakti": "द्वितीया", "singular": "लताम्", "dual": "लते", "plural": "लताः", "usage": "To the creeper"},
            {"vibhakti": "तृतीया", "singular": "लतया", "dual": "लताभ्याम्", "plural": "लताभिः", "usage": "With the creeper"},
            {"vibhakti": "चतुर्थी", "singular": "लतायै", "dual": "लताभ्याम्", "plural": "लताभ्यः", "usage": "For the creeper"},
            {"vibhakti": "पञ्चमी", "singular": "लतायाः", "dual": "लताभ्याम्", "plural": "लताभ्यः", "usage": "From the creeper"},
            {"vibhakti": "षष्ठी", "singular": "लतायाः", "dual": "लतयोः", "plural": "लतानाम्", "usage": "Of the creeper"},
            {"vibhakti": "सप्तमी", "singular": "लतायाम्", "dual": "लतयोः", "plural": "लतासु", "usage": "In the creeper"},
            {"vibhakti": "सम्बोधनम्", "singular": "हे लते!", "dual": "हे लते!", "plural": "हे लताः!", "usage": "O creeper!"}
        ]
    },
    "phala": {
        "word": "फल",
        "transliteration": "Phala",
        "type": "अकारान्तः नपुंसकलिङ्गः (Akārāntaḥ Napuṃsakaliṅgaḥ - Neuter ending in 'a')",
        "meaning": "Fruit / Result",
        "table": [
            {"vibhakti": "प्रथमा", "singular": "फलम्", "dual": "फले", "plural": "फलानि", "usage": "Fruit"},
            {"vibhakti": "द्वितीया", "singular": "फलम्", "dual": "फले", "plural": "फलानि", "usage": "To fruit"},
            {"vibhakti": "तृतीया", "singular": "फलेन", "dual": "फलाभ्याम्", "plural": "फलैः", "usage": "By fruit"},
            {"vibhakti": "चतुर्थी", "singular": "फलाय", "dual": "फलाभ्याम्", "plural": "फलेभ्यः", "usage": "For fruit"},
            {"vibhakti": "पञ्चमी", "singular": "फलात्", "dual": "फलाभ्याम्", "plural": "फलेभ्यः", "usage": "From fruit"},
            {"vibhakti": "षष्ठी", "singular": "फलस्य", "dual": "फलयोः", "plural": "फलानाम्", "usage": "Of fruit"},
            {"vibhakti": "सप्तमी", "singular": "फले", "dual": "फलयोः", "plural": "फलेषु", "usage": "In fruit"},
            {"vibhakti": "सम्बोधनम्", "singular": "हे फल!", "dual": "हे फले!", "plural": "हे फलानि!", "usage": "O fruit!"}
        ]
    },
    "asmad": {
        "word": "अस्मद्",
        "transliteration": "Asmad",
        "type": "सर्वनाम (Pronoun - First Person: 'I / We')",
        "meaning": "I / Me / We (Common to all genders)",
        "table": [
            {"vibhakti": "प्रथमा", "singular": "अहम् (I)", "dual": "आवाम् (We two)", "plural": "वयम् (We all)", "usage": "I / We"},
            {"vibhakti": "द्वितीया", "singular": "माम् / मा", "dual": "आवाम् / नौ", "plural": "अस्मान् / नः", "usage": "Me / Us"},
            {"vibhakti": "तृतीया", "singular": "मया", "dual": "आवाभ्याम्", "plural": "अस्माभिः", "usage": "By me / By us"},
            {"vibhakti": "चतुर्थी", "singular": "मह्यम् / मे", "dual": "आवाभ्याम् / नौ", "plural": "अस्मभ्यम् / नः", "usage": "To me / To us"},
            {"vibhakti": "पञ्चमी", "singular": "मत्", "dual": "आवाभ्याम्", "plural": "अस्मत्", "usage": "From me / From us"},
            {"vibhakti": "षष्ठी", "singular": "मम / मे", "dual": "आवयोः / नौ", "plural": "अस्माकम् / नः", "usage": "My / Our"},
            {"vibhakti": "सप्तमी", "singular": "मयि", "dual": "आवयोः", "plural": "अस्मासु", "usage": "In me / In us"}
        ]
    },
    "yushmad": {
        "word": "युष्मद्",
        "transliteration": "Yuṣmad",
        "type": "सर्वनाम (Pronoun - Second Person: 'You')",
        "meaning": "You (Common to all genders)",
        "table": [
            {"vibhakti": "प्रथमा", "singular": "त्वम् (You)", "dual": "युवाम् (You two)", "plural": "यूयम् (You all)", "usage": "You"},
            {"vibhakti": "द्वितीया", "singular": "त्वाम् / त्वा", "dual": "युवाम् / वाम्", "plural": "युष्मान् / वः", "usage": "To you"},
            {"vibhakti": "तृतीया", "singular": "त्वया", "dual": "युवाभ्याम्", "plural": "युष्माभिः", "usage": "By you"},
            {"vibhakti": "चतुर्थी", "singular": "तुभ्यम् / ते", "dual": "युवाभ्याम् / वाम्", "plural": "युष्मभ्यम् / वः", "usage": "For you"},
            {"vibhakti": "पञ्चमी", "singular": "त्वत्", "dual": "युवाभ्याम्", "plural": "युष्मत्", "usage": "From you"},
            {"vibhakti": "षष्ठी", "singular": "तव / ते", "dual": "युवयोः / वाम्", "plural": "युष्माकम् / वः", "usage": "Your"},
            {"vibhakti": "सप्तमी", "singular": "त्वयि", "dual": "युवयोः", "plural": "युष्मासु", "usage": "In you"}
        ]
    }
}

DHATURUPA_DATA = {
    "path": {
        "dhatu": "पठ्",
        "transliteration": "Paṭh",
        "meaning": "To read / to study (पठनम्)",
        "gana": "भ्वादिगणः (परस्मैपदी)",
        "lakaras": {
            "lat": {
                "name": "लट् लकारः (Present Tense - वर्तमानकालः)",
                "forms": [
                    {"purusha": "प्रथमपुरुषः (3rd person)", "singular": "पठति", "dual": "पठतः", "plural": "पठन्ति", "meaning": "He/she reads"},
                    {"purusha": "मध्यमपुरुषः (2nd person)", "singular": "पठसि", "dual": "पठथः", "plural": "पठथ", "meaning": "You read"},
                    {"purusha": "उत्तमपुरुषः (1st person)", "singular": "पठामि", "dual": "पठावः", "plural": "पठामः", "meaning": "I read"}
                ]
            },
            "lang": {
                "name": "लङ् लकारः (Past Tense - अनद्यतनभूतकालः)",
                "forms": [
                    {"purusha": "प्रथमपुरुषः", "singular": "अपठत्", "dual": "अपठताम्", "plural": "अपठन्", "meaning": "He read"},
                    {"purusha": "मध्यमपुरुषः", "singular": "अपठः", "dual": "अपठतम्", "plural": "अपठत", "meaning": "You read"},
                    {"purusha": "उत्तमपुरुषः", "singular": "अपठम्", "dual": "अपठाव", "plural": "अपठाम", "meaning": "I read"}
                ]
            },
            "lrit": {
                "name": "लृट् लकारः (Future Tense - भविष्यत्कालः)",
                "forms": [
                    {"purusha": "प्रथमपुरुषः", "singular": "पठिष्यति", "dual": "पठिष्यतः", "plural": "पठिष्यन्ति", "meaning": "He will read"},
                    {"purusha": "मध्यमपुरुषः", "singular": "पठिष्यसि", "dual": "पठिष्यथः", "plural": "पठिष्यथ", "meaning": "You will read"},
                    {"purusha": "उत्तमपुरुषः", "singular": "पठिष्यामि", "dual": "पठिष्यावः", "plural": "पठिष्यामः", "meaning": "I will read"}
                ]
            },
            "lot": {
                "name": "लोट् लकारः (Imperative - आज्ञार्थः)",
                "forms": [
                    {"purusha": "प्रथमपुरुषः", "singular": "पठतु", "dual": "पठताम्", "plural": "पठन्तु", "meaning": "Let him read"},
                    {"purusha": "मध्यमपुरुषः", "singular": "पठ", "dual": "पठतम्", "plural": "पठत", "meaning": "You read!"},
                    {"purusha": "उत्तमपुरुषः", "singular": "पठानि", "dual": "पठाव", "plural": "पठाम", "meaning": "Let me read"}
                ]
            }
        }
    },
    "gam": {
        "dhatu": "गम् (गच्छ्)",
        "transliteration": "Gam (Gacch)",
        "meaning": "To go (गमनम्)",
        "gana": "भ्वादिगणः (परस्मैपदी)",
        "lakaras": {
            "lat": {
                "name": "लट् लकारः (Present Tense - वर्तमानकालः)",
                "forms": [
                    {"purusha": "प्रथमपुरुषः", "singular": "गच्छति", "dual": "गच्छतः", "plural": "गच्छन्ति", "meaning": "He goes"},
                    {"purusha": "मध्यमपुरुषः", "singular": "गच्छसि", "dual": "गच्छथः", "plural": "गच्छथ", "meaning": "You go"},
                    {"purusha": "उत्तमपुरुषः", "singular": "गच्छामि", "dual": "गच्छावः", "plural": "गच्छामः", "meaning": "I go"}
                ]
            },
            "lrit": {
                "name": "लृट् लकारः (Future Tense - भविष्यत्कालः)",
                "forms": [
                    {"purusha": "प्रथमपुरुषः", "singular": "गमिष्यति", "dual": "गमिष्यतः", "plural": "गमिष्यन्ति", "meaning": "He will go"},
                    {"purusha": "मध्यमपुरुषः", "singular": "गमिष्यसि", "dual": "गमिष्यथः", "plural": "गमिष्यथ", "meaning": "You will go"},
                    {"purusha": "उत्तमपुरुषः", "singular": "गमिष्यामि", "dual": "गमिष्यावः", "plural": "गमिष्यामः", "meaning": "I will go"}
                ]
            }
        }
    },
    "kri": {
        "dhatu": "कृ",
        "transliteration": "Kṛ",
        "meaning": "To do / make (करणम्)",
        "gana": "तनादिगणः (उभयपदी)",
        "lakaras": {
            "lat": {
                "name": "लट् लकारः (Present Tense - वर्तमानकालः)",
                "forms": [
                    {"purusha": "प्रथमपुरुषः", "singular": "करोति", "dual": "कुरुतः", "plural": "कुर्वन्ति", "meaning": "He does"},
                    {"purusha": "मध्यमपुरुषः", "singular": "करोषि", "dual": "कुरुथः", "plural": "कुरुथ", "meaning": "You do"},
                    {"purusha": "उत्तमपुरुषः", "singular": "करोमि", "dual": "कुर्वः", "plural": "कुर्मः", "meaning": "I do"}
                ]
            }
        }
    },
    "bhu": {
        "dhatu": "भू (भव्)",
        "transliteration": "Bhū (Bhav)",
        "meaning": "To be / become (भवनम्)",
        "gana": "भ्वादिगणः (परस्मैपदी)",
        "lakaras": {
            "lat": {
                "name": "लट् लकारः (Present Tense - वर्तमानकालः)",
                "forms": [
                    {"purusha": "प्रथमपुरुषः", "singular": "भवति", "dual": "भवतः", "plural": "भवन्ति", "meaning": "He becomes / is"},
                    {"purusha": "मध्यमपुरुषः", "singular": "भवसि", "dual": "भवथः", "plural": "भवथ", "meaning": "You are"},
                    {"purusha": "उत्तमपुरुषः", "singular": "भवामि", "dual": "भवावः", "plural": "भवामः", "meaning": "I am"}
                ]
            }
        }
    }
}

SANDHI_RULES = [
    {
        "name": "दीर्घसन्धिः (Dīrgha Sandhi)",
        "sutra": "अकः सवर्णे दीर्घः (६.१.१०१)",
        "rule": "When similar simple vowels meet (a+a, i+i, u+u, ri+ri), they merge into their long vowel equivalent (ā, ī, ū, ṝ).",
        "examples": [
            {"split": "हिम + आलयः", "joined": "हिमालयः", "meaning": "Hima + Ālayaḥ = Himālayaḥ (Abode of snow)"},
            {"split": "विद्या + आलयः", "joined": "विद्यालयः", "meaning": "Vidyā + Ālayaḥ = Vidyālayaḥ (School / House of learning)"},
            {"split": "कवि + इन्द्रः", "joined": "कवीन्द्रः", "meaning": "Kavi + Indraḥ = Kavīndraḥ (Chief of poets)"},
            {"split": "भानु + उदयः", "joined": "भानूदयः", "meaning": "Bhānu + Udayaḥ = Bhānūdayaḥ (Sunrise)"},
            {"split": "पितृ + ऋणम्", "joined": "पितॄणम्", "meaning": "Pitṛ + Ṛṇam = Pitṝṇam (Debt to ancestors)"}
        ]
    },
    {
        "name": "गुणसन्धिः (Guṇa Sandhi)",
        "sutra": "आद्गुणः (६.१.८७)",
        "rule": "When 'a' or 'ā' is followed by 'i/ī', 'u/ū', or 'ṛ/ṝ', they turn into 'e', 'o', and 'ar' respectively.",
        "examples": [
            {"split": "नर + ईशः", "joined": "नरेशः", "meaning": "Nara + Īśaḥ = Nareśaḥ (King / Lord of men)"},
            {"split": "महा + उत्सवः", "joined": "महोत्सवः", "meaning": "Mahā + Utsavaḥ = Mahotsavaḥ (Great festival)"},
            {"split": "देव + ऋषिः", "joined": "देवर्षिः", "meaning": "Deva + Ṛṣiḥ = Devarṣiḥ (Divine sage)"},
            {"split": "सूर्य + उदयः", "joined": "सूर्योदयः", "meaning": "Sūrya + Udayaḥ = Sūryodayaḥ (Sunrise)"}
        ]
    },
    {
        "name": "वृद्धिसन्धिः (Vṛddhi Sandhi)",
        "sutra": "वृद्धिरेचि (६.१.८८)",
        "rule": "When 'a' or 'ā' is followed by 'e/ai' or 'o/au', they merge into 'ai' and 'au' respectively.",
        "examples": [
            {"split": "सदा + एव", "joined": "सदैव", "meaning": "Sadā + Eva = Sadaiva (Always)"},
            {"split": "एक + एकम्", "joined": "एकैकम्", "meaning": "Eka + Ekam = Ekaikam (One by one)"},
            {"split": "महा + औषधम्", "joined": "महौषधम्", "meaning": "Mahā + Auṣadham = Mahauṣadham (Great medicine)"},
            {"split": "जल + ओघः", "joined": "जलौघः", "meaning": "Jala + Oghaḥ = Jalaughaḥ (Current of water)"}
        ]
    },
    {
        "name": "यण्सन्धिः (Yaṇ Sandhi)",
        "sutra": "इको यणचि (६.१.७७)",
        "rule": "When 'i/ī', 'u/ū', or 'ṛ' are followed by a dissimilar vowel, they turn into 'y', 'v', and 'r'.",
        "examples": [
            {"split": "यदि + अपि", "joined": "यद्यपि", "meaning": "Yadi + Api = Yadyapi (Even though)"},
            {"split": "इति + आदि", "joined": "इत्यादि", "meaning": "Iti + Ādi = Ityādi (Etcetera / and so on)"},
            {"split": "अनु + अयः", "joined": "अन्वयः", "meaning": "Anu + Ayaḥ = Anvayaḥ (Prose order)"},
            {"split": "सु + आगतम्", "joined": "स्वागतम्", "meaning": "Su + Āgatam = Svāgatam (Welcome)"}
        ]
    },
    {
        "name": "अयादिसन्धिः (Ayādi Sandhi)",
        "sutra": "एचोऽयवायावः (६.१.७८)",
        "rule": "When 'e', 'ai', 'o', 'au' are followed by any vowel, they change into 'ay', 'āy', 'av', 'āv'.",
        "examples": [
            {"split": "ने + अनम्", "joined": "नयनम्", "meaning": "Ne + Anam = Nayanam (Eye)"},
            {"split": "भो + अनम्", "joined": "भवनम्", "meaning": "Bho + Anam = Bhavanam (Building / Mansion)"},
            {"split": "पौ + अकः", "joined": "पावकः", "meaning": "Pau + Akaḥ = Pāvakaḥ (Fire)"},
            {"split": "गै + अकः", "joined": "गायकः", "meaning": "Gai + Akaḥ = Gāyakaḥ (Singer)"}
        ]
    },
    {
        "name": "विसर्गसन्धिः (Visarga Sandhi)",
        "sutra": "विसर्जनीयस्य सः / ससजुषो रुः",
        "rule": "Transformation of Visarga (ः) before various consonants and vowels.",
        "examples": [
            {"split": "नमः + ते", "joined": "नमस्ते", "meaning": "Namaḥ + Te = Namaste (Salutations to you)"},
            {"split": "कः + अपि", "joined": "कोऽपि", "meaning": "Kaḥ + Api = Ko'pi (Someone / Anyone)"},
            {"split": "रामः + अवदत्", "joined": "रामोऽवदत्", "meaning": "Rāmaḥ + Avadat = Rāmo'vadat (Rama said)"},
            {"split": "निः + छलम्", "joined": "निश्छलम्", "meaning": "Niḥ + Chalam = Niśchalam (Without deceit)"}
        ]
    }
]

DICTIONARY_WORDS = [
    {"sa": "पुस्तकम्", "iast": "pustakam", "en": "book", "type": "noun"},
    {"sa": "लेखनी", "iast": "lekhanī", "en": "pen", "type": "noun"},
    {"sa": "गृहम्", "iast": "gṛham", "en": "house / home", "type": "noun"},
    {"sa": "विद्यालयः", "iast": "vidyālayaḥ", "en": "school", "type": "noun"},
    {"sa": "मित्रम्", "iast": "mitram", "en": "friend", "type": "noun"},
    {"sa": "माता", "iast": "mātā", "en": "mother", "type": "noun"},
    {"sa": "पिता", "iast": "pitā", "en": "father", "type": "noun"},
    {"sa": "भ्राता", "iast": "bhrātā", "en": "brother", "type": "noun"},
    {"sa": "भगिनी", "iast": "bhaginī", "en": "sister", "type": "noun"},
    {"sa": "जलम्", "iast": "jalam", "en": "water", "type": "noun"},
    {"sa": "भोजनम्", "iast": "bhojanam", "en": "food / meal", "type": "noun"},
    {"sa": "सूर्यः", "iast": "sūryaḥ", "en": "sun", "type": "noun"},
    {"sa": "चन्द्रः", "iast": "candraḥ", "en": "moon", "type": "noun"},
    {"sa": "वृक्षः", "iast": "vṛkṣaḥ", "en": "tree", "type": "noun"},
    {"sa": "पुष्पम्", "iast": "puṣpam", "en": "flower", "type": "noun"},
    {"sa": "नदी", "iast": "nadī", "en": "river", "type": "noun"},
    {"sa": "पर्वतः", "iast": "parvataḥ", "en": "mountain", "type": "noun"},
    {"sa": "नगरम्", "iast": "nagaram", "en": "city", "type": "noun"},
    {"sa": "ग्रामः", "iast": "grāmaḥ", "en": "village", "type": "noun"},
    {"sa": "देशः", "iast": "deśaḥ", "en": "country", "type": "noun"},
    {"sa": "पठति", "iast": "paṭhati", "en": "reads / studies", "type": "verb"},
    {"sa": "लिखति", "iast": "likhati", "en": "writes", "type": "verb"},
    {"sa": "गच्छति", "iast": "gacchati", "en": "goes", "type": "verb"},
    {"sa": "आगच्छति", "iast": "āgacchati", "en": "comes", "type": "verb"},
    {"sa": "वदति", "iast": "vadati", "en": "speaks / says", "type": "verb"},
    {"sa": "पश्यति", "iast": "paśyati", "en": "sees / watches", "type": "verb"},
    {"sa": "खादति", "iast": "khādati", "en": "eats", "type": "verb"},
    {"sa": "पिबति", "iast": "pibati", "en": "drinks", "type": "verb"},
    {"sa": "करोति", "iast": "karoti", "en": "does / makes", "type": "verb"},
    {"sa": "क्रीडति", "iast": "krīḍati", "en": "plays", "type": "verb"},
    {"sa": "अद्य", "iast": "adya", "en": "today", "type": "avyaya"},
    {"sa": "श्वः", "iast": "śvaḥ", "en": "tomorrow", "type": "avyaya"},
    {"sa": "ह्यः", "iast": "hyaḥ", "en": "yesterday", "type": "avyaya"},
    {"sa": "इदानीम्", "iast": "idānīm", "en": "now / currently", "type": "avyaya"},
    {"sa": "सदा / सर्वदा", "iast": "sadā / sarvadā", "en": "always", "type": "avyaya"},
    {"sa": "कुत्र", "iast": "kutra", "en": "where", "type": "avyaya"},
    {"sa": "कदा", "iast": "kadā", "en": "when", "type": "avyaya"},
    {"sa": "कथम्", "iast": "katham", "en": "how", "type": "avyaya"},
    {"sa": "किमर्थम्", "iast": "kimartham", "en": "why / for what purpose", "type": "avyaya"},
    {"sa": "किम्", "iast": "kim", "en": "what", "type": "pronoun"},
    {"sa": "अत्र", "iast": "atra", "en": "here", "type": "avyaya"},
    {"sa": "तत्र", "iast": "tatra", "en": "there", "type": "avyaya"},
    {"sa": "सर्वत्र", "iast": "sarvatra", "en": "everywhere", "type": "avyaya"},
    {"sa": "सुन्दरम्", "iast": "sundaram", "en": "beautiful", "type": "adjective"},
    {"sa": "मधुरम्", "iast": "madhuram", "en": "sweet", "type": "adjective"},
    {"sa": "उत्तमम्", "iast": "uttamam", "en": "excellent / best", "type": "adjective"},
    {"sa": "सत्यम्", "iast": "satyam", "en": "truth / true", "type": "noun/adj"},
    {"sa": "शान्तिः", "iast": "śāntiḥ", "en": "peace", "type": "noun"},
    {"sa": "ज्ञानम्", "iast": "jñānam", "en": "knowledge / wisdom", "type": "noun"},
    {"sa": "आनन्दः", "iast": "ānandaḥ", "en": "bliss / joy", "type": "noun"}
]
