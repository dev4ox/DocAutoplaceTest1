import sqlite3
import shutil


class ExportImport:
    def export_db(self, export_path):
        shutil.copy('orders.db', export_path)

    def import_db(self, import_path):
        shutil.copy(import_path, 'orders.db')