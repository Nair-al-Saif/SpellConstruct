# ComponentEditor.py
import tkinter as tk
from tkinter import ttk, messagebox
from Components import COMPONENTS
import os

class ComponentEditor:
    def __init__(self, parent, update_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Редактор компонентов")
        self.update_callback = update_callback  # Callback для обновления основного окна

        # Выбор категории
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(self.window, textvariable=self.category_var, 
                                        values=list(COMPONENTS.keys()))
        self.category_menu.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.category_menu.bind('<<ComboboxSelected>>', self.update_listbox)
        self.category_menu.set(list(COMPONENTS.keys())[0])  # Устанавливаем первую категорию по умолчанию

        # Список компонентов
        self.component_listbox = tk.Listbox(self.window, height=10)
        self.component_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.update_listbox(None)  # Инициализация списка

        # Поля ввода для добавления
        tk.Label(self.window, text="Русское название:").grid(row=2, column=0, padx=5, pady=5)
        self.rus_entry = tk.Entry(self.window)
        self.rus_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Латинский код:").grid(row=3, column=0, padx=5, pady=5)
        self.lat_entry = tk.Entry(self.window)
        self.lat_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопки
        tk.Button(self.window, text="Добавить", command=self.add_component).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(self.window, text="Удалить", command=self.remove_component).grid(row=4, column=1, padx=5, pady=5)
        tk.Button(self.window, text="Сохранить и закрыть", command=self.save_and_close).grid(row=5, column=0, columnspan=2, pady=5)

    def update_listbox(self, event):
        self.component_listbox.delete(0, tk.END)
        category = self.category_var.get()
        for rus in COMPONENTS[category].keys():
            self.component_listbox.insert(tk.END, rus)

    def add_component(self):
        rus = self.rus_entry.get().strip()
        lat = self.lat_entry.get().strip()
        category = self.category_var.get()

        if not rus or not lat:
            messagebox.showwarning("Ошибка", "Заполните оба поля!")
            return
        
        if rus in COMPONENTS[category]:
            messagebox.showwarning("Ошибка", f"Компонент '{rus}' уже существует в категории '{category}'!")
            return
        
        COMPONENTS[category][rus] = lat
        self.component_listbox.insert(tk.END, rus)
        self.rus_entry.delete(0, tk.END)
        self.lat_entry.delete(0, tk.END)
        self.save_to_file()  # Сохраняем изменения в файл

    def remove_component(self):
        selection = self.component_listbox.curselection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите компонент для удаления!")
            return
        
        category = self.category_var.get()
        rus = self.component_listbox.get(selection[0])
        del COMPONENTS[category][rus]
        self.component_listbox.delete(selection[0])
        self.save_to_file()  # Сохраняем изменения в файл

    def save_to_file(self):
        """Сохраняет обновленный словарь COMPONENTS в файл Components.py"""
        try:
            with open("Components.py", "w", encoding="utf-8") as f:
                f.write("# Components.py\n")
                f.write("COMPONENTS = {\n")
                for category, components in COMPONENTS.items():
                    f.write(f'    "{category}": {{\n')
                    for rus, lat in components.items():
                        f.write(f'        "{rus}": "{lat}",\n')
                    f.write("    },\n")
                f.write("}\n")
            # messagebox.showinfo("Успех", "Изменения сохранены в файл Components.py")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")

    def save_and_close(self):
        self.save_to_file()  # Сохраняем изменения перед закрытием
        self.update_callback()  # Обновляем основное окно
        self.window.destroy()