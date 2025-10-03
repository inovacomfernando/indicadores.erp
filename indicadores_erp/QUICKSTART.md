# ⚡ Quick Start - Comandos Rápidos

## 🚀 Setup Inicial (Execute uma vez)

```bash
# 1. Criar e entrar na pasta do projeto
mkdir dashboard-marketing-saas
cd dashboard-marketing-saas

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Criar os arquivos do projeto
# Copie os arquivos dos artifacts:
# - app.py
# - requirements.txt
# - README.md
# - .gitignore
# - LICENSE

# 5. Instalar dependências
pip install -r requirements.txt

# 6. Testar localmente
streamlit run app.py
```

## 📤 Subir para o GitHub (Execute uma vez)

```bash
# 1. Inicializar Git
git init

# 2. Adicionar todos os arquivos
git add .

# 3. Fazer primeiro commit
git commit -m "Initial commit: Dashboard Marketing SaaS ERP"

# 4. Criar repositório no GitHub
# Acesse: https://github.com/new
# Nome: dashboard-marketing-saas
# Visibilidade: Public
# Clique em "Create repository"

# 5. Conectar ao GitHub (SUBSTITUA SEU-USUARIO)
git remote add origin https://github.com/SEU-USUARIO/dashboard-marketing-saas.git
git branch -M main
git push -u origin main
```

## ☁️ Deploy no Streamlit Cloud (Execute uma vez)

1. Acesse: https://share.streamlit.io
2. Faça login com GitHub
3. Clique em "New app"
4. Selecione seu repositório: `SEU-USUARIO/dashboard-marketing-saas`
5. Branch: `main`
6. Main file: `app.py`
7. Clique em "Deploy!"

**Pronto! Em 3-5 minutos seu dashboard estará no ar! 🎉**

## 🔄 Atualizar o Dashboard

Sempre que fizer mudanças no código:

```bash
# 1. Adicionar alterações
git add .

# 2. Commitar (descreva o que mudou)
git commit -m "Adiciona nova funcionalidade X"

# 3. Enviar para GitHub
git push origin main
```

**O Streamlit Cloud atualiza automaticamente!** 🔄

## 🛑 Parar o servidor local

```bash
# Pressione no terminal:
Ctrl + C
```

## 🔌 Desativar ambiente virtual

```bash
deactivate
```

## 📋 Checklist Rápido

### Antes do primeiro deploy:
- [ ] Criar pasta do projeto
- [ ] Criar ambiente virtual
- [ ] Copiar todos os arquivos (app.py, requirements.txt, etc)
- [ ] Testar localmente com `streamlit run app.py`
- [ ] Verificar se abre no navegador (http://localhost:8501)

### Para subir no GitHub:
- [ ] Criar repositório no GitHub
- [ ] Executar comandos git (init, add, commit, push)
- [ ] Verificar se arquivos aparecem no GitHub

### Para fazer deploy:
- [ ] Acessar Streamlit Cloud
- [ ] Conectar com GitHub
- [ ] Criar novo app
- [ ] Aguardar deploy (3-5 min)
- [ ] Testar URL pública

## 🆘 Comandos Úteis

```bash
# Ver status do Git
git status

# Ver histórico de commits
git log --oneline

# Desfazer último commit (mantém alterações)
git reset --soft HEAD~1

# Ver diferenças antes de commitar
git diff

# Atualizar do GitHub (se houver mudanças remotas)
git pull origin main

# Ver URL do repositório remoto
git remote -v

# Criar nova branch
git checkout -b minha-feature

# Voltar para branch main
git checkout main
```

## 🎯 Estrutura Final do Projeto

```
dashboard-marketing-saas/
│
├── app.py              # ✅ Código principal
├── requirements.txt    # ✅ Dependências
├── README.md          # ✅ Documentação
├── .gitignore         # ✅ Arquivos ignorados
├── LICENSE            # ✅ Licença MIT
├── DEPLOY.md          # ✅ Guia detalhado
└── venv/              # ❌ NÃO commitar (está no .gitignore)
```

## 💡 Dicas Importantes

1. **Sempre ative o ambiente virtual** antes de trabalhar no projeto
2. **Teste localmente** antes de fazer push
3. **Commits descritivos** ajudam a entender o histórico
4. **O .gitignore já está configurado** - não precisa alterar
5. **Deploy é automático** após push no GitHub

## 🎉 Primeiro Acesso

Depois do deploy, você receberá uma URL tipo:
```
https://seu-app-nome-aleatorio.streamlit.app
```

**Compartilhe essa URL com quem quiser!** 🚀

---

## ⏱️ Tempo Estimado Total

- **Setup inicial**: 5-10 minutos
- **GitHub**: 5 minutos
- **Deploy**: 3-5 minutos
- **Total**: ~15-20 minutos

**Você terá um dashboard profissional no ar em menos de 30 minutos!** ⚡
