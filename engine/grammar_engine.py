"""
Sanskrit Grammar Engine (व्याकरण-तन्त्रम्)
Provides:
- Shabdarupa (Noun declensions) lookup and formatted display
- Dhaturupa (Verb conjugations) lookup across Lakaras
- Morphological analysis (identifying root, vibhakti/lakara, purusha, vachana)
"""

from typing import Dict, List, Optional, Any
from .knowledge_base import SHABDARUPA_DATA, DHATURUPA_DATA
from .transliteration import to_devanagari, to_iast, is_devanagari, normalize_sanskrit

class GrammarEngine:
    def __init__(self):
        self.shabdarupas = SHABDARUPA_DATA
        self.dhaturupas = DHATURUPA_DATA

        # Build reverse index for morphological analysis
        self.morph_index: Dict[str, List[Dict[str, str]]] = {}
        self._build_morph_index()

    def _build_morph_index(self):
        # Index shabda forms
        for key, sdata in self.shabdarupas.items():
            base_word = sdata["word"]
            for row in sdata["table"]:
                vibhakti = row["vibhakti"]
                for vachana, col in [("एकवचनम् (Singular)", "singular"),
                                      ("द्विवचनम् (Dual)", "dual"),
                                      ("बहुवचनम् (Plural)", "plural")]:
                    raw_val = row[col]
                    # Clean words like "अहम् (I)"
                    form = raw_val.split("(")[0].replace("!", "").replace("हे", "").strip()
                    for word_part in form.split("/"):
                        w = word_part.strip()
                        if w:
                            if w not in self.morph_index:
                                self.morph_index[w] = []
                            self.morph_index[w].append({
                                "type": "shabda",
                                "base": base_word,
                                "transliteration": sdata["transliteration"],
                                "vibhakti": vibhakti,
                                "vachana": vachana,
                                "usage": row.get("usage", "")
                            })

        # Index dhatu forms
        for key, ddata in self.dhaturupas.items():
            base_dhatu = ddata["dhatu"]
            for lakara_key, ldata in ddata["lakaras"].items():
                lakara_name = ldata["name"]
                for row in ldata["forms"]:
                    purusha = row["purusha"]
                    meaning = row.get("meaning", "")
                    for vachana, col in [("एकवचनम् (Singular)", "singular"),
                                          ("द्विवचनम् (Dual)", "dual"),
                                          ("बहुवचनम् (Plural)", "plural")]:
                        form = row[col].strip()
                        if form:
                            if form not in self.morph_index:
                                self.morph_index[form] = []
                            self.morph_index[form].append({
                                "type": "dhatu",
                                "base": base_dhatu,
                                "transliteration": ddata["transliteration"],
                                "lakara": lakara_name,
                                "purusha": purusha,
                                "vachana": vachana,
                                "meaning": meaning
                            })

    def lookup_shabda(self, query: str) -> Optional[Dict[str, Any]]:
        """Find shabdarupa declension table by noun name."""
        q = normalize_sanskrit(query)
        for key, data in self.shabdarupas.items():
            if (q == key or q in key or
                data["word"] == query or
                normalize_sanskrit(data["transliteration"]) == q or
                q in normalize_sanskrit(data["word"])):
                return data
        return None

    def lookup_dhatu(self, query: str, lakara: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Find dhaturupa conjugation table by verb root."""
        q = normalize_sanskrit(query)
        for key, data in self.dhaturupas.items():
            if (q == key or q in key or
                data["dhatu"] == query or
                normalize_sanskrit(data["transliteration"]) == q or
                q in normalize_sanskrit(data["dhatu"])):
                return data
        return None

    def analyze_word(self, word: str) -> List[Dict[str, str]]:
        """
        Perform morphological analysis on a single Sanskrit word.
        Returns matching base form, vibhakti/lakara, purusha/case, vachana, etc.
        """
        w = word.strip().replace("!", "").replace("?", "").replace(".", "")
        if not is_devanagari(w):
            w_deva = to_devanagari(w)
        else:
            w_deva = w

        results = []
        if w_deva in self.morph_index:
            results.extend(self.morph_index[w_deva])

        # Also check without trailing anusvara/visarga variations
        if not results:
            alt = w_deva.rstrip("ः").rstrip("म्")
            for k, v in self.morph_index.items():
                if k.startswith(alt) and len(k) <= len(alt) + 2:
                    results.extend(v)

        return results

    def format_shabda_markdown(self, data: Dict[str, Any]) -> str:
        """Format shabdarupa table into clean markdown."""
        md = f"### शब्दरूपम्: **{data['word']}** ({data['transliteration']})\n"
        md += f"**प्रकारः**: {data['type']}\n"
        md += f"**अर्थः**: {data['meaning']}\n\n"
        md += "| विभक्तिः (Case) | एकवचनम् (Singular) | द्विवचनम् (Dual) | बहुवचनम् (Plural) | अर्थः (Usage) |\n"
        md += "| :--- | :--- | :--- | :--- | :--- |\n"
        for row in data["table"]:
            md += f"| {row['vibhakti']} | **{row['singular']}** | {row['dual']} | {row['plural']} | {row['usage']} |\n"
        return md

    def format_dhatu_markdown(self, data: Dict[str, Any], lakara_filter: Optional[str] = None) -> str:
        """Format dhaturupa table into clean markdown."""
        md = f"### धातुरूपम्: **{data['dhatu']}** ({data['transliteration']})\n"
        md += f"**अर्थः**: {data['meaning']} | **गणः**: {data['gana']}\n\n"

        for lk_key, lk_data in data["lakaras"].items():
            if lakara_filter and lakara_filter.lower() not in lk_key.lower():
                continue
            md += f"#### {lk_data['name']}\n"
            md += "| पुरुषः (Person) | एकवचनम् (Singular) | द्विवचनम् (Dual) | बहुवचनम् (Plural) | English Meaning |\n"
            md += "| :--- | :--- | :--- | :--- | :--- |\n"
            for row in lk_data["forms"]:
                md += f"| {row['purusha']} | **{row['singular']}** | {row['dual']} | {row['plural']} | {row['meaning']} |\n"
            md += "\n"
        return md
