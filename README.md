# mcp-tickets

Serveur MCP (Model Context Protocol) en Python qui donne à un agent IA de développement (Claude Code, Gemini CLI) l'accès à une liste de tickets : il peut les lister, les lire et les commenter.

## Outils exposés

| Outil | Rôle |
|---|---|
| `list_tickets(status)` | Liste les tickets `open` ou `closed` (id, titre, priorité) |
| `get_ticket(ticket_id)` | Renvoie le détail d'un ticket, avec ses commentaires |
| `add_comment(ticket_id, text)` | Ajoute un commentaire et l'enregistre |

Un identifiant inconnu renvoie une erreur explicite à l'agent (`Ticket 99 introuvable`), pour qu'il puisse corriger sa demande.

## Installation

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Brancher sur un agent

**Claude Code**

```bash
claude mcp add tickets -- /chemin/vers/.venv/bin/python /chemin/vers/server.py
```

**Gemini CLI** : dans `.gemini/settings.json`

```json
{
  "mcpServers": {
    "tickets": {
      "command": "/chemin/vers/.venv/bin/python",
      "args": ["/chemin/vers/server.py"]
    }
  }
}
```

## Tests et CI

```bash
.venv/bin/python -m pytest
```

Le workflow GitHub Actions (`.github/workflows/ci.yml`) lance un lint (ruff) puis les tests à chaque push et à chaque pull request. Le fichier `.gitlab-ci.yml` décrit le même pipeline pour GitLab CI (image `python:3.12-slim`).

## Suite prévue

- Remplacer `tickets.json` par l'API GitLab Issues.
- Ajouter des traces OpenTelemetry pour mesurer la latence de chaque appel d'outil.
