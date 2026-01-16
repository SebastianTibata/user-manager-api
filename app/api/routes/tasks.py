from fastapi import APIRouter

router = APIRouter(
    prefix = "/tasks",
    tags = ["tasks"]
)

@router.get("/")
def tasks_ping():
    return {"message":"task router funcionando"}