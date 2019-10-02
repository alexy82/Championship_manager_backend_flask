from app import create_app
application = create_app()
application.app_context().push()

if __name__ == "__main__":

    application.run()

from app.core.models import db_session


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
