from app.config.settings import Provider
from app.llm.manager import LLMManager

llm = LLMManager()

print(llm.list_providers())

print(llm.chat("Hello"))

# Switch only if available
if Provider.GEMINI.value in llm.list_providers():
    llm.set_provider(Provider.GEMINI)
    print(llm.chat("Who are you?"))
else:
    print("Gemini provider is not available.")