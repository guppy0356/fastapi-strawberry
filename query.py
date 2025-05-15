import strawberry
from typing import List
from sqlalchemy.orm import Session
from strawberry.types import Info
from models import Post as PostModel, Author as AuthorModel, Comment as CommentModel
from database import get_db

@strawberry.type
class Comment:
    id: int
    text: str

@strawberry.type
class Author:
    id: int
    name: str

@strawberry.type
class Post:
    id: int
    title: str
    content: str = None
    
    @strawberry.field
    def author(self, info: Info) -> Author:
        db: Session = next(get_db())
        db_author = db.query(AuthorModel).filter(AuthorModel.id == info.context["post_author_id"]).first()
        return Author(id=db_author.id, name=db_author.name)
    
    @strawberry.field
    def comments(self, info: Info) -> List[Comment]:
        db: Session = next(get_db())
        db_comments = db.query(CommentModel).filter(CommentModel.post_id == self.id).all()
        return [Comment(id=comment.id, text=comment.text) for comment in db_comments]

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"
   
    @strawberry.field
    def bye(self) -> str:
        return "Bye!"
    
    @strawberry.field
    def posts(self, info: Info) -> List[Post]:
        db: Session = next(get_db())
        db_posts = db.query(PostModel).all()
        
        result = []
        for post in db_posts:
            post_obj = Post(id=post.id, title=post.title, content=post.content)
            info.context["post_author_id"] = post.author_id
            result.append(post_obj)
            
        return result