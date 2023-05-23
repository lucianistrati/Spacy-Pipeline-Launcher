from typing import List

import spacy
import os

# some abbreviations might differ from what the standard should be or some languages might have multiple abbreviations
SPACY_SUPPORTED_LANGUAGES = ["ca", "zh", "da", "nl", "en", "fi", "fr", "de", "el", "it", "ja", "ko", "lt", "mk", "xx",
                             "nb", "pl", "pt", "ro", "ru", "es", "sv", "af", "sq", "ar", "hy", "eu", "bn", "bg", "hr",
                             "cs", "et", "gu", "he", "hi", "hu", "is", "id", "ga", "kn", "ky", "lv", "lij", "dsb", "lb",
                             "ml", "mr", "ne", "fa", "sa", "sr", "tn", "si", "sk", "sl", "tl", "ta", "tt", "te", "th",
                             "tr", "uk", "hsb", "ur", "vi", "yo"]

code_to_lang = {"bs": "Bosnian", "sr": "Serbian", "hr": "Croatian", "sl": "Slovenian", "pl": "Polish", "sk": "Slovak",
                "cs": "Czech", "uk": "Ukrainian", "ru": "Russian", "mk": "Macedonian", "bg": "Bulgarian",
                "be": "Belarusian", "mn": "Mongolian", "ca": "Catalan", "gl": "Galician", "es": "Spanish",
                "an": "Aragonese", "pt": "Portuguese", "it": "Italian", "en": "English", "eo": "Esperanto",
                "af": "Afrikaans", "nl": "Dutch", "fr": "French", "cy": "Welsh", "sq": "Albanian", "eu": "Basque",
                "ro": "Romanian", "tl": "Tagalog", "vi": "Vietnamese", "et": "Estonian", "hy": "Armenian",
                "lv": "Latvian", "de": "German", "tr": "Turkish", "ko": "Korean", "la": "Latin",
                "az": "Azerbaijani", "lt": "Lithuanian", "mt": "Maltese", "zu": "Zulu", "br": "Breton",
                "hu": "Hungarian", "lb": "Luxembourgish", "fi": "Finnish", "ka": "Georgian", "Grek": "Greek",
                "ji": "Yiddish", "ig": "Igbo", "mi": "Maori", "yo": "Yoruba", "gv": "Manx", "ga": "Irish",
                "hi": "Hindi", "si": "Sinhala", "mr": "Marathi", "gu": "Gujarati", "sa": "Sanskrit", "bn": "Bengali",
                "kn": "Kannada", "te": "Telugu", "ta": "Tamil", "km": "Khmer", "my": "Burmese", "da": "Danish",
                "nn": "Norwegian Nynorsk", "sv": "Swedish", "fo": "Faroese", "is": "Icelandic", "id": "Indonesian",
                "jv": "Javanese", "so": "Somali", "ha": "Hausa", "fa": "Persian", "ur": "Urdu", "ar": "Arabic",
                "he": "Hebrew", "nb": "Norwegian Bokmål", "se": "Northern Sami", "tt": "Tatar", "kk": "Kazakh",
                "cmn": "Mandarin Chinese", "ja": "Japanese", "th": "Thai", "lo": "Lao", "oc": "Occitan",
                "ia": "Interlingua", "sw": "Swahili", "ne": "Nepali", "ms": "Malay", "gd": "Gaelic", "pa": "Punjabi",
                "ht": "Haitian Creole"}

