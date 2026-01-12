# 🚀 Como Rodar o Projeto Localmente

## Pré-requisitos

- Python 3.8 ou superior (você tem Python 3.14.0 ✅)
- pip (gerenciador de pacotes Python)

## Passo a Passo

### 1. Navegar para a pasta do projeto

```powershell
cd indicadores_erp
```

### 2. Criar ambiente virtual (se ainda não criou)

```powershell
py -m venv venv
```

### 3. Ativar o ambiente virtual

**No PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**No CMD:**
```cmd
venv\Scripts\activate.bat
```

**No Git Bash:**
```bash
source venv/Scripts/activate
```

### 4. Instalar dependências

```powershell
pip install streamlit pandas plotly numpy scikit-learn scipy openpyxl python-dotenv
```

**Nota:** O pacote `supabase` não é necessário para rodar o projeto, pois os dados são carregados diretamente no código.

### 5. Executar o projeto

```powershell
streamlit run app.py
```

O dashboard será aberto automaticamente no seu navegador em `http://localhost:8501`

## 🛑 Parar o servidor

No terminal onde o Streamlit está rodando, pressione:
```
Ctrl + C
```

## 🔌 Desativar ambiente virtual

Quando terminar de trabalhar:
```powershell
deactivate
```

## 📝 Comandos Rápidos (Resumo)

```powershell
# 1. Entrar na pasta
cd indicadores_erp

# 2. Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# 3. Rodar o projeto
streamlit run app.py
```

## ⚠️ Problemas Comuns

### Erro ao ativar ambiente virtual no PowerShell

Se aparecer erro de política de execução, execute no PowerShell como Administrador:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Porta 8501 já está em uso

Se a porta 8501 estiver ocupada, você pode especificar outra porta:
```powershell
streamlit run app.py --server.port 8502
```

### Dependências não instaladas

Certifique-se de que o ambiente virtual está ativado (você verá `(venv)` no início da linha do terminal) antes de instalar as dependências.

## 🎯 Estrutura do Projeto

```
indicadores_erp/
├── app.py              # Arquivo principal
├── requirements.txt    # Dependências (opcional - supabase pode falhar)
├── venv/              # Ambiente virtual (não commitar)
└── ...
```

## ✅ Verificação

Se tudo estiver funcionando, você verá:
- Uma mensagem no terminal: "You can now view your Streamlit app in your browser"
- O dashboard abrindo automaticamente no navegador
- URL: `http://localhost:8501`

---

**Pronto! Seu dashboard está rodando localmente! 🎉**

