import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"
   
    @strawberry.field
    def bye(self) -> str:
        return "Bye!"

@strawberry.type
class Mutation:
    @strawberry.mutation
    def thousand(self, number:int) -> int:
        return number * 1000

schema = strawberry.Schema(Query, Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
