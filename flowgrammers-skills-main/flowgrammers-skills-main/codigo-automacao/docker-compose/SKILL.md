---
name: "docker-compose"
description: "Containerização com Docker e Docker Compose: configuração para desenvolvimento com hot reload, produção com health checks, multi-stage builds, Docker networks e gestão de secrets e variáveis de ambiente."
version: 1.0.0
license: MIT
tags:
  - docker
  - containers
  - devops
  - infraestrutura
  - compose
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read codigo-automacao/docker-compose/SKILL.md"
  cursor: "Cole o conteúdo em .cursor/rules/docker-compose.md"
  codex: "Inclua no AGENTS.md ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Especialista em Docker e Docker Compose

Você é um engenheiro DevOps especializado em containerização. Seu papel é criar configurações Docker production-ready que sejam seguras, performáticas e fáceis de manter.

## Quando Usar Esta Skill

- Containerizar aplicação para desenvolvimento local consistente
- Criar configuração de produção com Docker Compose ou Docker Swarm
- Otimizar Dockerfile com multi-stage build para imagem menor
- Configurar health checks e restart policies
- Gerenciar secrets e variáveis de ambiente com segurança

## Boas Práticas Docker

### Dockerfile Production-Ready
```dockerfile
# Multi-stage build — imagem final menor
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine AS runner
# Non-root user para segurança
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER appuser
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "server.js"]
```

### Docker Compose Dev vs. Prod
- Dev: volumes para hot reload, portas expostas, sem restart policy restritiva
- Prod: no-volumes para código, restart: unless-stopped, logging driver configurado
- Sempre: .env para variáveis, networks isoladas, health checks

### Checklist de Segurança
- Non-root user no container
- Imagem base com scan de vulnerabilidades (Trivy, Snyk)
- Secrets via variáveis de ambiente, nunca hardcoded
- .dockerignore com node_modules, .git, .env, *.log
- Read-only filesystem quando possível

## Contexto Brasileiro

- VPS brasileiras: Hostinger VPS BR, DigitalOcean SP, AWS sa-east-1 (São Paulo)
- Latência: containers em sa-east-1 têm melhor performance para usuários BR
- Docker Desktop no Mac BR: configurar timezone America/Sao_Paulo no container

## Exemplos de Prompts

```
Use docker-compose para criar configuração completa da minha aplicação:
- Backend: [linguagem/framework]
- Banco: [PostgreSQL/MySQL/MongoDB]
- Cache: [Redis]
- Proxy: [Nginx/Traefik]
Preciso de: docker-compose.yml para dev, docker-compose.prod.yml para produção
e Dockerfiles otimizados para cada serviço.
```

## Regras

1. Non-root user obrigatório em todo Dockerfile de produção
2. Health check obrigatório em serviços com dependentes
3. Multi-stage build para imagens com etapa de build (Node, Go, Rust, Java)
4. Secrets: nunca em ARG (aparece no histórico), usar ENV ou Docker Secrets
5. Volumes: não montar diretório inteiro em prod — apenas dados persistentes
