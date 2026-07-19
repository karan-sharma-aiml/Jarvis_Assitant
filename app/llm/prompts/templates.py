"""
JARVIS Prompt Templates

Reusable task-specific prompt templates.

This module contains prompt templates that can be combined
with the master system prompt by PromptBuilder.

The templates are intentionally independent from any LLM provider.
"""

from __future__ import annotations

from enum import StrEnum


class PromptTemplate(StrEnum):
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    DEBUG = "debug"
    REFACTOR = "refactor"
    EXPLAIN_CODE = "explain_code"
    RESEARCH = "research"
    RAG = "rag"
    STUDY = "study"
    INTERVIEW = "interview"
    SUMMARY = "summary"
    PLANNING = "planning"
    DOCUMENTATION = "documentation"


TEMPLATES: dict[PromptTemplate, str] = {

    PromptTemplate.CODE_GENERATION: """
Generate production-quality code.

Requirements:

- Python 3.12+
- SOLID
- Clean Architecture
- Type hints
- Logging
- Proper exception handling
- Maintainability
- Readability
- PEP 8

Explain important design decisions only when useful.
""".strip(),

    PromptTemplate.CODE_REVIEW: """
Review the provided code.

Identify:

- Bugs
- Code smells
- Security issues
- Performance issues
- Maintainability issues
- Readability issues

Recommend improvements.

Preserve functionality whenever possible.
""".strip(),

    PromptTemplate.DEBUG: """
Act as an expert debugging engineer.

Find the root cause.

Explain:

- why the bug occurs

- why the solution works

Avoid guessing.

Verify assumptions.
""".strip(),

    PromptTemplate.REFACTOR: """
Improve the existing implementation.

Do not change functionality.

Improve:

- architecture

- readability

- maintainability

- type hints

- documentation

- performance when justified
""".strip(),

    PromptTemplate.EXPLAIN_CODE: """
Explain the provided code.

Start from high level.

Then explain:

- architecture

- flow

- important classes

- important functions

- execution

Use beginner-friendly language.
""".strip(),

    PromptTemplate.RESEARCH: """
Act as an AI Research Assistant.

Summarize research.

Compare approaches.

Identify strengths.

Identify limitations.

Suggest future improvements.

Clearly separate facts from assumptions.
""".strip(),

    PromptTemplate.RAG: """
Answer using the retrieved context.

Prioritize retrieved knowledge.

If information is missing,
clearly state the limitation.

Do not fabricate missing information.
""".strip(),

    PromptTemplate.STUDY: """
Teach the topic step by step.

Explain fundamentals first.

Provide examples.

Suggest exercises.

Recommend revision strategy.
""".strip(),

    PromptTemplate.INTERVIEW: """
Act as a Senior Technical Interviewer.

Ask realistic interview questions.

Evaluate answers.

Provide constructive feedback.

Suggest improvement areas.
""".strip(),

    PromptTemplate.SUMMARY: """
Summarize the provided information.

Keep important technical details.

Use headings.

Use bullet points where appropriate.
""".strip(),

    PromptTemplate.PLANNING: """
Help create a practical execution plan.

Break work into milestones.

Prioritize important tasks.

Recommend the next logical step.
""".strip(),

    PromptTemplate.DOCUMENTATION: """
Write professional documentation.

Use:

- clear headings

- concise language

- examples when useful

- consistent formatting

Focus on maintainability.
""".strip(),
}


def get_template(template: PromptTemplate) -> str:
    """
    Return the prompt template for the requested task.
    """

    return TEMPLATES[template]