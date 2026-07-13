"""
Lesson Generation Agent — Stage 3 of Workflow B.

Generates the final teaching artifact.
No ReAct loop.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm import call_llm
from utils.prompt_loader import load_prompt
import config


def run_lesson_agent(
    teaching_material: str,
    stage1_output: str,
    stage2_output: str,
    lecturer_request: str,
    model: str = config.DEFAULT_MODEL,
) -> dict:

    print("  [Lesson Generation Agent] Generating final artifact...")

    system_prompt = load_prompt("lesson_agent")

    user_content = f"""Teaching material:

{teaching_material}


Curriculum Design Agent Output:

{stage1_output}


Assessment Design Agent Output:

{stage2_output}


Lecturer Request:

{lecturer_request}


Generate the final teaching artifact.
"""

    raw_response = call_llm(
        system_prompt=system_prompt,
        user_content=user_content,
        model=model,
        temperature=config.TEMPERATURE_GENERATION,
    )

    print("  [Lesson Generation Agent] Done.")

    return {
        "agent": "Lesson",
        "success": True,
        "reasoning_trace": "",
        "structured_output": raw_response.strip(),
        "raw_response": raw_response,
        "error": None,
    }