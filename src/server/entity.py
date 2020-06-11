from typing import List

from dataclasses import dataclass, field


@dataclass
class QA:
    question: str
    answer: str


@dataclass()
class Dialog:
    source: List[QA] = field(default_factory=list)

    def serialize(self):
        return {
            'source': [qa.__dict__ for qa in self.source]
        }
