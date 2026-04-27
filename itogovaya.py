import tkinter as tk
import json
from tkinter import messagebox
import os

window = tk.Tk()
window.title("Трекер прочитанных книг")
window.geometry("550x650")

title_label = tk.Label(window, text="Название книги:").pack()
title_entry = tk.Entry(window, width=40)
title_entry.pack()

if os.path.exists("books.json"):
    with open("books.json", "r", encoding="utf-8") as f:
        books = json.load(f)
else:
    books = []


def save_books():
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


def update_list():
    listbox.delete(0, tk.END)
    genre_filter = filter_entry.get().lower()
    pages_filter = pages_filter_var.get()
    for b in books:
        if genre_filter and genre_filter not in b["Жанр"].lower():
            continue
        if pages_filter == ">200" and int(b["Страницы"]) <= 200:
            continue
        if pages_filter == "<200" and int(b["Страницы"]) >= 200:
            continue
        listbox.insert(tk.END, f"{b['Название']} - {b['Автор']} ({b['Жанр']}) - {b['Страницы']} стр.")
    counter_label.config(text=f"Всего книг: {len(books)}")


def on_filter_change(event):
    update_list()


def on_pages_filter_change(value):
    update_list()


def add_book():
    title = title_entry.get()
    author = author_entry.get()
    zanr = zanr_entry.get()
    pages = pages_entry.get()

    if not title or not author or not zanr or not pages:
        messagebox.showwarning("Ошибка", "Заполните все поля!")
        return
    if not pages.isdigit():
        messagebox.showwarning("Ошибка", "Страницы должны быть числом!")
        return

    books.append({"Название": title, "Автор": author, "Жанр": zanr, "Страницы": pages})
    save_books()
    update_list()
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    zanr_entry.delete(0, tk.END)
    pages_entry.delete(0, tk.END)


def delete_book():
    if not listbox.curselection():
        messagebox.showwarning("Ошибка", "Выберите книгу!")
        return
    selected = listbox.get(listbox.curselection()[0])
    for i, b in enumerate(books):
        if f"{b['Название']} - {b['Автор']} ({b['Жанр']}) - {b['Страницы']} стр." == selected:
            del books[i]
            break
    save_books()
    update_list()


def clear_filters():
    filter_entry.delete(0, tk.END)
    pages_filter_var.set("Все")
    update_list()


tk.Label(window, text="Автор:").pack()
author_entry = tk.Entry(window, width=40)
author_entry.pack()

zanr_label = tk.Label(window, text="Жанр:").pack()
zanr_entry = tk.Entry(window, width=40)
zanr_entry.pack()

pages_label = tk.Label(window, text="Количество страниц:").pack()
pages_entry = tk.Entry(window, width=40)
pages_entry.pack()

tk.Button(window, text="Добавить книгу", bg="green", command=add_book, fg="white").pack(pady=5)
tk.Button(window, text="Удалить книгу", bg="red", command=delete_book, fg="white").pack(pady=5)

listbox = tk.Listbox(window, width=65, height=12)
listbox.pack(pady=10)

tk.Label(window, text="--- ФИЛЬТРЫ ---").pack(pady=5)
tk.Label(window, text="Фильтр по жанру:").pack()
filter_entry = tk.Entry(window, width=30)
filter_entry.pack()
filter_entry.bind("<KeyRelease>", on_filter_change)

tk.Label(window, text="Фильтр по страницам:").pack()
pages_filter_var = tk.StringVar(value="Все")
filter_pages = tk.OptionMenu(window, pages_filter_var, "Все", ">200", "<200", command=on_pages_filter_change)
filter_pages.pack()

tk.Button(window, text="Сбросить фильтры", bg="orange", command=clear_filters, fg="white").pack(pady=5)

counter_label = tk.Label(window, text="Всего книг: 0", font=("Arial", 10, "bold"), fg="blue")
counter_label.pack(pady=5)

update_list()
window.mainloop()