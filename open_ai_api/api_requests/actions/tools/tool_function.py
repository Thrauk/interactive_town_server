from typing import Dict, Any


class ToolFunction:
    def __init__(self, name: str, description: str, parameters: Dict[str, Any]):
        self.name = name
        self.description = description
        self.parameters = parameters

    def __str__(self):
        return f"Tool(name={self.name}, description={self.description}, parameters={self.parameters})"

    def format(self):
        return {
            'type': 'function',
            'function': {
                'name': self.name,
                'description': self.description,
                'parameters': {
                    'type': 'object',
                    'properties': self.parameters,
                }
            },
            'required': list(self.parameters.keys()),
        }
