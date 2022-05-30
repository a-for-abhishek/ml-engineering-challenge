import dill
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

class X(BaseModel):
    input: float = 0.1

class X_arr(BaseModel):
    input: List[float] = []

app = FastAPI()

model = dill.load(open('slr.pkl', 'rb'))


@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.post("/stream/")
async def stream(diabetes_x: X):
    input = float(diabetes_x.input)
    # print ([input])
    output = model.predict(input)
    output = output.flatten()[0]
    # diabetes_X[:, np.newaxis, 2]
    return {"result": str(output)}

@app.post("/batch/")
async def batch(diabetes_x_arr: X_arr):
    prediction = []
    for x in diabetes_x_arr.input:
        output = model.predict(float(x))
        output = output.flatten()[0]
        prediction.append(output)
    # print (out)
    # diabetes_X[:, np.newaxis, 2]
    return {"result": str(prediction)}

if __name__ == '__main__':
    uvicorn.run(app)