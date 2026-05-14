class GeminiClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def call(self, prompt: str) -> str:
        return ""  # integrate real client
