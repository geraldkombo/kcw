from api.routes.farmers import router as farmers_router
from api.routes.loans import router as loans_router
from api.routes.payments import router as payments_router
from api.routes.securitisation import router as securitisation_router

__all__ = ["farmers_router", "loans_router", "payments_router", "securitisation_router"]
