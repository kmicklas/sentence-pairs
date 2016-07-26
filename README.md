This repository consists of two separate tools, which together can be used to generate an Anki deck to assist in learning any of a number of foreign languages.
A very well made [Anki deck for Chinese](https://ankiweb.net/shared/info/2003820603) serves as the inspiration.

# `find-pairs.py`

This script is designed to ingest [Tatoeba data](https://tatoeba.org/eng/downloads) and create a list of all sentences in a target language and their direct translations in any of a set of languages that you already understand.
You'll want to grab `sentences.csv` and `links.csv` from Tatoeba, or some other equivalently formatted data.

## Usage

    python3 find-pairs.py [--allow-empty-translations] sentences.csv links.csv target-language translation-languages...

The optional `--allow-empty-translations` flag (off by default) will keep in the output sentences which have no direct translations in any of the provided translation languages.
In this case, you could provide no translation languages, and just get all sentences in the target language.
`target-language` and each of `translation-languages` are the three letter [ISO 693-3 code](https://en.wikipedia.org/wiki/List_of_ISO_639-3_codes) used by Tatoeba.

The program will print to standard out a tab separated table where the first column is the target language sentences and the second column is a `<br>` separated list of translations. All sentences will be HTML escaped.

For example, to write all Polish sentences with English or Spanish translations to `pairs.csv`:

    python3 find-pairs.py sentences.csv links.csv pol eng spa > pairs.csv

If you don't care about the ordering, or want to study the sentences in random order, this file is ready to import into Anki.

# `sort.py`

This script will ingest the output of `find-pairs.py` or any equivalently formatted source and sort them by word frequencies in the target language sentences such that sentences will start with the most commonly used words and gradually introduce new vocabulary.
The exact sort order is defined first by the minimum frequency of any word in the sentence, then by the average log frequency of words in the sentence.
Note that when a new word is introduced, the first sentences using it will then likely be longer sentences with more context provided by frequently used words, which should improve passive assimilation of the vocabulary.

## Usage

    python3 sort.py target-lang pairs.csv

Note that in this case, `target-lang` is a two letter [ISO 693-1 code](https://en.wikipedia.org/wiki/ISO_639-1).

For example, to sort the Polish sentences produced above and write the output to `sorted.csv`:

    python sort.py pl pairs.csv > sorted.csv

# Installation

The only dependency besides Python 3 is the excellent [`wordfreq`](https://github.com/LuminosoInsight/wordfreq) package, which can be installed easily:

    pip3 install wordfreq

Then these scripts can be run directly.

# Importing into Anki

This should be straightforward, refer to the [Anki manual](http://ankisrs.net/docs/manual.html#importing).
Just make sure to enable HTML in the fields.

# FAQ

## What languages are supported?

Languages are limited to what [`wordfreq`](https://github.com/LuminosoInsight/wordfreq#sources-and-supported-languages) supports.
And obviously if you use Tatoeba you'll be limited to the languages they have there.
(Though it's quite extensive.)

## Why HTML escaping?

Because it was easier than trying to figure out how to do escaping properly with quotes and proper line breaks between the translations.
