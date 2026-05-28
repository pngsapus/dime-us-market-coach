from fastapi import APIRouter

from app.schemas.contracts import JournalEntry, JournalEntryCreate
from app.services.sqlite_store import store

router = APIRouter(tags=["journal"])


@router.get("/journal", response_model=list[JournalEntry])
def list_journal() -> list[JournalEntry]:
    return store.list_journal_entries()


@router.post("/journal", response_model=JournalEntry)
def create_journal(entry: JournalEntryCreate) -> JournalEntry:
    return store.create_journal_entry(entry)
