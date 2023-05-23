# Spacy-Pipeline-Launcher

Plug-and-play spacy pipeline launcher where you can just write: 
``` 
nlp = load_spacy_pipeline("en") 
```
and everything works seamlessly, instead of the classical
```
nlp = spacy.load("en_core_web_sm")
```
a good advantage besides simplicity of loading is that it also automatically takes care of this error and prevents it from occuring:
```
OSError: [E050] Can't find model 'en_core_web_sm'. It doesn't seem to be a shortcut link, a Python package or a valid path to a data directory.
```
by havin a pro-active attitude and installing the required pipeline:
```
python -m spacy download en_core_web_sm
```
last but not least, it can be customizable to your own taste with all the parameters spacy is already allowing, but much simpler to modify and setup:
```
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
```
