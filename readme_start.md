# 旅游行程规划系统 - 快速启动指南

## 📋 前置要求

### 系统要求
- **操作系统**: Windows 10/11, Linux, macOS
- **Python**: 3.7 或更高版本
- **Node.js**: 16 或更高版本
- **npm**: 8 或更高版本

### 安装检查

```bash
# 检查Python版本
python --version  # Windows
python3 --version  # Linux/macOS

# 检查Node.js版本
node --version

# 检查npm版本
npm --version
```

## 🚀 快速启动

### Windows系统

#### 1. 启动服务

双击运行 `start.bat` 或在命令行中执行：

```bash
start.bat
```

脚本会自动完成以下操作：
- ✅ 检查Python和Node.js环境
- ✅ 检查并安装后端依赖
- ✅ 检查并安装前端依赖
- ✅ 启动后端服务（端口9091）
- ✅ 启动前端服务（端口3000）

#### 2. 访问服务

启动完成后，可以访问以下地址：

- **前端应用**: http://localhost:3000
- **后端API**: http://127.0.0.1:9091
- **API文档**: http://127.0.0.1:9091/docs
- **ReDoc文档**: http://127.0.0.1:9091/redoc

#### 3. 停止服务

双击运行 `stop.bat` 或在命令行中执行：

```bash
stop.bat
```

### Linux/macOS系统

#### 1. 赋予执行权限

```bash
chmod +x start.sh stop.sh
```

#### 2. 启动服务

```bash
./start.sh
```

#### 3. 访问服务

与Windows系统相同

#### 4. 停止服务

```bash
./stop.sh
```

或按 `Ctrl+C` 停止所有服务

## 📁 项目结构

```
new_project/
├── start.bat              # Windows启动脚本
├── start.sh               # Linux/macOS启动脚本
├── stop.bat               # Windows停止脚本
├── stop.sh                # Linux/macOS停止脚本
├── requirements.txt       # 后端Python依赖
├── src/                   # 后端源代码
│   └── index.py          # 后端入口文件
├── frontend/             # 前端项目
│   ├── package.json      # 前端依赖配置
│   ├── vite.config.ts    # Vite配置
│   └── src/              # 前端源代码
└── docs/                 # 项目文档
```

## 🔧 手动启动（可选）

### 仅启动后端

**Windows**:
```bash
python src/index.py
```

**Linux/macOS**:
```bash
python3 src/index.py
```

### 仅启动前端

```bash
cd frontend
npm run dev
```

### 安装依赖

**后端依赖**:
```bash
pip install -r requirements.txt
```

**前端依赖**:
```bash
cd frontend
npm install
```

## 🐛 常见问题

### 1. Python未找到

**错误信息**: 未检测到Python

**解决方案**:
- 确保已安装Python 3.7+
- 将Python添加到系统PATH环境变量
- Windows用户可以从 https://python.org 下载安装

### 2. Node.js未找到

**错误信息**: 未检测到Node.js

**解决方案**:
- 确保已安装Node.js 16+
- 将Node.js添加到系统PATH环境变量
- 从 https://nodejs.org 下载安装

### 3. 端口被占用

**错误信息**: 端口9091或3000已被占用

**解决方案**:

**Windows**:
```bash
# 查找占用端口的进程
netstat -ano | findstr :9091
netstat -ano | findstr :3000

# 终止进程（替换<PID>为实际进程ID）
taskkill /PID <PID> /F
```

**Linux/macOS**:
```bash
# 查找占用端口的进程
lsof -i :9091
lsof -i :3000

# 终止进程（替换<PID>为实际进程ID）
kill -9 <PID>
```

### 4. 依赖安装失败

**后端依赖**:
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**前端依赖**:
```bash
# 使用国内镜像源
npm config set registry https://registry.npmmirror.com
npm install
```

### 5. 前端无法连接后端

**检查项**:
1. 确保后端服务正在运行
2. 检查浏览器控制台是否有CORS错误
3. 确认Vite代理配置正确（vite.config.ts）

## 📊 服务状态检查

### 检查后端服务

访问 http://127.0.0.1:9091/api/v1/health

正常响应：
```json
{
  "code": 200,
  "msg": "服务正常",
  "data": {
    "status": "healthy",
    "timestamp": "2026-05-23T22:00:00"
  }
}
```

### 检查前端服务

访问 http://localhost:3000

应该能看到旅游行程规划系统的首页

## 📝 开发模式

### 后端开发模式

使用热重载启动后端：

```bash
uvicorn src.index:app --host 0.0.0.0 --port 9091 --reload
```

### 前端开发模式

前端默认使用开发模式，支持热重载：

```bash
cd frontend
npm run dev
```

## 🔍 日志查看

### 后端日志

后端日志会显示在启动后端服务的终端窗口中

### 前端日志

前端日志会显示在启动前端服务的终端窗口中
浏览器控制台（F12）也会显示前端运行日志

## 📚 更多文档

- [项目主文档](README.md)
- [API接口文档](docs/API_INTERFACES_COMPLETE.md)
- [前端开发指南](frontend/README.md)
- [测试指南](docs/API_QUICK_REFERENCE.md)

## 💡 提示

1. 首次启动可能需要较长时间安装依赖
2. 建议使用终端窗口查看服务日志
3. 开发时建议分别启动前后端，便于查看日志
4. 修改代码后会自动重新加载（开发模式）

## 🆘 获取帮助

如遇问题，请：
1. 查看常见问题部分
2. 检查服务日志
3. 查看项目文档
4. 在团队群组中提问

---

**最后更新**: 2026-05-23
**版本**: 1.0.0
