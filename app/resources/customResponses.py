import string
from time import time
from datetime import datetime, timezone
import strawberry.type as type
from utils.neo4j_db.schema import Medication, Pacient
from typing import List, Union, Optional

@type
class MedicationToTake:
    def __init__(self, atTime = None, quantity = None, pacient = None, medication = None):
        self.atTime = atTime
        self.quantity = quantity
        self.medication = medication
        self.pacient = pacient
        pass
    
    atTime: Optional[datetime] = None
    quantity: int
    pacient: Pacient
    medication: Medication