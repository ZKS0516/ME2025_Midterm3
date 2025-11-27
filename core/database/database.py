import datetime
import os
import random
import sqlite3

class Database():
    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)

    @staticmethod
    def generate_order_id() -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"OD{timestamp}{random_num}"

    # 1. 根據 category 篩選商品名稱
    def get_product_names_by_category(self, category):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT product FROM commodity WHERE category = ?", (category,))
        result = [row[0] for row in cur.fetchall()]
        conn.close()
        return result

    # 2. 根據 product 名稱查詢單價
    def get_product_price(self, product):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT price FROM commodity WHERE product = ?", (product,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None

    # 3. 新增訂單
    def add_order(self, order_data):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO order_list 
            (order_id, product_date, customer_name, product_name, product_amount, product_total, product_status, product_note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.generate_order_id(),
            order_data["product_date"],
            order_data["customer_name"],
            order_data["product_name"],
            order_data["product_amount"],
            order_data["product_total"],
            order_data["product_status"],
            order_data["product_note"]
        ))
        conn.commit()
        conn.close()

    # 4. 取得所有訂單，並合併商品價格
    def get_all_orders(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            SELECT o.order_id, o.product_date, o.customer_name, o.product_name,
                   c.price, o.product_amount, o.product_total, o.product_status, o.product_note
            FROM order_list o
            LEFT JOIN commodity c ON o.product_name = c.product
            ORDER BY o.order_id ASC
        """)
        result = cur.fetchall()
        conn.close()
        return result

    # 5. 刪除訂單
    def delete_order(self, order_id):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM order_list WHERE order_id = ?", (order_id,))
        conn.commit()
        conn.close()