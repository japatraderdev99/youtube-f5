# 🎯 Finalizar Configuração - F5 YouTube Optimizer

## ✅ **JÁ CONFIGURADO:**
- 🔑 **Credenciais OAuth**: `client_secret.json` ✅
- 🌐 **Projeto Google Cloud**: `fabled-orbit-466718-j9` ✅  
- 📄 **Template .env**: `credentials_configured.env` ✅

## ⚡ **FINALIZAÇÃO RÁPIDA (5 minutos):**

### **OPÇÃO 1: Assistente Automático** (Recomendado)
```bash
python finalize_setup.py
```
*O script irá coletar as 3 credenciais necessárias e configurar tudo automaticamente*

### **OPÇÃO 2: Configuração Manual**

#### **1️⃣ Criar API Key YouTube** (2 min)
```bash
# Acesse diretamente o projeto:
https://console.cloud.google.com/apis/credentials?project=fabled-orbit-466718-j9
```
- **"CRIAR CREDENCIAIS"** → **"Chave de API"**
- **"RESTRINGIR CHAVE"** → Selecionar:
  - ✅ YouTube Data API v3
  - ✅ YouTube Analytics API
  - ✅ YouTube Reporting API
- Copiar a chave gerada

#### **2️⃣ Obter Channel ID F5** (1 min)
```bash
# Ferramenta online:
https://commentpicker.com/youtube-channel-id.php
```
- Colar URL do canal F5 Estratégia
- Copiar ID que começa com `UC...`

#### **3️⃣ Claude API Key** (2 min)  
```bash
# Console Anthropic:
https://console.anthropic.com/
```
- **API Keys** → **Create Key**
- Nome: `F5-YouTube-Optimizer`
- Copiar chave `sk-ant-...`

#### **4️⃣ Finalizar .env**
```bash
# Renomear arquivo
mv credentials_configured.env .env

# Editar e substituir:
YOUTUBE_API_KEY=SUA_API_KEY_AQUI          # ← Cole sua API Key
F5_CHANNEL_ID=UC_SEU_CHANNEL_ID_AQUI      # ← Cole Channel ID  
ANTHROPIC_API_KEY=sk-ant-sua_chave_aqui   # ← Cole Claude Key
```

## 🚀 **TESTAR SISTEMA:**

```bash
# Verificar configuração
python check_credentials.py

# Testar sistema
python main.py --mode suggestions --persona crescimento

# Iniciar dashboard
python main.py
```

**Dashboard:** http://localhost:8050

## 🆘 **Problemas Comuns:**

### ❌ "APIs não habilitadas"
- Acesse: https://console.cloud.google.com/apis/dashboard?project=fabled-orbit-466718-j9
- Habilite as 3 APIs do YouTube

### ❌ "Erro de autenticação"  
- Verifique se API Key está restrita corretamente
- Confirme se OAuth está configurado como "EXTERNO"

### ❌ "Channel ID inválido"
- ID deve começar com `UC`
- Use a ferramenta online para obter

---

## 📞 **Suporte Rápido:**
```bash
python check_credentials.py    # Verificar status
python finalize_setup.py       # Reconfigurar  
```

**Tempo estimado: 5 minutos** ⏱️ 