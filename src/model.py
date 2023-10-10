# @uthor: Giorgio Saldana @email: giorgio.saldana@studenti.unicam.it
# model per definire la classe Studente utilizzata all'interno l DB
from dataclasses import dataclass

@dataclass
class Student:
    id: int
    email: str
    name: str