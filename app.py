import sqlite3
import os
import uuid
from functools import wraps
from flask import Flask, render_template, request, flash, redirect, url_for, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Helper para obter conexão com SQLite retornando sqlite3.Row
def get_db():
    conn = sqlite3.connect(app.config['DATABASE_PATH'])
    conn.row_factory = sqlite3.Row
    return conn

# Inicialização do banco de dados SQLite
def init_db():
    os.makedirs(os.path.dirname(app.config['DATABASE_PATH']), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    conn = get_db()
    cursor = conn.cursor()

    # Tabela para mensagens de contato
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabela para usuários administradores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabela para tutoriais e conteúdos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tutorials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            content TEXT,
            image_path TEXT,
            is_published INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabela para projetos do portfólio
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            technologies TEXT,
            features TEXT,
            demo_url TEXT,
            repo_url TEXT,
            content TEXT,
            image_path TEXT,
            is_published INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Criar administrador padrão caso a tabela esteja vazia
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        default_hash = generate_password_hash('admin123')
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', ('admin', default_hash))

    # Popular itens demonstrativos iniciais se tabelas estiverem vazias
    cursor.execute('SELECT COUNT(*) FROM tutorials')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO tutorials (title, category, description, is_published)
            VALUES (?, ?, ?, 1)
        ''', ('Como estruturar uma aplicação Flask de forma modular', 'Desenvolvimento Web', 'Boas práticas na organização de pastas, arquivos estáticos e rotas para projetos Python simples e expansíveis.'))
        cursor.execute('''
            INSERT INTO tutorials (title, category, description, is_published)
            VALUES (?, ?, ?, 1)
        ''', ('Criando interfaces futuristas com CSS nativo', 'CSS3', 'Como aplicar sombras, transparências (backdrop-filter) e gradientes sem sobrecarregar o desempenho da página.'))

    cursor.execute('SELECT COUNT(*) FROM projects')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO projects (title, description, technologies, features, demo_url, repo_url, is_published)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        ''', ('Portal Tecnológico (Demonstração)', 'Sistema web dinâmico para publicação de artigos e gerenciamento de notícias sobre informática e programação.', 'Python, Flask, SQLite, CSS3', 'CRUD de postagens, busca por categoria, layout responsivo.', '#', '#'))
        cursor.execute('''
            INSERT INTO projects (title, description, technologies, features, demo_url, repo_url, is_published)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        ''', ('Landing Page para Serviços', 'Página de conversão otimizada para prestadores de serviços, com foco em velocidade de carregamento e design limpo.', 'HTML5, CSS3, JavaScript', 'Formulário responsivo, animações sutis, SEO otimizado.', '#', ''))

    conn.commit()
    conn.close()

init_db()

# Decorator para proteção de rotas administrativas
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Por favor, faça login para acessar a área administrativa.', 'error')
            return redirect(url_for('admin_login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

# Verificação e upload de arquivos seguros
def save_uploaded_image(file):
    if not file or file.filename == '':
        return None
    
    filename = file.filename
    if '.' in filename:
        ext = filename.rsplit('.', 1)[1].lower()
        if ext in app.config['ALLOWED_EXTENSIONS']:
            unique_filename = f"{uuid.uuid4().hex}_{secure_filename(filename)}"
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            return f"uploads/{unique_filename}"
    return None

# ========================================================
# Rotas Públicas
# ========================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def about():
    return render_template('about.html')

@app.route('/projetos')
def projects():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE is_published = 1 ORDER BY created_at DESC')
    published_projects = cursor.fetchall()
    conn.close()
    return render_template('projects.html', projects=published_projects)

@app.route('/servicos')
def services():
    return render_template('services.html')

@app.route('/tecnologias')
def technologies():
    return render_template('technologies.html')

@app.route('/conteudos')
def tutorials():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tutorials WHERE is_published = 1 ORDER BY created_at DESC')
    published_tutorials = cursor.fetchall()
    conn.close()
    return render_template('tutorials.html', tutorials=published_tutorials)

@app.route('/contato', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        # Validação no backend
        if not name or not email or not subject or not message:
            flash('Por favor, preencha todos os campos do formulário.', 'error')
            return redirect(url_for('contact'))

        if '@' not in email or '.' not in email:
            flash('Por favor, informe um e-mail válido.', 'error')
            return redirect(url_for('contact'))

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO contact_messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
                (name, email, subject, message)
            )
            conn.commit()
            conn.close()
            flash('Sua mensagem foi enviada com sucesso! Em breve entraremos em contato.', 'success')
        except Exception as e:
            flash('Ocorreu um erro ao salvar a mensagem. Tente novamente mais tarde.', 'error')

        return redirect(url_for('contact'))

    return render_template('contact.html')

# ========================================================
# Rotas Administrativas - Autenticação
# ========================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Por favor, preencha o usuário e a senha.', 'error')
            return render_template('admin/login.html')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['admin_logged_in'] = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Bem-vindo ao painel, {user["username"]}!', 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/admin'):
                return redirect(next_page)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Credenciais inválidas. Verifique seu usuário e senha.', 'error')

    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Você saiu do painel administrativo.', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    return redirect(url_for('admin_tutorials'))

# ========================================================
# Rotas Administrativas - Tutoriais / Conteúdos
# ========================================================

@app.route('/admin/tutoriais')
@admin_required
def admin_tutorials():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tutorials ORDER BY created_at DESC')
    items = cursor.fetchall()
    conn.close()
    return render_template('admin/tutorials_list.html', tutorials=items, active_tab='tutorials')

@app.route('/admin/tutoriais/novo', methods=['GET', 'POST'])
@admin_required
def admin_tutorial_new():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        content = request.form.get('content', '').strip()
        status = request.form.get('status', 'published')
        is_published = 1 if status == 'published' else 0

        if not title or not category or not description:
            flash('Título, categoria e resumo são campos obrigatórios.', 'error')
            return render_template('admin/tutorial_form.html', action='new', active_tab='tutorials')

        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            image_path = save_uploaded_image(file)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tutorials (title, category, description, content, image_path, is_published)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, category, description, content, image_path, is_published))
        conn.commit()
        conn.close()

        flash('Conteúdo cadastrado com sucesso!', 'success')
        return redirect(url_for('admin_tutorials'))

    return render_template('admin/tutorial_form.html', action='new', tutorial=None, active_tab='tutorials')

