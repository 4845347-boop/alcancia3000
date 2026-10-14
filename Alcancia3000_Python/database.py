"""Persistencia local SQLite. Montos enteros en centavos para evitar errores decimales."""
import sqlite3
from pathlib import Path

DEFAULT_PATH = Path.home() / '.alcancia3000' / 'alcancia.db'


class Database:
    def __init__(self, path=DEFAULT_PATH):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute('PRAGMA foreign_keys = ON')
        self.create_tables()

    def create_tables(self):
        self.conn.executescript('''
        CREATE TABLE IF NOT EXISTS categories (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          kind TEXT NOT NULL CHECK(kind IN ('ingreso','gasto')),
          UNIQUE(name,kind)
        );
        CREATE TABLE IF NOT EXISTS movements (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          kind TEXT NOT NULL CHECK(kind IN ('ingreso','gasto')),
          cents INTEGER NOT NULL CHECK(cents > 0),
          category_id INTEGER NOT NULL REFERENCES categories(id),
          description TEXT NOT NULL,
          movement_date TEXT NOT NULL,
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS goals (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          target_cents INTEGER NOT NULL CHECK(target_cents > 0),
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS contributions (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          goal_id INTEGER NOT NULL REFERENCES goals(id) ON DELETE CASCADE,
          cents INTEGER NOT NULL CHECK(cents > 0),
          contribution_date TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_mov_date ON movements(movement_date);
        CREATE INDEX IF NOT EXISTS idx_mov_category ON movements(category_id);
        ''')
        seed = {
            'ingreso': ['Mesada', 'Trabajo', 'Regalo', 'Venta', 'Otro ingreso'],
            'gasto': ['Alimentación', 'Transporte', 'Educación', 'Entretenimiento', 'Salud', 'Otro gasto']
        }
        for kind, names in seed.items():
            for name in names:
                self.conn.execute('INSERT OR IGNORE INTO categories(name,kind) VALUES (?,?)', (name, kind))
        self.conn.commit()

    def query(self, sql, params=()):
        return self.conn.execute(sql, params).fetchall()

    def one(self, sql, params=()):
        return self.conn.execute(sql, params).fetchone()

    def execute(self, sql, params=()):
        with self.conn:
            return self.conn.execute(sql, params)

    def close(self):
        self.conn.close()
