class parsed_sentence:
    def __init__(self):
        self.id = -1
        self.words = []
        self.NPs = []

    def get_lemma_by_index(self, ind):
        for word in self.words:
            if word.index == ind:
                return word.lemma
        return None

    def get_sequence_representation(self, hypo_indexes = [], hyper_indexes = []):
        if len(self.NPs) == 0:
            return "[]"
        s = "["
        np_i = 0
        for word in self.words:
            if word.pos.lower() == "dt":
                continue
            if word.index in hyper_indexes:
                word_h = "hyper, "
            elif word.index in hypo_indexes:
                word_h = "hypo, "
            else:
                word_h = ""
            if word.parent_index in hyper_indexes:
                parent = "hyper"
            elif word.parent_index in hypo_indexes:
                parent = "hypo"
            else:
                parent_index = word.parent_index
                parent = self.get_lemma_by_index(parent_index)
                if parent == None:
                    parent = word.parent
                # parent = word.parent
            if np_i > len(self.NPs) - 1:
                np_i = len(self.NPs) - 1
            np = self.NPs[np_i]
            if word.index >= np.start and word.index <= np.end:
                if word.index == np.end:
                    np_i += 1
                if word.index == np.root_index:
                    if word_h == "hypo, " and parent == "hypo":
                        continue
                    if word_h=="hypo, " or word_h == "hyper, ":
                        s += "(NP, " + word_h + word.lemma + "_lemma, " + word.pos + ", " + word.dep_rel + ", " + parent + "_dep), "
                    else:
                        s += "(" + np.text.replace(" ", "_") + "_label, NP, " + word_h + word.lemma + "_lemma, " + word.pos + ", " + word.dep_rel + ", " + parent + "_dep), "
            else:
                if word_h == "hypo, " and parent == "hypo":
                    continue
                s += "(" + word.word + "_label, " + word_h + word.lemma + "_lemma, " + word.pos + ", " + word.dep_rel + ", " + parent + "_dep), "
        s = s[:-2] + "]"
        return s

    def add_word(self, w, l, pos, i, par, parent_index, rel , ty):
        word = parsed_word(w, l, pos, i, par, parent_index, rel, ty)
        self.words.append(word)

    def add_NP(self, np, root, ri, start, end):
        np2 = noun_phrase(np, root, ri, start, end)
        self.NPs.append(np2)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return " ".join([word.word for word in self.words])

class parsed_word:
    def __init__(self, w, l, pos, i, par, parent_index, rel, ty):
        self.word = w
        self.lemma = l
        self.pos = pos
        self.index = i
        self.dep_rel = rel
        self.parent = par
        self.parent_index = parent_index
        self.type = ty

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "(" + self.word + ", " + self.lemma + ", " + self.pos + ", " + str(self.index) + ", " + self.parent + ", " + str(self.parent_index) + ", " + self.dep_rel+ ", " + self.type + ")"

class noun_phrase:
    def __init__(self, np, root, ri, start, end):
        self.text = np
        self.root = root
        self.root_index = ri
        self.start = start
        self.end = end

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "(" + self.text + ", " + self.root + ", " + str(self.root_index) + ", " + str(self.start) + ", " + str(self.end) + ")"