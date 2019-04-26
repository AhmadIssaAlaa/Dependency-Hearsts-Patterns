# The dependency patterns:
#             ("nsubj(hyperHead, hypoHead), cop(hyperHead, was|were|is|are)"),
#             ("case(hypoHead, such), mwe(such, as), nmod:such_as(hyperHead, hypoHead)"),
#             ("case(hypoHead, including), nmod:including(hyperHead, hypoHead)"),
#             ("amod(hyperHead, such), case(hypoHead, as), nmod:as(~, hypoHead)"),
#             ("cc(hypoHead, and/or), amod(hyperHead, other), conj:and/or(hypoHead, hyperHead)"),
#             ("advmod(hyperHead, especially), dep(hyperHead, hypoHead)")

from common import HyperHypoCouple as HH
from common import core_functions as cf

def get_NP(NPs, index):
    for np in NPs:
        if int(index) in range(int(np.start), int(np.end) + 1):
            return np.text
    return ""

def get_couples(parsed_sentence, hyper_index, hypo_index, j_index = 0):
    hyper_np = cf.remove_first_occurrences_stopwords(get_NP(parsed_sentence.NPs, hyper_index))
    hypo_np = cf.remove_first_occurrences_stopwords(get_NP(parsed_sentence.NPs, hypo_index))
    couples = []
    hypo_indexes = set()
    if hyper_np != "" and hypo_np != "" and hypo_np != hyper_np:
        hh = HH.HHCouple(hypo_np, hyper_np)
        couples.append(hh)
        hypo_indexes.add(hypo_index)
    parsed_words = parsed_sentence.words
    for i in range(0, len(parsed_words)):
        parsed_word = parsed_words[i]
        if str(parsed_word.dep_rel).__contains__("appos") and parsed_word.parent_index == hypo_index:
            new_hypo_index = parsed_word.index
            hypo_index = new_hypo_index
            new_hypo_np = cf.remove_first_occurrences_stopwords(get_NP(parsed_sentence.NPs, new_hypo_index))
            if hyper_np != "" and new_hypo_np != "" and new_hypo_np != hyper_np:
                new_hh = HH.HHCouple(new_hypo_np, hyper_np)
                couples.append(new_hh)
                hypo_indexes.add(new_hypo_index)
        if str(parsed_word.dep_rel).__contains__("conj") and parsed_word.parent_index == hypo_index:
            new_hypo_index = parsed_word.index
            new_hypo_np = cf.remove_first_occurrences_stopwords(get_NP(parsed_sentence.NPs, new_hypo_index))
            if hyper_np != "" and new_hypo_np != "" and new_hypo_np != hyper_np:
                new_hh = HH.HHCouple(new_hypo_np, hyper_np)
                couples.append(new_hh)
                hypo_indexes.add(new_hypo_index)
    return couples, hypo_indexes


def such_A_as_B(parsed_sentence):
    parsed_words = parsed_sentence.words
    for i in range(len(parsed_words)):
        parsed_word = parsed_words[i] #("amod(hyperHead, such), case(hypoHead, as), nmod:as(~, hypoHead)"),
        if str(parsed_word.dep_rel).__contains__("nmod:as"):
            hypo_index = parsed_word.index
            if not str(parsed_word.pos).__contains__("NN") and not str(parsed_word.pos).__contains__("JJ"):
                continue
            flag1 = False
            flag2 = False
            for j in range(i - 1, max(-1, i-10), -1):
                pre_word = parsed_words[j]
                if str(pre_word.dep_rel).__contains__("case") and pre_word.word == "as" and pre_word.parent_index == hypo_index:
                    flag1 = True
                elif str(pre_word.dep_rel).__contains__("amod") and pre_word.word == "such":
                    hyper_index = pre_word.parent_index
                    flag2 = True
                if flag1 and flag2:
                    couples, hypo_indexes = get_couples(parsed_sentence, hyper_index, hypo_index, j)
                    if len(couples) > 0:
                        return True, couples, hypo_indexes, hyper_index
    return False, [], [], -1

