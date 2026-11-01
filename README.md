# TECNOLAB — Site Institucional

Site institucional e portfólio da **TECNOLAB**, desenvolvido para apresentar serviços de desenvolvimento web, projetos, conteúdos tecnológicos e canais de contato.

O projeto busca oferecer uma experiência moderna, responsiva e acessível, com uma área administrativa para gerenciar os conteúdos publicados.

## ✨ Funcionalidades

- Página inicial com apresentação da marca.
- Página institucional sobre a TECNOLAB.
- Portfólio de projetos.
- Apresentação dos serviços oferecidos.
- Página de tecnologias e conteúdos.
- Formulário de contato.
- Painel administrativo com autenticação.
- Cadastro, edição e exclusão de tutoriais.
- Cadastro, edição e exclusão de projetos.
- Controle de publicação e rascunhos.
- Envio de imagens para os conteúdos.

## 🧰 Tecnologias

| Tecnologia | Aplicação |
|---|---|
| Python 3 | Backend |
| Flask | Aplicação web e rotas |
| HTML5 | Estrutura das páginas |
| CSS3 | Estilização e responsividade |
| JavaScript | Interatividade |
| Jinja2 | Templates dinâmicos |
| SQLite | Banco de dados |
| Werkzeug | Segurança de senhas e utilitários |

## 📁 Estrutura do projeto

```text
TECNOLAB/
├── app.py
├── config.py
├── create_admin.py
├── requirements.txt
├── templates/
│   ├── admin/
│   └── ...
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
└── ...
```

*Estrutura ilustrativa: a organização pode variar conforme a versão do projeto.*

## ⚙️ Como executar localmente

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
cd TECNOLAB
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

### 3. Ative o ambiente virtual

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure o administrador

Se o arquivo `create_admin.py` estiver presente, execute:

```bash
python create_admin.py
```

Siga as instruções para criar o usuário e definir uma senha própria.

### 6. Inicie a aplicação

```bash
python app.py
```

Acesse pelo navegador:

```text
http://127.0.0.1:5000
```

## 🔐 Painel administrativo

O sistema possui uma área administrativa protegida por autenticação.

**Endereço local:**

```text
http://127.0.0.1:5000/admin/login
```

Após entrar, é possível gerenciar os tutoriais e projetos, editar informações e controlar quais conteúdos ficam publicados.

As credenciais administrativas devem ser configuradas individualmente. Não utilize senhas padrão em ambientes públicos.

## 🗄️ Banco de dados

O projeto utiliza SQLite para armazenar informações como:

- Usuários administrativos.
- Tutoriais.
- Projetos.
- Mensagens enviadas pelo formulário de contato.

As imagens enviadas pelo painel administrativo são armazenadas no diretório de uploads configurado pela aplicação.

Em uma hospedagem pública, o banco de dados e os arquivos enviados precisam estar em armazenamento persistente para que não sejam perdidos em reinicializações ou atualizações.

## 🔒 Segurança

Antes de disponibilizar o projeto publicamente:

- Configure uma chave secreta própria para a aplicação.
- Utilize senhas administrativas fortes.
- Não publique arquivos `.env`, senhas ou dados privados.
- Desative o modo de depuração (`debug`) em produção.
- Utilize HTTPS.
- Configure corretamente o armazenamento do banco de dados e dos uploads.

## 🚀 Publicação

O projeto pode ser hospedado em um serviço compatível com aplicações Python e Flask.

A publicação deve utilizar um servidor adequado para produção e armazenamento persistente para os dados administrados pelo painel.

## 👨‍💻 Sobre o projeto

Desenvolvido como parte da iniciativa **TECNOLAB**, com foco em desenvolvimento web, soluções digitais, tecnologia e criação de projetos práticos.

---

**TECNOLAB — Conectando você à tecnologia.**