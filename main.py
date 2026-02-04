from fastapi import FastAPI, HTTPException, Path, Query, Depends, Body
from typing import Optional
from sqlalchemy.orm import Session

app = FastAPI()