code_to_idx = {"bs": 0, "sr": 1, "hr": 2, "sl": 3, "pl": 4, "sk": 5, "cs": 6, "uk": 7, "ru": 8, "mk": 9, "bg": 10,
               "be": 11, "mn": 12, "ca": 13, "gl": 14, "es": 15, "an": 16, "pt": 17, "it": 18, "en": 19, "eo": 20,
               "af": 21, "nl": 22, "fr": 23, "cy": 24, "sq": 25, "eu": 26, "ro": 27, "tl": 28, "vi": 29, "et": 30,
               "hy": 31, "lv": 32, "de": 33, "tr": 34, "ko": 35, "la": 36, "az": 37, "lt": 38, "mt": 39, "zu": 40,
               "br": 41, "hu": 42, "lb": 43, "fi": 44, "ka": 45, "Grek": 46, "ji": 47, "ig": 48, "mi": 49, "yo": 50,
               "gv": 51, "ga": 52, "hi": 53, "si": 54, "mr": 55, "gu": 56, "sa": 57, "bn": 58, "kn": 59, "te": 60,
               "ta": 61, "km": 62, "my": 63, "da": 64, "nn": 65, "sv": 66, "fo": 67, "is": 68, "id": 69, "jv": 70,
               "so": 71, "ha": 72, "fa": 73, "ur": 74, "ar": 75, "he": 76, "nb": 77, "se": 78, "tt": 79, "kk": 80,
               "cmn": 81, "ja": 82, "th": 83, "lo": 84, "oc": 85, "ia": 86, "sw": 87, "ne": 88, "ms": 89, "gd": 90,
               "pa": 91, "ht": 92}

idx_to_code = {0: "bs", 1: "sr", 2: "hr", 3: "sl", 4: "pl", 5: "sk", 6: "cs", 7: "uk", 8: "ru", 9: "mk", 10: "bg",
               11: "be", 12: "mn", 13: "ca", 14: "gl", 15: "es", 16: "an", 17: "pt", 18: "it", 19: "en", 20: "eo",
               21: "af", 22: "nl", 23: "fr", 24: "cy", 25: "sq", 26: "eu", 27: "ro", 28: "tl", 29: "vi", 30: "et",
               31: "hy", 32: "lv", 33: "de", 34: "tr", 35: "ko", 36: "la", 37: "az", 38: "lt", 39: "mt", 40: "zu",
               41: "br", 42: "hu", 43: "lb", 44: "fi", 45: "ka", 46: "Grek", 47: "ji", 48: "ig", 49: "mi", 50: "yo",
               51: "gv", 52: "ga", 53: "hi", 54: "si", 55: "mr", 56: "gu", 57: "sa", 58: "bn", 59: "kn", 60: "te",
               61: "ta", 62: "km", 63: "my", 64: "da", 65: "nn", 66: "sv", 67: "fo", 68: "is", 69: "id", 70: "jv",
               71: "so", 72: "ha", 73: "fa", 74: "ur", 75: "ar", 76: "he", 77: "nb", 78: "se", 79: "tt", 80: "kk",
               81: "cmn", 82: "ja", 83: "th", 84: "lo", 85: "oc", 86: "ia", 87: "sw", 88: "ne", 89: "ms", 90: "gd",
               91: "pa", 92: "ht"}

lang_to_idx = {"Bosnian": 0, "Serbian": 1, "Croatian": 2, "Slovenian": 3, "Polish": 4, "Slovak": 5, "Czech": 6,
               "Ukrainian": 7, "Russian": 8, "Macedonian": 9, "Bulgarian": 10, "Belarusian": 11, "Mongolian": 12,
               "Catalan": 13, "Galician": 14, "Spanish": 15, "Aragonese": 16, "Portuguese": 17, "Italian": 18,
               "English": 19, "Esperanto": 20, "Afrikaans": 21, "Dutch": 22, "French": 23, "Welsh": 24,
               "Albanian": 25, "Basque": 26, "Romanian": 27, "Tagalog": 28, "Vietnamese": 29, "Estonian": 30,
               "Armenian": 31, "Latvian": 32, "German": 33, "Turkish": 34, "Korean": 35, "Latin": 36,
               "Azerbaijani": 37, "Lithuanian": 38, "Maltese": 39, "Zulu": 40, "Breton": 41, "Hungarian": 42,
               "Luxembourgish": 43, "Finnish": 44, "Georgian": 45, "Greek": 46, "Yiddish": 47, "Igbo": 48, "Maori": 49,
               "Yoruba": 50, "Manx": 51, "Irish": 52, "Hindi": 53, "Sinhala": 54, "Marathi": 55, "Gujarati": 56,
               "Sanskrit": 57, "Bengali": 58, "Kannada": 59, "Telugu": 60, "Tamil": 61, "Khmer": 62, "Burmese": 63,
               "Danish": 64, "Norwegian Nynorsk": 65, "Swedish": 66, "Faroese": 67, "Icelandic": 68, "Indonesian": 69,
               "Javanese": 70, "Somali": 71, "Hausa": 72, "Persian": 73, "Urdu": 74, "Arabic": 75, "Hebrew": 76,
               "Norwegian Bokmål": 77, "Northern Sami": 78, "Tatar": 79, "Kazakh": 80, "Mandarin Chinese": 81,
               "Japanese": 82, "Thai": 83, "Lao": 84, "Occitan": 85, "Interlingua": 86, "Swahili": 87, "Nepali": 88,
               "Malay": 89, "Gaelic": 90, "Punjabi": 91, "Haitian Creole": 92}

