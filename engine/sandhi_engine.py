"""
Sanskrit Sandhi Engine
Handles:
- Rule lookup and explanation
- Sandhi Joiner (joining two words according to Sanskrit phonological rules)
- Sandhi Split examples
"""

from typing import Dict, List, Optional, Tuple
from .knowledge_base import SANDHI_RULES
from .transliteration import to_devanagari, to_iast, is_devanagari

class SandhiEngine:
    def __init__(self):
        self.rules = SANDHI_RULES

    def get_all_rules(self) -> List[Dict]:
        return self.rules

    def get_rule_by_name(self, query: str) -> Optional[Dict]:
        q = query.lower()
        for r in self.rules:
            if q in r["name"].lower() or q in r["sutra"].lower():
                return r
        return None

    def join_words(self, word1: str, word2: str) -> Dict[str, str]:
        """
        Join two words using Sanskrit sandhi rules.
        Works with both Devanagari and Latin inputs.
        """
        w1 = word1.strip()
        w2 = word2.strip()

        # Check known examples first
        for rule in self.rules:
            for ex in rule["examples"]:
                parts = [p.strip() for p in ex["split"].split("+")]
                if len(parts) == 2:
                    if (parts[0] == w1 and parts[1] == w2) or \
                       (to_iast(parts[0]).lower() == w1.lower() and to_iast(parts[1]).lower() == w2.lower()):
                        return {
                            "joined": ex["joined"],
                            "joined_iast": to_iast(ex["joined"]),
                            "rule_name": rule["name"],
                            "sutra": rule["sutra"],
                            "explanation": f"Joined via {rule['name']} ({rule['sutra']}): {rule['rule']}"
                        }

        # Phonetic joining logic (simplified for common Swara & Visarga sandhis)
        w1_iast = to_iast(to_devanagari(w1)).lower() if is_devanagari(w1) else w1.lower()
        w2_iast = to_iast(to_devanagari(w2)).lower() if is_devanagari(w2) else w2.lower()

        # Visarga sandhi: ...ah + ... -> ...o' ... or ...as...
        if w1_iast.endswith("ah") or w1_iast.endswith("aḥ"):
            base = w1_iast[:-2]
            if w2_iast.startswith("a") or w2_iast.startswith("ā"):
                res_iast = base + "o'" + w2_iast[1:]
                res_deva = to_devanagari(res_iast)
                return {
                    "joined": res_deva,
                    "joined_iast": res_iast,
                    "rule_name": "विसर्गसन्धिः (उत्त्वसन्धिः / अतो रोरप्लुतादप्लुते)",
                    "sutra": "अतो रोरप्लुतादप्लुते (६.१.११३)",
                    "explanation": "When 'aḥ' is followed by short 'a', visarga becomes 'o' and following 'a' becomes avagraha (ऽ)."
                }
            elif w2_iast.startswith("t") or w2_iast.startswith("th"):
                res_iast = base + "as" + w2_iast
                res_deva = to_devanagari(res_iast)
                return {
                    "joined": res_deva,
                    "joined_iast": res_iast,
                    "rule_name": "विसर्गसन्धिः (विसर्जनीयस्य सः)",
                    "sutra": "विसर्जनीयस्य सः (८.३.३४)",
                    "explanation": "Visarga becomes 's' before 't' or 'th'."
                }

        # Dirgha Sandhi (a/ā + a/ā -> ā, i/ī + i/ī -> ī, u/ū + u/ū -> ū)
        if (w1_iast.endswith("a") or w1_iast.endswith("ā")) and (w2_iast.startswith("a") or w2_iast.startswith("ā")):
            base1 = w1_iast[:-1]
            rem2 = w2_iast[1:] if not w2_iast.startswith("aa") else w2_iast[2:]
            res_iast = base1 + "ā" + rem2
            return {
                "joined": to_devanagari(res_iast),
                "joined_iast": res_iast,
                "rule_name": "दीर्घसन्धिः (Dīrgha Sandhi)",
                "sutra": "अकः सवर्णे दीर्घः (६.१.१०१)",
                "explanation": "Similar vowels (a/ā + a/ā) merge into long vowel (ā)."
            }

        # Guna Sandhi (a/ā + i/ī -> e, a/ā + u/ū -> o, a/ā + ri -> ar)
        if (w1_iast.endswith("a") or w1_iast.endswith("ā")):
            if w2_iast.startswith("i") or w2_iast.startswith("ī"):
                base1 = w1_iast[:-1]
                rem2 = w2_iast[1:] if not w2_iast.startswith("ii") else w2_iast[2:]
                res_iast = base1 + "e" + rem2
                return {
                    "joined": to_devanagari(res_iast),
                    "joined_iast": res_iast,
                    "rule_name": "गुणसन्धिः (Guṇa Sandhi)",
                    "sutra": "आद्गुणः (६.१.८७)",
                    "explanation": "'a/ā' followed by 'i/ī' turns into 'e'."
                }
            elif w2_iast.startswith("u") or w2_iast.startswith("ū"):
                base1 = w1_iast[:-1]
                rem2 = w2_iast[1:] if not w2_iast.startswith("uu") else w2_iast[2:]
                res_iast = base1 + "o" + rem2
                return {
                    "joined": to_devanagari(res_iast),
                    "joined_iast": res_iast,
                    "rule_name": "गुणसन्धिः (Guṇa Sandhi)",
                    "sutra": "आद्गुणः (६.१.८७)",
                    "explanation": "'a/ā' followed by 'u/ū' turns into 'o'."
                }

        # Vriddhi Sandhi (a/ā + e/ai -> ai, a/ā + o/au -> au)
        if (w1_iast.endswith("a") or w1_iast.endswith("ā")):
            if w2_iast.startswith("e") or w2_iast.startswith("ai"):
                base1 = w1_iast[:-1]
                rem2 = w2_iast[2:] if w2_iast.startswith("ai") else w2_iast[1:]
                res_iast = base1 + "ai" + rem2
                return {
                    "joined": to_devanagari(res_iast),
                    "joined_iast": res_iast,
                    "rule_name": "वृद्धिसन्धिः (Vṛddhi Sandhi)",
                    "sutra": "वृद्धिरेचि (६.१.८८)",
                    "explanation": "'a/ā' followed by 'e/ai' turns into 'ai'."
                }

        # Yan Sandhi (i/ī + vowel -> y + vowel, u/ū + vowel -> v + vowel)
        if w1_iast.endswith("i") or w1_iast.endswith("ī"):
            base1 = w1_iast[:-1]
            res_iast = base1 + "y" + w2_iast
            return {
                "joined": to_devanagari(res_iast),
                "joined_iast": res_iast,
                "rule_name": "यण्सन्धिः (Yaṇ Sandhi)",
                "sutra": "इको यणचि (६.१.७७)",
                "explanation": "'i/ī' followed by dissimilar vowel turns into 'y'."
            }

        # Fallback: simple combination
        combined = f"{w1} {w2}"
        return {
            "joined": combined,
            "joined_iast": to_iast(combined),
            "rule_name": "सामान्य-संयोगः",
            "sutra": "पदपाठः",
            "explanation": "No direct automatic sandhi modification matched."
        }
