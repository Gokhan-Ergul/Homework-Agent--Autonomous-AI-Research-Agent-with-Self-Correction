from fastapi import FastAPI
# router dosyasından 'router' değişkenini 'process_router' adıyla alıyoruz
from router import router as agent_router

app = FastAPI(
    title="Autonomous AI Research Agent API",
    description="LangGraph tabanlı araştırma, yazma ve formatlama yapan otonom sistem.",
    version="1.0"
)

# Endpoint'leri ana uygulamaya dahil et
app.include_router(agent_router, prefix="/agent", tags=["Research Agent"])

@app.get("/")
def root():
    return {"message": "Research Agent API is running! Go to /docs to use it."}