def A_is_a_B(parsed_sentence):
    vtb = ["is", "are", "was", "were"]
    parsed_words = parsed_sentence.words
    for i in range(len(parsed_words)):
        parsed_word = parsed_words[i] #("nsubj(hyperHead, hypoHead), cop(hyperHead, was|were|is|are)"),
        if str(parsed_word.dep_rel).__contains__("nsubj"):
            hypo_index = parsed_word.index
            if not str(parsed_word.pos).__contains__("NN") and not str(parsed_word.pos).__contains__("JJ"):
                continue
            hyper_index = parsed_word.parent_index
            for j in range(i + 1, min(len(parsed_words), i + 10)):
                next_word = parsed_words[j]
                if str(next_word.dep_rel).__contains__("cop") and next_word.word in vtb and next_word.parent_index == hyper_index:
                    couples, hypo_indexes = get_couples(parsed_sentence, hyper_index, hypo_index)
                    if len(couples) > 0:
                        return True, couples, hypo_indexes, hyper_index
    return False, [], [], -1


def A_and_other_B(parsed_sentence):
    conj = ["or", "and"]
    parsed_words = parsed_sentence.words
    for i in range(len(parsed_words)):
        parsed_word = parsed_words[i]  #("cc(hypoHead, and/or), amod(hyperHead, other), conj:and/or(hypoHead, hyperHead)"),
        if str(parsed_word.dep_rel).__contains__("conj"):
            hyper_index = parsed_word.index
            if not str(parsed_word.pos).__contains__("NN") and not str(parsed_word.pos).__contains__("JJ"):
                continue
            hypo_index = parsed_word.parent_index
            flag1 = False
            flag2 = False
            for j in range(i - 1, max(-1, i - 10), -1):
                pre_word = parsed_words[j]
                if str(pre_word.dep_rel).__contains__("amod") and pre_word.word == "other" and pre_word.parent_index == hyper_index:
                    flag1 = True
                elif str(pre_word.dep_rel).__contains__(
                        "cc") and pre_word.word in conj and pre_word.parent_index == hypo_index:
                    flag2 = True
                if flag1 and flag2:
                    couples, hypo_indexes = get_couples(parsed_sentence, hyper_index, hypo_index, j)
                    if len(couples) > 0:
                        return True, couples, hypo_indexes, hyper_index
    return False, [], [], -1
#

def A_especially_B(parsed_sentence):
    parsed_words = parsed_sentence.words
    for i in range(len(parsed_words)):
        parsed_word = parsed_words[i] #("advmod(hyperHead, especially), dep(hyperHead, hypoHead)")
        if str(parsed_word.dep_rel).__contains__("dep"):
            hypo_index = parsed_word.index
            if not str(parsed_word.pos).__contains__("NN") and not str(parsed_word.pos).__contains__("JJ"):
                continue
            hyper_index = parsed_word.parent_index
            for j in range(i - 1, max(-1, i - 10), -1):
                pre_word = parsed_words[j]
                if str(pre_word.dep_rel).__contains__("advmod") and pre_word.word == "especially" and pre_word.parent_index == hyper_index:
                    couples, hypo_indexes = get_couples(parsed_sentence, hyper_index, hypo_index, j)
                    if len(couples) > 0:
                        return True, couples, hypo_indexes, hyper_index
    return False, [], [], -1

def A_including_B(parsed_sentence):
    parsed_words = parsed_sentence.words
    for i in range(len(parsed_words)):
        parsed_word = parsed_words[i] #("case(hypoHead, including), nmod:including(hyperHead, hypoHead)"),
        if str(parsed_word.dep_rel).__contains__("nmod:including"):
            hypo_index = parsed_word.index
            if not str(parsed_word.pos).__contains__("NN") and not str(parsed_word.pos).__contains__("JJ"):
                continue
            hyper_index = parsed_word.parent_index
            for j in range(i - 1, max(-1, i - 10), -1):
                pre_word = parsed_words[j]
                if str(pre_word.dep_rel).__contains__("case") and pre_word.word == "including" and pre_word.parent_index == hypo_index:
                    couples, hypo_indexes = get_couples(parsed_sentence, hyper_index, hypo_index, j)
                    if len(couples) > 0:
                        return True, couples, hypo_indexes, hyper_index
    return False, [], [], -1

