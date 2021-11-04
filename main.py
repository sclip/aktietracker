from aktietracker import create_app, db
from aktietracker import models


app = create_app()


def main():
    # create_db()
    app.run(debug=True)


def create_db():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    main()
