"""
Zion Business Manager - Command Line Interface
Interactive menu-driven interface for business management
"""

import sys
from datetime import datetime
from services import (
    CustomerService, ProductService, CategoryService, 
    SupplierService, OrderService, InventoryService, 
    FinancialService, DashboardService
)


class ZionBusinessManagerCLI:
    """Main CLI class for Zion Business Manager"""
    
    def __init__(self):
        self.running = True
    
    def clear_screen(self):
        """Clear terminal screen"""
        print("\n" * 2)
    
    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "=" * 50)
        print(f"  ZION BUSINESS MANAGER - {title}")
        print("=" * 50)
    
    def print_menu(self, title: str, options: list):
        """Print menu options"""
        self.print_header(title)
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        print("  0. Back to Main Menu")
        print("-" * 50)
    
    def get_input(self, prompt: str) -> str:
        """Get user input"""
        return input(f"\n  {prompt}: ").strip()
    
    def get_int_input(self, prompt: str, default: int = None) -> int:
        """Get integer input"""
        while True:
            try:
                value = input(f"  {prompt}: ").strip()
                if value == "" and default is not None:
                    return default
                return int(value)
            except ValueError:
                print("  Please enter a valid number")
    
    def get_float_input(self, prompt: str) -> float:
        """Get float input"""
        while True:
            try:
                value = input(f"  {prompt}: ").strip()
                return float(value)
            except ValueError:
                print("  Please enter a valid number")
    
    def press_enter_to_continue(self):
        """Wait for user to press enter"""
        input("\n  Press Enter to continue...")
    
    def run(self):
        """Main application loop"""
        print("\n" + "=" * 50)
        print("  WELCOME TO ZION BUSINESS MANAGER")
        print("  Your Complete Business Solution")
        print("=" * 50)
        
        while self.running:
            self.main_menu()
    
    def main_menu(self):
        """Main menu options"""
        self.clear_screen()
        options = [
            "Dashboard",
            "Customers",
            "Products & Inventory",
            "Orders",
            "Suppliers",
            "Categories",
            "Financial Reports",
            "Inventory Reports"
        ]
        self.print_menu("MAIN MENU", options)
        
        choice = self.get_int_input("Enter your choice")
        
        menus = {
            1: self.dashboard_menu,
            2: self.customers_menu,
            3: self.products_menu,
            4: self.orders_menu,
            5: self.suppliers_menu,
            6: self.categories_menu,
            7: self.financial_menu,
            8: self.inventory_menu
        }
        
        if choice in menus:
            menus[choice]()
        elif choice == 0:
            self.running = False
            print("\n  Thank you for using Zion Business Manager!")
            print("  Goodbye!\n")
        else:
            print("  Invalid choice!")
    
    # ==================== DASHBOARD ====================
    
    def dashboard_menu(self):
        """Dashboard menu"""
        self.clear_screen()
        self.print_header("DASHBOARD")
        
        stats = DashboardService.get_dashboard_stats()
        
        print(f"\n  Total Customers: {stats['total_customers']}")
        print(f"  Total Products: {stats['total_products']}")
        print(f"  Total Orders: {stats['total_orders']}")
        print(f"  Total Revenue: ${stats['total_revenue']:.2f}")
        print(f"  Pending Orders: {stats['pending_orders']}")
        print(f"  Low Stock Alerts: {stats['low_stock_alerts']}")
        
        print("\n  Orders by Status:")
        for status, count in stats['orders_by_status'].items():
            print(f"    - {status}: {count}")
        
        print("\n  Recent Orders:")
        for order in stats['recent_orders']:
            print(f"    Order #{order['id']} - {order['status']} - ${order['total_amount']:.2f}")
        
        self.press_enter_to_continue()
    
    # ==================== CUSTOMERS ====================
    
    def customers_menu(self):
        """Customers management menu"""
        while True:
            self.clear_screen()
            options = [
                "View All Customers",
                "Add New Customer",
                "Search Customers",
                "Update Customer",
                "View Customer Details"
            ]
            self.print_menu("CUSTOMERS", options)
            
            choice = self.get_int_input("Enter your choice")
            
            if choice == 0:
                break
            elif choice == 1:
                self.view_all_customers()
            elif choice == 2:
                self.add_customer()
            elif choice == 3:
                self.search_customers()
            elif choice == 4:
                self.update_customer()
            elif choice == 5:
                self.view_customer_details()
    
    def view_all_customers(self):
        """View all customers"""
        self.clear_screen()
        self.print_header("ALL CUSTOMERS")
        
        customers = CustomerService.get_all_customers()
        
        if not customers:
            print("\n  No customers found!")
        else:
            for c in customers:
                print(f"\n  ID: {c['id']}")
                print(f"  Name: {c['name']}")
                print(f"  Email: {c['email']}")
                print(f"  Phone: {c['phone']}")
                print("-" * 30)
        
        self.press_enter_to_continue()
    
    def add_customer(self):
        """Add new customer"""
        self.clear_screen()
        self.print_header("ADD NEW CUSTOMER")
        
        name = self.get_input("Customer Name")
        email = self.get_input("Email (optional)")
        phone = self.get_input("Phone (optional)")
        address = self.get_input("Address (optional)")
        
        try:
            customer_id = CustomerService.register_customer(name, email, phone, address)
            print(f"\n  Customer added successfully! ID: {customer_id}")
        except Exception as e:
            print(f"\n  Error adding customer: {e}")
        
        self.press_enter_to_continue()
    
    def search_customers(self):
        """Search customers"""
        self.clear_screen()
        self.print_header("SEARCH CUSTOMERS")
        
        query = self.get_input("Search query (name or email)")
        customers = CustomerService.search_customers(query)
        
        if not customers:
            print("\n  No customers found!")
        else:
            for c in customers:
                print(f"\n  ID: {c['id']} - {c['name']} ({c['email']})")
        
        self.press_enter_to_continue()
    
    def update_customer(self):
        """Update customer"""
        self.clear_screen()
        self.print_header("UPDATE CUSTOMER")
        
        customer_id = self.get_int_input("Customer ID to update")
        customer = CustomerService.get_all_customers()
        found = [c for c in customer if c['id'] == customer_id]
        
        if not found:
            print("\n  Customer not found!")
            self.press_enter_to_continue()
            return
        
        print(f"\n  Current: {found[0]['name']}")
        name = self.get_input("New name (leave empty to keep current)")
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        email = self.get_input("New email")
        if email:
            kwargs['email'] = email
        
        phone = self.get_input("New phone")
        if phone:
            kwargs['phone'] = phone
        
        address = self.get_input("New address")
        if address:
            kwargs['address'] = address
        
        if kwargs:
            if CustomerService.update_customer(customer_id, **kwargs):
                print("\n  Customer updated successfully!")
            else:
                print("\n  Error updating customer!")
        else:
            print("\n  No changes made!")
        
        self.press_enter_to_continue()
    
    def view_customer_details(self):
        """View customer with orders"""
        self.clear_screen()
        self.print_header("CUSTOMER DETAILS")
        
        customer_id = self.get_int_input("Customer ID")
        customer = CustomerService.get_customer_with_orders(customer_id)
        
        if not customer:
            print("\n  Customer not found!")
        else:
            print(f"\n  Name: {customer['name']}")
            print(f"  Email: {customer['email']}")
            print(f"  Phone: {customer['phone']}")
            print(f"  Address: {customer['address']}")
            print(f"\n  Orders ({len(customer['orders'])}):")
            for order in customer['orders']:
                print(f"    - Order #{order['id']}: {order['status']} - ${order['total_amount']:.2f}")
        
        self.press_enter_to_continue()
    
    # ==================== PRODUCTS ====================
    
    def products_menu(self):
        """Products management menu"""
        while True:
            self.clear_screen()
            options = [
                "View All Products",
                "Add New Product",
                "Search Products",
                "Update Product",
                "Adjust Stock",
                "View Low Stock"
            ]
            self.print_menu("PRODUCTS & INVENTORY", options)
            
            choice = self.get_int_input("Enter your choice")
            
            if choice == 0:
                break
            elif choice == 1:
                self.view_all_products()
            elif choice == 2:
                self.add_product()
            elif choice == 3:
                self.search_products()
            elif choice == 4:
                self.update_product()
            elif choice == 5:
                self.adjust_stock()
            elif choice == 6:
                self.view_low_stock()
    
    def view_all_products(self):
        """View all products"""
        self.clear_screen()
        self.print_header("ALL PRODUCTS")
        
        products = ProductService.get_all_products()
        
        if not products:
            print("\n  No products found!")
        else:
            for p in products:
                print(f"\n  ID: {p['id']} | {p['name']}")
                print(f"  SKU: {p['sku']} | Price: ${p['price']:.2f}")
                print(f"  Stock: {p['quantity']} | Min: {p['min_quantity']}")
                print("-" * 30)
        
        self.press_enter_to_continue()
    
    def add_product(self):
        """Add new product"""
        self.clear_screen()
        self.print_header("ADD NEW PRODUCT")
        
        name = self.get_input("Product Name")
        sku = self.get_input("SKU")
        price = self.get_float_input("Price")
        description = self.get_input("Description (optional)")
        cost_price = self.get_float_input("Cost Price (optional, default 0)")
        quantity = self.get_int_input("Initial Quantity (default 0)", 0)
        min_quantity = self.get_int_input("Minimum Quantity (default 0)", 0)
        
        try:
            product_id = ProductService.add_product(
                name, sku, price, description, cost_price, quantity, min_quantity
            )
            print(f"\n  Product added successfully! ID: {product_id}")
        except Exception as e:
            print(f"\n  Error adding product: {e}")
        
        self.press_enter_to_continue()
    
    def search_products(self):
        """Search products"""
        self.clear_screen()
        self.print_header("SEARCH PRODUCTS")
        
        query = self.get_input("Search query")
        products = ProductService.search_products(query)
        
        if not products:
            print("\n  No products found!")
        else:
            for p in products:
                print(f"\n  ID: {p['id']} - {p['name']} (${p['price']:.2f})")
                print(f"  Stock: {p['quantity']}")
        
        self.press_enter_to_continue()
    
    def update_product(self):
        """Update product"""
        self.clear_screen()
        self.print_header("UPDATE PRODUCT")
        
        product_id = self.get_int_input("Product ID to update")
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            print("\n  Product not found!")
            self.press_enter_to_continue()
            return
        
        print(f"\n  Current: {product['name']}")
        name = self.get_input("New name (leave empty to keep current)")
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        sku = self.get_input("New SKU")
        if sku:
            kwargs['sku'] = sku
        
        price = self.get_input("New price")
        if price:
            try:
                kwargs['price'] = float(price)
            except ValueError:
                print("  Invalid price format!")
        
        description = self.get_input("New description")
        if description:
            kwargs['description'] = description
        
        if kwargs:
            if ProductService.update_product(product_id, **kwargs):
                print("\n  Product updated successfully!")
            else:
                print("\n  Error updating product!")
        
        self.press_enter_to_continue()
    
    def adjust_stock(self):
        """Adjust product stock"""
        self.clear_screen()
        self.print_header("ADJUST STOCK")
        
        product_id = self.get_int_input("Product ID")
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            print("\n  Product not found!")
            self.press_enter_to_continue()
            return
        
        print(f"\n  Current Stock: {product['quantity']}")
        quantity_change = self.get_int_input("Quantity change (+ to add, - to subtract)")
        
        if ProductService.adjust_stock(product_id, quantity_change):
            print("\n  Stock updated successfully!")
        else:
            print("\n  Error updating stock!")
        
        self.press_enter_to_continue()
    
    def view_low_stock(self):
        """View low stock products"""
        self.clear_screen()
        self.print_header("LOW STOCK ALERTS")
        
        products = ProductService.get_low_stock_products()
        
        if not products:
            print("\n  All products are well stocked!")
        else:
            print(f"\n  {len(products)} product(s) need restocking:")
            for p in products:
                print(f"\n  ID: {p['id']} - {p['name']}")
                print(f"  Current: {p['quantity']} | Minimum: {p['min_quantity']}")
        
        self.press_enter_to_continue()
    
    # ==================== ORDERS ====================
    
    def orders_menu(self):
        """Orders management menu"""
        while True:
            self.clear_screen()
            options = [
                "View All Orders",
                "Create New Order",
                "View Order Details",
                "Add Item to Order",
                "Update Order Status",
                "Cancel Order"
            ]
            self.print_menu("ORDERS", options)
            
            choice = self.get_int_input("Enter your choice")
            
            if choice == 0:
                break
            elif choice == 1:
                self.view_all_orders()
            elif choice == 2:
                self.create_order()
            elif choice == 3:
                self.view_order_details()
            elif choice == 4:
                self.add_item_to_order()
            elif choice == 5:
                self.update_order_status()
            elif choice == 6:
                self.cancel_order()
    
    def view_all_orders(self):
        """View all orders"""
        self.clear_screen()
        self.print_header("ALL ORDERS")
        
        orders = OrderService.get_all_orders()
        
        if not orders:
            print("\n  No orders found!")
        else:
            for o in orders:
                print(f"\n  Order #{o['id']} | Status: {o['status']}")
                print(f"  Total: ${o['total_amount']:.2f} | Date: {o['order_date']}")
                print("-" * 30)
        
        self.press_enter_to_continue()
    
    def create_order(self):
        """Create new order"""
        self.clear_screen()
        self.print_header("CREATE NEW ORDER")
        
        customer_id_input = self.get_input("Customer ID (optional, leave empty for walk-in)")
        
        if customer_id_input:
            try:
                customer_id = int(customer_id_input)
            except ValueError:
                customer_id = None
        else:
            customer_id = None
        
        notes = self.get_input("Order notes (optional)")
        
        order_id = OrderService.create_order(customer_id, notes)
        print(f"\n  Order created successfully! Order ID: {order_id}")
        print("  Now you can add items to this order.")
        
        self.press_enter_to_continue()
    
    def view_order_details(self):
        """View order details"""
        self.clear_screen()
        self.print_header("ORDER DETAILS")
        
        order_id = self.get_int_input("Order ID")
        order = OrderService.get_order_details(order_id)
        
        if not order:
            print("\n  Order not found!")
        else:
            print(f"\n  Order #{order['id']}")
            print(f"  Status: {order['status']}")
            print(f"  Customer: {order.get('customer_name', 'Walk-in')}")
            print(f"  Date: {order['order_date']}")
            print(f"\n  Items:")
            for item in order.get('items', []):
                print(f"    - {item['product_name']} x {item['quantity']} = ${item['quantity'] * item['unit_price']:.2f}")
            print(f"\n  Total: ${order['total_amount']:.2f}")
            print(f"  Notes: {order['notes']}")
        
        self.press_enter_to_continue()
    
    def add_item_to_order(self):
        """Add item to order"""
        self.clear_screen()
        self.print_header("ADD ITEM TO ORDER")
        
        order_id = self.get_int_input("Order ID")
        product_id = self.get_int_input("Product ID")
        quantity = self.get_int_input("Quantity")
        
        if OrderService.add_item_to_order(order_id, product_id, quantity):
            print("\n  Item added successfully!")
        else:
            print("\n  Error adding item. Check product availability!")
        
        self.press_enter_to_continue()
    
    def update_order_status(self):
        """Update order status"""
        self.clear_screen()
        self.print_header("UPDATE ORDER STATUS")
        
        order_id = self.get_int_input("Order ID")
        print("\n  Status options: pending, confirmed, processing, shipped, delivered, cancelled")
        status = self.get_input("New status")
        
        if OrderService.update_order_status(order_id, status.lower()):
            print("\n  Status updated successfully!")
        else:
            print("\n  Invalid status or order not found!")
        
        self.press_enter_to_continue()
    
    def cancel_order(self):
        """Cancel order"""
        self.clear_screen()
        self.print_header("CANCEL ORDER")
        
        order_id = self.get_int_input("Order ID to cancel")
        
        if OrderService.cancel_order(order_id):
            print("\n  Order cancelled successfully! Stock restored.")
        else:
            print("\n  Error cancelling order!")
        
        self.press_enter_to_continue()
    
    # ==================== SUPPLIERS ====================
    
    def suppliers_menu(self):
        """Suppliers management menu"""
        while True:
            self.clear_screen()
            options = [
                "View All Suppliers",
                "Add New Supplier",
                "Update Supplier"
            ]
            self.print_menu("SUPPLIERS", options)
            
            choice = self.get_int_input("Enter your choice")
            
            if choice == 0:
                break
            elif choice == 1:
                self.view_all_suppliers()
            elif choice == 2:
                self.add_supplier()
            elif choice == 3:
                self.update_supplier()
    
    def view_all_suppliers(self):
        """View all suppliers"""
        self.clear_screen()
        self.print_header("ALL SUPPLIERS")
        
        suppliers = SupplierService.get_all_suppliers()
        
        if not suppliers:
            print("\n  No suppliers found!")
        else:
            for s in suppliers:
                print(f"\n  ID: {s['id']}")
                print(f"  Name: {s['name']}")
                print(f"  Email: {s['email']}")
                print(f"  Phone: {s['phone']}")
                print("-" * 30)
        
        self.press_enter_to_continue()
    
    def add_supplier(self):
        """Add new supplier"""
        self.clear_screen()
        self.print_header("ADD NEW SUPPLIER")
        
        name = self.get_input("Supplier Name")
        email = self.get_input("Email (optional)")
        phone = self.get_input("Phone (optional)")
        address = self.get_input("Address (optional)")
        contact_person = self.get_input("Contact Person (optional)")
        
        supplier_id = SupplierService.create_supplier(name, email, phone, address, contact_person)
        print(f"\n  Supplier added successfully! ID: {supplier_id}")
        
        self.press_enter_to_continue()
    
    def update_supplier(self):
        """Update supplier"""
        self.clear_screen()
        self.print_header("UPDATE SUPPLIER")
        
        supplier_id = self.get_int_input("Supplier ID to update")
        
        kwargs = {}
        name = self.get_input("New name (leave empty to skip)")
        if name:
            kwargs['name'] = name
        
        email = self.get_input("New email")
        if email:
            kwargs['email'] = email
        
        if kwargs:
            if SupplierService.update_supplier(supplier_id, **kwargs):
                print("\n  Supplier updated successfully!")
            else:
                print("\n  Error updating supplier!")
        
        self.press_enter_to_continue()
    
    # ==================== CATEGORIES ====================
    
    def categories_menu(self):
        """Categories management menu"""
        while True:
            self.clear_screen()
            options = [
                "View All Categories",
                "Add New Category",
                "Update Category"
            ]
            self.print_menu("CATEGORIES", options)
            
            choice = self.get_int_input("Enter your choice")
            
            if choice == 0:
                break
            elif choice == 1:
                self.view_all_categories()
            elif choice == 2:
                self.add_category()
            elif choice == 3:
                self.update_category()
    
    def view_all_categories(self):
        """View all categories"""
        self.clear_screen()
        self.print_header("ALL CATEGORIES")
        
        categories = CategoryService.get_all_categories()
        
        if not categories:
            print("\n  No categories found!")
        else:
            for c in categories:
                print(f"\n  ID: {c['id']} - {c['name']}")
                print(f"  Description: {c['description']}")
        
        self.press_enter_to_continue()
    
    def add_category(self):
        """Add new category"""
        self.clear_screen()
        self.print_header("ADD NEW CATEGORY")
        
        name = self.get_input("Category Name")
        description = self.get_input("Description (optional)")
        
        category_id = CategoryService.create_category(name, description)
        print(f"\n  Category added successfully! ID: {category_id}")
        
        self.press_enter_to_continue()
    
    def update_category(self):
        """Update category"""
        self.clear_screen()
        self.print_header("UPDATE CATEGORY")
        
        category_id = self.get_int_input("Category ID to update")
        
        name = self.get_input("New name (leave empty to skip)")
        description = self.get_input("New description")
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        if description:
            kwargs['description'] = description
        
        if kwargs:
            if CategoryService.update_category(category_id, **kwargs):
                print("\n  Category updated successfully!")
            else:
                print("\n  Error updating category!")
        
        self.press_enter_to_continue()
    
    # ==================== FINANCIAL ====================
    
    def financial_menu(self):
        """Financial reports menu"""
        while True:
            self.clear_screen()
            options = [
                "View Financial Summary",
                "Record Transaction"
            ]
            self.print_menu("FINANCIAL REPORTS", options)
            
            choice = self.get_int_input("Enter your choice")
            
            if choice == 0:
                break
            elif choice == 1:
                self.view_financial_summary()
            elif choice == 2:
                self.record_transaction()
    
    def view_financial_summary(self):
        """View financial summary"""
        self.clear_screen()
        self.print_header("FINANCIAL SUMMARY")
        
        summary = FinancialService.get_financial_summary()
        
        print(f"\n  Revenue: ${summary['revenue']:.2f}")
        print(f"  Total Cost: ${summary['total_cost']:.2f}")
        print(f"  Profit: ${summary['profit']:.2f}")
        
        print("\n  By Transaction Type:")
        for trans_type, amount in summary['by_type'].items():
            print(f"    - {trans_type}: ${amount:.2f}")
        
        self.press_enter_to_continue()
    
    def record_transaction(self):
        """Record a transaction"""
        self.clear_screen()
        self.print_header("RECORD TRANSACTION")
        
        order_id_input = self.get_input("Order ID (optional)")
        order_id = int(order_id_input) if order_id_input else None
        trans_type = self.get_input("Transaction type (payment, expense, etc.)")
        amount = self.get_float_input("Amount")
        payment_method = self.get_input("Payment method (optional)")
        notes = self.get_input("Notes (optional)")
        
        transaction_id = FinancialService.record_transaction(
            trans_type, order_id, amount, payment_method, notes
        )
        print(f"\n  Transaction recorded successfully! ID: {transaction_id}")
        
        self.press_enter_to_continue()
    
    # ==================== INVENTORY REPORTS ====================
    
    def inventory_menu(self):
        """Inventory reports menu"""
        self.clear_screen()
        self.print_header("INVENTORY REPORTS")
        
        report = InventoryService.get_inventory_report()
        
        print(f"\n  Total Products: {report['total_products']}")
        print(f"  Total Items in Stock: {report['total_items']}")
        print(f"  Total Inventory Value: ${report['total_inventory_value']:.2f}")
        print(f"  Low Stock Items: {report['low_stock_count']}")
        
        if report['low_stock_products']:
            print("\n  Low Stock Products:")
            for p in report['low_stock_products']:
                print(f"    - {p['name']} (Stock: {p['quantity']})")
        
        self.press_enter_to_continue()


# Entry point
def main():
    """Main entry point"""
    # Initialize database
    from database import db_manager
    db_manager.initialize_db()
    
    # Start CLI
    cli = ZionBusinessManagerCLI()
    cli.run()


if __name__ == "__main__":
    main()
