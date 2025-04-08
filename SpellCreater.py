import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# Пары: отображаемое имя (русское) -> кодовое имя (латинское)
COMPONENTS = {
    "Слова силы": {
        "Воздух (Aer)": "Aer", "Вода (Aqua)": "Aqua", "Огонь (Ignis)": "Ignis",
        "Порядок (Ordo)": "Ordo", "Земля (Terra)": "Terra", "Разрушение (Perditio)": "Perditio",
        "Неизвестное (Aliens)": "Aliens", "Дерево (Arbor)": "Arbor", "Магия (Auram)": "Auram",
        "Аура (Praecantatio)": "Praecantatio", "Тепло (Calidium)": "Calidium", "Разум (Cognitio)": "Cognitio",
        "Плоть (Corpus)": "Corpus", "Нежить (Exanimis)": "Exanimis", "Создание (Fabrico)": "Fabrico",
        "Голод (Fames)": "Fames", "Холод (Frigore)": "Frigore", "Лёд (Gelum)": "Gelum", "Флора (Herba)": "Herba",
        "Путешествие (Iter)": "Iter", "Свет (Lux)": "Lux", "Механизм (Machina)": "Machina", "Зло (Malum)": "Malum",
        "Урожай (Messis)": "Messis", "Металл (Metallum)": "Metallum", "Жатва (Meto)": "Meto",
        "Смерть (Mortuus)": "Mortuus", "Движение (Motus)": "Motus", "Материя (Pannus)": "Pannus",
        "Добыча (Perfodio)": "Perfodio", "Рост (Permutatio)": "Permutatio", "Энергия (Potentia)": "Potentia",
        "Исцеление (Sano)": "Sano", "Осязание (Sensus)": "Sensus", "Дух (Spiritus)": "Spiritus",
        "Гроза (Tempestas)": "Tempestas", "Тьма (Tenebrae)": "Tenebrae", "Защита (Tutamen)": "Tutamen",
        "Пустота (Vacous)": "Vacous", "Яд (Venenum)": "Venenum", "Жизнь (Victus)": "Victus",
        "Ловушка (Vinculum)": "Vinculum", "Порча (Vitium)": "Vitium", "Стекло (Vitreus)": "Vitreus",
        "Полёт (Volatus)": "Volatus", "Физ. урон (Corporis)": "Corporis", "Переплавка (Liquescens)": "Liquescens",
        "Молния (Fulmen)": "Fulmen", "Удушие (Suffocatio)": "Suffocatio",
        "Маг. урон": "Corpiris Praecantatio", "Толчок": "Ventilabis",
        "Слепота": "Unlux", "Тишина": "Silentium"
    },
    "Слова цели": {
        "Я (Ego)": "Ego", "Цель (Eam)": "Eam", "Мы (Nos)": "Nos", "На себя (Ad Te Ipsum)": "Ad Te Ipsum",
        "Стена (Murum)": "Murum", "Человек (Humanus)": "Humanus", "Инструмент (Instrumentum)": "Instrumentum",
        "Зверь (Bestia)": "Bestia"
    },
    "Слова формы": {
        "Намерение (Intentio)": "Intentio", "Касание (Tactus)": "Tactus", "Луч (Trabem)": "Trabem",
        "Снаряд (Missile)": "Missile", "Волна (Fluctus)": "Fluctus", "Зона (Zonam)": "Zonam"
    },
    "Слова дополнения": {
        "Эффект по площади (La Area)": "La Area", "Ослабление (La Debilitare)": "La Debilitare",
        "Усиление (La Fortitudo)": "La Fortitudo", "Физика (La Gravitas)": "La Gravitas",
        "Отскок (La Repente)": "La Repente", "Днём сильнее (La Forza della Sol)": "La Forza della Sol",
        "Ночью сильнее (La Forza della Eclipse)": "La Forza della Eclipse",
        "Пронизывание (La Pungentes)": "La Pungentes", "Ускорение (La Celeritas)": "La Celeritas",
        "Урон (La Damnum)": "La Damnum"
    },
    "Слова греха": {
        "Лень (Desidia)": "Desidia", "Обжорство (Gula)": "Gula", "Зависть (Invidia)": "Invidia",
        "Гнев (Ira)": "Ira", "Похоть (Luxuria)": "Luxuria", "Гордость (Superbia)": "Superbia",
        "Жадность (Lucrum)": "Lucrum", "Тщеславие (Vanitas)": "Vanitas", "Ад (Infernus)": "Infernus"
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
        "от (a)": "a", "и (et)": "et", "но (sed)": "sed", "из (ab)": "ab", "из-за (quia)": "quia",
        "не (not)": "not", "анти (un')": "un'", "повтор (re')": "re'", "действие (tu)": "tu",
        "существо (es)": "es", "если (si)": "si", "то (modo)": "modo", "иначе (aliver)": "aliver"
    }
}
# [Оставляем COMPONENTS без изменений]

