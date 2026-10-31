# TECNOLAB — Site & Portfólio Profissional

Site institucional e portfólio profissional desenvolvido para a marca **TECNOLAB**[cite: 1], com a proposta de apresentar projetos de desenvolvimento web, divulgação de serviços e canal de contato com potenciais clientes.

## 🚀 Tecnologias Utilizadas
- **Backend:** Python 3 + Flask[cite: 1]
- **Frontend:** HTML5, CSS3 Nativo (Variáveis CSS, Flexbox/Grid) e JavaScript Nativo[cite: 1]
- **Template Engine:** Jinja2[cite: 1]
- **Banco de Dados:** SQLite 3[cite: 1]

## 🛠️ Como Executar o Projeto

1. Clone ou extraia a pasta do projeto `TECNOLAB`.
2. Crie e ative um ambiente virtual (opcional, porém recomendado):
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate


## 🔐 Painel Administrativo

O projeto conta com um painel administrativo protegido para gerenciamento dinâmico de conteúdos/tutoriais e projetos do portfólio.

### Como Acessar
1. Acesse no navegador: `http://localhost:5000/admin`
2. Credenciais padrão iniciais:
   - **Usuário:** `admin`
   - **Senha:** `admin123`

### Como Alterar ou Criar Nova Senha de Administrador
Execute o script interativo no terminal:
```bash
python create_admin.py
```
O script solicitará o nome de usuário (padrão `admin`) e a nova senha desejada com confirmação, gravando o hash seguro com `werkzeug.security` no SQLite.
