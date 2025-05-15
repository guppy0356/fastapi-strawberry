from seed_data import seed_database
from database import engine
from models import Base

if __name__ == "__main__":
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Add test data
    seed_database()
    print("テストデータの追加が完了しました。GraphQLでデータをクエリできます。")
