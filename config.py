import os
from dotenv import load_dotenv

load_dotenv()

# ── API Keys ───────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY      = os.getenv("GROQ_API_KEY", "")

# ── Models available ───────────────────────────────────────────────────────────
# Primary models for benchmarking
MODEL_CLAUDE   = "claude-sonnet-4-6"
MODEL_GPT_MINI = "gpt-4o-mini"
MODEL_LLAMA    = "llama3-70b-8192"   # via Groq free tier

DEFAULT_MODEL  = MODEL_GPT_MINI

# ── Generation settings ────────────────────────────────────────────────────────
MAX_TOKENS              = 4000
TEMPERATURE_REASONING   = 0.3   # Stage 1 and Stage 2 — structured reasoning
TEMPERATURE_GENERATION  = 0.5   # Stage 3 — artifact generation
TEMPERATURE_VERIFY      = 0.2   # Verification — strict checking

# ── Verification loop ──────────────────────────────────────────────────────────
MAX_VERIFICATION_ITERATIONS = 2

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR   = os.path.join(BASE_DIR, "prompts")
OUTPUTS_DIR   = os.path.join(BASE_DIR, "outputs")
MATERIALS_DIR = os.path.join(BASE_DIR, "materials")