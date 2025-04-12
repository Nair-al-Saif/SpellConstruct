// Глобальные переменные
let COMPONENTS = {}; // Список слов
let spellComponents = []; // Латинские коды
let spellDisplay = []; // Русские названия
let history = [];
let rusToCode = {};

// Загрузка компонентов из JSON
function loadComponents() {
	const input = document.getElementById('jsonInput');
	input.addEventListener('change', (event) => {
		const file = event.target.files[0];
		if (!file) {
			alert('Выберите файл components.json!');
			return;
		}
		const reader = new FileReader();
		reader.onload = (e) => {
			try {
				COMPONENTS = JSON.parse(e.target.result);
				if (!COMPONENTS || typeof COMPONENTS !== 'object') {
					throw new Error('Неверный формат JSON: ожидается объект');
				}
				initData();
				createComponentBlocks();
			} catch (error) {
				console.error('Ошибка парсинга components.json:', error);
				alert(`Не удалось загрузить components.json: ${error.message}\nПроверьте синтаксис JSON.`);
			}
		};
		reader.onerror = () => {
			alert('Ошибка чтения файла components.json.');
		};
		reader.readAsText(file);
	});
}

// Инициализация данных
function initData() {
	rusToCode = {};
	for (let category in COMPONENTS) {
		for (let rus in COMPONENTS[category]) {
			rusToCode[rus] = COMPONENTS[category][rus];
		}
	}
}

// Создание блоков компонентов
function createComponentBlocks() {
	const container = document.getElementById('componentContainer');
	container.innerHTML = '';
	for (let category in COMPONENTS) {
		const block = document.createElement('div');
		block.className = 'component-block';
		block.innerHTML = `<h3>${category}</h3>`;
		const select = document.createElement('select');
		select.size = 10;
		select.addEventListener('dblclick', () => addComponent(category, select));
		for (let rus in COMPONENTS[category]) {
			const option = document.createElement('option');
			option.value = rus;
			option.textContent = rus;
			select.appendChild(option);
		}
		block.appendChild(select);
		container.appendChild(block);
	}
}

// Добавление компонента
function addComponent(category, select) {
	const rus = select.value;
	if (!rus) return;
	const code = COMPONENTS[category][rus];
	history.push(['add', spellComponents.length, code, rus]);
	spellComponents.push(code);
	spellDisplay.push(rus);
	updateSpellDisplay();
}

// Поиск и добавление компонента
function addBySearch() {
	const searchText = document.getElementById('searchInput').value.trim();
	if (!searchText) return;
	if (rusToCode[searchText]) {
		const code = rusToCode[searchText];
		history.push(['add', spellComponents.length, code, searchText]);
		spellComponents.push(code);
		spellDisplay.push(searchText);
		updateSpellDisplay();
		document.getElementById('searchInput').value = '';
	} else {
		alert(`Компонент '${searchText}' не найден.`);
	}
}

// Обновление области заклинания
function updateSpellDisplay() {
	const spellArea = document.getElementById('spellArea');
	spellArea.innerHTML = '';
	spellDisplay.forEach((name, i) => {
		const div = document.createElement('div');
		div.className = 'spell-component';
		div.textContent = name;
		div.draggable = true;
		div.dataset.index = i;

		// Подсказка
		const tooltip = document.createElement('span');
		tooltip.className = 'tooltip';
		tooltip.textContent = spellComponents[i];
		div.appendChild(tooltip);

		// События перетаскивания
        div.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', i);
        });
        div.addEventListener('dragover', (e) => e.preventDefault());
        div.addEventListener('drop', (e) => {
            e.preventDefault();
            const fromIdx = parseInt(e.dataTransfer.getData('text/plain'));
            const toIdx = parseInt(div.dataset.index);
            if (fromIdx !== toIdx) {
                const [code, name] = [spellComponents[fromIdx], spellDisplay[fromIdx]];
                spellComponents.splice(fromIdx, 1);
                spellDisplay.splice(fromIdx, 1);
                spellComponents.splice(toIdx, 0, code);
                spellDisplay.splice(toIdx, 0, name);
                history.push(['move', fromIdx, toIdx, code, name]);
                updateSpellDisplay();
            }
        });

		// Удаление по правому клику
		div.addEventListener('contextmenu', (e) => {
			e.preventDefault();
			removeComponent(i);
		});

		spellArea.appendChild(div);
	});
}