class Spell:
    def __init__(self, components):
        self.components = components  # Список компонентов в произвольном порядке

    def cast(self):
        return " ".join(self.components)

class SpellGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ars Magicka: Конструктор Заклинаний")

        self.inputs = {}
        self.index_to_code = {}
        self.spell_components = []  # Список для хранения порядка компонентов (латинские коды)
        self.spell_display = []   # Список для хранения отображаемых русских названий
        self.history = []         # Стек для истории действий
        
        # Панель выбора компонентов (слева)
        component_frame = tk.Frame(root)
        component_frame.grid(row=0, column=0, sticky='nsew')

        for idx, (category, options) in enumerate(COMPONENTS.items()):
            label = tk.Label(component_frame, text=category)
            label.grid(row=idx, column=0, sticky='nw')

            listbox = tk.Listbox(component_frame, selectmode=tk.SINGLE, exportselection=False, height=6)
            listbox.grid(row=idx, column=1, sticky='nsew')
            listbox.bind('<Double-1>', lambda e, c=category: self.add_component(c))
            self.inputs[category] = listbox
            self.index_to_code[category] = {}

            for i, (rus, lat) in enumerate(options.items()):
                listbox.insert(tk.END, rus)
                self.index_to_code[category][i] = lat

        # Панель заклинания (справа)
        spell_frame = tk.Frame(root)
        spell_frame.grid(row=0, column=1, sticky='nsew')
        
        self.canvas = tk.Canvas(spell_frame, height=100)
        self.canvas.pack(fill='x', padx=5, pady=5)
        
        # Кнопки и вывод
        button_frame = tk.Frame(root)
        button_frame.grid(row=1, column=0, columnspan=2, sticky='ew')
        
        self.cast_button = tk.Button(button_frame, text="Сотворить Заклинание", command=self.cast_spell)
        self.cast_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.undo_button = tk.Button(button_frame, text="Отменить", command=self.undo_action)
        self.undo_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.clear_button = tk.Button(button_frame, text="Очистить", command=self.clear_spell)
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.output = tk.Text(root, height=4, wrap='word')
        self.output.grid(row=2, column=0, columnspan=2, sticky='nsew')

    def add_component(self, category):
        listbox = self.inputs[category]
        selected_idx = listbox.curselection()
        if not selected_idx:
            return
        
        idx = selected_idx[0]
        code = self.index_to_code[category][idx]
        name = listbox.get(idx)
        
        # Сохраняем текущее состояние в историю
        self.history.append(('add', len(self.spell_components), code, name))
        
        # Добавляем компонент в заклинание
        self.spell_components.append(code)
        self.spell_display.append(name)
        self.update_spell_display()

    def update_spell_display(self):
        self.canvas.delete("all")
        x_pos = 10
        
        for i, name in enumerate(self.spell_display):
            # Отображаем русский текст
            text_id = self.canvas.create_text(x_pos, 50, text=name, anchor='w', font=("Arial", 10))
            
            # Добавляем подсказку (латинский код)
            code = self.spell_components[i]
            self.canvas.tag_bind(text_id, "<Enter>", lambda e, t=code: self.show_tooltip(e, t))
            self.canvas.tag_bind(text_id, "<Leave>", lambda e: self.hide_tooltip())
            
            # Возможность удаления по правому клику
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
        
        # Сохраняем действие в историю
        self.history.append(('remove', idx, self.spell_components[idx], self.spell_display[idx]))
        
        # Удаляем компонент
        self.spell_components.pop(idx)
        self.spell_display.pop(idx)
        self.update_spell_display()

    def undo_action(self):
        if not self.history:
            return
        
        action, idx, code, name = self.history.pop()
        
        if action == 'add':
            # Отмена добавления
            if idx < len(self.spell_components):
                self.spell_components.pop(idx)
                self.spell_display.pop(idx)
        elif action == 'remove':
            # Отмена удаления
            self.spell_components.insert(idx, code)
            self.spell_display.insert(idx, name)
        
        self.update_spell_display()

    def clear_spell(self):
        # Сохраняем все компоненты в историю как одно действие
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
