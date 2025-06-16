# logic/trainer.py

from typing import List, Dict

class AITrainer:
    def __init__(self):
        self.examples = []

    def add_example(self, prompt: str, response: str):
        self.examples.append({"prompt": prompt, "response": response})

    def get_few_shot_examples(self) -> List[Dict[str, str]]:
        return self.examples[-5:]

    def train_summary(self) -> Dict[str, int]:
        return {"total_examples": len(self.examples)}
