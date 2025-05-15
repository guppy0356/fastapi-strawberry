import strawberry
from typing import Optional
from sqlalchemy.orm import Session
from strawberry.types import Info
from models import Author as AuthorModel, Post as PostModel, Comment as CommentModel
from database import get_db

@strawberry.type
class Mutation:
    @strawberry.mutation
    def thousand(self, number: int) -> int:
        return number * 1000

    @strawberry.mutation
    def create_author(self, name: str) -> int:
        db: Session = next(get_db())
        author = AuthorModel(name=name)
        db.add(author)
        db.commit()
        db.refresh(author)
        return author.id

    @strawberry.mutation
    def create_post(self, title: str, content: Optional[str], author_id: int) -> int:
        db: Session = next(get_db())
        post = PostModel(title=title, content=content, author_id=author_id)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post.id

    @strawberry.mutation
    def create_comment(self, post_id: int, text: str) -> int:
        db: Session = next(get_db())
        comment = CommentModel(post_id=post_id, text=text)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment.id