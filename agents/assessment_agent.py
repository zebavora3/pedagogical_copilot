"""
Assessment Design Agent — Stage 2 of Workflow B.

Applies Backward Design Stage 2 (Acceptable Evidence) using a ReAct reasoning loop.
Returns the reasoning trace and the structured assessment output.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm import call_llm
from utils.prompt_loader import load_prompt
import config


def run_assessment_agent(
    teaching_material: str,
    stage1_output: str,
    model: str = config.DEFAULT_MODEL,
) -> dict:
    """
    Run the Assessment Design Agent.
    """

    print("  [Assessment Agent] Starting Stage 2 reasoning loop...")

    system_prompt = load_prompt("assessment_agent")

    user_content = f"""Teaching material:

{teaching_material}


Curriculum Design Agent Output:

{stage1_output}


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

    print(f"  [Assessment Agent] Done. Success: {result['success']}")

    return result


def _parse_response(raw_response: str) -> dict:
    """
    Split the model response into:
        - reasoning trace
        - structured assessment output
    """

    start = "---ASSESSMENT AGENT OUTPUT---"
    end = "---END ASSESSMENT AGENT OUTPUT---"

    if start not in raw_response:
        return {
            "agent": "Assessment",
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
        "agent": "Assessment",
        "success": True,
        "reasoning_trace": reasoning_trace.strip(),
        "structured_output": structured_output,
        "raw_response": raw_response,
        "error": None
    }