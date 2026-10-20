# Plataforma Logística

App Streamlit que lê três planilhas do Google Sheets:
- **follow-up ativo** (aba Consolidado) — painéis operacionais e indicadores;
- **processos encerrados** (aba CONCLUIDOS, mesmas colunas) — histórico, entra só nos indicadores e na consulta de frete;
- **planilha de tarifas** — calculadora.

Se uma referência estiver nas duas bases, vale a linha do Consolidado.
O time continua preenchendo as planilhas; a plataforma é só leitura.

| Página | O que mostra |
|---|---|
| ⚓ Atracação de navios | Navios esperados/atracados em Navegantes, Itapoá e Itajaí (hoje / semana / 14 dias), busca por container |
| ⏳ Aguardando booking | Processos com Instrução de Embarque (AE) e sem Data de Embarque (M), com semáforo de dias |
| 📊 Dashboard de agentes | Containers por agente, frete médio por agente/origem, tempo de confirmação, transit time; filtro por agente, ano, meses |
| 🔎 Consulta de frete | Frete médio por origem de um agente nos últimos 3/6/12/24 meses, comparado à média geral |
| 🧮 Calculadora logística | Porte do Apps Script (armazenagem, parceiro, frete rodoviário), lendo as abas da planilha de tarifas |

## Identidade visual

Cores do Grupo CVF extraídas do logo oficial: **amarelo `#FCB600`** e **marinho `#0C0526`**
(definidas em `.streamlit/config.toml` e `core/ui.py`). Logo e ícone em `assets/`.
Verde/âmbar/vermelho são usados só como cores de status (atracado, atenção, crítico).

## Colunas usadas (aba Consolidado)

A equipe · B referência · D cliente · F modalidade · G status · K exportador · M embarque · N chegada ·
O transit time · P origem · Q destino · R incoterm · W embarcação · **Y quantidade de containers** ·
**Z números dos containers** · AD frete internacional · AE instrução de embarque · AF agente de cargas.
Se colunas mudarem de posição, ajuste `COLUNAS` em `core/data.py`.

Premissas: frete (AD) é **por container**, em US$; "Atracado" = data de chegada (N) ≤ hoje.

## Rodar localmente

```bash
pip install -r requirements.txt
```
```bash
python -m streamlit run app.py
```

Sem credenciais, o app lê `data/followup.xlsx`, `data/encerrados.xlsx` e `data/tarifas.xlsx` (modo desenvolvimento, sem login).
A pasta `data/` está no `.gitignore` — nunca suba dados para o GitHub.

## Publicar com segurança (≈ 30 min, gratuito)

1. **Conta de serviço (leitura das planilhas)**
   Google Cloud Console → novo projeto → ative *Google Sheets API* → *IAM → Contas de serviço* → criar →
   *Chaves → JSON*. Compartilhe as **três** planilhas com o e-mail da conta de serviço como **Leitor**.
2. **Login Google**
   *APIs e serviços → Tela de consentimento OAuth* (tipo Interno se tiverem Google Workspace) →
   *Credenciais → ID do cliente OAuth → Aplicativo da Web* → URI de redirecionamento:
   `https://SEU-APP.streamlit.app/oauth2callback`.
3. **GitHub**: crie um repositório **privado** e suba esta pasta (sem `data/` e sem `secrets.toml`).
4. **Streamlit Community Cloud** (share.streamlit.io) → *New app* → escolha o repo, `app.py` →
   *Advanced settings → Secrets*: cole o conteúdo de `.streamlit/secrets.toml.example` preenchido.
5. Em **[acesso]** liste os e-mails do time (ou o domínio da empresa).
6. Em **[planilhas]** ficam os IDs das 3 planilhas — eles **não** ficam no código, então o repositório
   pode ser público sem apontar para os dados. O `python gerar_secrets.py` monta tudo isso a partir dos links.

### Camadas de segurança
- Login Google obrigatório + lista de e-mails/domínio autorizados (`core/auth.py`).
- Conta de serviço com escopo **somente leitura**; credenciais apenas em *Secrets*.
- Código em repositório privado; dados nunca versionados.
- **Restrinja o compartilhamento das planilhas**: hoje as três estão como "qualquer pessoa com o link".
  Depois de configurar a conta de serviço, mude para "Restrito" — o app continua funcionando.

## Próxima fase: status de atracação automático
Hoje "Atracado" é inferido pela data de chegada. Para confirmar com dado real:
- ler o line-up publicado por Portonave, Porto Itapoá e Porto de Itajaí (checar termos de uso de cada site);
- ou APIs gratuitas de rastreio dos armadores (Maersk, Hapag-Lloyd, CMA CGM) pelo número do container;
- AIS gratuito (ex.: aisstream.io) como confirmação de chegada do navio na área do porto.