idx_to_lang = {0: "Bosnian", 1: "Serbian", 2: "Croatian", 3: "Slovenian", 4: "Polish", 5: "Slovak", 6: "Czech",
               7: "Ukrainian", 8: "Russian", 9: "Macedonian", 10: "Bulgarian", 11: "Belarusian", 12: "Mongolian",
               13: "Catalan", 14: "Galician", 15: "Spanish", 16: "Aragonese", 17: "Portuguese", 18: "Italian",
               19: "English", 20: "Esperanto", 21: "Afrikaans", 22: "Dutch", 23: "French", 24: "Welsh", 25: "Albanian",
               26: "Basque", 27: "Romanian", 28: "Tagalog", 29: "Vietnamese", 30: "Estonian", 31: "Armenian",
               32: "Latvian", 33: "German", 34: "Turkish", 35: "Korean", 36: "Latin", 37: "Azerbaijani",
               38: "Lithuanian", 39: "Maltese", 40: "Zulu", 41: "Breton", 42: "Hungarian", 43: "Luxembourgish",
               44: "Finnish", 45: "Georgian", 46: "Greek", 47: "Yiddish", 48: "Igbo", 49: "Maori", 50: "Yoruba",
               51: "Manx", 52: "Irish", 53: "Hindi", 54: "Sinhala", 55: "Marathi", 56: "Gujarati", 57: "Sanskrit",
               58: "Bengali", 59: "Kannada", 60: "Telugu", 61: "Tamil", 62: "Khmer", 63: "Burmese", 64: "Danish",
               65: "Norwegian Nynorsk", 66: "Swedish", 67: "Faroese", 68: "Icelandic", 69: "Indonesian",
               70: "Javanese", 71: "Somali", 72: "Hausa", 73: "Persian", 74: "Urdu", 75: "Arabic", 76: "Hebrew",
               77: "Norwegian Bokmål", 78: "Northern Sami", 79: "Tatar", 80: "Kazakh", 81: "Mandarin Chinese",
               82: "Japanese", 83: "Thai", 84: "Lao", 85: "Occitan", 86: "Interlingua", 87: "Swahili", 88: "Nepali",
               89: "Malay", 90: "Gaelic", 91: "Punjabi", 92: "Haitian Creole"}

lang_to_code = {"Bosnian": "bs", "Serbian": "sr", "Croatian": "hr", "Slovenian": "sl", "Polish": "pl", "Slovak": "sk",
                "Czech": "cs", "Ukrainian": "uk", "Russian": "ru", "Macedonian": "mk", "Bulgarian": "bg",
                "Belarusian": "be", "Mongolian": "mn", "Catalan": "ca", "Galician": "gl", "Spanish": "es",
                "Aragonese": "an", "Portuguese": "pt", "Italian": "it", "English": "en", "Esperanto": "eo",
                "Afrikaans": "af", "Dutch": "nl", "French": "fr", "Welsh": "cy", "Albanian": "sq", "Basque": "eu",
                "Romanian": "ro", "Tagalog": "tl", "Vietnamese": "vi", "Estonian": "et", "Armenian": "hy",
                "Latvian": "lv", "German": "de", "Turkish": "tr", "Korean": "ko", "Latin": "la", "Azerbaijani": "az",
                "Lithuanian": "lt", "Maltese": "mt", "Zulu": "zu", "Breton": "br", "Hungarian": "hu",
                "Luxembourgish": "lb", "Finnish": "fi", "Georgian": "ka", "Greek": "Grek", "Yiddish": "ji",
                "Igbo": "ig", "Maori": "mi", "Yoruba": "yo", "Manx": "gv", "Irish": "ga", "Hindi": "hi",
                "Sinhala": "si", "Marathi": "mr", "Gujarati": "gu", "Sanskrit": "sa", "Bengali": "bn", "Kannada": "kn",
                "Telugu": "te", "Tamil": "ta", "Khmer": "km", "Burmese": "my", "Danish": "da",
                "Norwegian Nynorsk": "nn", "Swedish": "sv", "Faroese": "fo", "Icelandic": "is", "Indonesian": "id",
                "Javanese": "jv", "Somali": "so", "Hausa": "ha", "Persian": "fa", "Urdu": "ur", "Arabic": "ar",
                "Hebrew": "he", "Norwegian Bokmål": "nb", "Northern Sami": "se", "Tatar": "tt", "Kazakh": "kk",
                "Mandarin Chinese": "cmn", "Japanese": "ja", "Thai": "th", "Lao": "lo", "Occitan": "oc",
                "Interlingua": "ia", "Swahili": "sw", "Nepali": "ne", "Malay": "ms", "Gaelic": "gd", "Punjabi": "pa",
                "Haitian Creole": "ht"}

