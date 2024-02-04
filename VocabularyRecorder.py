import tkinter as tk
from tkinter import messagebox
import json
import os


def record_en_words():
    """"able": {
        "part_of_speech": "adj.",
        "meaning": "能够；有能力的",
        "importance": 1
    }"""
    word = word_entry.get()
    part_of_speech = part_of_speech_entry.get()
    meaning = meaning_entry.get()

    if not (word and part_of_speech and meaning):
        messagebox.showerror('错误', '没有填写完整')
        return 0

    if os.path.exists('record.json'):
        with open('record.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {}

    if word in data:
        data[word]['importance'] += 1
    else:
        data[word] = {'part_of_speech': part_of_speech, 'meaning': meaning, 'importance': 1}

    with open('record.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return data[word]


def reset_entry():
    word_entry.delete(0, tk.END)
    part_of_speech_entry.delete(0, tk.END)
    meaning_entry.delete(0, tk.END)


root = tk.Tk()
root.title('Vocabulary Recorder')
root.geometry('750x390+374+182')

tk.Label(root, text='依次输入单词、词性、意思，即可录入').pack(pady=20)
# 对应update_en_words所需参数
word_entry = tk.Entry(root)
word_entry.pack(pady=20)

part_of_speech_entry = tk.Entry(root)
part_of_speech_entry.pack(pady=20)

meaning_entry = tk.Entry(root)
meaning_entry.pack(pady=20)

record_button = tk.Button(root, text='记录', command=lambda: (record_en_words(), reset_entry()))
record_button.pack(pady=20)

resetting_button = tk.Button(root, text='重置', command=reset_entry)
resetting_button.pack(pady=20)


root.mainloop()
