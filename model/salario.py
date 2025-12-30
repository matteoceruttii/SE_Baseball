from dataclasses import dataclass


@dataclass
class Salario:
    team_id : int
    team_code: str
    somma_salario : float

    def __str__(self):
        return f"{self.team_id} : {self.team_code} - {self.somma_salario}"

    def __repr__(self):
        return f"{self.team_id} : {self.team_code} - {self.somma_salario}"

    def __hash__(self):
        return hash(self.team_id)