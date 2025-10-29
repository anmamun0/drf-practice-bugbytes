# Django REST Framework - Django Redis
**Date:** 29 October 2025  
 
--- 

## Useful Resources Django  
 

- **Installation Process** : [github.com/redis/redis](https://github.com/redis/redis)
- **Web Guid** : [redis.io](https://redis.io/)
- **Install For (Windows User)** [my-blog](#for-you-windows-user)
<br> 
  
## What is Redis?

Redis is an in-memory data store and key-value database.
In-memory means data is stored in RAM, so it’s super fast.
Key-value store works like a Python dictionary — you get a value by its key.
Redis is commonly used as a cache, session store, message broker, or for real-time data.



### Key Features of Redis

| Feature                    | Description                                                   |
| -------------------------- | ------------------------------------------------------------- |
| **Fast**                 | Data is in RAM, so read/write operations are extremely fast.  |
| **Persistence Options** | Can save data to disk with snapshots or append-only files.    |
| **Key-Value Store**     | Access data via keys, like a dictionary.                      |
| **TTL Support**         | Keys can have expiration times (auto-delete after some time). |
| **Pub/Sub**             | Supports publish-subscribe for real-time messaging.           |
| **Atomic Operations**   | Commands are atomic — executed completely or not at all.      |


### Common Use Cases


<h6>


| Use Case                              | Explanation                                                                                             |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **1. Caching**                        | Store frequently accessed data in memory (e.g., query results, HTML fragments) to reduce database load. |
| **2. Session Store**                  | Store Django or Flask session data in Redis instead of database or cookies.                             |
| **3. Celery / Task Queue**            | Acts as a broker for background tasks (Celery), and optionally stores task results.                     |
| **4. Throttling / Rate Limiting**     | Keep counters for API requests per user/IP. DRF or custom code can check Redis for limits.              |
| **5. Real-Time Messaging (Pub/Sub)**  | Chat apps, notifications, live feeds, or multiplayer games can publish/subscribe messages via Redis.    |
| **6. Leaderboards / Counters**        | Keep live counters or rankings (e.g., top scores) using Redis sorted sets.                              |
| **7. Queues / Streams**               | Build job queues, event streams, or logs with Redis lists or streams.                                   |
| **8. Distributed Locking**            | Coordinate multiple processes safely with Redis locks.                                                  |
| **9. Feature Flags / Temporary Data** | Store short-lived data like OTPs, verification codes, or feature toggles.                               |
| **10. Analytics / Metrics**           | Count events, track active users, or generate real-time stats quickly.                                  |


</h6>

---

## Using Redis in Django

`Cache backend` — store frequently accessed data.
`Session backend` — keep session data in Redis.
`Celery broker/backend` — for background task queue.
`Django Channels` — real-time WebSocket communication.




### Development Example (Caching)
```py
# settings.py
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```




### Redis for Celery (Task Queue)
```py
# settings.py
# celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core", broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/0")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
```
Start Celery Worker
```sh
celery -A core worker --loglevel=info
```


### Redis for DRF Throttling
```py
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '5/minute',   # authenticated user
        'anon': '2/minute',   # anonymous user
    },
    'DEFAULT_CACHE_ALIAS': 'default',  # tells DRF to use Redis cache
}
```

---
<br>
<br>
<br>
<br>




 
 


# Redis Without Docker — 3 Common Ways

| Method                                   | Description                                                                       | Use Case                                                                  |
| ---------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **1. Native Installation (Recommended)** | Install Redis directly on your system (Windows, Linux, macOS).                    | Local development or production servers.                                  |
| **2. Using Docker**                      | Run Redis inside a container (easy isolation).                                    | When you want isolated environments or are deploying with Docker Compose. |
| **3. Using Cloud Service**               | Use managed Redis from cloud providers (like Redis Cloud, AWS ElastiCache, etc.). | For production where you don’t want to manage Redis manually.             |

<br>

#  For You (Windows User)
> You can install Redis natively, no Docker needed at all.

##  Option 1: Manual install
Download from GitHub: [github.com/tporadowski/redis/releases](https://github.com/tporadowski/redis/releases)
`Extract zip` → `open folder` → `run`:
```sh
redis-server.exe
```

> (end)
---
<br>

## Option 2: Install Redis with Scoop (Windows Package Manager)

- `Scoop` is a command-line installer for Windows. It's similar to `apt` on `Linux` or `brew` on `macOS`. 
- With Scoop, you can easily install, update, and manage programs, tools, and libraries entirely from the command line.

  
### Step 1: Run this in PowerShell (as Administrator) 
```sh
Set-ExecutionPolicy RemoteSigned -scope CurrentUser
irm get.scoop.sh | iex
```

### Step 2: Install Redis
Now run:
```sh
scoop install redis
```
After installation, start Redis: ✅
```sh
redis-server
```
- You should see something like:
- `[12345] *` Ready to accept connections
- That means Redis is running `successfully `


### Step 3: Test Redis
In another PowerShell window:
```sh
redis-cli
```

Then type:
```sh
ping
```

You should get:
```sh
PONG
```
- `PING` is a command in Redis to check if the server is alive.
- `PONG` is the response from Redis saying
```sh
$ redis-cli
127.0.0.1:6379> ping
PONG
127.0.0.1:6379> set name "AN Mamun"
OK
127.0.0.1:6379> get name
"AN Mamun"
```
### Step 4: Connect Django or Celery
You can now safely use:
```py
"LOCATION": "redis://127.0.0.1:6379/1"
```
> Would you like me to show how to make Redis automatically start every time your PC boots up (so you don’t need to run redis-server manually each time)?


--- 

> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)