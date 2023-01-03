import strawberry
from app.services import PacientQuery, MedicationQuery, MemberQuery


@strawberry.type
class Query (PacientQuery, MedicationQuery, MemberQuery):

    def NOT_USED(self):
        return None


    