sm_pipeline = "sm"
md_pipeline = "md"
lg_pipeline = "lg"

code_to_pipeline = {"ca": {sm_pipeline: "ca_core_news_sm",
                           md_pipeline: "ca_core_news_md",
                           lg_pipeline: "ca_core_news_lg",
                           "trf": "ca_core_news_trf"},
                    "zh": {sm_pipeline: "zh_core_web_sm",
                           md_pipeline: "zh_core_web_md",
                           lg_pipeline: "zh_core_web_lg",
                           "trf": "zh_core_web_trf"},
                    "da": {sm_pipeline: "da_core_news_sm",
                           md_pipeline: "da_core_news_md",
                           lg_pipeline: "da_core_news_lg",
                           "trf": "da_core_news_trf"},
                    "nl": {sm_pipeline: "nl_core_news_sm",
                           md_pipeline: "nl_core_news_md",
                           lg_pipeline: "nl_core_news_lg"},
                    "en": {sm_pipeline: "en_core_web_sm",
                           md_pipeline: "en_core_web_md",
                           lg_pipeline: "en_core_web_lg",
                           "trf": "en_core_web_trf"},
                    "fi": {sm_pipeline: "fi_core_news_sm",
                           md_pipeline: "fi_core_news_md",
                           lg_pipeline: "fi_core_news_lg"},
                    "fr": {sm_pipeline: "fr_core_news_sm",
                           md_pipeline: "fr_core_news_md",
                           lg_pipeline: "fr_core_news_lg",
                           "trf": "fr_dep_news_trf"},
                    "de": {sm_pipeline: "de_core_news_sm",
                           md_pipeline: "de_core_news_md",
                           lg_pipeline: "de_core_news_lg",
                           "trf": "de_dep_news_trf"},
                    "el": {sm_pipeline: "el_core_news_sm",
                           md_pipeline: "el_core_news_md",
                           lg_pipeline: "el_core_news_lg"},
                    "it": {sm_pipeline: "it_core_news_sm",
                           md_pipeline: "it_core_news_md",
                           lg_pipeline: "it_core_news_lg"},
                    "ja": {sm_pipeline: "ja_core_news_sm",
                           md_pipeline: "ja_core_news_md",
                           lg_pipeline: "ja_core_news_lg",
                           "trf": "ja_core_news_trf"},
                    "ko": {sm_pipeline: "ko_core_news_sm",
                           md_pipeline: "ko_core_news_md",
                           lg_pipeline: "ko_core_news_lg"},
                    "lt": {sm_pipeline: "lt_core_news_sm",
                           md_pipeline: "lt_core_news_md",
                           lg_pipeline: "lt_core_news_lg"},
                    "mk": {sm_pipeline: "mk_core_news_sm",
                           md_pipeline: "mk_core_news_md",
                           lg_pipeline: "mk_core_news_lg"},
                    "xx": {sm_pipeline: "xx_sent_ud_sm"},
                    "nb": {sm_pipeline: "nb_core_news_sm",
                           md_pipeline: "nb_core_news_md",
                           lg_pipeline: "nb_core_news_lg"},
                    "pl": {sm_pipeline: "pl_core_news_sm",
                           md_pipeline: "pl_core_news_md",
                           lg_pipeline: "pl_core_news_lg"},
                    "pt": {sm_pipeline: "pt_core_news_sm",
                           md_pipeline: "pt_core_news_md",
                           lg_pipeline: "pt_core_news_lg"},
                    "ro": {sm_pipeline: "ro_core_news_sm",
                           md_pipeline: "ro_core_news_md",
                           lg_pipeline: "ro_core_news_lg"},
                    "ru": {sm_pipeline: "ru_core_news_sm",
                           md_pipeline: "ru_core_news_md",
                           lg_pipeline: "ru_core_news_lg"},
                    "es": {sm_pipeline: "es_core_news_sm",
                           md_pipeline: "es_core_news_md",
                           lg_pipeline: "es_core_news_lg",
                           "trf": "es_dep_news_trf"},
                    "sv": {sm_pipeline: "sv_core_news_sm",
                           md_pipeline: "sv_core_news_md",
                           lg_pipeline: "sv_core_news_lg"}}

