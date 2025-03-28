from __init__ import create_app
# from tasks.celery import make_celery


app = create_app()
# celery = make_celery(app)

if __name__ == '__main__':
    with app.app_context():
        from extensions import db
        db.create_all()
    app.run(debug=True)



