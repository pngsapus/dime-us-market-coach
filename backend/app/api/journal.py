from datetime import datetime, timezone

from fastapi import APIRouter

from app.schemas.contracts import JournalEntry, JournalEntryCreate

router = APIRouter(tags=["journal"])
_journal: list[JournalEntry] = []


@router.get("/journal", response_model=list[JournalEntry])
def list_journal() -> list[JournalEntry]:
    return _journal


@router.post("/journal", response_model=JournalEntry)
def create_journal(entry: JournalEntryCreate) -> JournalEntry:
    saved = JournalEntry(id=len(_journal) + 1, created_at=datetime.now(timezone.utc), **entry.model_dump())
    _journal.append(saved)
    return saved