@app.route('/admin/tutoriais/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_tutorial_edit(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tutorials WHERE id = ?', (id,))
    tutorial = cursor.fetchone()

    if not tutorial:
        conn.close()
        flash('Conteúdo não encontrado.', 'error')
        return redirect(url_for('admin_tutorials'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        content = request.form.get('content', '').strip()
        status = request.form.get('status', 'published')
        is_published = 1 if status == 'published' else 0

        if not title or not category or not description:
            flash('Título, categoria e resumo são campos obrigatórios.', 'error')
            conn.close()
            return render_template('admin/tutorial_form.html', action='edit', tutorial=tutorial, active_tab='tutorials')

        image_path = tutorial['image_path']
        if 'image' in request.files:
            file = request.files['image']
            uploaded = save_uploaded_image(file)
            if uploaded:
                image_path = uploaded

        cursor.execute('''
            UPDATE tutorials
            SET title = ?, category = ?, description = ?, content = ?, image_path = ?, is_published = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, category, description, content, image_path, is_published, id))
        conn.commit()
        conn.close()

        flash('Conteúdo atualizado com sucesso!', 'success')
        return redirect(url_for('admin_tutorials'))

    conn.close()
    return render_template('admin/tutorial_form.html', action='edit', tutorial=tutorial, active_tab='tutorials')

@app.route('/admin/tutoriais/excluir/<int:id>', methods=['POST'])
@admin_required
def admin_tutorial_delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tutorials WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash('Conteúdo excluído com sucesso.', 'success')
    return redirect(url_for('admin_tutorials'))

# ========================================================
# Rotas Administrativas - Projetos
# ========================================================

@app.route('/admin/projetos')
@admin_required
def admin_projects():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects ORDER BY created_at DESC')
    items = cursor.fetchall()
    conn.close()
    return render_template('admin/projects_list.html', projects=items, active_tab='projects')

@app.route('/admin/projetos/novo', methods=['GET', 'POST'])
@admin_required
def admin_project_new():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        technologies = request.form.get('technologies', '').strip()
        features = request.form.get('features', '').strip()
        demo_url = request.form.get('demo_url', '').strip()
        repo_url = request.form.get('repo_url', '').strip()
        content = request.form.get('content', '').strip()
        status = request.form.get('status', 'published')
        is_published = 1 if status == 'published' else 0

        if not title or not description:
            flash('Título e descrição são campos obrigatórios.', 'error')
            return render_template('admin/project_form.html', action='new', active_tab='projects')

        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            image_path = save_uploaded_image(file)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projects (title, description, technologies, features, demo_url, repo_url, content, image_path, is_published)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, technologies, features, demo_url, repo_url, content, image_path, is_published))
        conn.commit()
        conn.close()

        flash('Projeto cadastrado com sucesso!', 'success')
        return redirect(url_for('admin_projects'))

    return render_template('admin/project_form.html', action='new', project=None, active_tab='projects')

@app.route('/admin/projetos/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_project_edit(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE id = ?', (id,))
    project = cursor.fetchone()

    if not project:
        conn.close()
        flash('Projeto não encontrado.', 'error')
        return redirect(url_for('admin_projects'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        technologies = request.form.get('technologies', '').strip()
        features = request.form.get('features', '').strip()
        demo_url = request.form.get('demo_url', '').strip()
        repo_url = request.form.get('repo_url', '').strip()
        content = request.form.get('content', '').strip()
        status = request.form.get('status', 'published')
        is_published = 1 if status == 'published' else 0

        if not title or not description:
            flash('Título e descrição são campos obrigatórios.', 'error')
            conn.close()
            return render_template('admin/project_form.html', action='edit', project=project, active_tab='projects')

        image_path = project['image_path']
        if 'image' in request.files:
            file = request.files['image']
            uploaded = save_uploaded_image(file)
            if uploaded:
                image_path = uploaded

        cursor.execute('''
            UPDATE projects
            SET title = ?, description = ?, technologies = ?, features = ?, demo_url = ?, repo_url = ?, content = ?, image_path = ?, is_published = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, description, technologies, features, demo_url, repo_url, content, image_path, is_published, id))
        conn.commit()
        conn.close()

        flash('Projeto atualizado com sucesso!', 'success')
        return redirect(url_for('admin_projects'))

    conn.close()
    return render_template('admin/project_form.html', action='edit', project=project, active_tab='projects')

@app.route('/admin/projetos/excluir/<int:id>', methods=['POST'])
@admin_required
def admin_project_delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM projects WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash('Projeto excluído com sucesso.', 'success')
    return redirect(url_for('admin_projects'))

# ========================================================
# Tratamento de Erros
# ========================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
