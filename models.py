"""
Zion Business Manager - Data Models
CRUD operations for all business entities
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from database import db_manager


class BaseModel:
    """Base model class with common operations"""
    
    @classmethod
    def get_all(cls) -> List[Dict]:
        """Get all records"""
        with db_manager.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {cls.table_name}")
            return [dict(row) for row in cursor.fetchall()]
    
    @classmethod
    def get_by_id(cls, record_id: int) -> Optional[Dict]:
        """Get record by ID"""
        with db_manager.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {cls.table_name} WHERE id = ?", (record_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @classmethod
    def delete(cls, record_id: int) -> bool:
        """Delete record by ID"""
        with db_manager.cursor() as cursor:
            cursor.execute(f"DELETE FROM {cls.table_name} WHERE id = ?", (record_id,))
            return cursor.rowcount > 0


class Customer(BaseModel):
    """Customer model"""
    table_name = "customers"
    
    @classmethod
    def create(cls, name: str, email: str = "", phone: str = "", address: str = "") -> int:
        """Create a new customer"""
        with db_manager.cursor() as cursor:
            cursor.execute("""
                INSERT INTO customers (name, email, phone, address)
                VALUES (?, ?, ?, ?)
            """, (name, email, phone, address))
            return cursor.lastrowid
    
    @classmethod
    def update(cls, record_id: int, **kwargs) -> bool:
        """Update customer record"""
        if not kwargs:
            return False
        
        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [record_id]
        
        with db_manager.cursor() as cursor:
            cursor.execute(f"""
                UPDATE customers SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, values)
            return cursor.rowcount > 0
    
    @classmethod
    def search(cls, query: str) -> List[Dict]:
        """Search customers by name or email"""
        with db_manager.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM customers 
                WHERE name LIKE ? OR email LIKE ?
            """, (f"%{query}%", f"%{query}%"))
            return [dict(row) for row in cursor.fetchall()]


class Supplier(BaseModel):
    """Supplier model"""
    table_name = "suppliers"
    
    @classmethod
    def create(cls, name: str, email: str = "", phone: str = "", 
               address: str = "", contact_person: str = "") -> int:
        """Create a new supplier"""
        with db_manager.cursor() as cursor:
            cursor.execute("""
                INSERT INTO suppliers (name, email, phone, address, contact_person)
                VALUES (?, ?, ?, ?, ?)
            """, (name, email, phone, address, contact_person))
            return cursor.lastrowid
    
    @classmethod
    def update(cls, record_id: int, **kwargs) -> bool:
        """Update supplier record"""
        if not kwargs:
            return False
        
        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [record_id]
        
        with db_manager.cursor() as cursor:
            cursor.execute(f"""
                UPDATE suppliers SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, values)
            return cursor.rowcount > 0


class Category(BaseModel):
    """Category model"""
    table_name = "categories"
    
    @classmethod
    def create(cls, name: str, description: str = "") -> int:
        """Create a new category"""
        with db_manager.cursor() as cursor:
            cursor.execute("""
                INSERT INTO categories (name, description)
                VALUES (?, ?)
            """, (name, description))
            return cursor.lastrowid
    
    @classmethod
    def update(cls, record_id: int, **kwargs) -> bool:
        """Update category record"""
        if not kwargs:
            return False
        
        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [record_id]
        
        with db_manager.cursor() as cursor:
            cursor.execute(f"""
                UPDATE categories SET {set_clause} WHERE id = ?
            """, values)
            return cursor.rowcount > 0


