# Spacy-Pipeline-Launcher

The Spacy-Pipeline-Launcher is a plug-and-play solution for launching spaCy pipelines with ease. Instead of the classical method of loading spaCy pipelines like this:

```python
nlp = spacy.load("en_core_web_sm")
```

You can simply write:

```python
nlp = load_spacy_pipeline("en")
```

This launcher not only simplifies the loading process but also proactively handles potential errors. For instance, it automatically installs the required pipeline if it's not already available, preventing errors like:

```
OSError: [E050] Can't find model 'en_core_web_sm'. It doesn't seem to be a shortcut link, a Python package or a valid path to a data directory.
```

By executing:

```
python -m spacy download en_core_web_sm
```

Moreover, the Spacy-Pipeline-Launcher is highly customizable, allowing you to tailor the pipeline to your specific needs. You can specify various parameters such as:

- `lang_code`: The 2-3 letter language code.
- `pipeline_type`: The type of spaCy pipeline (`sm_pipeline`, `md_pipeline`, `lg_pipeline`, or `"trf"`).
- `use_transformers`: Set to `True` to load a transformers-based model.
- `use_smallest_available`: Set to `True` to try loading a small pipeline even if a larger one was requested.
- `disable`: Specify components to disable in order to reduce computation time and resources.
- `use_lookup_lemmatizer`: Set to `True` to use a lookup-based lemmatizer for certain languages.
- `use_senter_over_parser`: Set to `True` for fast sentence segmentation without dependency parses.
- `use_default_over_trainable`: Replace trainable lemmatizers with default non-trainable ones.

By leveraging these parameters, you can easily configure the spaCy pipeline according to your preferences.

## Usage

To use the Spacy-Pipeline-Launcher, simply import the `load_spacy_pipeline` function and call it with the desired language code and optional parameters:

```python
from spacy_pipeline_launcher import load_spacy_pipeline

nlp = load_spacy_pipeline("en", pipeline_type="sm", disable=["ner"])
```

This will load a small spaCy pipeline for English with the named entity recognition (NER) component disabled.
