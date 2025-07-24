# 🚀 Guia Rápido de Configuração - F5 YouTube Optimizer

## ✅ Checklist de Setup (Para Iniciantes)

### **PASSO 1: Preparação**
- [ ] Python 3.8+ instalado
- [ ] Conta Gmail da F5 Estratégia
- [ ] Acesso administrativo ao canal do YouTube da F5

### **PASSO 2: Setup Automático**
```bash
# Execute este comando e siga as instruções:
python setup.py
```

### **PASSO 3: Google Cloud Console** 
📝 **O script abrirá automaticamente no navegador**

- [ ] Criar projeto: `F5-YouTube-Analytics-System`
- [ ] Habilitar APIs:
  - [ ] YouTube Data API v3
  - [ ] YouTube Analytics API  
  - [ ] YouTube Reporting API
- [ ] Configurar OAuth (tipo: EXTERNO)
- [ ] Criar credenciais OAuth 2.0 (aplicativo desktop)
- [ ] Baixar `client_secret.json`
- [ ] Criar API Key e restringir para YouTube APIs

### **PASSO 4: Configurar IA (Claude)**
📝 **O script abrirá automaticamente no navegador**

- [ ] Criar conta em: https://console.anthropic.com/
- [ ] Gerar API Key
- [ ] Copiar chave (sk-ant-...)

### **PASSO 5: Obter ID do Canal F5**
```bash
# MÉTODO FÁCIL: Use a ferramenta online
# 1. Vá para: https://commentpicker.com/youtube-channel-id.php
# 2. Cole a URL do canal da F5
# 3. Copie o ID (UC...)
```

### **PASSO 6: Finalizar Configuração**
- [ ] Editar arquivo `.env` com suas credenciais
- [ ] Colocar `client_secret.json` na pasta do projeto
- [ ] Executar: `python main.py`

---

## 🆘 Solução de Problemas

### ❌ "Erro: Variáveis de ambiente faltando"
```bash
# Verifique se o arquivo .env está configurado corretamente
python setup.py check
```

### ❌ "Arquivo client_secret.json não encontrado"
- Certifique-se de que baixou o arquivo do Google Cloud
- Renomeie para exatamente `client_secret.json`
- Coloque na mesma pasta do projeto

### ❌ "Erro de autenticação YouTube"
- Verifique se a API Key está correta
- Confirme se as APIs estão habilitadas no Google Cloud
- Verifique se o OAuth está configurado como "EXTERNO"

### ❌ "Erro de IA/Claude"
- Verifique se a chave da Anthropic está correta
- Confirme se tem créditos/acesso à API
- Como fallback, configure OpenAI

---

## 📞 Suporte

Se precisar de ajuda:

1. **Verificar logs**: Arquivo `logs/f5_youtube_optimizer.log`
2. **Documentação**: `README.md`
3. **Reexecutar setup**: `python setup.py`

---

## 🎯 Após Setup Completo

```bash
# Testar o sistema
python main.py --mode suggestions --persona crescimento

# Iniciar dashboard
python main.py

# Análise completa
python main.py --mode analysis
```

**Dashboard disponível em:** http://localhost:8050

---

*Tempo estimado de configuração: 15-30 minutos* 