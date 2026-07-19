# Constants

from pathlib import Path


# =========================
# Project
# =========================

APP_AUTHOR = "Karan Sharma"
APP_DESCRIPTION = "JARVIS Personal AI Assistant"


# =========================
# Directories
# =========================

ROOT_DIR = Path.cwd()

DATA_DIR = ROOT_DIR / "data"

LOG_DIR = ROOT_DIR / "logs"

MODEL_DIR = ROOT_DIR / "models"

UPLOAD_DIR = DATA_DIR / "uploads"

DOCUMENT_DIR = DATA_DIR / "documents"

VECTOR_DB_DIR = DATA_DIR / "vector_db"

MEMORY_DIR = DATA_DIR / "memory"

CACHE_DIR = DATA_DIR / "cache"


# =========================
# Supported LLM Providers
# =========================

OLLAMA = "ollama"

GEMINI = "gemini"

GROQ = "groq"

OPENAI = "openai"


SUPPORTED_PROVIDERS = (
    OLLAMA,
    GEMINI,
    GROQ,
    OPENAI,
)


# =========================
# Agent Names
# =========================

CODING_AGENT = "coding"

RESEARCH_AGENT = "research"

STUDY_AGENT = "study"

INTERVIEW_AGENT = "interview"

FILE_AGENT = "file"

AUTOMATION_AGENT = "automation"

BROWSER_AGENT = "browser"

PLANNER_AGENT = "planner"


# =========================
# File Types
# =========================

PDF = ".pdf"

DOCX = ".docx"

TXT = ".txt"

CSV = ".csv"

XLSX = ".xlsx"

PPTX = ".pptx"

PNG = ".png"

JPG = ".jpg"

JPEG = ".jpeg"


SUPPORTED_DOCUMENTS = (
    PDF,
    DOCX,
    TXT,
)

SUPPORTED_IMAGES = (
    PNG,
    JPG,
    JPEG,
)


# =========================
# Exit Commands
# =========================

EXIT_COMMANDS = (
    "exit",
    "quit",
    "bye",
    "goodbye",
)


# =========================
# Greetings
# =========================

WAKE_WORD = "jarvis"