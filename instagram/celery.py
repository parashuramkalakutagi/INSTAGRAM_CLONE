from __future__ import absolute_import ,unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE','instagram.settings')
app = Celery('instagram')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings,namespace='CELERY')

app.autodiscover_tasks()

#celery beat


# scheduled to delete object on particular time
app.conf.beat_schedule = {
    'delete-stories-after-24hours':{
        'task':'core.tasks.delete_old_story',
        'schedule':crontab(hour='*',minute='*/2'),
    }

}


@app.task(bind = True)
def debug_task(self):
    print(f'Request : {self.request!r}')