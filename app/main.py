from fastapi import FastAPI
import logging

from app.core import lifespan
from app.controllers.pages import page_controller
from app.controllers.api import auth_controller
from app.controllers.api import user_controller

from app.core.middlewares import cors_middleware
from app.core.middlewares import static_middleware
from app.core.security import rate_limiter
from app.core.security import csrf
from app.exceptions import handler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# apps
app = FastAPI(
    title="IFAM Sistema de Gerenciamento",
    description="API para o Sistema de Gerenciamento de Salas do IFAM",
    version="1.0.0",
    lifespan=lifespan.lifespan
) # jinja2 templates

api = FastAPI(
    title="IFAM API",
    description="API para o Sistema de Gerenciamento de Salas do IFAM",
    version="1.0.0",
    lifespan=lifespan.lifespan
) # api for json

# custom exception handlers
handler.add_html(app)
handler.add_json(api)

# add security middlewares to main app
static_middleware.add(app)  # Serve static files
cors_middleware.add(app)    # CORS protection for main app
cors_middleware.add(api)    # CORS protection for API
rate_limiter.apply_rate_limiting(app)  # Rate limiting
csrf.apply_csrf_middleware(app)  # CSRF protection

# Log application startup
logger.info("Starting IFAM Sistema de Gerenciamento with enhanced security features")
logger.info("Applied security: CORS, Rate Limiting, CSRF Protection, Secure Cookies")

# include page routers
app.include_router(page_controller.router)

# include api routers
api.include_router(auth_controller.router)
api.include_router(user_controller.router)

# mount api app
app.mount("/api", api)
