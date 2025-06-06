import os
from flask import Flask
from celery import Celery, Task

def celery_init_app(app:Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery_app = None
    if os.name == "posix":
        celery_app = Celery(app.name, task_cls=FlaskTask)
        celery_app.config_from_object(app.config["CELERY"])
        celery_app.set_default()
    else:
        celery_app = Celery(app.name)
        celery_app.config_from_object(app.config["CELERY"])
        celery_app.set_default()
        celery_app.Task = FlaskTask

    app.extensions["celery"] = celery_app

    return celery_app