from abc import abstractmethod
import strawberry
from routers.resources.graph import PacientQuery

@strawberry.type
class Query (PacientQuery):

    def NOT_USED(self):
        return None


    