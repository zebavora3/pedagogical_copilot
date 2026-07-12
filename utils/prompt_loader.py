"""
Loads agent prompts from the prompts/ directory.
"""

import os
import config


def load_prompt(agent_name: str) -> str:
    """
    Load a prompt markdown file from the prompts/ folder.

    Usage:
        system_prompt = load_prompt("curriculum_agent")
    """
    path = os.path.join(config.PROMPTS_DIR, f"{agent_name}.md")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()