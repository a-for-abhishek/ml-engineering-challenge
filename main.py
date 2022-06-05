import dill
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from auth import AuthHandler
import uvicorn
import random
import time

class X(BaseModel):
    input: float = 0.1

class X_arr(BaseModel):
    input: List[float] = []

class AuthDetails(BaseModel):
    username: str
    password: str

app = FastAPI()

auth_handler = AuthHandler()

model = dill.load(open('slr.pkl', 'rb'))

users = [{'username': 'abi', 'password': '$2b$12$vfX17MZ4F1udDGiZN6GRguDC1PDe8iawTilayLm8g1daF9eHl0yEK'}]

@app.get("/")
async def root():
    return {"message": "Welcome to Linear Regression API"}

@app.get("/get_model_details")
async def get_model_details():
    return {"learning rate": str(model.lr), "iterations": str(model.iterations)}

@app.get("/is-it-working")
async def is_it_working():
    start = time.time()
    input = random.uniform(50.51, 145.78)
    output = model.predict(input)
    output = output.flatten()[0]
    return {"message": "Made a test call for you!", "input": str(input),
            "output": str(output), "timetaken in ms": str((time.time() - start) * 1000)}

@app.post("/stream/")
async def stream(diabetes_x: X, username=Depends(auth_handler.auth_wrapper)):
    start = time.time()
    input = float(diabetes_x.input)
    output = model.predict(input)
    output = output.flatten()[0]
    return {"result": str(output), "timetaken in ms": str((time.time() - start) * 1000), "caller": username}

@app.post("/batch/")
async def batch(diabetes_x_arr: X_arr, username=Depends(auth_handler.auth_wrapper)):
    start = time.time()
    prediction = []
    for x in diabetes_x_arr.input:
        output = model.predict(float(x))
        output = output.flatten()[0]
        prediction.append(output)
    # print (out)
    # diabetes_X[:, np.newaxis, 2]
    return {"result": str(prediction), "timetaken in ms": str((time.time() - start) * 1000), "caller": username}

@app.post("/stream/predict_class/")
async def stream_class(diabetes_x: X, username=Depends(auth_handler.auth_wrapper)):
    start = time.time()
    input = float(diabetes_x.input)
    output = model.predict(input)
    output = output.flatten()[0]
    if output > 0.5:
        out_class = 'Class0.51-1'
    else:
        out_class = 'Class0-0.5'
    return {"result": str(output), "result_class": out_class, "timetaken in ms": str((time.time() - start) * 1000)
        , "caller": username}

# @app.post('/register', status_code=201)
# def register(auth_details: AuthDetails):
#     if any(x['username'] == auth_details.username for x in users):
#         raise HTTPException(status_code=400, detail='Username is taken')
#     hashed_password = auth_handler.hash_it(auth_details.password)
#     print (hashed_password)
#     users.append({
#         'username': auth_details.username,
#         'password': hashed_password
#     })
#     return

@app.post('/token')
def token(auth_details: AuthDetails):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break

    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token, ttl = auth_handler.encode_token(user['username'])
    return {'token': token, 'expires_on': ttl}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)