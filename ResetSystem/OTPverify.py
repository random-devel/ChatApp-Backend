from secrets import randbelow
from passlib.hash import argon2
from datetime import timedelta, datetime
from fastapi import HTTPException
from Authentication.settings import settings
from email.message import EmailMessage
import smtplib
from Authentication.MongoODM import OTPdocuments,TempStage1
from typing import Type
from Authentication.DuplicatedOpreations import delHandler, insertHandler, fetch

async def insertOTP(username: str, email: str):
    """Generates an OTP, sends it by email, hashes it, and stores it in the database."""
    OTP = str(randbelow(100000)).zfill(6)
    await SendMail(OTP, email)
    hashedOTP = argon2.hash(OTP)
    expire_time = datetime.utcnow() + timedelta(minutes=10)
    await insertHandler(
        OTPdocuments,
        False,
        username=username,
        hashedOTP=hashedOTP,
        expireAt=expire_time
    )

async def SendMail(OTP: str, targetEmail: str):
    """Sends the OTP code via email."""
    msg = EmailMessage()
    msg.set_content(f"Your OTP is {OTP}. Do not share it with anyone. It expires in 5 minutes.")
    msg["Subject"] = "Your OTP Code"
    msg["From"] = "arsiconanony@gmail.com"
    msg["To"] = targetEmail
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("arsiconanony@gmail.com", settings.app_password)
        smtp.send_message(msg)

async def verifyOTP(userOTP: str, username: Type[str]):
    """Verifies the provided OTP against the stored hashed OTP."""
    if data:= await fetch(OTPdocuments,username=username):
        try:
            if argon2.verify(userOTP, data.get('hashedOTP')):
                await delHandler(TempStage1,username=username)
                await delHandler(OTPdocuments,username=username)
            else:
                raise HTTPException(status_code=401, detail="Invalid OTP")
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"OTP verification failed{str(e)}")
    else:
        raise HTTPException(status_code=404, detail="OTP not found")
