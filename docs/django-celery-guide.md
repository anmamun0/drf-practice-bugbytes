# Django REST Framework - Django + Celery Guide
**Date:** 29 October 2025  
 
---
Celery is an asynchronous task queue that allows Django to perform background tasks like sending emails, generating reports, or handling long-running processes.
Redis is commonly used as a message broker and result backend for Celery.


## Useful Resources Django  
 

- **Official Github Guidline** : [github.com/celery/celery](https://github.com/celery/celery)
- **Use Guidline Celery** : [sing-celery-with-django](https://docs.celeryq.dev/en/main/django/first-steps-with-django.html#using-celery-with-django)
- **Celery Docs** : [docs.celeryq.dev/en/stable](https://docs.celeryq.dev/en/stable/)
- **Django Celery Docs**: [docs.celeryq.dev/en/stable/django](https://docs.celeryq.dev/en/stable/django/)


**Practice Code** : [Implement Celery ](https://github.com/anmamun0/drf-practice-BugBytes/commit/70272ba6b7ff8f6f92246dabe6734374725c9fd2) <br>  
 
  
--- 
  

# 1. Installation
Install Celery and Redis
```sh
pip install celery[redis]
pip install redis

```
**Redis Installing Guidline** : [ my-blog](https://github.com/anmamun0/drf-practice-BugBytes/edit/main/docs/django_redis_guide.md) (`!important`)

Optional (for monitoring tast)
```sh
pip install flower
celery -A core flower
```   
**Go to** : [localhost:5555](http://localhost:5555)

> ( end )
---
<br>
<br>



# 2. Django Settings
`settings.py`
```py
# Redis configuration
CELERY_BROKER_URL = "redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/1"

# Optional: task serialization and timezone
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
```

> ( end )
---
<br>
<br>

  
# 3. Run Celery Worker in production (Deployment)

Open a terminal and run: Concurrency pools (`prefork` , `solo`,` eventlet`, gevent`)

### Windows

### 1. Use the solo pool on Windows

The simplest fix is to run Celery with the solo pool (single-threaded):
```sh
celery -A myproject worker --loglevel=INFO -P solo
```
Works fine for development/testing, not recommended for production

- `-A myproject` → Celery project-name
- `worker` → worker process run
- `-l` info → show log
- `-P solo` → avoids the prefork issue on Windows

### 2. Use eventlet or gevent pools (optional)

Install eventlet:
```sh
pip install eventlet
```
Run Celery with eventlet:
```sh
celery -A core worker --loglevel=INFO -P eventlet
```
- This allows concurrent async tasks on Windows


## MacOs:

```sh
celery -A core worker --loglevel=INFO
```
### Run on Linux / WSL / Docker (Recommended for production)

- `Celery` + `Redis` works best on `Linux`
- On `Windows`, you may encounter concurrency issues
- Use Windows Subsystem for `Linux (WSL)` or a `Docker` container to run `Celery` properly



> ( end )
---
<br>
<br>


# 4. Use Case

project blue print
```sh
- proj/
  - manage.py
  - proj/
    - __init__.py
    - settings.py
    - celery.py
    - urls.py
  - app1/
      - tasks.py
      - models.py 
      - views.py 
```


`proj/proj/celery.py`
```py
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

 
`proj/proj/__init__.py`
```py
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
```


`app1/tasks.py`

```py
import logging
import time
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task
def send_email_task():
    logger.info("Sending email...")
    time.sleep(5)
    logger.info("Email sent successfully!")

shared_task
def add(x, y):
    return x + y
```

`app1/views.py`

```py
from .tasks import send_email_task
from rest_framework import generics
class UserListView(generics.ListAPIView): 
    queryset = User.objects.all()
    serializer_class = UserSerializer 

    def list(self, request, *args, **kwargs):
        send_email_task.delay()  # useing celery
        return super().list(request, *args, **kwargs)
```



> ( end )
---
<br>
<br>


# 5. Celery Task Invocation Methods in `views.py`
Celery provides multiple ways to call tasks asynchronously. The most commonly used are:

`.delay()`, `.apply_async()`, `.apply()` (synchronous, for testing)

<h6> 
 
| Method           | Async? | Use Case                             |
| ---------------- | ------ | ------------------------------------ |
| `.delay()`       | Yes  | Simple async call, shortcut          |
| `.apply_async()` | Yes  | Advanced async call with options     |
| `.apply()`       | No   | Synchronous call (testing/debugging) |
</h6>

### 1. `.delay()`

Simplest way to call a Celery task.
Arguments are passed directly like a normal function.
Returns an AsyncResult object, which can be used to check status or get the result.
 
`tasks.py`
```py
from celery import shared_task
import time

@shared_task
def add(x, y):
    time.sleep(2)
    return x + y
```
`views.py`
```py
from api.tasks import add

# Call task asynchronously
result = add.delay(5, 10)

# Check task ID
print(result.id)

# Check if task is done
print(result.ready())

# Get result (blocks until done)
print(result.get())
```


- `.delay(*args, **kwargs)` → shortcut for `task.apply_async(args, kwargs)`
- Runs in the background, doesn’t block your Django request.


### 2. `.apply_async()`
More advanced, allows you to configure schedules, countdown, retries, queues, etc.

```py
from api.tasks import add

# Run after 10 seconds
result = add.apply_async((5, 10), countdown=10)

# Run in specific queue
result = add.apply_async((5, 10), queue='high_priority')

# Retry in 30 seconds if failed
result = add.apply_async((5, 10), retry=True, retry_policy={
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 10,
    'interval_max': 30,
})
```

- `.apply_async()` gives full control over task execution.
- `.delay()` is just a shortcut for .apply_async(args, kwargs).


### 3. `.apply()`

- Synchronous execution, runs locally in the same process (blocking).
- Useful for testing tasks without running Celery worker.
```py
from api.tasks import add

# Run synchronously
result = add.apply((5, 10))
print(result.get())  # prints 15
```
- `.apply()` does not go to Celery worker.
- Not used in production for async tasks.


> ( end )
---
<br>
<br>

# 5. Celery Task Invocation Methods in `tasks.py`

<h6>

| Level               | Use Case                                        |
| ------------------- | ----------------------------------------------- |
| `logger.debug()`    | Detailed info for debugging                     |
| `logger.info()`     | Normal operational messages                     |
| `logger.warning()`  | Something unexpected happened, but not an error |
| `logger.error()`    | Error occurred in task                          |
| `logger.critical()` | Severe errors, critical failures                |
</h6>

 
`tasks.py`
```py
from celery import shared_task
import logging
import time

# Get a logger
logger = logging.getLogger(__name__)

@shared_task
def send_email_task():
    logger.info("Task started: sending email...")
    time.sleep(5)  # simulate sending email
    logger.info("Email sent successfully!")
 ```

Optional: Logging to File
`settings.py`
```py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'celery_tasks.log',
        },
    },
    'loggers': {
        'api.tasks': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```
Now all logs from api.tasks will be written to celery_tasks.log.


--- 

> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)