def A_such_as_B(parsed_sentence):
    parsed_words = parsed_sentence.words
    for i in range(len(parsed_words)):
        parsed_word = parsed_words[i]
        if str(parsed_word.dep_rel).__contains__("nmod:such_as"):
            hypo_index = parsed_word.index
            if not str(parsed_word.pos).__contains__("NN") and not str(parsed_word.pos).__contains__("JJ"):
                continue
            hyper_index = parsed_word.parent_index
            flag1 = False
            flag2 = False
            for j in range(i - 1, max(-1, i-10), -1):
                pre_word = parsed_words[j]
                if str(pre_word.dep_rel).__contains__("mwe") and pre_word.word == "as" and pre_word.parent == "such":
                    flag1 = True
                elif str(pre_word.dep_rel).__contains__("case") and pre_word.word == "such" and pre_word.parent_index == hypo_index:
                    flag2 = True
                if flag1 and flag2:
                    couples, hypo_indexes = get_couples(parsed_sentence, hyper_index, hypo_index, j)
                    if len(couples) > 0:
                        return True, couples, hypo_indexes, hyper_index
    return False, [], [], -1

def sentence_couples_annotation(sentence, couples):
    sentence = sentence.replace("_hypo", "").replace("_hyper", "").replace("_", " ")
    for i, couple in enumerate(couples):
        hyper = couple.hypernym
        hyper2 = hyper.replace(" ", "_")
        sentence = sentence.replace(" " + hyper + " ", " " + hyper2 + "_hyper ").strip()
        hypo = couple.hyponym
        hypo2 = hypo.replace(" ", "_")
        try:
            sentence = sentence.replace(" " + hypo + " ", " " + hypo2 + "_hypo ").strip()
        except:
            sentence = sentence
    return sentence


def match(parsed_sentence, sentence = ""):
    couples = []
    hypo_indexes = set()
    hyper_indexes = set()
    patterns = []
    # NP such as NP
    flag, co, hypo_ind, hyper_index = A_such_as_B(parsed_sentence)
    if flag:
        couples.extend(co)
        hypo_indexes = hypo_indexes.union(hypo_ind)
        hyper_indexes.add(hyper_index)
        patterns.append("NP such as NP")
    # NP including NP
    flag, co, hypo_ind, hyper_index = A_including_B(parsed_sentence)
    if flag:
        couples.extend(co)
        hypo_indexes = hypo_indexes.union(hypo_ind)
        hyper_indexes.add(hyper_index)
        patterns.append("NP including NP")
    # NP is a NP
    flag, co, hypo_ind, hyper_index = A_is_a_B(parsed_sentence)
    if flag:
        couples.extend(co)
        hypo_indexes = hypo_indexes.union(hypo_ind)
        hyper_indexes.add(hyper_index)
        patterns.append("NP is a NP")
    # NP and other NP
    flag, co, hypo_ind, hyper_index = A_and_other_B(parsed_sentence)
    if flag:
        couples.extend(co)
        hypo_indexes = hypo_indexes.union(hypo_ind)
        hyper_indexes.add(hyper_index)
        patterns.append("NP and other NP")
    # NP especially NP
    flag, co, hypo_ind, hyper_index = A_especially_B(parsed_sentence)
    if flag:
        couples.extend(co)
        hypo_indexes = hypo_indexes.union(hypo_ind)
        hyper_indexes.add(hyper_index)
        patterns.append("NP especially NP")
    # such NP as NP
    flag, co, hypo_ind, hyper_index = such_A_as_B(parsed_sentence)
    if flag:
        couples.extend(co)
        hypo_indexes = hypo_indexes.union(hypo_ind)
        hyper_indexes.add(hyper_index)
        patterns.append("such NP as NP")
    if len(couples) == 0:
        return False, "", "", "", [], []
    return True, couples, patterns, sentence_couples_annotation(sentence, couples), hypo_indexes, hyper_indexes
