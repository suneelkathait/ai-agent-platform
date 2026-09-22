from app.llm.client import LLMClient

class ChatService:
  def __init__(self):
    self.llm = LLMClient()

  async def chat(self, question: str) -> str:
    return await self.llm.generate(question)