// Удаление компонента
function removeComponent(idx) {
	if (idx < 0 || idx >= spellComponents.length) return;
	history.push(['remove', idx, spellComponents[idx], spellDisplay[idx]]);
	spellComponents.splice(idx, 1);
	spellDisplay.splice(idx, 1);
	updateSpellDisplay();
}

// Логика создания заклинания 
// Модифицированная функция castSpell для обработки произвольного текста
function castSpell() {
    if (!spellComponents.length) {
        alert('Добавьте хотя бы один компонент!');
        return;
    }
    const mathDigits = new Set(['Nulla', 'Uno', 'Dos', 'Tres', 'Quadro', 'Quinque', 'Six', 'Septem', 'Octo', 'Novem']);
    let result = [];
    let i = 0;
    while (i < spellComponents.length) {
        let current = spellComponents[i];
        if (mathDigits.has(current)) {
            let number = current;
            let j = i + 1;
            while (j < spellComponents.length && mathDigits.has(spellComponents[j])) {
                number += spellComponents[j];
                j++;
            }
            result.push(number);
            i = j;
        } else if (current.endsWith("'") && i + 1 < spellComponents.length) {
            result.push(current + spellComponents[i + 1]);
            i += 2;
        } else if (i === 0 || !spellComponents[i - 1].endsWith("'")) {
            result.push(current); // Произвольный текст обрабатывается как обычный компонент
            i++;
        } else {
            i++;
        }
    }
    const output = document.getElementById('output');
    output.value = result.join(' ');
}

// Инициализация обработчика для поля ввода произвольного текста
function initCustomInput() {
    const customInput = document.getElementById('customInput');
    customInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addCustomText();
        }
    });
}

// Отмена действия
function undoAction() {
	if (!history.length) return;
	const [action, idx, code, name] = history.pop();
	if (action === 'add') {
		spellComponents.splice(idx, 1);
		spellDisplay.splice(idx, 1);
	} else if (action === 'remove') {
		spellComponents.splice(idx, 0, code);
		spellDisplay.splice(idx, 0, name);
	} else if (action === 'clear') {
		spellComponents = [...code];
		spellDisplay = [...name];
	} else if (action === 'move') {
		const [fromIdx, toIdx] = [idx, code];
		const [movedCode, movedName] = [spellComponents[toIdx], spellDisplay[toIdx]];
		spellComponents.splice(toIdx, 1);
		spellDisplay.splice(toIdx, 1);
		spellComponents.splice(fromIdx, 0, movedCode);
		spellDisplay.splice(fromIdx, 0, movedName);
	}
	updateSpellDisplay();
}

// Очистка заклинания
function clearSpell() {
	if (spellComponents.length) {
		history.push(['clear', 0, [...spellComponents], [...spellDisplay]]);
	}
	spellComponents = [];
	spellDisplay = [];
	updateSpellDisplay();
	document.getElementById('output').value = '';
}

// Копирование заклинания
function copySpell() {
	const spellText = document.getElementById('output').value.trim();
	if (!spellText) {
		alert('Сначала сотворите заклинание!');
		return;
	}
	navigator.clipboard.writeText(spellText).then(() => {
		alert('Заклинание скопировано в буфер обмена!');
	});
}

// Открытие редактора (заглушка)
function openEditor() {
	alert('Редактор компонентов пока не реализован в веб-версии.');
	// Здесь можно добавить вызов модального окна для редактирования COMPONENTS
}

// Новая функция для добавления произвольного текста в заклинание
function addCustomText() {
    const customText = document.getElementById('customInput').value.trim();
    if (!customText) {
        alert('Введите слово для заклинания!');
        return;
    }
    // Добавляем произвольный текст как компонент
	const formattedText = `[${customText}]`;
    history.push(['add', spellComponents.length, formattedText, formattedText]);
    spellComponents.push(formattedText);
    spellDisplay.push(formattedText);
    updateSpellDisplay();
    document.getElementById('customInput').value = ''; // Очищаем поле ввода
}

// Инициализация
loadComponents()
initData();
createComponentBlocks();
initCustomInput();

// Обработка Enter в поиске
document.getElementById('searchInput').addEventListener('keypress', (e) => {
	if (e.key === 'Enter') addBySearch();
});