from time import time
import datetime
import strawberry.type as relationship
from utils.neo4j_db.schema import Medication

@relationship
class Pacient_TAKES_Medication:
    hour: datetime.time
    quantity: int
    medication: Medication