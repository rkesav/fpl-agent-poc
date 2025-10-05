import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class OpenAIAgent:
    """POC wrapper. In POC, we just craft a reply locally if key missing.
    Later, swap to OpenAI Responses API to summarize tool outputs nicely.
    """
    def __init__(self):
        self.enabled = bool(OPENAI_API_KEY)

    async def reply(self, user_msg: str, captain: str, rationale: str) -> str:
        if not self.enabled:
            return (
                f"(Local POC) Suggested captain: {captain}.\n"
                f"Reason: {rationale}. Ask me to fetch FPL bootstrap to try again."
            )
        # If you want, add OpenAI Responses call here to polish the reply.
        # Keeping it minimal to avoid external calls during POC.
        return f"Suggested captain: {captain}. Reason: {rationale}."