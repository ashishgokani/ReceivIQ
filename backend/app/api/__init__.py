"""
API package router bundle.
"""
from fastapi import APIRouter
from app.api.routes_invoices import router as invoices_router
from app.api.routes_customers import router as customers_router
from app.api.routes_agent import router as agent_router
from app.api.routes_approvals import router as approvals_router
from app.api.routes_simulation import router as simulation_router
from app.api.routes_analytics import router as analytics_router
from app.api.routes_automation import router as automation_router
from app.api.routes_settings import router as settings_router
from app.api.routes_activity import router as activity_router

api_router = APIRouter()
api_router.include_router(invoices_router)
api_router.include_router(customers_router)
api_router.include_router(agent_router)
api_router.include_router(activity_router)
api_router.include_router(approvals_router)
api_router.include_router(simulation_router)
api_router.include_router(analytics_router)
api_router.include_router(automation_router)
api_router.include_router(settings_router)

