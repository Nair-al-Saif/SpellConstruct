import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# Пары: отображаемое имя (русское) -> кодовое имя (латинское)
COMPONENTS = {
    "Слова силы": {
        "Воздух": "Aer", "Вода": "Aqua", "Огонь": "Ignis",
        "Порядок": "Ordo", "Земля": "Terra", "Разрушение": "Perditio",
        "Неизвестное": "Aliens", "Дерево": "Arbor", "Магия": "Auram",
        "Аура": "Praecantatio", "Тепло": "Calidium", "Разум": "Cognitio",
        "Плоть": "Corpus", "Нежить": "Exanimis", "Создание": "Fabrico",
        "Голод": "Fames", "Холод": "Frigore", "Лёд": "Gelum", "Флора": "Herba",
        "Путешествие": "Iter", "Свет": "Lux", "Механизм": "Machina", "Зло": "Malum",
        "Урожай": "Messis", "Металл": "Metallum", "Жатва": "Meto",
        "Смерть": "Mortuus", "Движение": "Motus", "Материя": "Pannus",
        "Добыча": "Perfodio", "Рост": "Permutatio", "Энергия": "Potentia",
        "Исцеление": "Sano", "Осязание": "Sensus", "Дух": "Spiritus",
        "Гроза": "Tempestas", "Тьма": "Tenebrae", "Защита": "Tutamen",
        "Пустота": "Vacous", "Яд": "Venenum", "Жизнь": "Victus",
        "Ловушка": "Vinculum", "Порча": "Vitium", "Стекло": "Vitreus",
        "Полёт": "Volatus", "Физ. урон": "Corporis", "Переплавка": "Liquescens",
        "Молния": "Fulmen", "Удушие": "Suffocatio",
        "Маг. урон": "Corpiris Praecantatio", "Толчок": "Ventilabis",
        "Тишина": "Silentium"
    },
    "Слова цели": {
        "Я": "Ego", "Цель": "Eam", "Мы": "Nos", "На себя": "Ad Te Ipsum",
        "Стена": "Murum", "Человек": "Humanus", "Инструмент": "Instrumentum",
        "Зверь": "Bestia"
    },
    "Слова формы": {
        "Взгляд": "Intentio", "Касание": "Tactus", "Луч": "Trabem",
        "Снаряд": "Missile", "Волна": "Fluctus", "Зона": "Zonam"
    },
    "Слова дополнения": {
        "Эффект по площади": "La Area", "Ослабление": "La Debilitare",
        "Усиление": "La Fortitudo", "Физика": "La Gravitas",
        "Отскок": "La Repente", "Днём сильнее": "La Forza della Sol",
        "Ночью сильнее": "La Forza della Eclipse",
        "Пронизывание": "La Pungentes", "Ускорение": "La Celeritas",
        "Урон": "La Damnum"
    },
    "Слова греха": {
        "Лень": "Desidia", "Обжорство": "Gula", "Зависть": "Invidia",
        "Гнев": "Ira", "Похоть": "Luxuria", "Гордость": "Superbia",
        "Жадность": "Lucrum", "Тщеславие": "Vanitas", "Ад": "Infernus"
    },
    "Слова благодетели": {
        "Целомудрие (Castitas)": "Castitas", "Умеренность (Temperantia)": "Temperantia",
        "Любовь (Caritas)": "Caritas", "Усердие (Industria)": "Industria",
        "Терпение (Patientia)": "Patientia", "Доброта (Humanitas)": "Humanitas",
        "Смирение (Humilitas)": "Humilitas"
    },
    "Слова времени": {
        "Время (Tempore)": "Tempore", "Назад (Restursum)": "Restursum", "Вперёд (Protinus)": "Protinus",
        "Петля (Loop)": "Loop", "Секунда (Secundo)": "Secundo", "Минута (Minute)": "Minute",
        "Час (Hora)": "Hora", "День (Dies)": "Dies", "Год (Annus)": "Annus", "Век (Saeculum)": "Saeculum",
        "Начало (Principium)": "Principium", "Конец (Finis Tempore)": "Finis Tempore"
    },
    "Условия и прочее": {
        "от": "a", "и": "et", "но": "sed", "из": "ab", "из-за": "quia",
        "не": "not", "анти": "un'", "повтор": "re'", "действие": "tu",
        "существо": "es", "если": "si", "то": "modo", "иначе": "aliver"
    }
}
# [Оставляем COMPONENTS без изменений]

class Spell:
    def __init__(self, components):
        self.components = components

    def cast(self):
        return " ".join(self.components)

class SpellGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ars Magicka: Конструктор Заклинаний")

        self.inputs = {}
        self.index_to_code = {}
        self.rus_to_code = {}  # Для поиска: русское название -> код
        self.spell_components = []
        self.spell_display = []
        self.history = []

        # Создаем общий словарь для поиска
        for category, options in COMPONENTS.items():
            for rus, lat in options.items():
                self.rus_to_code[rus] = lat

        # Верхняя часть: компоненты в блоках
        self.component_frame = tk.Frame(root)
        self.component_frame.pack(side=tk.TOP, fill='x', padx=5, pady=5)

        self.create_component_blocks()

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

        # Поиск
        self.search_frame = tk.Frame(self.bottom_frame)
        self.search_frame.pack(fill='x', pady=5)
        tk.Label(self.search_frame, text="Поиск:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill='x', expand=True)
        self.search_entry.bind('<Return>', lambda e: self.add_by_search())
        tk.Button(self.search_frame, text="Добавить", command=self.add_by_search).pack(side=tk.LEFT, padx=5)

        # Вывод
        self.output = tk.Text(self.bottom_frame, height=4, wrap='word')
        self.output.pack(fill='x', pady=5)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = SpellGUI(root)
    root.mainloop()
