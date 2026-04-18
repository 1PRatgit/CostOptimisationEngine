from fastapi import FastAPI
from api.routes import router
import uvicorn

app = FastAPI(title="Cost Optimisation Engine",
                  description="API for estimating costs based on various parameters",
                  version="1.0.0",
                  docs_url="/docs",
       redoc_url="/redoc",
                )

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
