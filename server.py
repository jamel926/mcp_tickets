"""Serveur MCP qui donne à un agent IA l'accès à une liste de tickets."""

import json
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

TICKETS_FILE = Path(__file__).parent / "tickets.json"

mcp = MCPServer("tickets")


def load_tickets() -> list[dict]:
    return json.loads(TICKETS_FILE.read_text(encoding="utf-8"))


def save_tickets(tickets: list[dict]) -> None:
    TICKETS_FILE.write_text(json.dumps(tickets, ensure_ascii=False, indent=2), encoding="utf-8")


def find_ticket(tickets: list[dict], ticket_id: int) -> dict:
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    raise ToolError(f"Ticket {ticket_id} introuvable")


@mcp.tool()
def list_tickets(status: str = "open") -> list[dict]:
    """Liste les tickets filtrés par statut ("open" ou "closed"), avec id, titre et priorité."""
    return [
        {"id": t["id"], "title": t["title"], "priority": t["priority"]}
        for t in load_tickets()
        if t["status"] == status
    ]


@mcp.tool()
def get_ticket(ticket_id: int) -> dict:
    """Renvoie le détail complet d'un ticket : description, statut, priorité et commentaires."""
    return find_ticket(load_tickets(), ticket_id)


@mcp.tool()
def add_comment(ticket_id: int, text: str) -> dict:
    """Ajoute un commentaire à un ticket et renvoie le ticket mis à jour."""
    tickets = load_tickets()
    ticket = find_ticket(tickets, ticket_id)
    ticket["comments"].append(text)
    save_tickets(tickets)
    return ticket


if __name__ == "__main__":
    mcp.run()
