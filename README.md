
# 💻 Setup do backend Django passo a passo

## 🎯 Criação do ambiente virtual

```powershell
py -m venv venv
```
Cria um ambiente virtual chamado `venv` na pasta atual, para isolar as dependências do projeto.

---

## ✅ Ativação do ambiente virtual

```powershell
./venv/Scripts/activate
```
Ativa o ambiente virtual no Windows (PowerShell). Após ativar, todos os pacotes serão instalados localmente.

---

## 📦 Instalação das dependências

```powershell
pip install django djangorestframework django-cors-headers
```
Instala o Django, Django REST Framework (para APIs) e django-cors-headers (para permitir requisições de outros domínios).

---

## 💾 Gerar arquivo de requisitos (JÁ FEITO)

```powershell
pip freeze > requirements.txt
```
Gera o arquivo `requirements.txt` com as versões exatas das bibliotecas instaladas, facilitando replicar o ambiente.

---

## ⚙️ Criação do projeto Django (JÁ FEITO)

```powershell
django-admin startproject backe
```
Cria um projeto Django chamado `backe` (possivelmente seria `backend`). Isso cria a estrutura base do projeto.

---

## 🗂️ Criação do app interno

```powershell
py manage.py startapp api
```
Cria um app chamado `api`, onde ficarão os modelos, views, serializers e rotas específicas.

---

## 🛠️ Gerar migrações dos modelos

```powershell
py manage.py makemigrations
```
Gera arquivos de migração para refletir alterações nos modelos no banco de dados.

---

## 🔄 Confirmar migrações adicionais

```powershell
py manage.py makemigrations
```
Executado novamente para garantir que todas alterações estejam migradas.

---

## 🗄️ Aplicar migrações ao banco

```powershell
py manage.py migrate
```
Executa as migrações e cria/atualiza as tabelas no banco de dados (SQLite por padrão).

---

## 👤 Criar superusuário

```powershell
py manage.py createsuperuser
```
Cria um usuário administrador para acessar o painel `/admin/`. Será solicitado username, email e senha.  (JÁ FOI FEITO)

---

## 🚀 Iniciar o servidor de desenvolvimento

```powershell
py manage.py runserver
```
Inicia o servidor local Django em `http://127.0.0.1:8000/`. Este comando foi executado três vezes durante o processo para reiniciar o servidor após alterações.

---

### 💡 Observação final
O comando `runserver` pode ser interrompido com `CTRL + C` e reiniciado a qualquer momento para carregar as novas alterações no código.

---
