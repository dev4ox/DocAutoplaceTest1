import sqlite3


class DBHandler:
    def __init__(self):
        # Подключение к базе данных
        self.conn = sqlite3.connect('orders.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        # Создание таблиц, если они еще не существуют
        cursor = self.conn.cursor()

        # Таблица для клиентов (ФИО)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT UNIQUE NOT NULL
            )
        ''')

        # Таблица для приказов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_text TEXT NOT NULL
            )
        ''')

        self.conn.commit()

    def add_client(self, full_name):
        """Добавляет нового клиента (ФИО) в базу данных"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO clients (full_name) VALUES (?)", (full_name,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # ФИО уже существует

    def get_clients(self):
        """Возвращает список всех клиентов (ФИО) из базы данных"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT full_name FROM clients")
        return [row[0] for row in cursor.fetchall()]

    def save_order(self, order_text):
        """Сохраняет новый приказ в базу данных"""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO orders (order_text) VALUES (?)", (order_text,))
        self.conn.commit()

    def get_all_orders(self):
        """Возвращает список всех приказов с их id и текстом"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, order_text FROM orders")
        return [{'id': row[0], 'text': row[1][:100] + '...'} for row in cursor.fetchall()]

    def get_all_orders_desc(self):
        """Возвращает все приказы в порядке убывания по id"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT order_text FROM orders ORDER BY id DESC")
        return [row[0] for row in cursor.fetchall()]

    def update_order(self, order_id, new_text):
        """Обновляет текст приказа по id"""
        cursor = self.conn.cursor()
        cursor.execute("UPDATE orders SET order_text = ? WHERE id = ?", (new_text, order_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_order(self, order_id):
        """Удаляет приказ по id"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def update_fio(self, old_fio, new_fio):
        """Обновляет ФИО клиента"""
        cursor = self.conn.cursor()
        cursor.execute("UPDATE clients SET full_name = ? WHERE full_name = ?", (new_fio, old_fio))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_fio(self, fio):
        """Удаляет ФИО клиента"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM clients WHERE full_name = ?", (fio,))
        self.conn.commit()
        return cursor.rowcount > 0

    def search_clients(self, query):
        """Возвращает список клиентов (ФИО) по введенному запросу в алфавитном порядке"""
        cursor = self.conn.cursor()
        query_pattern = f'{query}%'
        cursor.execute("SELECT full_name FROM clients WHERE lower(full_name) LIKE ? ORDER BY full_name ASC",
                       (query_pattern,))
        return [row[0] for row in cursor.fetchall()]

    def get_clients_sorted(self, order="ASC"):
        """Возвращает список всех клиентов (ФИО) с сортировкой по алфавиту"""
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT full_name FROM clients ORDER BY full_name {order}")
        return [row[0] for row in cursor.fetchall()]
