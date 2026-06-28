from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llm.warmup import warmup_llm
from config.settings import settings
from config.redis import redis_client
from auth.routes.auth_routes import router as auth_router
from messages.routes.message_routes import router as message_router
from chat_sessions.routes.chat_session_routes import router as chat_session_router
from config.database import init_models
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from llm.llm_pipeline import router as llm_router

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.APP_DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("🚀 Starting backend...")

    # LLM warmup
    await warmup_llm()

    #create mdoels if they odnt exist
    await init_models()

    print(f"🔥 {settings.APP_NAME} is ready")

@app.on_event("shutdown")
async def shutdown_event():
    await redis_client.close()
    print("🧹 Cleanup complete")


app.include_router(auth_router)
app.include_router(chat_session_router)
app.include_router(message_router)
app.include_router(llm_router)


app.mount("/static", StaticFiles(directory="frontend"), name="static")

# HTML pages
@app.get("/")
def index():
    return FileResponse("frontend/index.html")

@app.get("/chat_sessions")
def chat_sessions():
    return FileResponse("frontend/chat_sessions.html")

@app.get("/chat")
def chat():
    return FileResponse("frontend/chat.html")


@app.get("/health")
def health():
    return {"message": "ok"}