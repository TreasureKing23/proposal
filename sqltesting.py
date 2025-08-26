import sqlite3

db_path = '/home/reon/Desktop/testdb'

def view_exams():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Exams")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

if __name__ == "__main__":
    view_exams()