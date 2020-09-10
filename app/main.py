from app import server
from app.application import app
from app.routes import health, v1


app.include_router(health.router)
app.include_router(v1.get_router(), prefix="/v1")


def run():
    server.run(app)


if __name__ == "__main__":
    server.debug(app)
