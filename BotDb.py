import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Union

class Database:
    def __init__(self, db_name: str = 'database.db'):
        self.db_name = db_name
        self._create_tables()

    def _create_tables(self):
        """Создает таблицы, если они не существуют"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Таблица пользователей
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                privilege TEXT DEFAULT NULL,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Таблица заказов
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                price REAL,
                last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            ''')
            
            # Таблица истории цен
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
            )
            ''')
            
            # Создание индексов
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_tg_id ON users(tg_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_price_history_order_id ON price_history(order_id)')

    def _get_connection(self):
        """Возвращает соединение с базой данных"""
        return sqlite3.connect(self.db_name)

    # ========== Users Functions ==========
    def user_exists(self, tg_id: int) -> bool:
        """Проверяет, существует ли пользователь с указанным telegram ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM users WHERE tg_id = ?', (tg_id,))
            return cursor.fetchone() is not None
    def add_user(self, tg_id: int, username: Optional[str] = None, privilege: Optional[str] = None) -> int:
        """Добавляет нового пользователя"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (tg_id, username, privilege) VALUES (?, ?, ?)',
                (tg_id, username, privilege)
            )
            return cursor.lastrowid

    def get_user_by_tg_id(self, tg_id: int) -> Optional[Dict]:
        """Получает пользователя по telegram ID"""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE tg_id = ?', (tg_id,))
            user = cursor.fetchone()
            return dict(user) if user else None

    def update_user_activity(self, tg_id: int):
        """Обновляет время последней активности пользователя"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET last_activity = CURRENT_TIMESTAMP WHERE tg_id = ?',
                (tg_id,)
            )

    def update_user_privilege(self, tg_id: int, privilege: str):
        """Обновляет привилегии пользователя"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET privilege = ? WHERE tg_id = ?',
                (privilege, tg_id)
            )

    def delete_user(self, tg_id: int):
        """Удаляет пользователя (каскадно удалит его заказы и историю цен)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE tg_id = ?', (tg_id,))

    # ========== Orders Functions ==========
    def add_order(
        self,
        user_tg_id: int,
        name: str,
        url: str,
        price: float,
        status: str = 'active'
    ) -> int:
        """Добавляет новый заказ"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Получаем user_id по tg_id
            user = self.get_user_by_tg_id(user_tg_id)
            if not user:
                raise ValueError(f"User with tg_id {user_tg_id} not found")
            
            cursor.execute(
                '''INSERT INTO orders 
                (user_id, name, url, status, price) 
                VALUES (?, ?, ?, ?, ?)''',
                (user['id'], name, url, status, price)
            )
            order_id = cursor.lastrowid
            
            # Добавляем запись в историю цен
            self._add_price_history(cursor,order_id, price)
            
            return order_id

    def get_order_by_id(self, order_id: int) -> Optional[Dict]:
        """Получает заказ по ID"""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
            order = cursor.fetchone()
            return dict(order) if order else None

    def get_user_orders(self, user_tg_id: int) -> List[Dict]:
        """Получает все заказы пользователя"""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            user = self.get_user_by_tg_id(user_tg_id)
            if not user:
                return []
            
            cursor.execute('SELECT * FROM orders WHERE user_id = ?', (user['id'],))
            return [dict(row) for row in cursor.fetchall()]

    def update_order_price(self, order_id: int, new_price: float):
        """Обновляет цену заказа и добавляет запись в историю цен"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Обновляем цену в заказе
            cursor.execute(
                '''UPDATE orders 
                SET price = ?, last_update = CURRENT_TIMESTAMP 
                WHERE id = ?''',
                (new_price, order_id)
            )
            
            # Добавляем запись в историю цен
            self._add_price_history(cursor,order_id, new_price)

    def update_order_status(self, order_id: int, new_status: str):
        """Обновляет статус заказа"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''UPDATE orders 
                SET status = ?, last_update = CURRENT_TIMESTAMP 
                WHERE id = ?''',
                (new_status, order_id)
            )

    def delete_order(self, order_id: int):
        """Удаляет заказ (каскадно удалит историю цен)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM orders WHERE id = ?', (order_id,))

    # ========== Price History Functions ==========
    def _add_price_history(self,cursor, order_id: int, price: float):
        """Внутренняя функция для добавления записи в историю цен"""
        cursor.execute(
            'INSERT INTO price_history (order_id, price) VALUES (?, ?)',
            (order_id, price)
        )

    def get_price_history(self, order_id: int, limit: int = 10) -> List[Dict]:
        """Получает историю цен для заказа"""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT * FROM price_history 
                WHERE order_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?''',
                (order_id, limit)
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_price_changes_stats(self, order_id: int) -> Dict:
        """Возвращает статистику по изменению цен"""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Получаем текущую цену
            cursor.execute('SELECT price FROM orders WHERE id = ?', (order_id,))
            current_price = cursor.fetchone()[0]
            
            # Получаем минимальную цену
            cursor.execute('SELECT MIN(price) FROM price_history WHERE order_id = ?', (order_id,))
            min_price = cursor.fetchone()[0]
            
            # Получаем максимальную цену
            cursor.execute('SELECT MAX(price) FROM price_history WHERE order_id = ?', (order_id,))
            max_price = cursor.fetchone()[0]
            
            return {
                'current': current_price,
                'min': min_price,
                'max': max_price,
                'diff_current_min': round(current_price - min_price, 2),
                'diff_current_max': round(current_price - max_price, 2)
            }

    # ========== Utility Functions ==========
    def get_all_active_orders(self) -> List[Dict]:
        """Получает все активные заказы"""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders WHERE status = 'active'")
            return [dict(row) for row in cursor.fetchall()]

    def close(self):
        """Закрывает соединение с базой данных (для контекстного менеджера)"""
        self._get_connection().close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()