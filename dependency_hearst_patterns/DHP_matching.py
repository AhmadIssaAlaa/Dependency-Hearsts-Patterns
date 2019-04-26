from dependency_hearst_patterns.DHP import *
from os import path
import operator

def DHP_matching(input_file):
    """
    Match DHP and output the couples extracted (with sentence annotation) by a specific pattern into a corresponding output file
    :param input_dir: a directory for labeled and processed corpus files exists
    :return:
    """
    output_dir = path.dirname(input_file)
    cop_dict = dict()
    for parsed_sentence in cf.get_sentences(input_file):
        _, couples, _, _, _, _ = match(parsed_sentence)
        for co in couples:
            if co in cop_dict.keys():
                cop_dict[co] += 1
            else:
                cop_dict[co] = 1
    # sorted_couples = sorted(cop_dict.items(), key=operator.itemgetter(1), reverse=True)
    out = open(output_dir + r"\extracted_couples.csv", "w")
    for co, fre in sorted(cop_dict.items(), key=operator.itemgetter(1), reverse=True):
        out.write(str(co.hyponym) + ", " + str(co.hypernym) + ", " + str(fre) + "\n")
    out.close()
    return len(cop_dict)

