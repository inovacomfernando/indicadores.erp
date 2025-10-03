# 🚀 Guia de Deploy - Dashboard Marketing SaaS ERP

Este guia mostra como fazer o deploy do seu dashboard Streamlit no GitHub e Streamlit Cloud.

## 📦 Passo 1: Preparar o Projeto Localmente

### 1.1 Criar estrutura de pastas

```bash
mkdir dashboard-marketing-saas
cd dashboard-marketing-saas
```

### 1.2 Criar os arquivos

Crie os seguintes arquivos na raiz do projeto:
- `app.py` (código principal do dashboard)
- `requirements.txt` (dependências)
- `README.md` (documentação)
- `.gitignore` (arquivos a ignorar)
- `LICENSE` (licença MIT)

### 1.3 Testar localmente

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No Mac/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
streamlit run app.py
```

Acesse `http://localhost:8501` para verificar se está funcionando.

## 🔧 Passo 2: Configurar Git

### 2.1 Inicializar repositório Git

```bash
git init
git add .
git commit -m "Initial commit: Dashboard Marketing SaaS ERP"
```

### 2.2 Criar repositório no GitHub

1. Acesse [github.com](https://github.com)
2. Clique em **New repository**
3. Nome: `dashboard-marketing-saas`
4. Descrição: `Dashboard interativo de KPIs de marketing para SaaS ERP`
5. Escolha: **Public** (para deploy gratuito no Streamlit Cloud)
6. **NÃO** marque "Initialize with README" (já temos um)
7. Clique em **Create repository**

### 2.3 Conectar repositório local ao GitHub

```bash
git remote add origin https://github.com/SEU-USUARIO/dashboard-marketing-saas.git
git branch -M main
git push -u origin main
```

**Substitua `SEU-USUARIO` pelo seu username do GitHub!**

## ☁️ Passo 3: Deploy no Streamlit Cloud (GRATUITO)

### 3.1 Criar conta no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em **Sign up with GitHub**
3. Autorize o Streamlit a acessar seus repositórios

### 3.2 Fazer Deploy

1. No Streamlit Cloud, clique em **New app**
2. Preencha os campos:
   - **Repository**: `SEU-USUARIO/dashboard-marketing-saas`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Clique em **Deploy!**

### 3.3 Aguardar Deploy

- O deploy leva de 2-5 minutos
- Você receberá uma URL pública: `https://seu-app.streamlit.app`
- O app será atualizado automaticamente a cada push no GitHub

## 🔄 Passo 4: Atualizar o Dashboard

Sempre que quiser atualizar o dashboard:

```bash
# Fazer alterações no código
# ...

# Adicionar alterações
git add .

# Commitar
git commit -m "Descrição das alterações"

# Enviar para GitHub
git push origin main
```

O Streamlit Cloud detectará as mudanças e fará o redeploy automaticamente!

## 🎨 Passo 5: Personalizar o Deploy (Opcional)

### 5.1 Criar arquivo de configuração

Crie o arquivo `.streamlit/config.toml`:

```bash
mkdir .streamlit
```

Crie o arquivo `.streamlit/config.toml` com:

```toml
[theme]
primaryColor = "#073763"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
```

### 5.2 Atualizar .gitignore

Edite o `.gitignore` e adicione:

```
# Streamlit config
.streamlit/secrets.toml
```

**Importante**: O `config.toml` pode ser commitado, mas **NUNCA** commite o `secrets.toml` se tiver dados sensíveis!

### 5.3 Fazer commit e push

```bash
git add .streamlit/config.toml
git add .gitignore
git commit -m "Add Streamlit config"
git push origin main
```

## 📊 Passo 6: Adicionar Dados Reais (Opcional)

Se quiser usar dados reais de um arquivo CSV:

### 6.1 Criar arquivo de dados

Crie `data/kpis_marketing.csv` com seus dados reais.

### 6.2 Modificar app.py

```python
@st.cache_data
def load_data():
    # Se existir arquivo CSV, carrega dele
    if os.path.exists('data/kpis_marketing.csv'):
        df = pd.read_csv('data/kpis_marketing.csv')
        return df
    # Senão, usa dados mockados
    else:
        data = {
            'Mês': ['Mai/25', 'Jun/25', ...],
            # ... resto dos dados
        }
        return pd.DataFrame(data)
```

### 6.3 Atualizar .gitignore

```
# Data files
data/*.csv
```

### 6.4 Upload no Streamlit Cloud

1. Acesse seu app no Streamlit Cloud
2. Clique em **Settings** > **Secrets**
3. Ou faça upload manual do CSV via interface

## 🔐 Passo 7: Adicionar Secrets (Opcional)

Se precisar de API keys ou dados sensíveis:

### 7.1 No Streamlit Cloud

1. Vá em **Settings** > **Secrets**
2. Adicione no formato TOML:

```toml
[database]
host = "seu-host"
user = "seu-usuario"
password = "sua-senha"

[api]
key = "sua-api-key"
```

### 7.2 No código

```python
import streamlit as st

# Acessar secrets
db_host = st.secrets["database"]["host"]
api_key = st.secrets["api"]["key"]
```

## 📱 Passo 8: Compartilhar o Dashboard

Depois do deploy, você terá uma URL pública:
- `https://seu-app.streamlit.app`

Você pode:
- ✅ Compartilhar a URL com qualquer pessoa
- ✅ Incorporar em sites (iframe)
- ✅ Adicionar ao LinkedIn/portfólio
- ✅ Usar em apresentações

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"
**Solução**: Verifique se todas as bibliotecas estão no `requirements.txt`

### Erro: "Port already in use"
**Solução**: 
```bash
# Windows
taskkill /F /IM streamlit.exe

# Mac/Linux
pkill streamlit
```

### App não atualiza no Streamlit Cloud
**Solução**: 
1. Vá em **Manage app** > **Reboot app**
2. Ou force um novo commit:
```bash
git commit --allow-empty -m "Force rebuild"
git push origin main
```

### Deploy falhou
**Solução**: 
1. Verifique os logs no Streamlit Cloud
2. Teste localmente primeiro
3. Confirme que o `requirements.txt` está correto

## 📞 Recursos Úteis

- 📚 [Documentação Streamlit](https://docs.streamlit.io)
- 🎓 [Tutoriais Streamlit](https://docs.streamlit.io/library/get-started)
- 💬 [Fórum Streamlit](https://discuss.streamlit.io)
- 🐛 [Issues GitHub](https://github.com/streamlit/streamlit/issues)

## ✅ Checklist Final

Antes de fazer o deploy, verifique:

- [ ] Todos os arquivos criados e salvos
- [ ] `app.py` testado localmente
- [ ] `requirements.txt` com todas as dependências
- [ ] `.gitignore` configurado
- [ ] README.md atualizado
- [ ] Repositório GitHub criado
- [ ] Código commitado e enviado ao GitHub
- [ ] Deploy feito no Streamlit Cloud
- [ ] URL pública funcionando
- [ ] Dashboard carregando corretamente

## 🎉 Pronto!

Seu dashboard está no ar e acessível para qualquer pessoa!

**URL**: `https://[seu-app].streamlit.app`

---

**Dúvidas?** Abra uma issue no repositório ou consulte a documentação do Streamlit.
