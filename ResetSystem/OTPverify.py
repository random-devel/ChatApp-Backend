from secrets import randbelow
from passlib.hash import argon2
from datetime import timedelta, datetime
from fastapi import HTTPException
from Authentication.settings import settings
from Authentication.MongoODM import OTPdocuments,TempStage1
from typing import Type
from Authentication.DuplicatedOpreations import delHandler, insertHandler, fetch
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr , SecretStr
from .Models import INSERTotp, SendMails, VerifyOTP

conf = ConnectionConfig(
    MAIL_USERNAME=settings.email,
    MAIL_PASSWORD= SecretStr(settings.app_password) ,
    MAIL_FROM=settings.email,
    MAIL_PORT=587,
    MAIL_SERVER=settings.email_provider,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

mail = FastMail(conf)


async def insertOTP(data: INSERTotp):

    OTP = str(randbelow(100000)).zfill(6)
    hashedOTP = argon2.hash(OTP)
    expire_time = datetime.utcnow() + timedelta(minutes=10)
    try:
        await insertHandler(
            OTPdocuments,
            False,
            username=data.username,
            hashedOTP=hashedOTP,
            expireAt=expire_time
        )
    except Exception:
        raise HTTPException(501, detail='failed to insert the otp')
    try:
        await SendMail(SendMails(OTP=OTP, TargetMail=data.email))
    except Exception as e:
        raise HTTPException(501, detail=f'failed to send the otp: {str(e)}')

async def SendMail(data: SendMails):
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #0d1117;
            color: #c9d1d9;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 500px;
            margin: auto;
            background: #161b22;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }}
        h2 {{
            color: #58a6ff;
        }}
        .otp-box {{
            background-color: #238636;
            color: #fff;
            padding: 12px 20px;
            border-radius: 8px;
            display: inline-block;
            font-size: 20px;
            font-weight: bold;
            letter-spacing: 3px;
            margin: 15px 0;
        }}
        .note {{
            margin-top: 20px;
            font-size: 14px;
            color: #8b949e;
        }}
        </style>
    </head>
    <body>
        <div class="container">
        <h2>Password Reset Request</h2>
        <p>Hello 👋,</p>
        <p>We received a request to reset your password. Here is your OTP:</p>
        <div class="otp-box">{data.OTP}</div>
        <p>Please use this OTP to reset your password.</p>
        <p class="note">If you did not request this, you can ignore this email.</p>
        </div>
    </body>
    </html>
    """

    mailMessage = MessageSchema(
        recipients=[data.TargetMail],
        subject='Password Reset OTP',
        body=html_body,
        subtype=MessageType.html
    )

    await mail.send_message(mailMessage)


async def verifyOTP(data: VerifyOTP):
    """Verifies the provided OTP against the stored hashed OTP."""
    if fetched_data:= await fetch(OTPdocuments,username=data.username):
        try:
            if argon2.verify(data.otp, fetched_data.get('hashedOTP')):
                await delHandler(TempStage1,username=data.username)
                await delHandler(OTPdocuments,username=data.username)
            else:
                raise HTTPException(status_code=401, detail="Invalid OTP")
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"OTP verification failed{str(e)}")
    else:
        raise HTTPException(status_code=404, detail="OTP not found")
