from fastapi.responses import JSONResponse
from sql_app.database import SessionLocal

def create_response(status_code=200, data=[], errors=[], success=True, message=""):
    return JSONResponse(status_code=status_code, content={"message": message, "success": success, 
    "data": data, "errors": errors}, headers={"Access-Control-Allow-Origin": "*"})

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()