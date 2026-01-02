from dataclasses import dataclass


@dataclass
class Squadre:
    team_id : int
    team_code: str
    name : str
    somma_salario : float

    def __str__(self):
        return f"{self.team_id} : {self.team_code} ({self.name}) - {self.somma_salario}"

    def __repr__(self):
        return f"{self.team_id} : {self.team_code} ({self.name}) - {self.somma_salario}"

    def __lt__(self, other):
        return self.team_code < other.team_code

    def __hash__(self):
        return hash(self.team_id)