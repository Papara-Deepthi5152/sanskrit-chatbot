"""
Sanskrit Transliteration Engine
High-fidelity bidirectional conversion between Devanagari, IAST, and phonetic English.
Handles conjuncts, matras, halanta, visarga, and anusvara.
"""

import re
from typing import Dict, List, Tuple

# Independent vowels
INDEPENDENT_VOWELS: Dict[str, str] = {
    'aa': 'आ', 'ā': 'आ', 'A': 'आ',
    'a': 'अ',
    'ii': 'ई', 'ī': 'ई', 'I': 'ई',
    'i': 'इ',
    'uu': 'ऊ', 'ū': 'ऊ', 'U': 'ऊ',
    'u': 'उ',
    'rri': 'ॠ', 'ṝ': 'ॠ',
    'ri': 'ऋ', 'ṛ': 'ऋ', 'R': 'ऋ',
    'lli': 'ॡ', 'ḹ': 'ॡ',
    'li': 'ऌ', 'ḷ': 'ऌ',
    'ai': 'ऐ',
    'e': 'ए',
    'au': 'औ',
    'o': 'ओ',
}

# Dependent vowel signs (Matras)
VOWEL_MATRAS: Dict[str, str] = {
    'aa': 'ा', 'ā': 'ा', 'A': 'ा',
    'ii': 'ी', 'ī': 'ी', 'I': 'ी',
    'i': 'ि',
    'uu': 'ू', 'ū': 'ू', 'U': 'ू',
    'u': 'ु',
    'rri': 'ॄ', 'ṝ': 'ॄ',
    'ri': 'ृ', 'ṛ': 'ृ', 'R': 'ृ',
    'lli': 'ॣ', 'ḹ': 'ॣ',
    'li': 'ॢ', 'ḷ': 'ॢ',
    'ai': 'ै',
    'e': 'े',
    'au': 'ौ',
    'o': 'ो',
    'a': ''  # inherent 'a' removes virama
}

# Consonant bases with virama (halanta)
CONSONANTS: Dict[str, str] = {
    'k': 'क्', 'kh': 'ख्', 'g': 'ग्', 'gh': 'घ्', 'ng': 'ङ्', 'ṅ': 'ङ्',
    'chh': 'छ्', 'ch': 'च्', 'c': 'च्', 'jh': 'झ्', 'j': 'ज्', 'ny': 'ञ्', 'ñ': 'ञ्',
    'ṭh': 'ठ्', 'thh': 'ठ्', 'Th': 'ठ्', 'ṭ': 'ट्', 'T': 'ट्',
    'ḍh': 'ढ्', 'dhh': 'ढ्', 'Dh': 'ढ्', 'ḍ': 'ड्', 'D': 'ड्',
    'ṇ': 'ण्', 'N': 'ण्',
    'th': 'थ्', 't': 'त्',
    'dh': 'ध्', 'd': 'द्',
    'n': 'न्',
    'ph': 'फ्', 'p': 'प्',
    'bh': 'भ्', 'b': 'ब्',
    'm': 'म्',
    'y': 'य्', 'r': 'र्', 'l': 'ल्', 'v': 'व्', 'w': 'व्',
    'shh': 'ष्', 'ṣ': 'ष्', 'Sh': 'ष्',
    'sh': 'श्', 'ś': 'श्',
    's': 'स्', 'h': 'ह्',
    'ksh': 'क्ष्', 'kṣ': 'क्ष्',
    'tr': 'त्र्',
    'gy': 'ज्ञ्', 'jn': 'ज्ञ्', 'jñ': 'ज्ञ्'
}

SORTED_CONSONANTS = sorted(CONSONANTS.keys(), key=lambda x: len(x), reverse=True)
SORTED_VOWEL_MATRAS = sorted(VOWEL_MATRAS.keys(), key=lambda x: len(x), reverse=True)
SORTED_IND_VOWELS = sorted(INDEPENDENT_VOWELS.keys(), key=lambda x: len(x), reverse=True)

