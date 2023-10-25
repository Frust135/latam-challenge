import fastapi
from challenge.model import DelayModel

app = fastapi.FastAPI()

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(data: dict) -> dict:
    try:
        predicts = []
        model = DelayModel()
        flights = data["flights"]
        for flight in flights:
            if flight["TIPOVUELO"] not in ["N", "I"]:
                raise Exception("Invalid TIPOVUELO")
            if flight["MES"] not in range(1, 13):
                raise Exception("Invalid MES")
            features = model.preprocess(flight)
            prediction = model.predict(features)
            predicts.append(prediction[0])
        return {
            "predict": predicts
        }
    except Exception as e:
        return fastapi.Response(content=str(e), status_code=400)