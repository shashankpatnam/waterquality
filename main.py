from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import pickle
import numpy
import pandas
import gunicorn

class model(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float

pickle_in = open("class.pkl", "rb")
cls = pickle.load(pickle_in)

pickle_in2 = open("random_cls.pkl", "rb")
cls1 = pickle.load(pickle_in2)

def predic(df, num :int):
    if(num==1):
        return cls1.predict(df)
    else:
        return cls.predict(df)

myApp = FastAPI()

@myApp.get("/")
def homeFunction():
    return "Hello"

@myApp.post("/water_quality")
def getStudent(quer : model, mdl : int):
    query = quer.dict()
    parameters = [[query['ph'],query['Hardness'],query['Solids'],query['Chloramines'],query['Sulfate'],query['Conductivity'],query['Organic_carbon'],query['Trihalomethanes'],query['Turbidity']]]
    arr = numpy.array(parameters, dtype=float)
    columns = []
    for i in query.keys():
        columns.append(i)
    df = pandas.DataFrame(arr, columns=columns)
    output = predic(df, mdl)
    if(output[0]==1):
        return "Safe to drink"
    else:
        return "Unsafe to drink"

# gunicorn -w 4 -k uvicorn.workers.UvicornWorker mai:myApp
#uvicorn.run(myApp)
