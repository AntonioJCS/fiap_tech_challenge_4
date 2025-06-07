# Proposta de Arquitetura Híbrida Ajustada: Previsão de Ações com LSTM

## Introdução

Com base no contexto detalhado em [[Pos_Tech - MLET - Tech Challenge Fase 4.pdf]] (previsão de fechamento de ações com LSTM, usando `yfinance`, FastAPI, autenticação, persistência e monitoramento), foi definida uma arquitetura híbrida com o objetivo é manter os benefícios de coesão, baixo acoplamento e desenvolvimento paralelo.

## Estrutura de Diretórios
1.  **Separação de Processos:**
	Isolamos a **ingestão/processamento de dados** (`data_pipeline/`), o **ciclo de vida do modelo ML** (`ml_lifecycle/`) e a **aplicação API** (`app/`) em diretórios de alto nível (Camadas).
	
2.  **Organização Funcional Interna:**
	Dentro da API, a organização primária é por funcionalidade (`features/`).
	
3.  **Componentes Compartilhados:**
	Centralizamos código reutilizável para consistência.

```plaintext
projeto_lstm_acoes/
│
├── data_pipeline/           # CRITÉRIO 1: Coleta e Pré-processamento
│   ├── __init__.py
│   ├── sources/
│   │   └── yfinance_collector.py # Coleta dados usando yfinance
│   ├── processing/
│   │   └── lstm_preprocessor.py  # Limpeza, normalização, criação de sequências para LSTM
│   ├── storage/
│   │   └── feature_store.py    # (Opcional) Interação com local de armazenamento (DB, S3, etc.)
│   └── run_pipeline.py         # Orquestra a execução da coleta e processamento
│
├── ml_lifecycle/            # CRITÉRIO 2 & 3: Desenvolvimento e Exportação do Modelo
│   ├── __init__.py
│   ├── models/
│   │   └── lstm_model.py       # Definição da arquitetura do modelo LSTM (ex: Keras/TensorFlow)
│   ├── training/
│   │   ├── train.py            # Script principal de treinamento
│   │   └── configs/            # Arquivos de configuração para treinamento (hiperparâmetros)
│   ├── evaluation/
│   │   └── evaluate.py         # Script para avaliar o modelo treinado
│   ├── export/
│   │   └── export_model.py     # Script para salvar/exportar o modelo treinado (ex: .h5, MLflow)
│   └── artifacts/              # Local (ou referência) para modelos exportados/métricas
│
├── app/                     # CRITÉRIO 0, 4 & 5: API, Auth, DB, Monitoramento
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada FastAPI, configuração global, middleware (monitoramento)
│   ├── config.py            # Carregamento de configurações
│   │
│   ├── core/                # Componentes centrais compartilhados
│   │   ├── __init__.py
│   │   ├── security.py      # CRITÉRIO 0: Lógica de autenticação/autorização
│   │   ├── database.py      # CRITÉRIO 0: Configuração da sessão do BD
│   │   └── monitoring/      # CRITÉRIO 5: Utilitários/configuração de monitoramento (ex: logging, métricas)
│   │       ├── __init__.py
│   │       └── metrics.py     # (Exemplo) Helpers para Prometheus/etc.
│   │
│   ├── models/              # CRITÉRIO 0: Modelos ORM compartilhados
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── prediction_log.py # (Opcional) Para logar requisições/predições
│   │
│   ├── schemas/             # Schemas Pydantic compartilhados
│   │   ├── __init__.py
│   │   ├── token.py
│   │   └── user.py
│   │
│   └── features/            # Módulos organizados por funcionalidade
│       ├── __init__.py
│       │
│       └── stock_prediction/ # Funcionalidade principal de previsão
│           ├── __init__.py
│           ├── router.py      # Endpoint API: /predict/{ticker} (com dependência de auth)
│           ├── schemas.py     # Schemas: PredictionRequest, PredictionResponse
│           ├── service.py     # Lógica: recebe request, chama predictor, loga, monitora
│           ├── predictor.py   # Carrega modelo exportado (CRITÉRIO 3), faz inferência
│           └── crud.py        # (Opcional) Buscar dados recentes ou logar predições no BD
│
├── tests/                   # Testes automatizados
│   ├── __init__.py
│   ├── app/
│   ├── data_pipeline/
│   └── ml_lifecycle/
│
├── .env.example
├── .gitignore
├── Dockerfile               # Para a aplicação 'app'
├── Dockerfile.ml_lifecycle  # (Opcional) Se o treinamento for containerizado
├── Dockerfile.data_pipeline # (Opcional) Se a ingestão for containerizada
├── README.md
├── requirements.txt
└── pyproject.toml
```

