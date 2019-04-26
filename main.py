import tkinter
from os import path
import time
from dependency_hearst_patterns import DHP_matching as DHP
from tkinter.scrolledtext import ScrolledText
from corpus_processing import corpus_parsing
from tkinter import filedialog
import os

from tkinter import ttk

class GUI_main():
    def __init__(self):
        self.java_model_path = ""
        self.parsed_file = ""
        self.corpus_files= []
        self.initialize()

    def initialize(self):
        window = tkinter.Tk()
        window.state('zoomed')
        window.title("Hypernym Patterns")

        # tab pages
        tab_control = ttk.Notebook(window)
        # tab 1
        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='Dependency Hearst Patterns')

        self.tab1_controls(tab1)

        tab_control.pack(expand=1, fill='both')
        window.mainloop()

        # end tab pages

    def tab1_controls(self, tab1):

        def select_pre_processed_file():
            file = filedialog.askopenfilename(filetypes=(("Text file", "*.txt"),))
            txt_parsed.delete(0, tkinter.END)
            txt_parsed.insert(0, str(file))
            self.parsed_file = file

        def run_DHP_matching():
            start = time.time()
            nb_of_couples = DHP.DHP_matching(self.parsed_file)
            end = time.time()
            sc_text.insert(tkinter.END, "Hypernymy Extraction: Finish \n")
            sc_text.insert(tkinter.END, "Total extracted couples:" + str(nb_of_couples) +"\n")
            sc_text.insert(tkinter.END, "Matching Time (sec): " + str(end - start) + "\n\n")

        def run_corpus_parsing():
            for file in self.corpus_files:
                res = corpus_parsing.corpus_parsing_from_java(file, self.java_model_path)
                sc_text.insert(tkinter.END, res)


        def select_java_model_directory():
            file = filedialog.askopenfilename(filetypes=(("Jar files", "*.jar"),))
            txt2.delete(0, tkinter.END)
            txt2.insert(0, str(file))
            self.java_model_path = file

        def select_corpus_files():
            files = filedialog.askopenfilenames(filetypes=(("Text files", "*.txt"),))
            txt1.delete(0, tkinter.END)
            self.corpus_files = []
            for i, file in enumerate(files):
                self.corpus_files.append(str(file))
                if i == 0:
                    txt1.insert(0, str(file))
                else:
                    txt1.insert(0, str(file) + " & ")


        lbl = tkinter.Label(tab1, text="Corpus Pre-processing", font=("Arial Bold", 14))
        lbl.grid(column=1, row=0, sticky='W', padx=4, pady=4, ipadx=4, ipady=4)

        # row 1
        # label
        lbl1 = tkinter.Label(tab1, text="corpus files", font=("Arial Bold", 12))
        lbl1.grid(column=1, row=1, sticky='W', padx=4, pady=4, ipadx=4, ipady=4)
        # text
        txt1 = tkinter.Entry(tab1, width=100)
        txt1.grid(column=2, row=1, sticky='W', padx=4, pady=4, ipadx=4, ipady=4)
        # button
        B1 = tkinter.Button(tab1, text="select corpus files", command=select_corpus_files)
        B1.grid(column=3, row=1, sticky='W', padx=4, pady=4, ipadx=4, ipady=4)

        # row2
        # label
        lbl2 = tkinter.Label(tab1, text="Pre-processing Java Model Path", font=("Arial Bold", 12))
        lbl2.grid(column=1, row=2, sticky='W', padx=4, pady=4, ipadx=4, ipady=4)
        # text
        txt2 = tkinter.Entry(tab1, width=100)
        txt2.grid(column=2, row=2, sticky='W', padx=4, pady=4, ipadx=4, ipady=4)
        # button
        B2 = tkinter.Button(tab1, text="select model path", command=select_java_model_directory)
        B2.grid(column=3, row=2, sticky='W', padx=4, pady=4, ipadx=4, ipady=4)

        #row 4
        # button
        B3 = tkinter.Button(tab1, text="Run corpus pre-processing", command=run_corpus_parsing)
        B3.grid(column=2, row=4, sticky='W', padx=4, pady=4, ipadx=4, ipady=4)

        # row 5
        lbl = tkinter.Label(tab1, text="Hypernymy Extraction by DHP Matching", font=("Arial Bold", 14))
        lbl.grid(column=1, row=5, sticky='W', padx=4, pady=4, ipadx=4, ipady=4)

        # row 6
        # label
        lbl0 = tkinter.Label(tab1, text="Pre-processed corpus file", font=("Arial Bold", 12))
        lbl0.grid(column=1, row=6, sticky='W', padx=4, pady=4, ipadx=4, ipady=4)
        # text
        txt_parsed = tkinter.Entry(tab1, width=100)
        txt_parsed.grid(column=2, row=6, sticky='W', padx=4, pady=4, ipadx=4, ipady=4)
        # button
        B0 = tkinter.Button(tab1, text="select pre-processed file", command=select_pre_processed_file)
        B0.grid(column=3, row=6, sticky='W', padx=4, pady=4, ipadx=4, ipady=4)

        # row 7
        # button
        B2 = tkinter.Button(tab1, text="Run DHP Matching", command=run_DHP_matching)
        B2.grid(column=2, row=7, sticky='W', padx=4, pady=4, ipadx=4, ipady=4)
        #row 10
        sc_text = ScrolledText(tab1, width=80, height=12)
        sc_text.grid(column=2, row=10, sticky='W', padx=4, pady=4, ipadx=4, ipady=4)

if __name__ == '__main__':
    GUI_main()