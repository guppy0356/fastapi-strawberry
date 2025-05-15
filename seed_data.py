from sqlalchemy.orm import Session
from models import Author, Post, Comment, Base
from database import SessionLocal, engine

def seed_database():
    # Create a new session
    db = SessionLocal()
    
    try:
        # First clear existing data
        db.query(Comment).delete()
        db.query(Post).delete()
        db.query(Author).delete()
        
        # Create authors
        author1 = Author(name="山田太郎")
        author2 = Author(name="佐藤花子")
        author3 = Author(name="鈴木一郎")
        
        db.add_all([author1, author2, author3])
        db.commit()
        
        # Create posts
        post1 = Post(
            title="SQLAlchemyの使い方",
            content="SQLAlchemyはPythonのORMライブラリです。データベース操作を簡単に行うことができます。",
            author_id=author1.id
        )
        
        post2 = Post(
            title="GraphQLとは",
            content="GraphQLは柔軟なAPIクエリ言語であり、クライアントが必要なデータだけを取得できるようにします。",
            author_id=author1.id
        )
        
        post3 = Post(
            title="FastAPIの基本",
            content="FastAPIは高速なPythonのWebフレームワークで、自動APIドキュメント生成機能があります。",
            author_id=author2.id
        )
        
        post4 = Post(
            title="Strawberryを使ったGraphQL",
            content="StrawberryはPythonでGraphQLを実装するためのライブラリです。",
            author_id=author3.id
        )
        
        db.add_all([post1, post2, post3, post4])
        db.commit()
        
        # Create comments
        comments = [
            Comment(post_id=post1.id, text="とても参考になりました！"),
            Comment(post_id=post1.id, text="初心者にもわかりやすい説明ですね。"),
            Comment(post_id=post2.id, text="GraphQLは最近注目されていますよね。"),
            Comment(post_id=post2.id, text="RESTと比較するとどうなのでしょうか？"),
            Comment(post_id=post3.id, text="FastAPIは本当に速いですね！"),
            Comment(post_id=post3.id, text="自動ドキュメント機能が便利です。"),
            Comment(post_id=post4.id, text="Strawberryの使い方の詳細も知りたいです。"),
            Comment(post_id=post4.id, text="コード例があるとさらにわかりやすいと思います。"),
        ]
        
        db.add_all(comments)
        db.commit()
        
        print("データベースへのテストデータ追加が完了しました。")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Seed the database
    seed_database()
