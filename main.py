import strawberry

from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter
from query import Query
from mutation import Mutation
from database import engine, get_db
from models import Base
from sqlalchemy.orm import Session
from typing import Any

# Create all tables in the database
Base.metadata.create_all(bind=engine)

schema = strawberry.Schema(Query, Mutation)

# Create context with database session
async def get_context(db: Session = Depends(get_db)) -> dict[str, Any]:
    return {"db": db, "post_author_id": None}

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
