import httpx
import json
import asyncio
from typing import AsyncGenerator
from backend.config import settings

class OllamaClient:
    # Supported languages for translation - Comprehensive list
    SUPPORTED_LANGUAGES = {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Italian": "it",
        "Portuguese": "pt",
        "Chinese": "zh",
        "Japanese": "ja",
        "Korean": "ko",
        "Russian": "ru",
        "Arabic": "ar",
        "Hindi": "hi",
        "Afar": "aa",
        "Abkhazian": "ab",
        "Afrikaans": "af",
        "Akan": "ak",
        "Amharic": "am",
        "Aragonese": "an",
        "Assamese": "as",
        "Azerbaijani": "az",
        "Bashkir": "ba",
        "Belarusian": "be",
        "Bulgarian": "bg",
        "Bambara": "bm",
        "Bengali": "bn",
        "Tibetan": "bo",
        "Breton": "br",
        "Bosnian": "bs",
        "Catalan": "ca",
        "Chechen": "ce",
        "Corsican": "co",
        "Czech": "cs",
        "Chuvash": "cv",
        "Welsh": "cy",
        "Danish": "da",
        "Divehi": "dv",
        "Dzongkha": "dz",
        "Ewe": "ee",
        "Greek": "el",
        "Esperanto": "eo",
        "Estonian": "et",
        "Basque": "eu",
        "Persian": "fa",
        "Fulah": "ff",
        "Finnish": "fi",
        "Faroese": "fo",
        "Western Frisian": "fy",
        "Irish": "ga",
        "Scottish Gaelic": "gd",
        "Galician": "gl",
        "Guarani": "gn",
        "Gujarati": "gu",
        "Manx": "gv",
        "Hausa": "ha",
        "Hebrew": "he",
        "Croatian": "hr",
        "Haitian": "ht",
        "Hungarian": "hu",
        "Armenian": "hy",
        "Interlingua": "ia",
        "Indonesian": "id",
        "Interlingue": "ie",
        "Igbo": "ig",
        "Sichuan Yi": "ii",
        "Inupiaq": "ik",
        "Ido": "io",
        "Icelandic": "is",
        "Inuktitut": "iu",
        "Javanese": "jv",
        "Georgian": "ka",
        "Kikuyu": "ki",
        "Kazakh": "kk",
        "Kalaallisut": "kl",
        "Central Khmer": "km",
        "Kannada": "kn",
        "Kashmiri": "ks",
        "Kurdish": "ku",
        "Cornish": "kw",
        "Kyrgyz": "ky",
        "Latin": "la",
        "Luxembourgish": "lb",
        "Ganda": "lg",
        "Lingala": "ln",
        "Lao": "lo",
        "Lithuanian": "lt",
        "Luba-Katanga": "lu",
        "Latvian": "lv",
        "Malagasy": "mg",
        "Maori": "mi",
        "Macedonian": "mk",
        "Malayalam": "ml",
        "Mongolian": "mn",
        "Marathi": "mr",
        "Malay": "ms",
        "Maltese": "mt",
        "Burmese": "my",
        "Norwegian Bokmål": "nb",
        "North Ndebele": "nd",
        "Nepali": "ne",
        "Dutch": "nl",
        "Norwegian Nynorsk": "nn",
        "Norwegian": "no",
        "South Ndebele": "nr",
        "Navajo": "nv",
        "Chichewa": "ny",
        "Occitan": "oc",
        "Oromo": "om",
        "Oriya": "or",
        "Ossetian": "os",
        "Punjabi": "pa",
        "Polish": "pl",
        "Pashto": "ps",
        "Quechua": "qu",
        "Romansh": "rm",
        "Rundi": "rn",
        "Romanian": "ro",
        "Sanskrit": "sa",
        "Sardinian": "sc",
        "Sindhi": "sd",
        "Northern Sami": "se",
        "Sango": "sg",
        "Sinhala": "si",
        "Slovak": "sk",
        "Slovenian": "sl",
        "Shona": "sn",
        "Somali": "so",
        "Albanian": "sq",
        "Serbian": "sr",
        "Swati": "ss",
        "Southern Sotho": "st",
        "Sundanese": "su",
        "Swedish": "sv",
        "Swahili": "sw",
        "Tamil": "ta",
        "Telugu": "te",
        "Tajik": "tg",
        "Thai": "th",
        "Tigrinya": "ti",
        "Turkmen": "tk",
        "Tagalog": "tl",
        "Tswana": "tn",
        "Tonga": "to",
        "Turkish": "tr",
        "Tsonga": "ts",
        "Tatar": "tt",
        "Uyghur": "ug",
        "Ukrainian": "uk",
        "Urdu": "ur",
        "Uzbek": "uz",
        "Venda": "ve",
        "Vietnamese": "vi",
        "Volapük": "vo",
        "Walloon": "wa",
        "Wolof": "wo",
        "Xhosa": "xh",
        "Yiddish": "yi",
        "Yoruba": "yo",
        "Zhuang": "za",
        "Zulu": "zu",
    }

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.ocr_model = settings.OCR_MODEL
        self.translation_model = settings.TRANSLATION_MODEL

    async def _chat_stream(self, model: str, messages: list[dict], options: dict = None) -> AsyncGenerator[str, None]:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
        }
        if options:
            payload["options"] = options

        async with httpx.AsyncClient(timeout=300.0) as client:
            async with client.stream("POST", url, json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            if "message" in chunk and "content" in chunk["message"]:
                                yield chunk["message"]["content"]
                        except json.JSONDecodeError:
                            continue

    async def _chat_request(self, model: str, messages: list[dict], options: dict = None) -> str:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
        }
        if options:
            payload["options"] = options

        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"]

    async def ocr_image(self, image_b64: str, prompt: str = "Extract the text from this image.") -> str:
        messages = [{
            "role": "user",
            "content": prompt,
            "images": [image_b64]
        }]
        return await self._chat_request(self.ocr_model, messages)

    async def ocr_image_stream(self, image_b64: str, prompt: str = "Extract the text from this image.") -> AsyncGenerator[str, None]:
        messages = [{
            "role": "user",
            "content": prompt,
            "images": [image_b64]
        }]
        async for token in self._chat_stream(self.ocr_model, messages):
            yield token

    async def translate_text(self, text: str, target_lang: str) -> str:
        # Validate target language
        # Robust matching: try exact match first, then try matching base name before parentheses
        target_code = None
        if target_lang in self.SUPPORTED_LANGUAGES:
            target_code = self.SUPPORTED_LANGUAGES[target_lang]
        else:
            # Try to match the base name (e.g., "Spanish (Mexico)" -> "Spanish")
            base_lang = target_lang.split("(")[0].strip()
            if base_lang in self.SUPPORTED_LANGUAGES:
                target_code = self.SUPPORTED_LANGUAGES[base_lang]
        
        if not target_code:
            supported = ", ".join(list(self.SUPPORTED_LANGUAGES.keys())[:20]) + "..."
            raise ValueError(f"Unsupported target language: '{target_lang}'. Closest supported: {supported}")
        
        source_lang_name = "English" # Defaulting to English source for simplicity
        source_code = "en"
        
        prompt = f"""You are a professional {source_lang_name} ({source_code}) to {target_lang} ({target_code}) translator. Your goal is to accurately convey the meaning and nuances of the original {source_lang_name} text while adhering to {target_lang} grammar, vocabulary, and cultural sensitivities.
Produce only the {target_lang} translation, without any additional explanations or commentary. Please translate the following {source_lang_name} text into {target_lang}:


{text}"""

        messages = [{"role": "user", "content": prompt}]
        return await self._chat_request(self.translation_model, messages)

ollama_client = OllamaClient()
