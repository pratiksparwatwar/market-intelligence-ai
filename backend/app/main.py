from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.routers import articles, themes, assets, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Market Intelligence AI",
    description="AI-powered market intelligence platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articles.router)
app.include_router(themes.router)
app.include_router(assets.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "Market Intelligence AI"}
