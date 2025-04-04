from fastapi import FastAPI
from dashboard.api.routes import measurements
from dashboard.api.routes import weather

app = FastAPI(title="Environmental Monitoring API")

app.include_router(measurements.router, prefix="/measurements", tags=["Measurements"])
app.include_router(weather.router, prefix="/weather", tags=["Weather"])

@app.get("/")
def root():
    return {"status": "API is running"}
