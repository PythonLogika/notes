from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import json

notes = []
note = []
name = 0

app = QApplication([])

notes_win = QWidget()
notes_win.setWindowTitle("Notes")
notes_win.resize(900, 600)

list_notes = QListWidget()
list_notes_label = QLabel("Список заміток")

field_tag = QLineEdit("")
field_tag.setPlaceholderText("Введіть тег")
field_text = QTextEdit()

button_note_create = QPushButton("Створити замітку")
button_note_delete = QPushButton("Видалити замітку")
button_note_save = QPushButton("Збегерти замітку")

button_tag_search = QPushButton("Шукати тег")
button_tag_add = QPushButton("Додати тег")
button_tag_del = QPushButton("Видалити тег")

list_tags = QListWidget()
list_tags_label = QLabel("Список тегів")

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_delete)

row_2 = QHBoxLayout()
row_2.addWidget(button_note_save) 

col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)

row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Додати замітку", "Назва замітки")    
    if ok and note_name != "":
        note = list()
        note = [note_name, '', []]
        notes.append(note)
        list_notes.addItem(note[0])
        list_tags.addItems(note[2])
        print(notes)
        with open(str(len(notes)-1)+ ".txt", "w", encoding="utf-8") as file:
            file.write(note[0]+'\n')

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    for note in notes:
        if note[0] == key:
            field_text.setText(note[1])
            list_tags.clear()
            list_tags.addItems(note[2])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        index = 0
        for note in notes:
            if note[0] == key:
                note[1] = field_text.toPlainText()
                with open(str(index) + ".txt", "w") as file:
                    file.write(note[0] + "\n")
                    file.write(note[1] + "\n")
                    for tag in note[2]:
                        file.write(tag + " ")
                    file.write("\n")
            index += 1
        print(notes)
    else:
        print("Нотатка для збереження не вибрана")

def delete_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)

        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Нотатка для видалення не знайдена")

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Нотатка для додавання не була вибрана")

def delete_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])

        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print("Теги для видалення не вибрані")

def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == "Знайти нотатку по тегу" and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        button_tag_search.setText("Скинути пошук")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(button_tag_search.text())
    elif button_tag_search.text() == "Скинути пошук":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Знайти нотатку по тегу")
        print(button_tag_search.text())
    else:
        pass

list_notes.clicked.connect(show_note)

button_note_create.clicked.connect(add_note)
button_note_delete.clicked.connect(delete_note)
button_note_save.clicked.connect(save_note)

button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(delete_tag)
button_tag_search.clicked.connect(search_tag)

while True:
    filename = str(name) + ".txt"
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.replace('\n', "")
                note.append(line)
        tags = note[2].split(" ")
        note[2] = tags
        notes.append(note)
        note = []
        name += 1
    except IOError:
        break

notes_win.show()
app.exec_()