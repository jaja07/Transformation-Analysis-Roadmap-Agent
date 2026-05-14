class LlamaClient:
    def __init__(self, model_path: str | None = None):
        self.model_path = model_path

    def generate(self, prompt: str) -> str:
        return ""
