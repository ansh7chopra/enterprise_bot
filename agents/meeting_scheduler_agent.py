# agents/meeting_scheduler_agent.py
import os, uuid, sqlite3, datetime as dt
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field
from ics import Calendar, Event
# from langchain_core.tools import tool

DB_FILE = Path("calendar.db")      # SQLite file
ICS_DIR = Path("invites")          # where .ics files are saved
JOIN_ROOT = "https://meet.demo.ai" # mock join‑link root

# ---------- SQLite init -----------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id TEXT PRIMARY KEY,
            title TEXT,
            start_iso TEXT,
            end_iso TEXT,
            participants TEXT,
            created_at TEXT
        )
    """)
    conn.commit(); conn.close()

# ---------- Pydantic schema (for LangChain tool) ---------------------------
class MeetingRequest(BaseModel):
    title: str = Field(..., description="Meeting subject/title")
    date: str = Field(..., pattern=r"\d{4}-\d{2}-\d{2}", description="Date in YYYY-MM-DD format")
    time: str = Field(..., pattern=r"\d{2}:\d{2}", description="Time in HH:MM 24hr format")
    duration: int = Field(..., description="Duration in minutes")
    participants: List[str] = Field(..., description="List of email addresses")


# ---------- The actual tool -------------------------------------------------
# @tool
def schedule_meeting_tool(req: MeetingRequest) -> str:
    """Store meeting in SQLite, create .ics, and return confirmation string."""
    init_db()

    start = dt.datetime.fromisoformat(f"{req.date}T{req.time}:00")
    end   = start + dt.timedelta(minutes=req.duration)
    mid   = str(uuid.uuid4())

    # 1) write to SQLite
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO meetings VALUES (?,?,?,?,?,?)",
        (
            mid,
            req.title,
            start.isoformat(),
            end.isoformat(),
            ",".join(req.participants),
            dt.datetime.utcnow().isoformat()
        )
    )
    conn.commit(); conn.close()

    # 2) generate .ics file
    c = Calendar(); e = Event()
    e.name  = req.title
    e.begin = start
    e.end   = end
    e.organizer = "mailto:nexa@demo.ai"
    e.attendees = req.participants
    join_url = f"{JOIN_ROOT}/{mid}"
    e.url   = join_url
    c.events.add(e)

    ICS_DIR.mkdir(exist_ok=True)
    ics_path = ICS_DIR / f"{mid}.ics"
    ics_path.write_text(str(c))

    # 3) return a markdown summary
    return (
        f"📅 **{req.title}** scheduled on {start:%d %b %Y %H:%M} "
        f"for {req.duration} min with {', '.join(req.participants)}.\n\n"
        f"🔗 Join link: {join_url}\n"
        f"📎 [Download invite]({ics_path})"
    )

# ---------- Wrap as LangChain StructuredTool -------------------------------
from langchain.tools import StructuredTool

# end of file …
meeting_tool = StructuredTool.from_function(
    func=schedule_meeting_tool,
    name="schedule_meeting",
    description="Schedule a meeting when the user explicitly asks.",
    args_schema=MeetingRequest,
    return_direct=True,
)


