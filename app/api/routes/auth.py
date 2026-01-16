from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get("/")
def auth_ping():
    return {"message": "auth router funcionando"}
