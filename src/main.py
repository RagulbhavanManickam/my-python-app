from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Python CI/CD Pipeline! v2"}

@app.get("/health")
def health():
    return {"status": "healthy"}