# Common Sanskrit dictionary mappings for instant exact matches
COMMON_TRANSLITERATIONS = {
    "namaste": "नमस्ते",
    "namaskarah": "नमस्कारः",
    "namaskara": "नमस्कारः",
    "shubhaprabhatam": "शुभप्रभातम्",
    "suprabhatam": "सुप्रभातम्",
    "shubhadinam": "शुभदिनम्",
    "dhanyavadah": "धन्यवादः",
    "dhanyavada": "धन्यवादः",
    "swagatam": "स्वागतम्",
    "svagatam": "स्वागतम्",
    "kshamytam": "क्षम्यताम्",
    "kshamyatam": "क्षम्यताम्",
    "kripaya": "कृपया",
    "punah milamah": "पुनः मिलामः",
    "punarmilamah": "पुनर्मिलामः",
    "alpam": "अल्पम्",
    "aam": "आम्",
    "na": "न",
    "satyam": "सत्यम्",
    "shubharatrih": "शुभरात्रिः",
    "shubharatri": "शुभरात्रिः",
    "katham asti": "कथम् अस्ति",
    "katham asti bhavan": "कथम् अस्ति भवान्?",
    "katham asti bhavati": "कथम् अस्ति भवती?",
    "bhavatah nama kim": "भवतः नाम किम्?",
    "bhavatyaah nama kim": "भवत्याः नाम किम्?",
    "mama nama": "मम नाम",
    "aham": "अहम्",
    "tvam": "त्वम्",
    "bhavan": "भवान्",
    "bhavati": "भवती",
    "sah": "सः",
    "saa": "सा",
    "tat": "तत्",
    "kutra": "कुत्र",
    "kada": "कदा",
    "kimartham": "किमर्थम्",
    "katham": "कथम्",
    "kim": "किम्",
    "kah": "कः",
    "kaa": "का",
    "vidya": "विद्या",
    "pustakam": "पुस्तकम्",
    "mitram": "मित्रम्",
    "griham": "गृहम्",
    "gacchati": "गच्छति",
    "pathati": "पठति",
    "likhati": "लिखति",
    "vadati": "वदति",
    "pashyati": "पश्यति",
    "karoti": "करोति"
}

DEVA_TO_IAST_VOWELS = {
    'अ': 'a', 'आ': 'ā', 'इ': 'i', 'ई': 'ī', 'उ': 'u', 'ऊ': 'ū',
    'ऋ': 'ṛ', 'ॠ': 'ṝ', 'ऌ': 'ḷ', 'ॡ': 'ḹ', 'ए': 'e', 'ऐ': 'ai',
    'ओ': 'o', 'औ': 'au', 'ं': 'ṃ', 'ः': 'ḥ', 'ँ': 'm̐', 'ऽ': "'"
}

DEVA_TO_IAST_MATRAS = {
    'ा': 'ā', 'ि': 'i', 'ी': 'ī', 'ु': 'u', 'ू': 'ū',
    'ृ': 'ṛ', 'ॄ': 'ṝ', 'ॢ': 'ḷ', 'ॣ': 'ḹ', 'े': 'e', 'ै': 'ai',
    'ो': 'o', 'ौ': 'au', '्': ''
}

DEVA_TO_IAST_CONSONANTS = {
    'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ṅ',
    'च': 'c', 'छ': 'ch', 'ज': 'j', 'झ': 'jh', 'ञ': 'ñ',
    'ट': 'ṭ', 'ठ': 'ṭh', 'ड': 'ḍ', 'ढ': 'ḍh', 'ण': 'ṇ',
    'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
    'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
    'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v',
    'श': 'ś', 'ष': 'ṣ', 'स': 's', 'ह': 'h',
    'ळ': 'ḷ', 'क्ष': 'kṣ', 'ज्ञ': 'jñ'
}

VIRAMA = '्'

def is_devanagari(text: str) -> bool:
    """Check if string contains Devanagari characters."""
    for ch in text:
        if '\u0900' <= ch <= '\u097F':
            return True
    return False

