import json

import pytest
from mcp.server.mcpserver.exceptions import ToolError

import server

SAMPLE_TICKETS = [
    {"id": 1, "title": "Bug A", "status": "open", "priority": "high", "description": "...", "comments": []},
    {"id": 2, "title": "Bug B", "status": "closed", "priority": "low", "description": "...", "comments": []},
]


@pytest.fixture(autouse=True)
def tickets_file(tmp_path, monkeypatch):
    path = tmp_path / "tickets.json"
    path.write_text(json.dumps(SAMPLE_TICKETS), encoding="utf-8")
    monkeypatch.setattr(server, "TICKETS_FILE", path)
    return path


def test_list_tickets_filters_by_status():
    assert [t["id"] for t in server.list_tickets("open")] == [1]
    assert [t["id"] for t in server.list_tickets("closed")] == [2]


def test_get_ticket_returns_full_ticket():
    assert server.get_ticket(1)["title"] == "Bug A"


def test_get_ticket_unknown_id_raises_tool_error():
    with pytest.raises(ToolError, match="Ticket 99 introuvable"):
        server.get_ticket(99)


def test_add_comment_is_saved(tickets_file):
    server.add_comment(1, "Piste de correction")
    saved = json.loads(tickets_file.read_text(encoding="utf-8"))
    assert saved[0]["comments"] == ["Piste de correction"]
