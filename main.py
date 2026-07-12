import os

import config

from utils.pdf_loader import extract_pages

from agents.curriculum_agent import run_curriculum_agent
from agents.assessment_agent import run_assessment_agent
from agents.lesson_agent import run_lesson_agent
from agents.verification_agent import run_verification_agent


# Load Teaching Material

pdf_path = os.path.join(
    config.MATERIALS_DIR,
    "/Users/Zeba/Desktop/pedagogical_copilot/experiments/materials/statistics_notes.pdf"
)

teaching_material = extract_pages(
    pdf_path,
    start_page=77,
    end_page=131
)


# Lecturer Request

lecturer_request = """
Generate a complete university lesson plan for this topic.

Include:
- learning objectives
- teaching sequence
- explanations
- examples where appropriate
- classroom activities
- formative assessment
"""


print("WORKFLOW B")


# Stage 1 — Curriculum Design Agent

curriculum = run_curriculum_agent(teaching_material)

print("\n")
print("STAGE 1 COMPLETE")

print(curriculum["structured_output"])


# Stage 2 — Assessment Design Agent


assessment = run_assessment_agent(
    teaching_material,
    curriculum["structured_output"]
)

print("\n")
print("STAGE 2 COMPLETE")

print(assessment["structured_output"])


# Stage 3 — Lesson Generation Agent

lesson = run_lesson_agent(
    teaching_material=teaching_material,
    stage1_output=curriculum["structured_output"],
    stage2_output=assessment["structured_output"],
    lecturer_request=lecturer_request
)

print("\n")
print("STAGE 3 COMPLETE")

print(lesson)



# Stage 4 — Verification Agent

verification = run_verification_agent(
    teaching_material=teaching_material,
    stage1_output=curriculum["structured_output"],
    stage2_output=assessment["structured_output"],
    stage3_artifact=lesson
)

print("\n")
print("VERIFICATION")


print("Decision:", verification["decision"])

print("\n")

print(verification["reasoning_trace"])