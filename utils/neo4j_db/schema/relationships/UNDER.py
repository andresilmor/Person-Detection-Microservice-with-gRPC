import string
from time import time
import datetime
import strawberry.type as relationship
from utils.neo4j_db.schema import Medication
from typing import List, Union, Optional

@relationship
class Medication_UNDER_Receipt:
    def __init__(self, intOfTime = None, isAvailable = None, quantityPer = None, timeMeasure = None, medication = None):
        self.intOfTime = intOfTime
        self.isAvailable = isAvailable
        self.quantityPer = quantityPer
        self.timeMeasure = timeMeasure
        self.medication = medication
        pass
    
    intOfTime: int
    isAvailable: bool
    quantityPer: int
    timeMeasure: str
    medication: Medication

    
