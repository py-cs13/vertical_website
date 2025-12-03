from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 创建FastAPI应用实例
app = FastAPI(
    title="垂直领域内容变现平台API",
    description="提供内容管理、用户认证和商业化功能的API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fastapi-backend"}

# 根路径
@app.get("/")
async def root():
    return {"message": "垂直领域内容变现平台API服务正在运行"}

# 示例端点 - 获取内容列表
@app.get("/api/content/list")
async def get_content_list():
    # 这里将来会连接数据库，现在返回示例数据
    return {
        "status": "success",
        "data": [
            {
                "id": 1,
                "title": "示例内容1",
                "category": "母婴育儿",
                "summary": "这是第一条示例内容",
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "id": 2,
                "title": "示例内容2",
                "category": "健康养生",
                "summary": "这是第二条示例内容",
                "created_at": "2024-01-02T00:00:00Z"
            }
        ],
        "total": 2
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)