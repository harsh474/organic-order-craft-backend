from fastapi import APIRouter
router = APIRouter(prefix="/order", tags=["order"])

@router.post("/create_order")
def create(order_details:OrderCreate, session: Session = Depends(get_session)):  
     
     