class Product(BaseModel):
    """Product model"""
    table_name = "products"
    
    @classmethod
    def create(cls, name: str, sku: str, price: float, 
               description: str = "", cost_price: float = 0,
               quantity: int = 0, min_quantity: int = 0,
               category_id: int = None, supplier_id: int = None) -> int:
        """Create a new product"""
        with db_manager.cursor() as cursor:
            cursor.execute("""
                INSERT INTO products (name, sku, price, description, cost_price, 
                                     quantity, min_quantity, category_id, supplier_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, sku, price, description, cost_price, 
                  quantity, min_quantity, category_id, supplier_id))
            return cursor.lastrowid
    
    @classmethod
    def update(cls, record_id: int, **kwargs) -> bool:
        """Update product record"""
        if not kwargs:
            return False
        
        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [record_id]
        
        with db_manager.cursor() as cursor:
            cursor.execute(f"""
                UPDATE products SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, values)
            return cursor.rowcount > 0
    
    @classmethod
    def update_quantity(cls, record_id: int, quantity_change: int) -> bool:
        """Update product quantity by adding/subtracting"""
        with db_manager.cursor() as cursor:
            cursor.execute("""
                UPDATE products SET quantity = quantity + ?, 
                updated_at = CURRENT_TIMESTAMP WHERE id = ?
            """, (quantity_change, record_id))
            return cursor.rowcount > 0
    
    @classmethod
    def get_low_stock(cls) -> List[Dict]:
        """Get products with quantity below minimum"""
        with db_manager.cursor() as cursor:
            cursor.execute("""
                SELECT p.*, c.name as category_name 
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.quantity <= p.min_quantity
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    @classmethod
    def search(cls, query: str) -> List[Dict]:
        """Search products by name, sku, or description"""
        with db_manager.cursor() as cursor:
            cursor.execute("""
                SELECT p.*, c.name as category_name 
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.name LIKE ? OR p.sku LIKE ? OR p.description LIKE ?
            """, (f"%{query}%", f"%{query}%", f"%{query}%"))
            return [dict(row) for row in cursor.fetchall()]


class Order(BaseModel):
    """Order model"""
    table_name = "orders"
    
    @classmethod
    def create(cls, customer_id: int = None, notes: str = "") -> int:
        """Create a new order"""
        with db_manager.cursor() as cursor:
            cursor.execute("""
                INSERT INTO orders (customer_id, notes)
                VALUES (?, ?)
            """, (customer_id, notes))
            return cursor.lastrowid
    
    @classmethod
    def update(cls, record_id: int, **kwargs) -> bool:
        """Update order record"""
        if not kwargs:
            return False
        
        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [record_id]
        
        with db_manager.cursor() as cursor:
            cursor.execute(f"""
                UPDATE orders SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, values)
            return cursor.rowcount > 0
    
    @classmethod
    def get_order_details(cls, order_id: int) -> Dict:
        """Get complete order details with items"""
        with db_manager.cursor() as cursor:
            # Get order info
            cursor.execute("""
                SELECT o.*, c.name as customer_name, c.email as customer_email
                FROM orders o
                LEFT JOIN customers c ON o.customer_id = c.id
                WHERE o.id = ?
            """, (order_id,))
            order = dict(cursor.fetchone()) if cursor.fetchone() else None
            
            if order:
                # Get order items
                cursor.execute("""
                    SELECT oi.*, p.name as product_name, p.sku
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.id
                    WHERE oi.order_id = ?
                """, (order_id,))
                order['items'] = [dict(row) for row in cursor.fetchall()]
            
            return order
    
    @classmethod
    def get_by_status(cls, status: str) -> List[Dict]:
        """Get orders by status"""
        with db_manager.cursor() as cursor:
            cursor.execute("""
                SELECT o.*, c.name as customer_name
                FROM orders o
                LEFT JOIN customers c ON o.customer_id = c.id
                WHERE o.status = ?
                ORDER BY o.order_date DESC
            """, (status,))
            return [dict(row) for row in cursor.fetchall()]


class OrderItem(BaseModel):
    """Order Item model"""
    table_name = "order_items"
    
    @classmethod
    def create(cls, order_id: int, product_id: int, 
               quantity: int, unit_price: float) -> int:
        """Create order item and update product quantity"""
        with db_manager.cursor() as cursor:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
            """, (order_id, product_id, quantity, unit_price))
            
            # Reduce product quantity
            cursor.execute("""
                UPDATE products SET quantity = quantity - ?,
                updated_at = CURRENT_TIMESTAMP WHERE id = ?
            """, (quantity, product_id))
            
            return cursor.lastrowid


class Transaction(BaseModel):
    """Transaction model for financial tracking"""
    table_name = "transactions"
    
    @classmethod
    def create(cls, transaction_type: str, order_id: int = None, 
               amount: float = 0, payment_method: str = "", notes: str = "") -> int:
        """Create a new transaction"""
        with db_manager.cursor() as cursor:
            cursor.execute("""
                INSERT INTO transactions (order_id, transaction_type, amount, 
                                        payment_method, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, transaction_type, amount, payment_method, notes))
            return cursor.lastrowid
    
    @classmethod
    def get_summary(cls, start_date: str = None, end_date: str = None) -> Dict:
        """Get transaction summary"""
        query = """
            SELECT transaction_type, SUM(amount) as total
            FROM transactions
        """
        params = []
        
        if start_date and end_date:
            query += " WHERE transaction_date BETWEEN ? AND ?"
            params = [start_date, end_date]
        elif start_date:
            query += " WHERE transaction_date >= ?"
            params = [start_date]
        elif end_date:
            query += " WHERE transaction_date <= ?"
            params = [end_date]
        
        query += " GROUP BY transaction_type"
        
        with db_manager.cursor() as cursor:
            cursor.execute(query, params)
            results = {row['transaction_type']: row['total'] for row in cursor.fetchall()}
            return results
