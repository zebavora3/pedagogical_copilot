"""
Curriculum Design Agent — Stage 1 of Workflow B.

Applies Backward Design Stage 1 (Desired Results) using a ReAct reasoning loop.
Returns the full reasoning trace and the structured output block.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm import call_llm
from utils.prompt_loader import load_prompt
import config


def run_curriculum_agent(
    teaching_material: str,
    model: str = config.DEFAULT_MODEL
) -> dict:
    """
    Run the Curriculum Design Agent.
    """

    print("  [Curriculum Agent] Starting Stage 1 reasoning loop...")

    system_prompt = load_prompt("curriculum_agent")

    user_content = f"""Teaching material:

{teaching_material}

Begin your Thought → Action → Observation reasoning now.
Work through as many cycles as needed.
Call FINALISE() only when all criteria are satisfied.
"""

    raw_response = call_llm(
        system_prompt=system_prompt,
        user_content=user_content,
        model=model,
        temperature=config.TEMPERATURE_REASONING,
    )

    result = _parse_response(raw_response)

    print(f"  [Curriculum Agent] Done. Success: {result['success']}")

    return result


def _parse_response(raw_response: str) -> dict:
    """
    Split the model response into:
        - reasoning trace
        - structured output
    """

    start = "---CURRICULUM AGENT OUTPUT---"
    end = "---END CURRICULUM AGENT OUTPUT---"

    if start not in raw_response:
        return {
            "agent": "Curriculum",
            "success": False,
            "reasoning_trace": raw_response,
            "structured_output": "",
            "raw_response": raw_response,
            "error": "Output delimiter not found."
        }

    reasoning_trace, remainder = raw_response.split(start, 1)

    if end in remainder:
        structured_output = remainder.split(end, 1)[0].strip()
    else:
        structured_output = remainder.strip()

    return {
        "agent": "Curriculum",
        "success": True,
        "reasoning_trace": reasoning_trace.strip(),
        "structured_output": structured_output,
        "raw_response": raw_response,
        "error": None
    }