from fastapi import FastAPI

from storybook.api.routes.stories import router

app = FastAPI(title="Storybook AI")
app.include_router(router, prefix="/api")


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
