from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.database import engine, Base
from api.books import router as books_api_router

# Intialize app
app = FastAPI()

# mount static
app.mount("/static", StaticFiles(directory='static'), name='static')

# app routers

app.include_router(books_api_router)

# Create DB tables
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
