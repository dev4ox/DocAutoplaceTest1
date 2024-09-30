from flask import Flask, render_template, request, send_file, redirect, url_for
from docx import Document
import io
from data import fios_list  # Импорт базового списка ФИО из data.py
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///docautoplace.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Модель для таблицы clients
class Client(db.Model):
    __tablename__ = 'clients'
    user_id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Client {self.fio}>'


# Модель для таблицы orders
class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)  # Текст приказа


# Добавление нового клиента
@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        fio = request.form['fio']
        if fio:
            new_client = Client(fio=fio)
            db.session.add(new_client)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('add_client.html')


# Редактирование клиента
@app.route('/edit_client/<int:user_id>', methods=['GET', 'POST'])
def edit_client(user_id):
    client = Client.query.get_or_404(user_id)
    if request.method == 'POST':
        fio = request.form['fio']
        if fio:
            client.fio = fio
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('edit_client.html', client=client)


# Удаление клиента
@app.route('/delete_client/<int:user_id>')
def delete_client(user_id):
    client = Client.query.get_or_404(user_id)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('index'))


# Просмотр списка приказов
@app.route('/orders_list', methods=['GET'])
def orders_list():
    # Загружаем все приказы
    orders = Order.query.order_by(Order.order_id).all()
    return render_template('orders_list.html', orders=orders)


# Удаление отдельного приказа
@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    # Удаление приказа по его ID
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('orders_list'))


# Генерация общего документа
@app.route('/generate_all_orders_docx')
def generate_all_orders_docx():
    # Получаем все приказы
    orders = Order.query.order_by(Order.order_id).all()

    # Создаем новый документ
    doc = Document()

    # Перебираем все приказы и добавляем каждый в новый документ
    for order in orders:
        doc.add_paragraph(order.text)

    # Сохраняем документ в памяти
    byte_io = io.BytesIO()
    doc.save(byte_io)
    byte_io.seek(0)

    # Отправляем документ пользователю для скачивания
    filename = "Список_приказов.docx"
    return send_file(
        byte_io,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем данные из формы
        order_number = request.form['order_number']
        order_date = request.form['order_date']
        employees_input = request.form['employees_input']
        job_date = request.form['job_date']

        # Преобразуем введенные ФИО в список и удаляем возможные лишние пробелы
        employees_list = [emp.strip() for emp in employees_input.split(',') if emp.strip()]
        employees = ', '.join(employees_list)


        # Создаем контекст для замены плейсхолдеров
        context = {
            'order_number': order_number,
            'order_date': order_date,
            'employees': employees,
            'job_date': job_date
        }

        # Сохраняем приказ в базу данных
        text_order = f"Приказ № 7-{order_number} от {order_date}г. " \
                     f"Приказ о привлечении к работе: {employees} {job_date}г."
        order_number = float(order_number)
        new_order = Order(order_id=int(order_number*10), text=text_order)
        db.session.add(new_order)
        db.session.commit()
    clients = Client.query.order_by(Client.fio).all()
    fios = [client.fio for client in clients]
    return render_template('index.html', fios=fios, clients=clients)


# Запуск приложения и инициализация базы данных
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Проверяем, если база данных пуста, добавляем базовый список ФИО
        if Client.query.count() == 0:
            for fio in fios_list:
                client = Client(fio=fio)
                db.session.add(client)
            db.session.commit()
    app.run(debug=True)