def to_devanagari(text: str) -> str:
    """
    Convert Latin / phonetic English Sanskrit string to Devanagari.
    Preserves existing Devanagari.
    """
    if not text:
        return ""
    if is_devanagari(text):
        return text

    clean_lower = text.strip().lower()
    if clean_lower in COMMON_TRANSLITERATIONS:
        return COMMON_TRANSLITERATIONS[clean_lower]

    words = text.split(' ')
    out_words = []

    for word in words:
        if not word:
            out_words.append('')
            continue

        w_lower = word.lower().strip("?!.,;:\"'")
        if w_lower in COMMON_TRANSLITERATIONS:
            # Reattach trailing punctuation if any
            punct = word[len(w_lower):]
            out_words.append(COMMON_TRANSLITERATIONS[w_lower] + punct)
            continue

        res = []
        i = 0
        n = len(word)

        while i < n:
            ch = word[i]

            # Non-alphabetical marks
            if not ch.isalpha() and ch not in ["'", "~", ":"]:
                res.append(ch)
                i += 1
                continue

            # Visarga check: 'H', ':', 'ah' at end, 'h' at end
            if ch == ':' or ch == 'ḥ' or (ch == 'H' and (i == n - 1 or not word[i+1].isalpha())):
                res.append('ः')
                i += 1
                continue

            # Anusvara check: 'M', 'ṃ'
            if ch == 'M' or ch == 'ṃ':
                res.append('ं')
                i += 1
                continue

            # Avagraha
            if ch == "'":
                res.append('ऽ')
                i += 1
                continue

            # Chandrabindu
            if ch == '~':
                res.append('ँ')
                i += 1
                continue

            # Try consonant
            matched_c = None
            for c_pat in SORTED_CONSONANTS:
                # Handle case sensitivity for T, D, N, Sh
                if c_pat in ['T', 'Th', 'D', 'Dh', 'N', 'Sh']:
                    if word[i:i+len(c_pat)] == c_pat:
                        matched_c = c_pat
                        break
                else:
                    if word[i:i+len(c_pat)].lower() == c_pat.lower():
                        matched_c = c_pat
                        break

            if matched_c:
                i += len(matched_c)
                base_halant = CONSONANTS[matched_c]
                base_char = base_halant[:-1]  # remove virama

                # Check if followed by vowel matra
                matched_v = None
                for v_pat in SORTED_VOWEL_MATRAS:
                    if v_pat in ['A', 'I', 'U', 'R']:
                        if word[i:i+len(v_pat)] == v_pat:
                            matched_v = v_pat
                            break
                    else:
                        if word[i:i+len(v_pat)].lower() == v_pat.lower():
                            matched_v = v_pat
                            break

                if matched_v is not None:
                    i += len(matched_v)
                    matra = VOWEL_MATRAS[matched_v]
                    res.append(base_char + matra)

                    # Check for trailing anusvara or visarga attached to this syllable
                    if i < n:
                        # End-of-word 'h' -> visarga if preceded by vowel 'a', 'i', 'u' etc.
                        if word[i] in ['ḥ', 'H'] or (word[i].lower() == 'h' and (i + 1 == n or not word[i+1].isalpha())):
                            res.append('ः')
                            i += 1
                        # End-of-word 'm' -> halant म् (or anusvara if explicitly M or ṃ)
                        elif word[i] in ['ṃ', 'M']:
                            res.append('ं')
                            i += 1
                else:
                    # End of word consonant or conjunct:
                    # If it's at end of word and is 'm', keep halanta 'म्'
                    res.append(base_halant)
            else:
                # Independent vowel
                matched_iv = None
                for iv_pat in SORTED_IND_VOWELS:
                    if iv_pat in ['A', 'I', 'U', 'R']:
                        if word[i:i+len(iv_pat)] == iv_pat:
                            matched_iv = iv_pat
                            break
                    else:
                        if word[i:i+len(iv_pat)].lower() == iv_pat.lower():
                            matched_iv = iv_pat
                            break

                if matched_iv:
                    i += len(matched_iv)
                    res.append(INDEPENDENT_VOWELS[matched_iv])
                else:
                    res.append(ch)
                    i += 1

        out_words.append("".join(res))

    return " ".join(out_words)

def to_iast(text: str) -> str:
    """
    Convert Devanagari text to IAST transliteration.
    """
    if not text:
        return ""
    if not is_devanagari(text):
        return text

    res = []
    i = 0
    n = len(text)

    while i < n:
        ch = text[i]

        if ch in DEVA_TO_IAST_VOWELS:
            res.append(DEVA_TO_IAST_VOWELS[ch])
            i += 1
        elif ch in DEVA_TO_IAST_CONSONANTS:
            cons = DEVA_TO_IAST_CONSONANTS[ch]
            # Check next char
            if i + 1 < n:
                next_ch = text[i + 1]
                if next_ch == VIRAMA:
                    res.append(cons)
                    i += 2
                elif next_ch in DEVA_TO_IAST_MATRAS:
                    res.append(cons + DEVA_TO_IAST_MATRAS[next_ch])
                    i += 2
                elif next_ch in DEVA_TO_IAST_VOWELS:
                    res.append(cons + 'a')
                    i += 1
                else:
                    res.append(cons + 'a')
                    i += 1
            else:
                res.append(cons + 'a')
                i += 1
        elif ch in DEVA_TO_IAST_MATRAS:
            res.append(DEVA_TO_IAST_MATRAS[ch])
            i += 1
        else:
            res.append(ch)
            i += 1

    return "".join(res)

def normalize_sanskrit(text: str) -> str:
    """
    Normalize Sanskrit query for robust search & matching.
    """
    if not text:
        return ""
    t = text.strip().lower()
    replacements = {
        'ā': 'a', 'ī': 'i', 'ū': 'u', 'ṛ': 'ri', 'ṝ': 'ri',
        'ḷ': 'li', 'ḹ': 'li', 'ṃ': 'm', 'ḥ': 'h', 'ś': 'sh',
        'ṣ': 'sh', 'ṭ': 't', 'ṭh': 'th', 'ḍ': 'd', 'ḍh': 'dh',
        'ṇ': 'n', 'ñ': 'n', 'ṅ': 'n'
    }
    for k, v in replacements.items():
        t = t.replace(k, v)
    t = re.sub(r'[\?!.,;:"\'()\-–—]', ' ', t)
    return " ".join(t.split())
