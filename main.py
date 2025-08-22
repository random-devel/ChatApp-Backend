from fastapi import FastAPI
from Authentication.routes import auth
from Admin.routes import Admin
from ResetSystem.routes import AuthReset
from Profile.routes import Profile
from Chat.routes import chat
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from Authentication.MongoODM import (
    UserCred,
    UserInfo,
    OTPdocuments,
    TempStage1,
    TempStage2,
    Sessions,
    AdminSessions
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],              
    allow_headers=["*"],
)

app.include_router(auth)
app.include_router(Admin)
app.include_router(AuthReset)
app.include_router(Profile)
app.include_router(chat)


@app.on_event("startup")
async def startup_event():
    global client
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["users"]
    await init_beanie(
        database=db, # type: ignore
        document_models=[
            UserCred,
            UserInfo,
            OTPdocuments,
            TempStage1,
            TempStage2,
            Sessions,
            AdminSessions
        ]
    )

@app.on_event("shutdown")
async def shutdown_event():
    global client
    if client:
        client.close()
        print("🔒 MongoDB connection closed.")
