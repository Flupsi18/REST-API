from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api.api import router as api_router
from .core.config import Settings
from .database.mongodb import connect_to_mongodb, close_mongodb_connection

app = FastAPI(docs_url=Settings.DOCS_URL, title=Settings.PROJECT_NAME, description=Settings.PROJECT_DESCRIPTION)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_mongodb)
app.add_event_handler("shutdown", close_mongodb_connection)

app.include_router(api_router)
