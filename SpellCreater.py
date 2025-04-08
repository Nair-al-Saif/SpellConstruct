import tkinter as tk
from tkinter import ttk, messagebox

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

class Spell:
    def __init__(self, power, form, target, modifiers, condition=None):
        self.power = power
        self.form = form
        self.target = target
        self.modifiers = modifiers
        self.condition = condition

    def _format(self, items):
        return " et ".join(items)

    def _build_condition(self):
        if not self.condition:
            return ""
        si, modo, *aliver = self.condition
        cond = f"si {si} modo {modo}"
        if aliver:
            cond += f" aliver {aliver[0]}"
        return cond

    def cast(self):
        parts = []
        if self.condition:
            parts.append(self._build_condition())

        base = ["tu"]
        if self.power:
            base.append(self._format(self.power))
        if self.form:
            base.append(self._format(self.form))
        if self.target:
            base.append(self._format(self.target))
        if self.modifiers:
            base.append(self._format(self.modifiers))

        parts.append(" ".join(base))
        return " ".join(parts)

class SpellGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ars Magicka: Конструктор Заклинаний")

        self.inputs = {}
        self.index_to_code = {}

        for idx, (category, options) in enumerate(COMPONENTS.items()):
            label = tk.Label(root, text=category)
            label.grid(row=idx, column=0, sticky='nw')

            listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, exportselection=False, height=6)
            listbox.grid(row=idx, column=1, sticky='nsew')
            self.inputs[category] = listbox
            self.index_to_code[category] = {}

            for i, (rus, lat) in enumerate(options.items()):
                listbox.insert(tk.END, rus)
                self.index_to_code[category][i] = lat

        self.cast_button = tk.Button(root, text="Сотворить Заклинание", command=self.cast_spell)
        self.cast_button.grid(row=len(COMPONENTS), column=0, columnspan=2)

        self.output = tk.Text(root, height=4, wrap='word')
        self.output.grid(row=len(COMPONENTS) + 1, column=0, columnspan=2, sticky='nsew')

    def get_selection(self, name):
        listbox = self.inputs[name]
        selected_indices = listbox.curselection()
        return [self.index_to_code[name][i] for i in selected_indices]

    def cast_spell(self):
        power = self.get_selection("Слова силы")
        form = self.get_selection("Слова формы")
        target = self.get_selection("Слова цели")
        modifiers = self.get_selection("Слова дополнения")
        condition = self.get_selection("Условия и прочее")

        spell = Spell(power, form, target, modifiers, condition if condition else None)
        result = spell.cast()

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpellGUI(root)
    root.mainloop()
