from fastapi import FastAPI
from routers.transcript import transcript_router
app = FastAPI()

app.include_router(transcript_router.router)

@app.get("/")
def main():
    return{"Transcript":"Transcript"}



 
