import json
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
import sys


been_fetch = False


def fetch_random_word():
    global current_word, current_word_key, been_fetch
    word_keys = list(words_data.keys())

    # 检查列表是否为空
    if not word_keys:
        messagebox.showerror('错误', '目标文件为空，试试VocabularyRecorder.py记录单词')
        return 1

    current_word_key = random.choice(word_keys)
    current_word = words_data[current_word_key]
    meaning_label.config(text=current_word['meaning'])
    entry.delete(0, tk.END)
    been_fetch = True


def check_answer():
    global read_file
    user_input = entry.get()

    # 如果没有随机一个单词，提示并随机
    if not been_fetch:
        messagebox.showerror('错误', '请随机一个单词')
        fetch_random_word()
        return 1

    # 判断learned_words.json是否存在
    # 不存在
    if not os.path.exists('learned_words.json'):
        with open('learned_words.json', 'w', encoding='utf-8') as f:
            pass

    # 存在
    with open('learned_words.json', 'r', encoding='utf-8') as f2:
        data = f2.read()
        if data:
            print(data)
            data = json.loads(data)
        # 没有{}
        else:
            with open('learned_words.json', 'w', encoding='utf-8') as f3:
                f3.write('{}')
                f3.close()
            data = {}

        # 检查current_word_key是否被记录
        if current_word_key in data:
            # 读取熟练度
            proficiency = data[current_word_key]
        else:
            proficiency = 0

    # 判断用户输入是否正确
    if user_input == current_word_key:
        messagebox.showinfo('正确!', '好!')
        proficiency += 1
    else:
        messagebox.showwarning('错误!', f'正确答案是：{current_word_key}')
        proficiency -= 1

    # 如果熟练度达到要求
    if proficiency >= 10 and messagebox.askyesno(title='Title', message='Do you want to proceed?'):
        # 删除词汇在readfile中的记录
        with open(read_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            del data[current_word_key]

        with open(read_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # 删除词汇在learned_words.json中的记录
        with open('learned_words.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            del data[current_word_key]

        with open('learned_words.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    data[current_word_key] = proficiency
    with open('learned_words.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

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

    with open(read_file, 'r', encoding='utf-8') as f2:
        words_data = json.load(f2)
        for i in words_data:
            if not check_word_format(words_data[i]):
                messagebox.showerror('错误', f'目标文件有没有符合要求的键值对：{words_data[i]}，正在退出')
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
