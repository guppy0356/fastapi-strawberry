import strawberry
from typing import List
from sqlalchemy.orm import Session
from strawberry.types import Info
from models import Post as PostModel, Author as AuthorModel, Comment as CommentModel
from database import get_db
from strawberry.dataloader import DataLoader
import logging

# SQLAlchemyのログ設定
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

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
    async def comments(self, info: Info) -> List[Comment]:
        loader = info.context.get("comments_loader")
        if loader is None:
            loader = DataLoader(load_fn=load_comments)
            info.context["comments_loader"] = loader
        return await loader.load(self.id)

async def load_comments(post_ids: List[int]) -> List[List[Comment]]:
    db: Session = next(get_db())
    # Filter comments by the requested post IDs
    db_comments = db.query(CommentModel).filter(CommentModel.post_id.in_(post_ids)).all()

    # Group comments by post ID
    comments_by_post_id = {post_id: [] for post_id in post_ids}
    for comment in db_comments:
        comments_by_post_id[comment.post_id].append(
            Comment(id=comment.id, text=comment.text)
        )

    # Return comments in the same order as post_ids
    return [comments_by_post_id[post_id] for post_id in post_ids]

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"
   
    @strawberry.field
    def bye(self) -> str:
        return "Bye!"
    
    @strawberry.field
    async def posts(self, info: Info) -> List[Post]:
        db: Session = next(get_db())
        # SQL実行前にログを出力
        logging.info("Fetching all posts from database")
        db_posts = db.query(PostModel).all()
        
        result = []
        for post in db_posts:
            post_obj = Post(id=post.id, title=post.title, content=post.content)
            info.context["post_author_id"] = post.author_id
            result.append(post_obj)
            
        return result