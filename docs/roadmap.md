# 🧭 MU Forge — Roadmap Oficial

Este documento descreve todas as etapas de desenvolvimento do MU Forge, desde a estrutura inicial até o lançamento da versão 1.0 com frontend web.

---

# 📌 FASE 1 — FUNDAMENTOS (Núcleo em Python)

## 1. Estrutura inicial do projeto
- Criar pastas: `src/`, `src/core/`, `src/data/`
- Criar arquivos vazios necessários (`.py` e `.json`)
- Criar `.gitignore`
- Criar este `roadmap.md`

---

## 2. Modelo de dados do MU Online
Criar arquivos JSON em `src/data/`:

### Itens
---> v1.0
- weapons.json
- armors.json
- sets.json
- accessories.json
- wings.json
- pentagrams.json
- others.json

---> v1.2
- Errtels
- Artifacts

### Estrutura típica de item
```json
{
  "id": "word",
  "name": "Sword",
  "class_restriction": ["dark-knight"],
  "requirements": {
    "strength": 450,
    "agility": 150
  },
  "stats": {
    "attack_min": 110,
    "attack_max": 125,
    "speed": 40
  },
  "excellent_options": [],
  "socket_options": [],
  "bonuses": []
}
```

### Classes
Criar `classes.json` com:
---> v1.0
- Dark Knight
- Dark Wizard
- Fairy Elf
- Magic Gladiator
- Dark Lord

---> v1.2
- Summoner
- Rage Fighter 
- Grow Lancer
- Rune Wizard
- Slayer

---> v1.3
- Gun Crusher
- White Wizard: Kundun Mephis
- Meiji: Lemuria
- Illusion Knight: Jacquard
- Alchemist
- Crusader Paladin

### Tipos de build
- early_game
- mid_game
- end_game
- pve
- pvp
- support

---

## 3. Núcleo lógico (Core Engine)

### loader.py
- Carregar JSON
- Validar estrutura
- Cache em memória

### calculator.py
- Calcular DPS
- Calcular Defesa Efetiva
- Calcular velocidade de ataque
- Score geral do item
- Score por tipo de build

### optimizer.py
- Encontrar melhor combinação:
  - máximo DPS  
  - máxima defesa  
  - melhor custo-benefício  
  - melhor para PvE/PvP 
  - melhores skills/skill tree
- Aplicar restrições de classe e requisitos

### validator.py
- Validar builds
- Validar requisitos
- Impedir combinações incompatíveis

---

## 4. Interface CLI (modo offline)
Arquivo: `src/main.py`

Funcionalidades:
- escolher classe
- escolher tipo de build
- gerar build recomendada
- mostrar estatísticas totais
- salvar build em JSON

---

# 📌 FASE 2 — SISTEMA COMPLETO EM PYTHON

## 5. Sistema de Builds específicas
Pasta: `src/builds/`

Criar:
- `wizard.py`
- `knight.py`
- `elf.py`
- etc

Cada módulo deve:
- definir prioridades da classe
- definir estilo de jogo
- definir melhores itens por fase (early/mid/end)
- integrar com o optimizer

---

## 6. Ferramentas complementares (v1.2)
- Comparar duas builds  
- Exportar/importar builds  
- Calcular efeito de trocar item  
- Mostrar impacto por atributo  

---

## 7. Testes (pytest)
Criar pasta `tests/` com:
- test_loader.py  
- test_calculator.py  
- test_optimizer.py  
- test_builds.py  

---

# 📌 FASE 3 — API (Back-End)

## 8. API com FastAPI
Criar pasta `api/`

Endpoints:

### GET /items
Lista todos os itens

### GET /classes
Lista classes e atributos

### POST /optimize
Entrada:
```json
{
  "class": "dark-wizard",
  "build": "pve",
  "level": 400,
  "stats": {"str": 30, "agi": 60, "vit": 100, "ene": 500},
  "budget": null
}
```

Retorno:
- Melhores arma  
- Melhores set  
- Melhor combinação  
- Score final  

### POST /compare (v1.2)
Comparar 2 builds

---

## 9. Persistência
Começar simples:
- JSON local  
- ou TinyDB  

Migrar depois para:
- SQLite

---

# 📌 FASE 4 — WEB (Frontend + Integração)

## 10. Versão simples (Jinja2 + FastAPI)
Páginas:
- home (selecionar classe + build)
- resultados
- comparação
- exportação da build

---

## 11. Versão moderna (opcional)
Fazer upgrade para:
- React  
- Next.js  
- Vue  
- Svelte  

Apenas no futuro.

---

# 📌 FASE 5 — PUBLICAÇÃO

## 12. Preparar ambiente
- Ajustar caminhos
- Corrigir imports
- Criar build da API
- Dockerfile simples (opcional)

---

## 13. Hospedar
Opções recomendadas:
- Render  
- Railway  
- Deta Space  
- Fly.io  

---

# 📌 FASE 6 — FINALIZAÇÃO

## 14. Criar README profissional
Somente aqui, quando tudo estiver funcional.

## 15. Criar documentação completa
Na pasta `/docs/`:
- arquitetura
- modelo de dados
- exemplos de API
- performance
- changelog

## 16. Lançamento da versão 1.0
Tags:
- `v0.1` — Core funcional
- `v0.2` — Optimizer pronto
- `v0.3` — API funcionando
- `v1.0` — Web completa
