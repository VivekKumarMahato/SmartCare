from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import Base, engine

# import models (IMPORTANT for table creation)
from app.models import user, donor, blood_request

# import routers
from app.api.v1.routes.user import router as user_router
from app.api.v1.routes.donor import router as donor_router
from app.api.v1.routes.blood_request import router as request_router

app = FastAPI()



@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)



@app.get("/")
def root():
    return {"message": "API is running"}



app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(donor_router, prefix="/api/v1/donors", tags=["Donors"])
app.include_router(request_router, prefix="/api/v1/requests", tags=["Blood Requests"])



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)