import requests


class LocalModel:
    def __init__(self, model: str = "llama3.1", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def generate(self, prompt: str, system: str = "") -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
            },
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=180,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except Exception as exc:
            raise RuntimeError(f"Local model call failed: {exc}") from exc
