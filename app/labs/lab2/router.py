from fastapi import APIRouter, HTTPException, BackgroundTasks
import asyncio
import time
import httpx
from datetime import date, datetime


router = APIRouter(prefix="/lab2", tags=["Lab2 "])