## Mapeamento dos Critérios na Arquitetura

*   **Critério 0 (Auth, DB, etc.):**
    *   **Autenticação:** Centralizada em `app/core/security.py` e aplicada nos endpoints relevantes (`app/features/stock_prediction/router.py`). Modelos e Schemas de usuário em `app/models/user.py` e `app/schemas/user.py`.
    *   **Persistência:** Configuração em `app/core/database.py`. Modelos ORM em `app/models/`. Lógica CRUD pode existir em `app/features/*/crud.py` para necessidades específicas (ex: logar predições).
    
*   **Critério 1 (Coleta e Pré-processamento):** 
	Isolado no diretório `data_pipeline/`. `sources/yfinance_collector.py` busca os dados, e `processing/lstm_preprocessor.py` realiza a limpeza e transformação necessárias para o formato LSTM.
	
*   **Critério 2 (Desenvolvimento LSTM):**
	Contido em `ml_lifecycle/`. A definição do modelo está em `models/lstm_model.py`, o treinamento em `training/train.py` (usando dados do `data_pipeline`), e a avaliação em `evaluation/evaluate.py`.
	
*   **Critério 3 (Exportação do Modelo):**
	O script `ml_lifecycle/export/export_model.py` é responsável por salvar o modelo treinado e validado em um formato utilizável (ex: `.h5`, ONNX) e/ou registrá-lo (ex: MLflow). O `app/features/stock_prediction/predictor.py` carregará este artefato exportado.
	
*   **Critério 4 (Servir via API):**
	A aplicação `app/` é responsável por isso. O `main.py` inicia o FastAPI. O `features/stock_prediction/router.py` define o endpoint, `schemas.py` define a interface, `service.py` orquestra a lógica, e `predictor.py` carrega o modelo (Critério 3) e faz a inferência.
	
*   **Critério 5 (Escalabilidade e Monitoramento):**
    *   **Escalabilidade:** A separação em `data_pipeline`, `ml_lifecycle`, e `app` permite escalar cada componente independentemente (ex: mais instâncias da API `app`, workers para `data_pipeline`). A arquitetura interna da `app` (FastAPI assíncrono) também ajuda.
    *   **Monitoramento:** Pode ser configurado em múltiplos níveis:
        *   **Infraestrutura/API:** Middleware no `app/main.py` pode expor métricas (tempo de resposta, requisições/seg, uso de CPU/memória) para ferramentas como Prometheus/Grafana (helpers em `app/core/monitoring/metrics.py`).
        *   **Aplicação:** Logging detalhado em `app/features/stock_prediction/service.py` para rastrear requisições e possíveis erros.
        *   **Modelo:** (Mais avançado) Processos adicionais (talvez em `ml_lifecycle` ou um novo diretório `monitoring`) poderiam periodicamente reavaliar o modelo em produção contra dados novos para detectar drift ou queda de performance, logando resultados no BD.

## Conclusão Ajustada

Esta estrutura híbrida ajustada fornece diretórios dedicados para os principais estágios do seu projeto (pipeline de dados, ciclo de vida do ML, API), promovendo separação de interesses de alto nível. Dentro da API (`app/`), a organização por funcionalidade (`features/stock_prediction/`) permite o desenvolvimento paralelo e mantém a coesão funcional. Os componentes compartilhados (`core`, `models`, `schemas`) garantem consistência. Essa abordagem mapeia diretamente seus critérios, oferecendo uma base sólida, escalável e manutenível para o projeto de previsão de ações com LSTM.

