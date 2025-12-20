import sqlite3

DB_NAME = "inventory.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS inventory(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
                )

''')
    conn.commit()
    conn.close()
    
def check_data():
    conn = sqlite3.connect(DB_NAME)
    cr = conn.cursor()
    cr.execute('SELECT * FROM inventory')
    print(cr.fetchall())
    
    conn.close()
    
# Function to Get All the Items
def get_all_items():
    conn = sqlite3.connect(DB_NAME)
    cr = conn.cursor()
    cr.execute('SELECT * FROM inventory')
    items = cr.fetchall()
    conn.close()
    return items

# Function to Add Inventory to Table
def add_item(name, qty, price):
    conn = sqlite3.connect(DB_NAME)
    cr = conn.cursor()
    cr.execute('INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)',(name, qty, price))
    conn.commit()
    conn.close()

# Function to Delete an Item 
def delete_item(item_id):
    conn = sqlite3.connect(DB_NAME)
    cr = conn.cursor()
    cr.execute('DELETE FROM inventory WHERE id=?' ,(item_id,))
    conn.commit()
    conn.close()

# Function to get Item based on ID
def get_item_by_id(item_id):
    conn = sqlite3.connect(DB_NAME)
    cr = conn.cursor()
    cr.execute('SELECT * from inventory WHERE id=?',(item_id,))
    item = cr.fetchone()
    conn.close()
    return item

# Function to update items 
def update_item(item_id, name, qty, price):
    conn = sqlite3.connect(DB_NAME)
    cr = conn.cursor()
    cr.execute('UPDATE inventory SET name=?, quantity=?, price=? WHERE id=?',(name, qty, price, item_id))
    conn.commit()
    conn.close()    




if __name__ == "__main__":
    init_db()
    check_data()
    

