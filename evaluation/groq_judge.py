from deepeval.models.base_model import DeepEvalBaseLLM
from langchain_groq import ChatGroq


class GroqJudgeLLM(DeepEvalBaseLLM):

    def __init__(self, api_key, model="llama-3.3-70b-versatile"):
        
        self.api_key = api_key
        self.model_name = model
        self.model = None

        self.load_model()
    
    def load_model(self):
        """Initialize the Groq model."""

        self.model = ChatGroq(
            model=self.model_name,
            api_key=self.api_key,
            temperature=0
        )

    def generate(self, prompt: str) -> str:

        response = self.model.ainvoke(prompt)

        return response.content

    async def a_generate(self, prompt: str) -> str:

        response = await self.model.ainvoke(prompt)

        return response.content

    def get_model_name(self):

        return f"Groq-{self.model_name}"