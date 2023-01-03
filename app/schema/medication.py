import strawberry.type as type
from datetime import datetime
from typing import Optional

from .pacient import Pacient

@type
class Medication:
    def __init__(self, uuid = None, label = None, name = None):
        self.uuid = uuid
        self.label = label
        self.name = name
        pass
    
    uuid: str
    label: str
    name: str

@type
class MedicationToTake:
    def __init__(self, atTime = None, quantity = None, timeMeasure = None, intOfTime = None, pacient = None, medication = None):
        self.atTime = atTime
        self.quantity = quantity
        self.timeMeasure = timeMeasure
        self.intOfTime = intOfTime
        self.medication = medication
        self.pacient = pacient
        pass
    
    atTime: Optional[datetime] = None
    quantity: int
    timeMeasure: str
    intOfTime: int
    pacient: Pacient
    medication: Medication