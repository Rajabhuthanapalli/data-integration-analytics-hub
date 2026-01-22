from fastapi import FastAPI

app = FastAPI(title="Smart Task & Productivity Manager")

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Task & Productivity Manager"}
