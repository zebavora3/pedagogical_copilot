"""
Universal LLM caller.
Routes to the correct API based on the model name.
"""

import anthropic
from openai import OpenAI
import config


def call_llm(
    system_prompt: str,
    user_content: str,
    model: str = config.DEFAULT_MODEL,
    temperature: float = config.TEMPERATURE_REASONING,
    max_tokens: int = config.MAX_TOKENS,
) -> str:
    """
    Send a prompt to an LLM and return the text response.

    Supported models:
      - claude-*          → Anthropic API
      - gpt-*             → OpenAI API
      - llama-* / groq-*  → Groq API
    """
    model_lower = model.lower()

    if "claude" in model_lower:
        return _call_anthropic(system_prompt, user_content, model, temperature, max_tokens)
    elif "gpt" in model_lower:
        return _call_openai(system_prompt, user_content, model, temperature, max_tokens)
    elif any(x in model_lower for x in ["llama", "groq", "mixtral"]):
        return _call_groq(system_prompt, user_content, model, temperature, max_tokens)
    else:
        raise ValueError(f"Unknown model family for: {model}")


# ── Private helpers ────────────────────────────────────────────────────────────

def _call_anthropic(system_prompt, user_content, model, temperature, max_tokens):
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )
    return response.content[0].text


def _call_openai(system_prompt, user_content, model, temperature, max_tokens):
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_content},
        ],
    )
    return response.choices[0].message.content


def _call_groq(system_prompt, user_content, model, temperature, max_tokens):
    from groq import Groq
    client = Groq(api_key=config.GROQ_API_KEY)
    response = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_content},
        ],
    )
    return response.choices[0].message.content