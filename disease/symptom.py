import symptom_char

class Symptom:
    def __init__(self, name, severity, duration, discription, characteristic, age_range):
        self.name = name
        self.discription = discription
        self.severity = severity
        self.duration = duration
        self.charachteristic = characteristic
        self.age_range = age_range

    def __str__(self):
        return f"Symptom: {self.name}, Severity: {self.severity}, Duration: {self.duration}"
