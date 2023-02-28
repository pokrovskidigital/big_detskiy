from app.configuration.routes.routes import *
from app.internal.routes import user, auth, catalog, utils
# from app.internal.routes import catalog

__routes__ = Routes(routers=(user.router, auth.router, catalog.router,utils.router))
