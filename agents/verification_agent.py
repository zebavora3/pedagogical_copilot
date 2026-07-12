"""
Verification Agent — Final stage of Workflow B.

Reviews the generated teaching artifact against the curriculum design,
assessment design, and source teaching material.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm import call_llm
from utils.prompt_loader import load_prompt
import config


def run_verification_agent(
    teaching_material: str,
    stage1_output: str,
    stage2_output: str,
    stage3_artifact: str,
    model: str = config.DEFAULT_MODEL,
) -> dict:
    """
    Run the Verification Agent.

    Returns:
        reasoning_trace
        structured_output
        success
    """

    print("  [Verification Agent] Starting verification...")

    system_prompt = load_prompt("verification_agent")

    user_content = f"""
Teaching material:

{teaching_material}


Curriculum Design Agent Output:

{stage1_output}


Assessment Design Agent Output:

{stage2_output}


Lesson Generation Agent Output:

{stage3_artifact}


Begin your Thought → Action → Observation reasoning now.

Work through as many cycles as needed.

Conclude by calling either PASS(), CRITIQUE(), or HUMAN_REVIEW_REQUIRED().
"""

    raw_response = call_llm(
        system_prompt=system_prompt,
        user_content=user_content,
        model=model,
        temperature=config.TEMPERATURE_VERIFY,
    )

    result = _parse_response(raw_response)

    print(f"  [Verification Agent] Done. Success: {result['success']}")

    return result


def _parse_response(raw_response: str) -> dict:
    """
    The verification agent doesn't use delimiters.
    Instead we detect the final decision.
    """

    if "PASS()" in raw_response:
        decision = "PASS"

    elif "CRITIQUE(" in raw_response:
        decision = "CRITIQUE"

    elif "HUMAN_REVIEW_REQUIRED" in raw_response:
        decision = "HUMAN_REVIEW_REQUIRED"

    else:
        decision = "UNKNOWN"

    return {
        "reasoning_trace": raw_response,
        "decision": decision,
        "success": decision != "UNKNOWN",
    }