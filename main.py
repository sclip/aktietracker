from aktietracker import create_app, db
from aktietracker import models


app = create_app()


def main():
    # create_db()
    app.run(debug=True)
    # app.run(debug=True, host="0.0.0.0")
    # host="0.0.0.0"


def create_db():
    with app.app_context():
        db.drop_all()
        db.create_all()


if __name__ == '__main__':
    main()
