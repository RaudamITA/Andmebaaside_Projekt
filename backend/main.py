import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes.api import router as api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "This is hotel booking API", "docs": "http://api.tammekand.ee/docs"}


app.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000,
                log_level="info", reload=True)