future_spacy_packages = {"af": {}, "sq": {}, "ar": {}, "hy": {}, "eu": {}, "bn": {}, "bg": {}, "hr": {}, "cs": {},
                         "et": {}, "gu": {}, "he": {}, "hi": {}, "hu": {}, "is": {}, "id": {}, "ga": {}, "kn": {},
                         "ky": {}, "lv": {}, "lij": {}, "dsb": {}, "lb": {}, "ml": {}, "mr": {}, "ne": {}, "fa": {},
                         "sa": {}, "sr": {}, "tn": {}, "si": {}, "sk": {}, "sl": {}, "tl": {}, "ta": {}, "tt": {},
                         "te": {}, "th": {}, "tr": {}, "uk": {}, "hsb": {}, "ur": {}, "vi": {}, "yo": {}}

ALL_LANGUAGE_CODES = ["nb", "pl", "lt", "so", "oc", "fi", "my", "hy", "ml", "nn", "zh", "ga", "zu", "he", "bn", "eo",
                      "ca", "af", "az", "hu", "de", "da", "hr", "sk", "ur", "yo", "gv", "be", "cs", "ms", "pa", "hi",
                      "en", "sw", "eu", "fo", "si", "tl", "et", "mk", "dsb", "ru", "ha", "cy", "bg", "sr", "ht", "kn",
                      "sa", "tn", "es", "pt", "an", "lb", "tt", "sq", "la", "uk", "ka", "se", "it", "gl", "bs", "ko",
                      "nl", "lo", "ky", "xx", "mt", "hsb", "id", "gd", "vi", "fa", "mi", "mn", "gu", "sv", "Grek",
                      "cmn", "ia", "th", "ta", "kk", "ro", "lij", "ar", "lv", "ig", "fr", "mr", "el", "jv", "ne",
                      "tr", "ji", "is", "ja", "br", "te", "km", "sl"]


def get_pipeline_sizes(lang_code: str) -> List[str]:
    """
    Size: Package size indicator, sm, md, lg or trf.

    sm and trf pipelines have no static word vectors.

    For pipelines with default vectors, md has a reduced word vector table with 20k unique vectors for ~500k words and
    lg has a large word vector table with ~500k entries.

    For pipelines with floret vectors, md vector tables have 50k entries and lg vector tables have 200k entries.

    :param lang_code: 2-3 letters code languages
    :return: available pipeline sizes
    """
    return list(code_to_pipeline[lang_code].keys())


def get_pipeline_genre(lang_code: str) -> str:
    """
    :param lang_code: 2-3 letters code languages
    :return: type of text the pipeline is trained on (can be "ud", "web" or "news")
    """
    pipeline = code_to_pipeline[lang_code][sm_pipeline]
    tags = pipeline.split("_")
    return tags[2]


def get_pipeline_type(lang_code: str) -> str:
    """
    Capabilities (e.g. core for general-purpose pipeline with tagging, parsing, lemmatization and named entity
    recognition, or dep for only tagging, parsing and lemmatization).
    :param lang_code: 2-3 letters code languages
    :return: type of text the pipeline is trained on (can be "dep", "core" or "sent")
    """
    pipeline = code_to_pipeline[lang_code][sm_pipeline]
    tags = pipeline.split("_")
    return tags[1]


