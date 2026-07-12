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

    Returns:
        reasoning_trace
        structured_output
        success
    """

    print("  [Assessment Agent] Starting Stage 2 reasoning loop...")

    system_prompt = load_prompt("assessment_agent")

    user_content = f"""
Teaching material:

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

    delimiter_start = "---ASSESSMENT AGENT OUTPUT---"
    delimiter_end = "---END ASSESSMENT AGENT OUTPUT---"

    if delimiter_start not in raw_response:
        return {
            "reasoning_trace": raw_response,
            "structured_output": "",
            "success": False,
            "error": "Assessment output delimiter not found.",
        }

    reasoning_trace, output_block = raw_response.split(delimiter_start, 1)

    if delimiter_end in output_block:
        output_block = output_block.split(delimiter_end, 1)[0]

    return {
        "reasoning_trace": reasoning_trace.strip(),
        "structured_output": output_block.strip(),
        "success": True,
        "error": None,
    }