# 🔄 SQLAlchemy vs Sequelize 自动同步功能对比

## 📊 核心功能对比

| 功能 | Sequelize (Node.js) | SQLAlchemy (Python) | 说明 |
|------|---------------------|---------------------|------|
| **基础同步** | `sequelize.sync()` | `Base.metadata.create_all()` | 创建所有表 |
| **强制重建** | `sequelize.sync({ force: true })` | `Base.metadata.drop_all()` + `create_all()` | 删除后重建 |
| **安全重建** | `sequelize.sync({ alter: true })` | ❌ 不直接支持 | 修改现有表结构 |
| **单个表操作** | `Model.sync()` | `Model.__table__.create()` | 创建特定表 |
| **检查表存在** | `sequelize.getQueryInterface().tableExists()` | `inspect(engine).get_table_names()` | 检查表是否存在 |
| **迁移工具** | `sequelize-cli` | `Alembic` | 版本化迁移 |

---

## 💻 代码示例对比

### 1. 基础同步

#### Sequelize (Node.js)
```javascript
const { Sequelize } = require('sequelize');

const sequelize = new Sequelize('database', 'username', 'password', {
  host: 'localhost',
  dialect: 'postgres'
});

// 同步所有模型
await sequelize.sync();
console.log('所有表已创建');
```

#### SQLAlchemy (Python)
```python
from src.database import engine, Base

# 同步所有模型
Base.metadata.create_all(bind=engine)
print('所有表已创建')
```

---

### 2. 强制重建

#### Sequelize (Node.js)
```javascript
// ⚠️ 会删除所有数据！
await sequelize.sync({ force: true });
console.log('所有表已重建');
```

#### SQLAlchemy (Python)
```python
# ⚠️ 会删除所有数据！
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print('所有表已重建')
```

或使用我们的脚本：
```bash
python scripts/sync_db.py --force
```

---

### 3. 单个表操作

#### Sequelize (Node.js)
```javascript
// 只同步 User 模型
await User.sync();

// 强制重建 User 表
await User.sync({ force: true });
```

#### SQLAlchemy (Python)
```python
from src.models.db_models import City
from src.database import engine

# 只创建 City 表
City.__table__.create(bind=engine)

# 或使用我们的工具
from scripts.db_migration import DatabaseMigration
migration = DatabaseMigration()
migration.create_single_table("cities")
```

---

### 4. 检查表是否存在

#### Sequelize (Node.js)
```javascript
const queryInterface = sequelize.getQueryInterface();
const tables = await queryInterface.showAllTables();

if (tables.includes('Users')) {
  console.log('Users 表存在');
}
```

#### SQLAlchemy (Python)
```python
from sqlalchemy import inspect
from src.database import engine

inspector = inspect(engine)
tables = inspector.get_table_names()

if 'users' in tables:
    print('Users 表存在')
```

---

### 5. 添加列

#### Sequelize (Node.js)
```javascript
// Sequelize 需要手动执行 SQL 或使用迁移
await sequelize.getQueryInterface().addColumn('Users', 'age', {
  type: Sequelize.INTEGER,
  allowNull: true
});
```

#### SQLAlchemy (Python)
```python
# 使用我们的高级工具
from scripts.db_migration import DatabaseMigration

migration = DatabaseMigration()
migration.add_column("users", "age", "INTEGER", nullable=True)
```

或使用 Alembic（推荐）：
```python
# alembic/versions/xxx_add_age_column.py
def upgrade():
    op.add_column('users', sa.Column('age', sa.Integer(), nullable=True))
```

---

## 🎯 使用场景对比

### 开发环境

#### Sequelize
```javascript
// development.js
if (process.env.NODE_ENV === 'development') {
  await sequelize.sync({ force: true });
}
```

#### SQLAlchemy
```bash
# 每次启动时
python scripts/sync_db.py --force
```

