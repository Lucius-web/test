import sqlite3  


class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name  
        self.connection = None  

    def open_connection(self):
        if self.connection is None:  
            self.connection = sqlite3.connect(self.db_name)  
            self.connection.row_factory = sqlite3.Row  

    def close_connection(self):
        if self.connection is not None:  
            self.connection.close()  
            self.connection = None  

    def search_user(self, username):
        self.open_connection()  
        cursor = self.connection.cursor() 
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))  
        user = cursor.fetchone()  
        self.close_connection()  
        return user  

    def execute_transaction(self, operations):
        self.open_connection() 
        try:
            cursor = self.connection.cursor() 
            for operation in operations: 
                cursor.execute(*operation) 
            self.connection.commit()  
        except Exception as e:
            self.connection.rollback()  
            print(f"Transaction failed: {e}")  
        finally:
            self.close_connection()  



class User:
    def __init__(self, db_manager):
        self.db_manager = db_manager  

    def add_user(self, username, email):
        self.db_manager.open_connection() 
        cursor = self.db_manager.connection.cursor()  
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email)) 
        self.db_manager.connection.commit()  
        self.db_manager.close_connection()  

    def get_user_by_id(self, user_id):
        self.db_manager.open_connection()  
        cursor = self.db_manager.connection.cursor()  
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))  
        user = cursor.fetchone()
        self.db_manager.close_connection()  
        return user  

    def delete_user(self, user_id):
        self.db_manager.open_connection() 
        cursor = self.db_manager.connection.cursor()  
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))  
        self.db_manager.connection.commit()  
        self.db_manager.close_connection()  


class Admin(User):
    def __init__(self, db_manager):
        super().__init__(db_manager)  



    def add_admin(self, username, email, admin_level):
        self.add_user(username, email)  
        self.db_manager.open_connection()  
        cursor = self.db_manager.connection.cursor() 
        cursor.execute("INSERT INTO admins (username, email, admin_level) VALUES (?, ?, ?)", 
                       (username, email, admin_level))  
        self.db_manager.connection.commit()  
        self.db_manager.close_connection() 


class Customer(User):
    def __init__(self, db_manager):
        super().__init__(db_manager)  

    def add_customer(self, username, email, loyalty_points):
        self.add_user(username, email)  
        self.db_manager.open_connection()  
        cursor = self.db_manager.connection.cursor()  
        cursor.execute("INSERT INTO customers (username, email, loyalty_points) VALUES (?, ?, ?)", 
                       (username, email, loyalty_points)) 
        self.db_manager.connection.commit()  
        self.db_manager.close_connection()  



if __name__ == "__main__":
    db_manager = DatabaseManager('database.db')  

    
    db_manager.open_connection()  
    cursor = db_manager.connection.cursor()  

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        admin_level INTEGER NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        loyalty_points INTEGER NOT NULL
    )
    """)
    db_manager.connection.commit()
    db_manager.close_connection()  

    
    user_manager = User(db_manager)  
    user_manager.add_user('john_doe', 'john@example.com')  

  
    user_data = db_manager.search_user('john_doe')  
    print(user_data)  

    
    admin_manager = Admin(db_manager)  
    admin_manager.add_admin('admin_user', 'admin@example.com', 1) 

    
    customer_manager = Customer(db_manager)  
    customer_manager.add_customer('customer_user', 'customer@example.com', 100)  

  
    operations = [
        ("INSERT INTO users (username, email) VALUES (?, ?)", ('user1', 'user1@example.com')),
        ("INSERT INTO users (username, email) VALUES (?, ?)", ('user2', 'user2@example.com')),
    ]
    db_manager.execute_transaction(operations) 