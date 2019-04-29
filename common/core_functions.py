from common import parsed_sentence as ps
from spacy.lang.en.stop_words import STOP_WORDS
stopWords = set(STOP_WORDS)
stopWords.add("seven")
stopWords.add("especially")
stopWords.add("other")
stopWords.add("major")
stopWords.add("numerous")
stopWords.add("different")
stopWords.add("new")
stopWords.add("newer")
stopWords.add("primary")
stopWords.add("slower")
stopWords.add("similar")
stopWords.add("recent")
stopWords.add("later")
stopWords.add("better")
stopWords.add("biggest")
stopWords.add("good")

def get_sentences(corpus_file):
    """
    Returns all the (content) sentences in a processed corpus file
    :param corpus_file: the processed corpus file (may be compressed or not)
    :return: the next sentence (yield)
    """
    sent = ps.parsed_sentence()
    # Read all the sentences in the file

    f_in = open(corpus_file, 'r')
    # with gzip.open(corpus_file, 'r') as f_in:
    isNP = False
    is_root = False
    root = ""
    ri = 0
    np = ""
    np_indexes = []
    for line in f_in:
        # Ignore start and end of doc
        if '<text' in line:
            continue
        if '<s' in line:
            sent.id = line.split("'")[1]
            continue
        # End of sentence
        elif '</s>' in line:
            yield sent
            isNP = False
            is_root = False
            root = ""
            ri = 0
            np = ""
            np_indexes = []
            sent = ps.parsed_sentence()
        elif '<NP>' in line:
            isNP = True
        elif '</NP>' in line:
            isNP = False
            sent.add_NP(np.strip(), root, ri, min(np_indexes), max(np_indexes))
            np = ""
            np_indexes = []
        elif '<root>' in line:
            is_root = True
        elif '</root>' in line:
            is_root = False
        else:
            try:
                word, lemma, pos, index, parent, parent_index, dep, type = line.split("\t")
                if is_root:
                    root = word
                    ri = int(index)
                if isNP:
                    np_indexes.append(int(index))
                    np = np + " " + word
                sent.add_word(word, lemma, pos, int(index), parent, int(parent_index), dep, type.strip())
            # One of the items is a space - ignore this token
            except Exception as e:
                print (str(e))
                continue


def remove_kind_of_like(text):
    kind_like = ["kind", "kinds", "variety", "varieties", "species", "form", "forms", "example", "examples", "type", "types", "one", "some"]
    words = text.split()
    if len(words) < 3:
        return text
    if words[0].strip().lower() in ["the", "a", "an"]:
        text = (" " + text).replace(" " + words[0] + " ", "")
        words = words[1:]
    if words[0].strip().lower() in kind_like and words[1].strip().lower() == "of":
        return text.replace(words[0] + " of ", "").strip()
    return text

def remove_first_occurrences_stopwords(text):
    """
    :param text: text string
    :return: the text after removing the first occurrences of stop words in the text
    """
    text = text.lower()
    text = remove_kind_of_like(text)
    if text == "":
        return text
    words = text.split()
    if words[0] in stopWords:
        text = str("s" + text + " ").replace("s" + words[0] + " ", "").strip()
        return remove_first_occurrences_stopwords(text)
    else:
        return text
