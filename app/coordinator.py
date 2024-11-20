import uvicorn

from app.main import FastAPI, app
from app.utils.logger import logger


class Coordinator:
    def __init__(self):
        self.app = FastAPI()
        self.can_execute = 0

    def run(self):
        uvicorn.run(app)
        logger.info("Stopping API...")
