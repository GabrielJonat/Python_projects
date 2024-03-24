import sqlite3

def  Create_Table():
    conn = sqlite3.connect('Employees.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (id TEXT PRIMARY KEY,
                                              name TEXT,
                                              role TEXT,
                                              gender TEXT,
                                              status TEXT)''')
    conn.commit()
    conn.close()

def Fetch_Employees():
    conn = sqlite3.connect('Employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Employees')
    employees = cursor.fetchall()
    conn.close()
    return employees

def Insert_Employee(id,name,role,gender,status):
    conn = sqlite3.connect('Employees.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Employees (id,name,role,gender,status) VALUES (?,?,?,?,?)', (id,name,role,gender,status))
    conn.commit()
    conn.close()

def Delete_Employee(id):
    conn = sqlite3.connect('Employees.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Employees WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def Update_Employee(new_name,new_role,new_gender,new_status,id):
    conn = sqlite3.connect('Employees.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE Employees SET name = ?, role = ?, gender = ?, status = ? WHERE id = ?', (new_name,new_role,new_gender,new_status,id))
    conn.commit()
    conn.close()

def Id_Exists(id):
    conn = sqlite3.connect('Employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Employees WHERE id = ?', (id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0

Create_Table()
