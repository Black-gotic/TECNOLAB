import unittest
import sys
import os
import io

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, get_db

class TecnoLabAdminTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_public_pages(self):
        # Testar se páginas públicas continuam acessíveis
        for path in ['/', '/sobre', '/projetos', '/servicos', '/tecnologias', '/conteudos', '/contato']:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, f"Falha na rota pública {path}")

    def test_admin_protection(self):
        # Acesso sem login a /admin deve redirecionar para login
        res = self.client.get('/admin', follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertIn('/admin/login', res.headers['Location'])

        res2 = self.client.get('/admin/tutoriais', follow_redirects=False)
        self.assertEqual(res2.status_code, 302)
        self.assertIn('/admin/login', res2.headers['Location'])

        res3 = self.client.get('/admin/projetos', follow_redirects=False)
        self.assertEqual(res3.status_code, 302)
        self.assertIn('/admin/login', res3.headers['Location'])

    def test_admin_login_and_logout(self):
        # Teste com senha errada
        res = self.client.post('/admin/login', data={'username': 'admin', 'password': 'wrongpassword'}, follow_redirects=True)
        self.assertIn('Credenciais inválidas'.encode('utf-8'), res.data)

        # Teste com login correto
        res_ok = self.client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(res_ok.status_code, 200)
        self.assertIn('Painel Administrativo'.encode('utf-8'), res_ok.data)

        # Teste de logout
        res_logout = self.client.get('/admin/logout', follow_redirects=True)
        self.assertEqual(res_logout.status_code, 200)
        self.assertIn('Login Administrativo'.encode('utf-8'), res_logout.data)

    def test_tutorial_crud_and_public_visibility(self):
        # Login
        self.client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'})

        # 1. Adicionar tutorial publicado
        res = self.client.post('/admin/tutoriais/novo', data={
            'title': 'Tutorial Teste Automatizado',
            'category': 'Python',
            'description': 'Resumo do teste automatizado de tutorial.',
            'content': 'Passo a passo do teste.',
            'status': 'published'
        }, follow_redirects=True)
        self.assertIn('Tutorial Teste Automatizado'.encode('utf-8'), res.data)

        # 2. Verificar se aparece na página pública /conteudos
        res_pub = self.client.get('/conteudos')
        self.assertIn('Tutorial Teste Automatizado'.encode('utf-8'), res_pub.data)

        # 3. Pegar id do tutorial criado
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tutorials WHERE title = 'Tutorial Teste Automatizado'")
        tut_id = cursor.fetchone()['id']
        conn.close()

        # 4. Editar para Rascunho (draft)
        self.client.post(f'/admin/tutoriais/editar/{tut_id}', data={
            'title': 'Tutorial Teste Automatizado Editado',
            'category': 'Python',
            'description': 'Resumo alterado.',
            'content': 'Passo a passo atualizado.',
            'status': 'draft'
        }, follow_redirects=True)

        # 5. Conferir que como rascunho NÃO aparece no site público /conteudos
        res_pub_draft = self.client.get('/conteudos')
        self.assertNotIn('Tutorial Teste Automatizado Editado'.encode('utf-8'), res_pub_draft.data)

        # 6. Excluir tutorial
        self.client.post(f'/admin/tutoriais/excluir/{tut_id}', follow_redirects=True)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tutorials WHERE id = ?", (tut_id,))
        deleted = cursor.fetchone()
        conn.close()
        self.assertIsNone(deleted)

    def test_project_crud_and_public_visibility(self):
        # Login
        self.client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'})

        # 1. Adicionar projeto publicado
        res = self.client.post('/admin/projetos/novo', data={
            'title': 'Projeto E-commerce Teste',
            'description': 'Descrição do projeto de teste para verificar funcionamento.',
            'technologies': 'Python, Flask, SQLite',
            'features': 'Checkout, catálogo responsivo',
            'demo_url': 'https://exemplo.com/demo',
            'repo_url': 'https://github.com/exemplo/repo',
            'status': 'published'
        }, follow_redirects=True)
        self.assertIn('Projeto E-commerce Teste'.encode('utf-8'), res.data)

        # 2. Verificar se aparece na página pública /projetos
        res_pub = self.client.get('/projetos')
        self.assertIn('Projeto E-commerce Teste'.encode('utf-8'), res_pub.data)

        # 3. Pegar id do projeto criado
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM projects WHERE title = 'Projeto E-commerce Teste'")
        proj_id = cursor.fetchone()['id']
        conn.close()

        # 4. Editar projeto para Rascunho
        self.client.post(f'/admin/projetos/editar/{proj_id}', data={
            'title': 'Projeto E-commerce Teste Modificado',
            'description': 'Descrição alterada.',
            'technologies': 'Python, Vue',
            'features': 'Nova feature',
            'demo_url': '',
            'repo_url': '',
            'status': 'draft'
        }, follow_redirects=True)

        # 5. Conferir que rascunho NÃO aparece na página pública
        res_pub2 = self.client.get('/projetos')
        self.assertNotIn('Projeto E-commerce Teste Modificado'.encode('utf-8'), res_pub2.data)

        # 6. Excluir projeto
        self.client.post(f'/admin/projetos/excluir/{proj_id}', follow_redirects=True)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (proj_id,))
        deleted = cursor.fetchone()
        conn.close()
        self.assertIsNone(deleted)

if __name__ == '__main__':
    unittest.main()
