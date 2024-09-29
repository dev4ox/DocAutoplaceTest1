// Маска для проверки ФИО в формате Фамилия И.О.
function validateFIO(input) {
    const fioPattern = /^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.[А-ЯЁ]\.$/;
    return fioPattern.test(input);
}

// Обработка ввода в поле ФИО с автозаполнением
document.addEventListener('input', function(event) {
    if (event.target && event.target.classList.contains('fioInput')) {
        const inputField = event.target;
        const suggestionsBox = inputField.nextElementSibling;
        const query = inputField.value.trim().toLowerCase();

        // Запрос автоподсказок
        if (query.length > 1) {
            fetch(`/suggest_fio?query=${query}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Очистка старых подсказок
                    suggestionsBox.innerHTML = '';
                    // Добавление новых подсказок
                    data.suggestions.forEach(fio => {
                        const suggestionItem = document.createElement('div');
                        suggestionItem.classList.add('suggestion-item');
                        suggestionItem.textContent = fio;
                        suggestionItem.addEventListener('click', function() {
                            inputField.value = fio;
                            suggestionsBox.innerHTML = '';  // Очистка после выбора
                        });
                        suggestionsBox.appendChild(suggestionItem);
                    });
                }
            });
        } else {
            suggestionsBox.innerHTML = '';  // Очистка, если ввод короткий
        }
    }
});

// Добавление нового поля для ФИО
function addFIOInputField() {
    const dynamicTemplate = document.getElementById('dynamicTemplate');

    // Создаем новое поле для ввода ФИО
    const newFIOField = document.createElement('div');
    newFIOField.classList.add('fio-container');
    newFIOField.innerHTML = `
        <input type="text" class="fioInput" placeholder="Введите Фамилия И.О." style="width: 200px;">
        <div class="suggestions"></div>
    `;
    dynamicTemplate.appendChild(newFIOField);

    // Фокус на новое поле ввода
    newFIOField.querySelector('.fioInput').addEventListener('input', function() {
        this.style.borderColor = ''; // Убираем красную границу при новом вводе
    });
}

// Обработка ввода в поле ФИО
document.addEventListener('keydown', function(event) {
    if (event.target && event.target.classList.contains('fioInput') && event.key === 'Enter') {
        event.preventDefault();
        const inputField = event.target;
        const query = inputField.value.trim();

        // Проверка валидности по маске
        if (validateFIO(query)) {
            // Если ФИО подходит по маске и не найдено в базе, добавляем
            fetch(`/add_client`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({ full_name: query })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Если успешно добавлено, очищаем поле и создаем новое
                    inputField.style.borderColor = 'green';
                    addFIOInputField();
                } else {
                    alert(data.message);
                }
            });
        } else {
            inputField.style.borderColor = 'red';
            alert('ФИО должно быть в формате: Фамилия И.О.');
        }
    }
});

// Обработка загрузки шаблона
document.getElementById('templateForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = new FormData();
    let fileInput = document.getElementById('templateFile').files[0];
    formData.append('templateFile', fileInput);

    fetch('/load_template', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('dynamicTemplate').innerHTML = data.template_html;
        } else {
            alert(data.message);
        }
    });
});

// Загрузка списка приказов в левую панель
function loadOrders() {
    fetch('/get_orders')
    .then(response => response.json())
    .then(data => {
        const ordersList = document.getElementById('ordersList');
        ordersList.innerHTML = '';
        data.orders.forEach(order => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                ${order.text}
                <button onclick="editOrder(${order.id})">Редактировать</button>
                <button onclick="deleteOrder(${order.id})">Удалить</button>
            `;
            ordersList.appendChild(listItem);
        });
    });
}

// Загрузка списка ФИО в правую панель
function loadFIOList() {
    fetch('/get_fio_list')
    .then(response => response.json())
    .then(data => {
        const fioList = document.getElementById('fioList');
        fioList.innerHTML = '';
        data.fio.forEach(fio => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                ${fio}
                <button onclick="editFIO('${fio}')">Редактировать</button>
                <button onclick="deleteFIO('${fio}')">Удалить</button>
            `;
            fioList.appendChild(listItem);
        });
    });
}

// Функция редактирования приказа
function editOrder(orderId) {
    const newOrderText = prompt('Введите новый текст приказа:');
    if (newOrderText) {
        fetch(`/edit_order`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ id: orderId, text: newOrderText })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadOrders(); // Перезагрузка списка приказов
            } else {
                alert(data.message);
            }
        });
    }
}

// Функция удаления приказа
function deleteOrder(orderId) {
    if (confirm('Вы уверены, что хотите удалить этот приказ?')) {
        fetch(`/delete_order`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ id: orderId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadOrders(); // Перезагрузка списка приказов
            } else {
                alert(data.message);
            }
        });
    }
}

// Функция редактирования ФИО
function editFIO(fio) {
    const newFIO = prompt('Введите новое ФИО:', fio);
    if (newFIO && validateFIO(newFIO)) {
        fetch(`/edit_fio`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ old_fio: fio, new_fio: newFIO })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadFIOList(); // Перезагрузка списка ФИО
            } else {
                alert(data.message);
            }
        });
    } else {
        alert('ФИО должно быть в формате: Фамилия И.О.');
    }
}

// Функция удаления ФИО
function deleteFIO(fio) {
    if (confirm('Вы уверены, что хотите удалить это ФИО?')) {
        fetch(`/delete_fio`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ fio: fio })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadFIOList(); // Перезагрузка списка ФИО
            } else {
                alert(data.message);
            }
        });
    }
}

// Генерация общего документа
document.getElementById('generateDocumentBtn').addEventListener('click', function() {
    fetch('/generate_document')
    .then(response => response.json())
    .then(data => {
        document.getElementById('documentContent').textContent = data.document;
    });
});

// Загрузка списка ФИО с сортировкой
function loadFIOList(order = 'ASC') {
    fetch(`/get_fio_list_sorted?order=${order}`)
    .then(response => response.json())
    .then(data => {
        const fioList = document.getElementById('fioList');
        fioList.innerHTML = '';
        data.fio.forEach(fio => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                ${fio}
                <button onclick="editFIO('${fio}')">Редактировать</button>
                <button onclick="deleteFIO('${fio}')">Удалить</button>
            `;
            fioList.appendChild(listItem);
        });
    });
}

// Загрузка данных при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    loadOrders();
    loadFIOList();  // Загружаем список ФИО по возрастанию по умолчанию
});
