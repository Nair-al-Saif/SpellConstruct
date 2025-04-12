import tkinter as tk
import os
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Components import COMPONENTS
from ComponentsEditor import ComponentEditor

class Spell:
    def __init__(self, components):
        self.components = components

    def cast(self):
        if not self.components:
            return ""
        
        result = []
        math_digits = {"Nulla", "Uno", "Dos", "Tres", "Quadro", "Quinque", "Six", "Septem", "Octo", "Novem"}
        i = 0
        while i < len(self.components):
            current = self.components[i]
            
            # Проверяем, является ли текущий компонент цифрой из категории "Математика"
            if current in math_digits:
                number = current
                # Собираем все следующие цифры в одно число
                j = i + 1
                while j < len(self.components) and self.components[j] in math_digits:
                    number += self.components[j]
                    j += 1
                result.append(number)
                i = j
            # Обрабатываем слова с "'", присоединяя их к следующему слову
            elif current.endswith("'") and i + 1 < len(self.components):
                result.append(current + self.components[i + 1])
                i += 2
            # Добавляем обычные слова с пробелом (если предыдущее не заканчивалось на "'")
            elif i == 0 or not self.components[i - 1].endswith("'"):
                result.append(current)
                i += 1
            else:
                i += 1  # Пропускаем, если это слово уже присоединено к предыдущему
        
        return " ".join(result)

class SpellGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Конструктор Заклинаний")
        self.root.geometry("800x600")  # Устанавливаем начальный размер окна

        self.inputs = {}
        self.index_to_code = {}
        self.rus_to_code = {}  # Для поиска: русское название -> код
        self.spell_components = []
        self.spell_display = []
        self.history = []
        
        self.update_component_data()
        
        # Создаем общий словарь для поиска
        for category, options in COMPONENTS.items():
            for rus, lat in options.items():
                self.rus_to_code[rus] = lat

        # Верхняя часть: компоненты в блоках с прокруткой
        self.component_container = tk.Frame(root)
        self.component_container.pack(side=tk.TOP, fill='x', padx=5, pady=5)

        self.component_canvas = tk.Canvas(self.component_container, height=200)  # Фиксированная высота для блоков
        self.component_scrollbar = tk.Scrollbar(self.component_container, orient="horizontal", command=self.component_canvas.xview)
        self.component_canvas.configure(xscrollcommand=self.component_scrollbar.set)

        self.component_frame = tk.Frame(self.component_canvas)
        self.component_canvas.create_window((0, 0), window=self.component_frame, anchor="nw")

        self.component_scrollbar.pack(side=tk.BOTTOM, fill='x')
        self.component_canvas.pack(side=tk.TOP, fill='x')
        self.create_component_blocks()

        # Привязка событий для обновления области прокрутки
        self.component_frame.bind("<Configure>", lambda e: self.component_canvas.configure(scrollregion=self.component_canvas.bbox("all")))
        # Средняя часть: область заклинания
        self.spell_frame = tk.Frame(root)
        self.spell_frame.pack(fill='x', padx=5, pady=5)
        self.canvas = tk.Canvas(self.spell_frame, height=100)
        self.canvas.pack(fill='x')

        # Нижняя часть: кнопки, поиск и вывод
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill='x', padx=5, pady=5)

        # Кнопки
        self.button_frame = tk.Frame(self.bottom_frame)
        self.button_frame.pack(fill='x')
        self.cast_button = tk.Button(self.button_frame, text="Сотворить Заклинание", command=self.cast_spell)
        self.cast_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.undo_button = tk.Button(self.button_frame, text="Отменить", command=self.undo_action)
        self.undo_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.clear_button = tk.Button(self.button_frame, text="Очистить", command=self.clear_spell)
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.edit_button = tk.Button(self.button_frame, text="Редактировать компоненты", command=self.open_editor)
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.copy_button = tk.Button(self.button_frame, text="Скопировать", command=self.copy_spell)
        self.copy_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Поиск
        self.search_frame = tk.Frame(self.bottom_frame)
        self.search_frame.pack(fill='x', pady=5)
        tk.Label(self.search_frame, text="Поиск:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill='x', expand=True)
        self.search_entry.bind('<Return>', lambda e: self.add_by_search())
        tk.Button(self.search_frame, text="Добавить", command=self.add_by_search).pack(side=tk.LEFT, padx=5)

        # Новое поле для ввода произвольного текста
        self.custom_frame = tk.Frame(self.bottom_frame)
        self.custom_frame.pack(fill='x', pady=5)
        tk.Label(self.custom_frame, text="Произвольное слово:").pack(side=tk.LEFT)
        self.custom_var = tk.StringVar()
        self.custom_entry = tk.Entry(self.custom_frame, textvariable=self.custom_var)
        self.custom_entry.pack(side=tk.LEFT, fill='x', expand=True)
        self.custom_entry.bind('<Return>', lambda e: self.add_custom_text())
        tk.Button(self.custom_frame, text="Добавить слово", command=self.add_custom_text).pack(side=tk.LEFT, padx=5)

        # Вывод
        self.output = tk.Text(self.bottom_frame, height=4, wrap='word')
        self.output.pack(fill='x', pady=5)

    def update_component_data(self):
        self.rus_to_code.clear()
        for category, options in COMPONENTS.items():
            for rus, lat in options.items():
                self.rus_to_code[rus] = lat

    def create_component_blocks(self):
        for idx, (category, options) in enumerate(COMPONENTS.items()):
            # Создаем фрейм для каждого блока
            block = tk.LabelFrame(self.component_frame, text=category, padx=5, pady=5)
            block.grid(row=0, column=idx, sticky='ns', padx=5)

            # Создаем прокручиваемый список
            scrollbar = tk.Scrollbar(block)
            scrollbar.pack(side=tk.RIGHT, fill='y')

            listbox = tk.Listbox(block, selectmode=tk.SINGLE, exportselection=False, height=10,
                               yscrollcommand=scrollbar.set)
            scrollbar.config(command=listbox.yview)
            listbox.pack(fill='y')
            listbox.bind('<Double-1>', lambda e, c=category: self.add_component(c))

            self.inputs[category] = listbox
            self.index_to_code[category] = {}

            for i, (rus, lat) in enumerate(options.items()):
                listbox.insert(tk.END, rus)
                self.index_to_code[category][i] = lat

    def open_editor(self):
        ComponentEditor(self.root, self.refresh_components)
        
    def refresh_components(self):
        self.update_component_data()
        self.create_component_blocks()
        self.update_spell_display()
        
    def add_component(self, category):
        listbox = self.inputs[category]
        selected_idx = listbox.curselection()
        if not selected_idx:
            return
        
        idx = selected_idx[0]
        code = self.index_to_code[category][idx]
        name = listbox.get(idx)
        
        self.history.append(('add', len(self.spell_components), code, name))
        self.spell_components.append(code)
        self.spell_display.append(name)
        self.update_spell_display()

    def add_custom_text(self):
        custom_text = self.custom_var.get().strip()
        if not custom_text:
            messagebox.showwarning("Ошибка", "Введите слово для заклинания!")
            return
        
        # Добавляем произвольный текст как компонент
        self.history.append(('add', len(self.spell_components), custom_text, custom_text))
        self.spell_components.append(custom_text)
        self.spell_display.append(custom_text)
        self.update_spell_display()
        self.custom_var.set("")  # Очищаем поле ввода

    def add_by_search(self):
        search_text = self.search_var.get().strip()
        if not search_text:
            return
        
        if search_text in self.rus_to_code:
            code = self.rus_to_code[search_text]
            name = search_text
            self.history.append(('add', len(self.spell_components), code, name))
            self.spell_components.append(code)
            self.spell_display.append(name)
            self.update_spell_display()
            self.search_var.set("")  # Очистка поля поиска
        else:
            messagebox.showinfo("Поиск", f"Компонент '{search_text}' не найден.")

    def update_spell_display(self):
        self.canvas.delete("all")
        x_pos = 10
        
        for i, name in enumerate(self.spell_display):
            text_id = self.canvas.create_text(x_pos, 50, text=name, anchor='w', font=("Arial", 10))
            code = self.spell_components[i]
            self.canvas.tag_bind(text_id, "<Enter>", lambda e, t=code: self.show_tooltip(e, t))
            self.canvas.tag_bind(text_id, "<Leave>", lambda e: self.hide_tooltip())
            self.canvas.tag_bind(text_id, "<Button-3>", lambda e, idx=i: self.remove_component(idx))
            x_pos += self.canvas.bbox(text_id)[2] - self.canvas.bbox(text_id)[0] + 10

    def show_tooltip(self, event, text):
        x, y = event.x + 10, event.y + 10
        self.tooltip = tk.Toplevel(self.root)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{self.root.winfo_x() + x}+{self.root.winfo_y() + y}")
        label = tk.Label(self.tooltip, text=text, background="yellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self):
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()
            del self.tooltip

    def remove_component(self, idx):
        if idx < 0 or idx >= len(self.spell_components):
            return
        
        self.history.append(('remove', idx, self.spell_components[idx], self.spell_display[idx]))
        self.spell_components.pop(idx)
        self.spell_display.pop(idx)
        self.hide_tooltip()
        self.update_spell_display()

    def undo_action(self):
        if not self.history:
            return
        
        action, idx, code, name = self.history.pop()
        
        if action == 'add':
            if idx < len(self.spell_components):
                self.spell_components.pop(idx)
                self.spell_display.pop(idx)
        elif action == 'remove':
            self.spell_components.insert(idx, code)
            self.spell_display.insert(idx, name)
        elif action == 'clear':
            self.spell_components = code[:]
            self.spell_display = name[:]
        
        self.update_spell_display()

    def clear_spell(self):
        if self.spell_components:
            self.history.append(('clear', 0, self.spell_components.copy(), self.spell_display.copy()))
        self.spell_components.clear()
        self.spell_display.clear()
        self.update_spell_display()
        self.output.delete(1.0, tk.END)

    def cast_spell(self):
        if not self.spell_components:
            messagebox.showwarning("Ошибка", "Добавьте хотя бы один компонент!")
            return
        
        spell = Spell(self.spell_components)
        result = spell.cast()
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, result)
        
    def copy_spell(self):
        spell_text = self.output.get(1.0, tk.END).strip()
        if not spell_text:
            messagebox.showwarning("Ошибка", "Сначала сотворите заклинание!")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(spell_text)
        self.root.update()  # Обновляем буфер обмена
        messagebox.showinfo("Успех", "Заклинание скопировано в буфер обмена!")

def open_spell_gui():
    spell_window = tk.Toplevel()
    SpellGUI(spell_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpellGUI(root)
    root.mainloop()
