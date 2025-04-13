from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.internal import scrap_router


app = FastAPI(title='Scraper',
              description='Fastapi service for scrap html',
              version='0.1')

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Adding v1 namespace route
app.include_router(scrap_router)


@app.get('/health',
         tags=['System probs'])
def health() -> int:
    return status.HTTP_200_OK
