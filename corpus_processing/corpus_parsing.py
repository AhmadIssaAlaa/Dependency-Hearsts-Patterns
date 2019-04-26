import subprocess
def corpus_parsing_from_java(file, model_path):
    res = subprocess.check_output(['java', '-jar', model_path, file])
    return res

