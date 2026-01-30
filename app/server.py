from fastapi import FastAPI
from app.routes.index import router as main_router
from app.config.connection import Base, engine

app = FastAPI()


Base.metadata.drop_all(bind=engine)   
Base.metadata.create_all(bind=engine) 

app.include_router(main_router)

