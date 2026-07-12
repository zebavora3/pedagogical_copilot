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


def run_curriculum_agent(teaching_material: str, model: str = config.DEFAULT_MODEL) -> dict:
    """
    Run the Curriculum Design Agent.

    Returns a dict with:
        reasoning_trace  — the full Thought/Action/Observation chain
        structured_output — everything between the output delimiters
        success          — True if FINALISE was called and output was parsed
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
    Split the response into reasoning trace and structured output.
    Looks for the ---CURRICULUM AGENT OUTPUT--- delimiter.
    """
    delimiter_start = "---CURRICULUM AGENT OUTPUT---"
    delimiter_end   = "---END CURRICULUM AGENT OUTPUT---"

    if delimiter_start not in raw_response:
        # Model did not call FINALISE properly — return full response as trace
        return {
            "reasoning_trace":   raw_response,
            "structured_output": "",
            "success":           False,
            "error":             "FINALISE() not called — output delimiter not found",
        }

    parts = raw_response.split(delimiter_start, 1)
    reasoning_trace = parts[0].strip()

    output_block = parts[1]
    if delimiter_end in output_block:
        output_block = output_block.split(delimiter_end, 1)[0]

    structured_output = output_block.strip()

    return {
        "reasoning_trace":   reasoning_trace,
        "structured_output": structured_output,
        "success":           True,
        "error":             None,
    }

