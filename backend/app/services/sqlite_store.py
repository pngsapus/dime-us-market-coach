from datetime import datetime, timezone
import os
from pathlib import Path
import sqlite3

from app.schemas.contracts import JournalEntry, JournalEntryCreate, RiskProfile


def default_database_path() -> Path:
    backend_dir = Path(__file__).resolve().parents[2]
    return backend_dir / "data" / "app.db"


def get_database_path() -> Path:
    configured = os.getenv("DIME_DB_PATH")
    return Path(configured) if configured else default_database_path()


class SQLiteStore:
    def __init__(self, database_path: Path | None = None) -> None:
        self.database_path = database_path or get_database_path()

    def _connect(self) -> sqlite3.Connection:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def init_schema(self) -> None:
        connection = self._connect()
        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS risk_profile (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    beginner_level TEXT NOT NULL,
                    max_loss_per_trade_thb REAL NOT NULL,
                    max_trades_per_day INTEGER NOT NULL,
                    minimum_risk_reward REAL NOT NULL,
                    preferred_setup_type TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS journal_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    reason TEXT NOT NULL DEFAULT '',
                    result TEXT NOT NULL DEFAULT '',
                    lesson_learned TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.commit()
        finally:
            connection.close()

    def get_risk_profile(self) -> RiskProfile:
        self.init_schema()
        connection = self._connect()
        try:
            row = connection.execute(
                """
                SELECT beginner_level, max_loss_per_trade_thb, max_trades_per_day,
                       minimum_risk_reward, preferred_setup_type
                FROM risk_profile
                WHERE id = 1
                """
            ).fetchone()
        finally:
            connection.close()
        if row is None:
            return RiskProfile()
        return RiskProfile(**dict(row))

    def save_risk_profile(self, profile: RiskProfile) -> RiskProfile:
        self.init_schema()
        connection = self._connect()
        try:
            connection.execute(
                """
                INSERT INTO risk_profile (
                    id, beginner_level, max_loss_per_trade_thb, max_trades_per_day,
                    minimum_risk_reward, preferred_setup_type, updated_at
                )
                VALUES (1, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    beginner_level = excluded.beginner_level,
                    max_loss_per_trade_thb = excluded.max_loss_per_trade_thb,
                    max_trades_per_day = excluded.max_trades_per_day,
                    minimum_risk_reward = excluded.minimum_risk_reward,
                    preferred_setup_type = excluded.preferred_setup_type,
                    updated_at = excluded.updated_at
                """,
                (
                    profile.beginner_level,
                    profile.max_loss_per_trade_thb,
                    profile.max_trades_per_day,
                    profile.minimum_risk_reward,
                    profile.preferred_setup_type,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            connection.commit()
        finally:
            connection.close()
        return profile

    def list_journal_entries(self) -> list[JournalEntry]:
        self.init_schema()
        connection = self._connect()
        try:
            rows = connection.execute(
                """
                SELECT id, symbol, decision, reason, result, lesson_learned, created_at
                FROM journal_entries
                ORDER BY datetime(created_at) DESC, id DESC
                """
            ).fetchall()
        finally:
            connection.close()
        return [JournalEntry(**dict(row)) for row in rows]

    def create_journal_entry(self, entry: JournalEntryCreate) -> JournalEntry:
        self.init_schema()
        created_at = datetime.now(timezone.utc).isoformat()
        connection = self._connect()
        try:
            cursor = connection.execute(
                """
                INSERT INTO journal_entries (symbol, decision, reason, result, lesson_learned, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    entry.symbol,
                    entry.decision,
                    entry.reason,
                    entry.result,
                    entry.lesson_learned,
                    created_at,
                ),
            )
            entry_id = int(cursor.lastrowid)
            connection.commit()
        finally:
            connection.close()
        return JournalEntry(id=entry_id, created_at=created_at, **entry.model_dump())


store = SQLiteStore()
