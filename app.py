from flask import Flask, render_template, request, jsonify
from db_handler import DBHandler
from template_handler import TemplateHandler
import os

app = Flask(__name__)
db = DBHandler()
template_handler = TemplateHandler()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/load_template', methods=['POST'])
def load_template():
    if 'templateFile' not in request.files:
        return jsonify({'success': False, 'message': 'Файл не загружен'})

    template_file = request.files['templateFile']
    template_content = template_file.read().decode('utf-8')

    try:
        # Генерация HTML для шаблона
        template_html = template_handler.generate_html_from_template(template_content)
        return jsonify({'success': True, 'template_html': template_html})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/add_client', methods=['POST'])
def add_client():
    full_name = request.form['full_name']
    if db.add_client(full_name):
        return jsonify({'success': True, 'client': full_name})
    return jsonify({'success': False, 'message': 'Ошибка при добавлении клиента'})


@app.route('/save_order', methods=['POST'])
def save_order():
    # Получение данных из формы для сохранения приказа
    custom_inputs = request.form.getlist('custom_input')
    client_inputs = request.form.getlist('client_input')

    # Формирование текста приказа на основе шаблона
    order_text = template_handler.create_order_text(custom_inputs, client_inputs)

    # Сохранение приказа в базе данных
    db.save_order(order_text)

    return jsonify({'success': True})


@app.route('/get_orders')
def get_orders():
    orders = db.get_all_orders()
    return jsonify({'orders': orders})


@app.route('/get_fio_list')
def get_fio_list():
    fio_list = db.get_clients()
    return jsonify({'fio': fio_list})


@app.route('/edit_order', methods=['POST'])
def edit_order():
    order_id = request.form['id']
    new_text = request.form['text']
    success = db.update_order(order_id, new_text)
    if success:
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Ошибка при редактировании приказа'})


@app.route('/delete_order', methods=['POST'])
def delete_order():
    order_id = request.form['id']
    success = db.delete_order(order_id)
    if success:
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Ошибка при удалении приказа'})


@app.route('/edit_fio', methods=['POST'])
def edit_fio():
    old_fio = request.form['old_fio']
    new_fio = request.form['new_fio']
    success = db.update_fio(old_fio, new_fio)
    if success:
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Ошибка при редактировании ФИО'})


@app.route('/delete_fio', methods=['POST'])
def delete_fio():
    fio = request.form['fio']
    success = db.delete_fio(fio)
    if success:
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Ошибка при удалении ФИО'})


@app.route('/generate_document')
def generate_document():
    orders = db.get_all_orders_desc()
    return jsonify({'document': '\n\n'.join(orders)})


@app.route('/suggest_fio')
def suggest_fio():
    query = request.args.get('query', '').strip().lower()  # Получаем строку запроса
    suggestions = db.search_clients(query)
    return jsonify({'success': True, 'suggestions': suggestions})


@app.route('/get_fio_list_sorted')
def get_fio_list_sorted():
    order = request.args.get('order', 'ASC')  # Получаем параметр сортировки
    fio_list = db.get_clients_sorted(order)
    return jsonify({'fio': fio_list})



if __name__ == '__main__':
    app.run(debug=True)
