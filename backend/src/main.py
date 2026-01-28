
from fastapi import FastAPI, status

app = FastAPI(
    title="Secure Chat",
    version="0.1"
)

@app.get("/health", status_code=status.HTTP_200_OK)
async def health()->dict:
    return {"message":"OK"}