def load_spacy_pipeline(lang_code: str, pipeline_type: str = sm_pipeline, use_transformers: bool = False,
                        use_smallest_available: bool = False, disable: List[str] = None,
                        use_lookup_lemmatizer: bool = False, use_senter_over_parser: bool = False,
                        use_default_over_trainable: bool = False) -> spacy.lang:
    """
    :param lang_code: 2-3 letters code languages
    :param pipeline_type: type of spacy pipeline, has to be sm_pipeline, md_pipeline, lg_pipeline or "trf"
    :param use_transformers: if set to True, it will load a transformers based model
    :param use_smallest_available: if set to True, it will try to load a small pipeline, even if md, lg or trf was
    requested
    :param disable: specify components that should be disabled in order to reduce computation time and involved
    resources (can be any of the: ["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer", "ner"]
    :param use_lookup_lemmatizer: if set to True, then for Dutch, English, French, Greek, Macedonian, Norwegian and
    Spanish (at least, as of June 2022), then the current lemmatizer (which can be either trainable or rule-based) to
    a lookup-based one
    :param use_senter_over_parser: set it to True if you need fast sentence segmentation without dependency parses,
    (basically what is happening is that you disable the parser use the senter component instead). The senter
    component is ~10× faster than the parser and more accurate than the rule-based sentencizer. Do check that this
    is allowed.
    :param use_default_over_trainable: since v3.3, a number of pipelines use a trainable lemmatizer. You can check
    whether the lemmatizer is trainable. If you’d like to switch to a non-trainable lemmatizer that’s similar to v3.2
    or earlier, you can replace the trainable lemmatizer with the default non-trainable lemmatizer. Do check that this
    is allowed
    :return: spacy pipeline
    """
    if use_transformers:
        pipeline_type = "trf"

    if lang_code in code_to_pipeline.keys():
        pipelines_dict = code_to_pipeline[lang_code]

        if pipeline_type not in pipelines_dict.keys():
            if use_smallest_available:
                pipeline_type = sm_pipeline
            else:
                raise Exception(f"There is no pipeline_type for: {pipeline_type}")
        pipeline_name = pipelines_dict[pipeline_type]

        if disable is None:
            try:
                nlp = spacy.load(pipeline_name)
            except OSError:
                os.system(f"python -m spacy download {pipeline_name}")
                nlp = spacy.load(pipeline_name)
        else:
            try:
                nlp = spacy.load(pipeline_name)
            except OSError:
                os.system(f"python -m spacy download {pipeline_name}")
                nlp = spacy.load(pipeline_name)
    elif lang_code in future_spacy_packages:
        raise Exception(f"There is no pipeline for {lang_code}, but soon one should came up!")
    else:
        raise Exception(f"There is no pipeline for {lang_code} and there is no prospect of one in the future!")

    lemmatizer_pipeline = "lemmatizer"

    if use_lookup_lemmatizer:
        if lang_code not in ["nl", "en", "fr", "el", "es", "nn", "mk", "nb", "nn"]:
            raise Exception(f"Cannot switch to lookup lemmatizer with {lang_code} language!")
        nlp.remove_pipe(lemmatizer_pipeline)
        nlp.add_pipe(lemmatizer_pipeline, config={"mode": "lookup"}).initialize()

    if use_senter_over_parser:
        nlp.disable_pipe("parser")
        nlp.enable_pipe("senter")

    if use_default_over_trainable:
        if nlp.get_pipe(lemmatizer_pipeline).is_trainable:
            nlp.remove_pipe(lemmatizer_pipeline)
            nlp.add_pipe(lemmatizer_pipeline).initialize()

    return nlp


def get_all_ner_labels_available_in_pipeline(spacy_nlp: spacy.lang) -> List[str]:
    return list(spacy_nlp.get_pipe("ner").labels)


def main():
    nlp = load_spacy_pipeline("en")
    print(get_all_ner_labels_available_in_pipeline(nlp))


if __name__ == "__main__":
    main()
