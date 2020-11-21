import asyncio 
import os 
import datetime
import time
from dotenv import load_dotenv

async def sleep_async(seconds):
    print(f"Sleeping for {seconds} seconds.")
    await asyncio.sleep(seconds)

def getEnvVar(tag):
    load_dotenv()
    return os.getenv(tag)

def utcnow():
    return datetime.datetime.utcnow()

def utcnowtimestamp():
    return utcnow().timestamp()

def MakeDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)