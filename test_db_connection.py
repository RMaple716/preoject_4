import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sqlalchemy import text
from src.database import engine, SessionLocal

def test_database_connection():
    """测试数据库连接"""
    try:
        # 测试基本连接
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ 数据库连接成功!")
            print(f"PostgreSQL版本: {version}")

        # 测试表是否存在
        db = SessionLocal()
        try:
            # 检查user_requirements表
            result = db.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'user_requirements'
            """))
            if result.fetchone():
                print("✅ user_requirements表存在")
            else:
                print("❌ user_requirements表不存在")

            # 检查cities表
            result = db.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'cities'
            """))
            if result.fetchone():
                print("✅ cities表存在")

                # 查询城市数量
                result = db.execute(text("SELECT COUNT(*) FROM cities"))
                count = result.fetchone()[0]
                print(f"   城市数量: {count}")
            else:
                print("❌ cities表不存在")

        finally:
            db.close()

    except Exception as e:
        print(f"❌ 数据库连接失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database_connection()
