import sqlite3
from datetime import datetime
from tabulate import tabulate

# Инициализация базы данных
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    priority INTEGER NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT NOT NULL
)
''')
conn.commit()

def add_task(title, priority, due_date):
    cursor.execute('INSERT INTO tasks (title, priority, due_date, status) VALUES (?, ?, ?, ?)',
                   (title, priority, due_date, 'pending'))
    conn.commit()

def complete_task(task_id):
    cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', ('completed', task_id))
    conn.commit()

def edit_task(task_id, title=None, priority=None, due_date=None):
    task = cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if task:
        title = title if title else task[1]
        priority = priority if priority else task[2]
        due_date = due_date if due_date else task[3]
        cursor.execute('UPDATE tasks SET title = ?, priority = ?, due_date = ? WHERE id = ?',
                       (title, priority, due_date, task_id))
        conn.commit()

def delete_task(task_id):
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()

def list_tasks():
    tasks = cursor.execute('SELECT * FROM tasks ORDER BY priority DESC, due_date ASC').fetchall()
    headers = ["ID", "Title", "Priority", "Due Date", "Status"]
    print(tabulate(tasks, headers, tablefmt="grid"))

# Пример использования
add_task("Complete Python script", 1, "2024-08-01")
add_task("Write project report", 2, "2024-08-03")
add_task("Plan weekend trip", 3, "2024-08-05")

print("Tasks before completion:")
list_tasks()

complete_task(1)

print("\nTasks after completion:")
list_tasks()

edit_task(2, priority=1)

print("\nTasks after editing:")
list_tasks()

delete_task(3)

print("\nTasks after deletion:")
list_tasks()

# Закрытие соединения с базой данных
conn.close()

