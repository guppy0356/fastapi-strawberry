import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"
   
    @strawberry.field
    def bye(self) -> str:
        return "Bye!"