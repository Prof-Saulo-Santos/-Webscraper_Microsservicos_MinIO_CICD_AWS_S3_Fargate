![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Docker](https://img.shields.io/badge/docker-available-blue.svg)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![MinIO](https://img.shields.io/badge/MinIO-local--only-C72E49?style=flat&logo=minio&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat&logo=amazon-aws&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=flat&logo=poetry&logoColor=white)
![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![Bump2Version](https://img.shields.io/badge/bump2version-semantic-ff69b4?style=flat)

# MBA: Machine Learning in Production — ITI | UFSCar

## Projeto  
## Arquitetura de Microsserviços para Ingestão, Processamento e Busca Semântica  
## de Artigos Científicos (arXiv) utilizando Arquitetura Medalhão (Bronze/Silver)

Projeto acadêmico focado na aplicação prática de **boas práticas de Engenharia de Software, Data Engineering, Docker, CI/CD e Cloud AWS**, com evolução progressiva de um ambiente local para uma infraestrutura em nuvem moderna, observável e financeiramente eficiente.

---

## 🧠 Visão Geral da Arquitetura

Este projeto implementa uma **arquitetura de microsserviços orientada a eventos** para ingestão, processamento e consulta semântica de artigos científicos do repositório **arXiv**.

A solução segue o padrão de **Arquitetura Medalhão**, organizando os dados em camadas:

- **Bronze:** dados brutos ingeridos
- **Silver:** dados limpos, enriquecidos e prontos para consulta

O projeto evolui em fases:
- **Fases 1 a 3:** ambiente local com Docker, simulando serviços cloud (MinIO como S3 local)
- **Fase 4:** migração para AWS utilizando Infraestrutura como Código (Terraform)
- **Fase 5:** observabilidade, monitoramento e controle de custos (FinOps)

A arquitetura prioriza:
- Separação de responsabilidades
- Automação
- Segurança por padrão (least privilege)
- Eficiência de custos
- Reprodutibilidade

---

## 🏗️ Estrutura do Projeto (Monorepo)

O projeto está organizado em um **monorepo**, dividido em fases independentes, cada uma com responsabilidade clara e documentação própria.

- 🔴 Atenção: Se o seu objetivo é avaliar o projeto sob a perspectiva de sua implantação local usando MinIO, faça a clonagem do projeto até a fase 3 (processing_service), pois na fase 4, os arquivos de configuração (ajustados para minIO) foram sobrescritos por aquilo que foi ajustado para AWS.

### 🟢 Fase 1 — Ingestion Service  
📁 [`./ingestion_service`](./ingestion_service)

- **Clone isolado (Fase 1):** Para estudar apenas esta fase:
  ```bash
  # Clona e vai direto para o ponto no tempo onde a Fase 1 foi finalizada
  git clone --branch v0.1.0 https://github.com/Prof-Saulo-Santos/Webscraper_Microsservicos_MinIO_CICD_AWS_S3_Fargate arxiv
  ```
  - **Leia:** `ingestion_service/README.md`
  - **Nota:** Neste ponto da história, as pastas `processing_service` e `frontend_service` ainda não existiam ou estavam vazias.

- **Recriação do Zero:** Siga o guia [`passo_a_passo_fase_1.md`](docs/passo_a_passo_fase_1.md) para recriar todas as etapas desta fase manualmente.
- **Responsabilidade:** Coleta de dados (scraping) e persistência bruta (camada Bronze)
- **Status:** ✅ Implementado e Testado localmente
- **Tecnologias:** Python, FastAPI, Docker, MinIO (simulação local do S3)
- **Versionamento:** v0.1.0
- **Testes:**
  ```bash
  make test ou poetry run pytest tests/ -v
  ``` 
- **Execução:**
  ```bash
  make run ou docker compose up --build -d
  ```
- **Acesse:**  
  ```bash
  http://localhost:8000/docs para fazer ingestão de dados em bronze minIO
  http://localhost:9000 para acessar o console do minIO  
  Login: minioadmin / Senha: minioadmin 
  ```   

- 🔴 **Antes de iniciar a fase 2, é obrigatório parar a fase 1 para evitar conflito de portas:**
  ```bash
  docker compose down
  ```

### 🟢 Fase 2 — Processing Service  
📁 [`./processing_service`](./processing_service)

- **Clone isolado (Fase 2):** Para estudar apenas as fases 1 e 2:
  ```bash
  git clone --branch v0.2.0 https://github.com/Prof-Saulo-Santos/Webscraper_Microsservicos_MinIO_CICD_AWS_S3_Fargate arxiv
  ```
  - **Leia:** `processing_service/README.md`

- **Recriação do Zero:** Siga o guia [`passo_a_passo_fase_2.md`](docs/passo_a_passo_fase_2.md) para recriar todas as etapas desta fase manualmente.
- **Responsabilidade:** Limpeza de dados, geração de embeddings e persistência refinada (camada Silver)
- **Status:** ✅ Implementado e Testado localmente
- **Tecnologias:** Python, Pandas/Polars, BERT/Transformers, VectorDB
- **Versionamento:** v0.2.0
- **Testes:**
  ```bash
  cd processing_service
  make test ou poetry run pytest tests/ -v
  ```
- **Execução:**
  ```bash
  cd processing_service
  make run ou docker compose up --build -d
  ```
- **Acesse:**
  ```bash
  http://localhost:8001/docs para acessar a API de Processamento (Swagger)
  http://localhost:9000 para acessar o console do minIO (Login: minioadmin / Senha: minioadmin)
  ```

### 🟢 Fase 3 — Frontend Service
📁 [`./frontend_service`](./frontend_service)

- **Clone isolado (Fase 3):** Para estudar apenas as fases 1, 2 e 3:
  ```bash
  git clone --branch v0.3.0 https://github.com/Prof-Saulo-Santos/Webscraper_Microsservicos_MinIO_CICD_AWS_S3_Fargate arxiv
  ```
  - **Leia:** `frontend_service/README.md`

- **Recriação do Zero:** Siga o guia [`passo_a_passo_fase_3.md`](docs/passo_a_passo_fase_3.md) para recriar todas as etapas desta fase manualmente.
- **Responsabilidade:** Interface do usuário para busca e visualização dos artigos
- **Status:** ✅ Implementado e Testado localmente
- **Tecnologias:** Streamlit
- **Versionamento:** v0.3.0
- **Testes:**
  ```bash
  cd frontend_service
  make test ou poetry run pytest tests/ -v
  ```
- **Execução:**
  ```bash
  cd frontend_service
  make run ou docker compose up --build -d
  ```
- **Acesse:**
  ```bash
  http://localhost:8501 (Interface Web Streamlit)
  http://localhost:9000 (Console MinIO)
  ```
- **📸 Screenshot — Busca Semântica**
  ![Demo](docs/img/semantic_search_demo.jpg)

- 🔴 **Nota:** A Fase 3 **necessita** do MinIO rodando (que é fornecido pela Fase 1 ou Fase 2).
  - **Não há conflito de portas** entre Fase 2 (8001) e Fase 3 (8501). Você pode rodar ambas juntas.
  - **Atenção à Memória:** Se tiver pouca RAM, você pode parar a Fase 2 (`docker stop processing_service`) mas **deixe o container do MinIO rodando**, ou suba apenas a Fase 1 (que é mais leve) para fornecer o MinIO.


### 🟢 Fase 4 — AWS Infrastructure (IaC com Terraform)
📁 [`./aws_infrastructure`](./aws_infrastructure)

- **Clone isolado (Fase 4):** Para estudar todas as fases anteriores a esta fase:
- 🔴 Atenção: Se o seu objetivo é avaliar o projeto sob a perspectiva de sua implantação na nuvem AWS, faça a clonagem do projeto inteiro (use este git clone), pois os seguintes arquivos de configuração (ajustados para minIO) serão sobrescritos por aquilo que foi ajustado para AWS: 

- 📂 Ingestion Service
- ingestion_service/README.md
  - ingestion_service/app/core/config.py
  - ingestion_service/app/main.py
  - ingestion_service/app/scrapers/arxiv_scraper.py
  - ingestion_service/docker-compose.yml
  - ingestion_service/poetry.lock
- 📂 Processing Service
  - processing_service/README.md
  - processing_service/Makefile
  - processing_service/app/core/config.py
  - processing_service/app/main.py
  - processing_service/docker-compose.yml
- 📂 Frontend Service
  - frontend_service/app/core/config.py
  - frontend_service/app/main.py  
  ```bash
  git clone --branch v0.4.0 https://github.com/Prof-Saulo-Santos/Webscraper_Microsservicos_MinIO_CICD_AWS_S3_Fargate
  ```
  - **Leia:** `aws_infrastructure/README.md`

- **Recriação do Zero:** Siga o guia [`passo_a_passo_fase_4.md`](docs/passo_a_passo_fase_4.md) para recriar todas as etapas desta fase manualmente.
- **Responsabilidade:** Provisionamento da infraestrutura em nuvem
- **Status:** ✅ Implementado e Validado (IaC + Deploy funcional)
- **Tecnologias:** AWS ECS Fargate, S3, ECR, EventBridge, IAM, Terraform
- **Versionamento:** v0.4.0
- **Testes (Validação IaC):**
  ```bash
  cd aws_infrastructure
  terraform init
  terraform validate
  ```
- **Execução (Provisionamento):**
  ```bash
  cd aws_infrastructure
  terraform plan
  terraform apply
  ```
- **Acesse:**
  - AWS Console (ECS, S3, CloudWatch)
  - URL do Load Balancer (após deploy)

- **Destaques:**
    - Tasks batch agendadas
    - Uso de Fargate Spot (FinOps)
    - Data Lake em S3 (Bronze/Silver)
    - IAM com princípio do menor privilégio

### 🟢 Fase 5 — Observabilidade, Monitoramento e FinOps
📁 *Integrada à Fase 4*

- **Responsabilidade:** Monitoramento, auditoria e controle de custos
- **Tecnologias:** CloudWatch Logs & Metrics, EventBridge Events, AWS Budgets
- **Destaques:**
    - Logs centralizados
    - Alarmes de falha de tasks
    - Orçamento mensal protegido
    - Governança mínima e profissional

---


## 🏛️ Decisões Arquiteturais

1.  **Arquitetura Medalhão** para rastreabilidade e qualidade dos dados
2.  **Microsserviços** para isolamento de responsabilidades
3.  **Containers** para portabilidade e padronização
4.  **Evolução planejada** de ambiente local para cloud
5.  **Workloads batch e agendados** visando eficiência de custos (FinOps)
6.  **Infraestrutura como Código** para reprodutibilidade

---

## 🎓 Escopo Acadêmico

Este projeto foi desenvolvido com fins acadêmicos no contexto do **MBA em Machine Learning in Production**, priorizando:
- Boas práticas de arquitetura
- Observabilidade
- Segurança
- Controle de custos

Aspectos como alta disponibilidade global e escalabilidade massiva não fazem parte do escopo, mas a arquitetura é compatível com tais evoluções.

---

## 📝 Autor

**Saulo Santos**

- GitHub: [https://github.com/Prof-Saulo-Santos](https://github.com/Prof-Saulo-Santos)
- LinkedIn: [https://www.linkedin.com/in/santossaulo/](https://www.linkedin.com/in/santossaulo/)