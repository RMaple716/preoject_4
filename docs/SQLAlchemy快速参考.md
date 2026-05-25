# 🚀 SQLAlchemy 自动同步建表 - 快速参考

## 一句话总结
> 像 Sequelize 一样，用 Python 代码定义数据库结构，自动同步到 PostgreSQL。

---

## ⚡ 快速命令

```bash
# 1. 普通同步（推荐）
python scripts/sync_db.py

# 2. 强制重建（会丢失数据！）
python scripts/sync_db.py --force

# 3. 交互式管理
python scripts/db_migration.py

# 4. 查看示例
python scripts/sync_examples.py
```

---

## 📂 文件清单

| 文件 | 用途 | 命令 |
|------|------|------|
| `scripts/sync_db.py` | 基础同步工具 | `python scripts/sync_db.py` |
| `scripts/db_migration.py` | 高级迁移工具 | `python scripts/db_migration.py` |
| `scripts/sync_examples.py` | 使用示例 | `python scripts/sync_examples.py` |
| `docs/SQLAlchemy自动同步建表说明.md` | 详细文档 | - |
| `scripts/README.md` | 快速指南 | - |

---

## 🎯 常用场景

### 场景 1: 首次初始化
```bash
python scripts/sync_db.py
```

### 场景 2: 新增模型后
```bash
# 1. 在 src/models/db_models.py 中添加新模型
# 2. 运行同步
python scripts/sync_db.py
```

### 场景 3: 开发环境重置
```bash
python scripts/sync_db.py --force
```

### 场景 4: 检查数据库状态
```bash
python scripts/db_migration.py
# 选择选项 2
```

---

## 💻 代码集成

### 应用启动时自动同步
```python
from src.database import engine, Base

# 在 app 启动时调用
Base.metadata.create_all(bind=engine)
```

### 测试环境中使用
```python
import pytest
from src.database import engine, Base

@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
```

---

## 🔍 核心 API

### 基础同步
```python
from src.database import engine, Base

# 创建所有表（幂等操作）
Base.metadata.create_all(bind=engine)

# 删除所有表
Base.metadata.drop_all(bind=engine)
```

### 检查表是否存在
```python
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()

if 'cities' in tables:
    print("表存在")
```

### 单个表操作
```python
from scripts.db_migration import DatabaseMigration

migration = DatabaseMigration()

# 创建单个表
migration.create_single_table("cities")

# 删除单个表
migration.drop_single_table("cities")

# 添加列
migration.add_column("cities", "population", "INTEGER")

# 删除列
migration.drop_column("cities", "population")
```

---

## 📊 当前数据库表

### 基础数据表（5个）
- `cities` - 城市信息
- `attractions` - 景点信息
- `locations` - 地点信息
- `hotels` - 酒店信息
- `restaurants` - 餐厅信息

### 业务数据表（3个）
- `user_requirements` - 用户需求
- `tasks` - 任务分解
- `itineraries` - 行程方案

---

## ⚠️ 注意事项

### ✅ 推荐做法
- 开发环境使用 `sync_db.py`
- 生产环境使用 Alembic
- 定期备份重要数据
- 修改模型后及时同步

### ❌ 避免做法
- 生产环境使用 `--force`
- 不备份就重建表
- 忽略表结构差异
- 直接修改数据库结构

---

## 🆘 常见问题

**Q: 表没有创建？**  
A: 确保在 `sync_db.py` 中导入了所有模型

**Q: 如何只创建某个表？**  
A: 使用 `db_migration.py` 的选项 3

**Q: 数据丢失了怎么办？**  
A: 从备份恢复，或重新导入初始数据

**Q: 生产环境怎么用？**  
A: 使用 Alembic 进行版本化迁移

---

## 📚 更多信息

- 📖 [详细文档](./SQLAlchemy自动同步建表说明.md)
- 📝 [实现总结](./SQLAlchemy自动同步建表-实现总结.md)
- 🔗 [SQLAlchemy 官方文档](https://docs.sqlalchemy.org/)
- 🔗 [Alembic 迁移工具](https://alembic.sqlalchemy.org/)

---

**最后更新**: 2026-05-24  
**维护者**: Project Team
