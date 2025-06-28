from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.database import engine, Base

# Intialize app
app = FastAPI()

# mount static
app.mount("/static", StaticFiles(directory='static'), name='static')


# Create DB tables
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
