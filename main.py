import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "data/trainings.json"

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.create_widgets()
        self.load_data()
        self.update_table()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = tk.Entry(self.root)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10)

        # Фильтры
        tk.Label(self.root, text="Фильтр по типу:").grid(row=4, column=0, padx=5, pady=5)
        self.filter_type = tk.Entry(self.root)
        self.filter_type.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=5, column=0, padx=5, pady=5)
        self.filter_date = tk.Entry(self.root)
        self.filter_date.grid(row=5, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Применить фильтр", command=self.apply_filter).grid(row=6, column=0, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("date", "type", "duration"), show='headings')
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип")
        self.tree.heading("duration", text="Длительность")
        self.tree.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.trainings = json.load(f)
        else:
            self.trainings = []

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for tr in self.trainings:
            self.tree.insert("", "end", values=(tr["date"], tr["type"], tr["duration"]))

    def add_training(self):
        date = self.date_entry.get()
        tr_type = self.type_entry.get()
        duration = self.duration_entry.get()

        # Валидация даты
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return

        # Валидация длительности
        try:
            duration = float(duration)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return

        self.trainings.append({"date": date, "type": tr_type, "duration": duration})
        self.save_data()
        self.update_table()

    def apply_filter(self):
        filter_type = self.filter_type.get().lower()
        filter_date = self.filter_date.get()

        filtered = []

        for tr in self.trainings:
            date_match = not filter_date or tr["date"] == filter_date
            type_match = not filter_type or filter_type in tr["type"].lower()
            if date_match and type_match:
                filtered.append(tr)

        for i in self.tree.get_children():
            self.tree.delete(i)
        for tr in filtered:
            self.tree.insert("", "end", values=(tr["date"], tr["type"], tr["duration"]))