或在代码中：
```python
import os
from src.database import engine, Base

if os.getenv('ENV') == 'development':
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
```

---

### 测试环境

#### Sequelize
```javascript
// test/setup.js
beforeEach(async () => {
  await sequelize.sync({ force: true });
  // 填充测试数据
});

afterAll(async () => {
  await sequelize.close();
});
```

#### SQLAlchemy
```python
# tests/conftest.py
import pytest
from src.database import engine, Base

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
```

---

### 生产环境

#### Sequelize
```javascript
// 使用 sequelize-cli 进行迁移
// npx sequelize-cli db:migrate
```

#### SQLAlchemy
```bash
# 使用 Alembic 进行迁移
# alembic upgrade head
```

---

## 📦 生态系统对比

### Sequelize 生态
```
sequelize (核心库)
├── sequelize-cli (命令行工具)
├── @sequelize/postgres (PostgreSQL 驱动)
├── @sequelize/mysql (MySQL 驱动)
└── sequelize-typescript (TypeScript 支持)
```

### SQLAlchemy 生态
```
SQLAlchemy (核心库)
├── Alembic (迁移工具)
├── psycopg2 (PostgreSQL 驱动)
├── pymysql (MySQL 驱动)
└── SQLAlchemy-Utils (实用工具)
```

---

## 🔧 配置对比

### 数据库连接

#### Sequelize
```javascript
const sequelize = new Sequelize('database', 'username', 'password', {
  host: 'localhost',
  port: 5432,
  dialect: 'postgres',
  logging: false,  // 禁用日志
  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000
  }
});
```

#### SQLAlchemy
```python
from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://username:password@localhost:5432/database',
    echo=False,  # 禁用日志
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)
```

---

## 🎓 学习曲线对比

| 方面 | Sequelize | SQLAlchemy | 说明 |
|------|-----------|------------|------|
| **入门难度** | ⭐⭐ | ⭐⭐⭐ | SQLAlchemy 概念更多 |
| **文档质量** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | SQLAlchemy 文档更详细 |
| **灵活性** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | SQLAlchemy 更灵活 |
| **性能** | ⭐⭐⭐ | ⭐⭐⭐⭐ | SQLAlchemy 性能更好 |
| **社区支持** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | SQLAlchemy 社区更大 |
| **TypeScript** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Sequelize 对 TS 支持更好 |

---

## 💡 最佳实践对比

### Sequelize 最佳实践
```javascript
// 1. 使用迁移而不是 sync
// npx sequelize-cli migration:generate --name add-age-column

// 2. 定义模型时使用 TypeScript
interface UserAttributes {
  id: number;
  name: string;
  age?: number;
}

// 3. 使用事务
await sequelize.transaction(async (t) => {
  await User.create({ name: 'John' }, { transaction: t });
  await Profile.create({ userId: 1 }, { transaction: t });
});
```

### SQLAlchemy 最佳实践
```python
# 1. 使用 Alembic 进行迁移
# alembic revision --autogenerate -m "add age column"

# 2. 使用类型提示（Python 3.10+）
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

# 3. 使用会话管理
from sqlalchemy.orm import Session

with Session(engine) as session:
    user = User(name="John")
    session.add(user)
    session.commit()
```

---

## 🚀 总结

### 选择 Sequelize 的理由
- ✅ 项目使用 Node.js/TypeScript
- ✅ 需要更好的 TypeScript 支持
- ✅ 团队熟悉 JavaScript 生态

### 选择 SQLAlchemy 的理由
- ✅ 项目使用 Python
- ✅ 需要更高的性能和灵活性
- ✅ 需要复杂的查询和关系管理
- ✅ 更大的社区和更多的扩展

### 共同点
- ✅ 都支持自动同步建表
- ✅ 都有成熟的迁移工具
- ✅ 都支持多种数据库
- ✅ 都有活跃的社区

---

**最后更新**: 2026-05-24  
**作者**: AI Assistant
