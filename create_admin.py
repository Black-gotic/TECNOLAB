import sys
import os
import sqlite3
import getpass
from werkzeug.security import generate_password_hash

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import Config

def create_admin():
    db_path = Config.DATABASE_PATH
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    print("=== Gerenciador de Administrador TECNOLAB ===")
    username = input("Nome de usuário (padrão: admin): ").strip() or "admin"
    password = getpass.getpass("Digite a senha: ")
    if not password:
        print("Erro: A senha não pode ser vazia.")
        conn.close()
        return

    password_confirm = getpass.getpass("Confirme a senha: ")
    if password != password_confirm:
        print("Erro: As senhas não coincidem.")
        conn.close()
        return

    password_hash = generate_password_hash(password)

    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    existing = cursor.fetchone()
    if existing:
        cursor.execute('UPDATE users SET password_hash = ? WHERE username = ?', (password_hash, username))
        print(f"Senha do usuário '{username}' atualizada com sucesso!")
    else:
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        print(f"Usuário administrador '{username}' criado com sucesso!")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_admin()
