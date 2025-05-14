import strawberry

@strawberry.type
class Mutation:
    @strawberry.mutation
    def thousand(self, number: int) -> int:
        return number * 1000