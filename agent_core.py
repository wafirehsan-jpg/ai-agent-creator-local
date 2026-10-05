import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from local_model import LocalModel


@dataclass
class ToolDefinition:
    name: str
    description: str
    function: Any


@dataclass
class AgentConfig:
    name: str
    role: str
    goal: str
    instructions: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    model: str = "llama3.1"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "goal": self.goal,
            "instructions": self.instructions,
            "tools": self.tools,
            "model": self.model,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentConfig":
        return cls(
            name=data.get("name", "Agent"),
            role=data.get("role", "Assistant"),
            goal=data.get("goal", "Help the user"),
            instructions=data.get("instructions", []),
            tools=data.get("tools", []),
            model=data.get("model", "llama3.1"),
        )


class Memory:
    def __init__(self, path: str = "memory/memory.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def load(self) -> List[Dict[str, str]]:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return []

    def add(self, key: str, value: str):
        items = self.load()
        items.append({"key": key, "value": value})
        self.path.write_text(json.dumps(items, indent=2), encoding="utf-8")

    def get_recent(self, limit: int = 5) -> List[Dict[str, str]]:
        items = self.load()
        return items[-limit:]


class Agent:
    def __init__(self, config: AgentConfig, memory_path: str = "memory/memory.json"):
        self.config = config
        self.memory = Memory(memory_path)
        self.model = LocalModel(model=config.model)

    def build_system_prompt(self) -> str:
        instructions = "\n".join(f"- {item}" for item in self.config.instructions) if self.config.instructions else "- Be helpful and concise."
        tools = ", ".join(self.config.tools) if self.config.tools else "No external tools"

        return f"""
You are {self.config.name}.

Role:
{self.config.role}

Goal:
{self.config.goal}

Rules:
{instructions}

Available tools:
{tools}

Behavior:
- Work entirely offline.
- Do not ask for an API key.
- Be honest when uncertain.
- Use memory when helpful.
- Keep answers clear and practical.
""".strip()

    def run(self, user_input: str) -> str:
        memory_context = ""
        recent_memory = self.memory.get_recent(5)
        if recent_memory:
            memory_context = "\nRecent memory:\n"
            for item in recent_memory:
                memory_context += f"- {item['key']}: {item['value']}\n"

        prompt = f"""
User request:
{user_input}

{memory_context}
Answer with practical guidance.
""".strip()

        response = self.model.generate(prompt, system=self.build_system_prompt())
        self.memory.add("last_response", response)
        return response

    def save(self, path: str):
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(self.config.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str, memory_path: str = "memory/memory.json") -> "Agent":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(config=AgentConfig.from_dict(data), memory_path=memory_path)


def create_agent_file(name: str, role: str, goal: str, instructions: List[str], tools: List[str], model: str):
    config = AgentConfig(
        name=name,
        role=role,
        goal=goal,
        instructions=instructions,
        tools=tools,
        model=model,
    )

    file_path = Path("agents") / f"{name.lower().replace(' ', '_')}.json"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    agent = Agent(config=config)
    agent.save(str(file_path))
    print(f"Agent created: {file_path}")


def run_agent_file(agent_path: str, prompt: str):
    agent = Agent.load(agent_path)
    output = agent.run(prompt)
    print(output)
