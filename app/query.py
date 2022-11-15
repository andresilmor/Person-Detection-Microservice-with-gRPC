from abc import abstractmethod
import strawberry
from app.resources.graph import PacientQuery, MedicationQuery, CaregiverQuery


@strawberry.type
class Query (PacientQuery, MedicationQuery, CaregiverQuery):

    def NOT_USED(self):
        return None


    