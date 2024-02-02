import json
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
import sys


def fetch_random_word():
    global current_word, current_word_key
    word_keys = list(words_data.keys())
    current_word_key = random.choice(word_keys)
    current_word = words_data[current_word_key]
    meaning_label.config(text=current_word['meaning'])
    entry.delete(0, tk.END)


def check_answer():
    global read_file
    user_input = entry.get()

    if not user_input:
        messagebox.showerror('错误', '请写下你的答案')

    elif user_input == current_word_key:
        messagebox.showinfo('正确!', '好!')
        # 创建一个新的JSON文件来记录已掌握的单词
        with open("learned_words.json", 'w', encoding='utf-8') as f:
            learned_words = {current_word_key: 1}
            json.dump(learned_words, f, ensure_ascii=False, indent=4)
    else:
        messagebox.showwarning('错误!', f"正确答案是'{current_word_key}'")
    fetch_random_word()


def file_path_setting(setting_path):
    global read_file, options_data
    with open('options.json', 'w', encoding='utf-8') as f:
        a = {setting_path: filedialog.askopenfilename()}
        json.dump(a, f, ensure_ascii=False, indent=4)
    return a


def check_word_format(word):
    # 检查word是否是字典，并且具有所需的键
    if not isinstance(word, dict) or list(word.keys()) != ['part_of_speech', 'meaning', 'importance']:
        return False

    # 键是否符合格式
    if not isinstance(word['part_of_speech'], str):
        return False
    if not isinstance(word['meaning'], str):
        return False
    if not isinstance(word['importance'], int):
        return False

    return True


# 排除缺少必要文件options.json的错误
if not os.path.exists('options.json'):
    messagebox.showerror('提示', '缺少必要文件options.json，我们无法知道你要指向哪一文件，将帮你重建')
    file_path_setting('read_file_path')

with open('options.json', 'r', encoding='utf-8') as f:
    options_data = json.load(f)
    read_file = options_data['read_file_path']
    # options.json: read_file_path(read_file)为空错误
    if not read_file:
        messagebox.showerror('提示', '必要文件options.json没有指向我们需要的文件，将帮你重建')
        read_file = file_path_setting('read_file_path')['read_file_path']

    with open(read_file, 'r', encoding='utf-8') as f:
        words_data = json.load(f)
        for i in words_data:
            if not check_word_format(words_data[i]):
                messagebox.showerror('错误',f'目标文件有没有符合要求的键值对{words_data[i]}')
                sys.exit()

# 创建主窗口
root = tk.Tk()
root.title('Vocabulary Trainer')
root.geometry('750x390+374+182')

# 显示单词的含义
meaning_label = tk.Label(root, text='')
meaning_label.pack(pady=20)

# 输入单词
entry = tk.Entry(root)
entry.pack(pady=20)

# 检查答案
check_button = tk.Button(root, text='检查答案', command=check_answer)
check_button.pack(pady=20)

# 获取随机单词
fetch_button = tk.Button(root, text='随机生成一个词', command=fetch_random_word)
fetch_button.pack(pady=20)

# 目标读取文件设置
read_file_path_setting_button = tk.Button(root, text='读取文件路径设置',
                                          command=lambda: file_path_setting('read_file_path'))
read_file_path_setting_button.pack(pady=20)

# 运行主循环
root.mainloop()
