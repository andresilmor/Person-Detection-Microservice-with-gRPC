from time import time
import datetime
import strawberry.type as relationship
from utils.neo4j_db.schema import Medication
from typing import List, Union, Optional

@relationship
class Pacient_TAKES_Medication:
    def __init__(self, hour = None, quantity = None, medication = None):
        self.hour = hour
        self.quantity = quantity
        self.medication = medication
        pass
    
    hour: datetime.time
    quantity: int
    medication: Medication

    
