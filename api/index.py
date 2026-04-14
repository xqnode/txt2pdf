from fastapi import FastAPI
# 导入你原来的逻辑
# from .convert import some_function
# from .merge import some_other_function

app = FastAPI()

@app.get("/api/convert")
def convert():
    return {"message": "conversion logic here"}

@app.get("/api/merge")
def merge():
    return {"message": "merge logic here"}