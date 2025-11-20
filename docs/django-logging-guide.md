# Django REST Framework - Logging Report
**Date:** 20 November 2025  
 
---

> Django uses Python's built-in `logging` module. The logging system has four main components:
- **logging Doc** : [djoser.readthedocs.io](https://docs.djangoproject.com/en/5.2/topics/logging/)
 

     

### Table of Contents 
1. [Logging `Handlers` Explained](#1-logging-handlers-explained)
2. [Logging `Formatters`](#2-logging-formatters)
3. [Django Settings `Configuration`](#3-django-settings-configuration)
4. [REST API Request Logging](#4-rest-api-request-logging)
5. [Practical Use Cases](#5-practical-use-cases)

--- 


To track what is happening inside your application useing logging file. `To debug problems`, `To monitor system health`, `To detect security issues`, `To maintain audit trail`, `To analyze user behavior`, `To alert administrators`, `To rotate and manage log files`, `To record exceptions`
 
- **Loggers**: Entry point for logging messages
- **Handlers**: Determine where log messages go
- **Filters**: Control which log records get processed
- **Formatters**: Define the structure of log messages


### In short
**Logging** = *Memory of your backend.*
- Without logs, you are blind.
- With logs, you can debug, monitor, analyze, and secure your system.**

---






## 1. Logging Handlers Explained 

<h6>

| Handler Name          | Module           | Purpose              | When to Use         | Key Parameters     | Example Use Case    |
| ------------ | ---------------- | --------------- | ------------------------ | --------------------------- | ---------------------- |
| **FileHandler**  [Go](#1-loggingfilehandler)     | logging          | Writes logs to a file                                             | General file logging                      | `filename`, `mode`, `encoding`               | Django API logs, server logs      |
| **StreamHandler**   [GO](#2-loggingstreamhandler)  | logging          | Sends logs to streams (console, stderr, stdout)                   | Development, debugging                    | `stream`                                     | Print logs in console             |
| **SMTPHandler**    [GO](#3-logginghandlerssmtphandler) | logging.handlers | Sends logs via email                                              | CRITICAL alerts                           | `mailhost`, `fromaddr`, `toaddrs`, `subject` | Critical server errors            |
| **NullHandler**   [GO](#4-loggingnullhandler) | logging          | Discards all log records                                          | For libraries to avoid “no handler found” | None                                         | Third-party libraries             |
| **RotatingFileHandler** [GO](#5-logginghandlersrotatingfilehandler) | logging.handlers | Rotates log file when it reaches a size                           | Prevent unlimited growth                  | `maxBytes`, `backupCount`                    | API logs, request logs            |
| **TimedRotatingFileHandler**  [GO](#6-logginghandlerstimedrotatingfilehandler)   | logging.handlers | Time-based rotation                                               | Daily logs                                | `when`, `interval`                           | Audit logs                        |
| **WatchedFileHandler**                        | logging.handlers | Watches log file; reopens if rotated externally (Linux logrotate) | Production Linux systems                  | `filename`                                   | Works well with Linux `logrotate` |
| **TimedRotatingFileHandler**                  | logging.handlers | Rotates logs based on time (daily, hourly, etc.)                  | Daily/weekly log rotation                 | `when`, `interval`, `backupCount`            | Daily audit logs                  |
| **SocketHandler**                             | logging.handlers | Sends logs over TCP sockets                                       | Distributed logging systems               | `host`, `port`                               | Microservice logging              |
| **DatagramHandler**                           | logging.handlers | Sends logs using UDP datagrams                                    | Faster, fire-and-forget logging           | `host`, `port`                               | Logging to UDP collectors         |
| **SysLogHandler**                             | logging.handlers | Sends logs to Unix syslog                                         | Linux servers                             | `address`, `facility`                        | System-level logs                 |
| **NTEventLogHandler**                         | logging.handlers | Sends logs to Windows Event Log                                   | Windows servers                           | `appname`, `logtype`                         | Windows production servers        |
| **HTTPHandler**                               | logging.handlers | Sends logs via HTTP GET/POST                                      | Central log collector via API             | `host`, `url`, `method`                      | Remote monitoring                 |
| **MemoryHandler**                             | logging.handlers | Stores logs in memory and flushes when full                       | Performance optimization                  | `capacity`, `flushLevel`, `target`           | High-load applications            |
| **QueueHandler**                              | logging.handlers | Sends logs to a queue (thread-safe)                               | Multithreading/multiprocessing            | `queue`                                      | Async logging                     |
| **QueueListener** (NOT a handler but related) | logging.handlers | Listens to a queue and dispatches logs                            | Background async logging                  | `handlers`                                   | For multiprocessing logs          |
| **BufferingHandler**                          | logging.handlers | Base class for buffered handlers                                  | Custom buffered logging                   | `capacity`                                   | Custom buffers                    |
| **MemoryHandler (subclass)**                  | logging.handlers | Logs buffered and flushes to another handler                      | Temporary storage                         | `target`                                     | Burst logging                     |
| **BaseRotatingHandler**                       | logging.handlers | Abstract class for rotating handlers                              | Not used directly                         | —                                            | Parent for rotating handlers      |

</h6>

---

<br>
<br>
<br>


### 1. logging.FileHandler

Writes log messages to a file on disk. To permanently store logs. Good for request logs, error logs, audit logs.
**Use Case**: Permanent storage of application logs for debugging and auditing.

```python
import os
BASE_DIR = Path(__file__).resolve().parent.parent
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {name} | {message}",
            "style": "{",
        },
    },
    # The handler tells where the log will be written (file, console, email, etc.) and from which level to start. 
    # and will save the log messages to a file.
    'handlers': {
        'filehandler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            "filename": os.path.join(BASE_DIR, "logs", "api.log"),
            'formatter': 'verbose',
        },
    },

    # Where log messages are generated from
    'loggers': {
        'django': {
            'handlers': ['filehandler'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

```py
import logging
import json

api_logger = logging.getLogger("api_logger")
api_logger.info(
    json.dumps({
        "method": request.method,
        "path": request.path,
        "user": str(user),
        "headers": dict(request.headers),
        "body": request.body.decode("utf-8", errors="ignore"),
    })
)

```

**Pros**: Simple, persistent storage <br>
**Cons**: Can grow indefinitely without rotation

- `version: 1`
This represents the version number of the Python logging configuration schema.
We always keep it as 1 because it is the standard and only supported version.

- `disable_existing_loggers: False`
This setting controls whether existing loggers (created by Django or installed libraries) should be disabled.
  - `False` → existing loggers remain active
  - `True` → Django’s default loggers would be disabled <br>
We keep it False so that Django's built-in logging system continues working along with our custom logging.

- `formatters`
Formatters define how each log line will look.

 
---

<br>
<br>





### 2. logging.StreamHandler

Sends log messages to streams like such as console `sys.stdout` or `sys.stderr`. 
**Use Case**: Development environments, Docker containers where logs are captured from stdout. Development environments, Docker logs, Debug mode

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

**Pros**: Immediate visibility, works well with container orchestration
**Cons**: No persistence, can clutter terminal

---

<br>
<br>


### 3. logging.handlers.SMTPHandler

Sends log messages via email. To notify administrators about critical errors immediately.
**Use Case**: Critical errors that require immediate attention, production alerts.

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        # Or use standard SMTPHandler
        'smtp': {
            'level': 'CRITICAL',
            'class': 'logging.handlers.SMTPHandler',
            'mailhost': ('smtp.gmail.com', 587),
            'fromaddr': 'server@example.com',
            'toaddrs': ['admin@example.com'],
            'subject': 'Django Critical Error',
            'credentials': ('username', 'password'),
            'secure': (),  # Use TLS
        },
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
        },
    },
}
```

**Pros**: Immediate notification for critical issues
**Cons**: Can flood inbox, email delays, requires SMTP configuration

---

<br>
<br>


### 4. logging.NullHandler

Discards all log messages (does nothing).

**Use Case**: Libraries that want to allow users to configure logging without forcing it, silencing specific loggers.

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    },
}
```

**Use Case Example**: Silencing noisy third-party library logs during testing.

---

<br>
<br>


### 5. logging.handlers.RotatingFileHandler

Rotates log files based on size. Writes logs to a file and automatically rotates it when the file reaches a specific size.

**Use Case**: Production environments where you want to limit log file sizes.

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'rotating_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs/rotating.log"),
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,  # Keep 5 backup files
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['rotating_file'],
            'level': 'INFO',
        },
    },
}
```

**Behavior**: When `app.log` reaches 10MB, it's renamed to `app.log.1`, and a new `app.log` is created. Keeps up to 5 backups.

**Pros**: Prevents disk space issues
**Cons**: Size-based rotation may split related log entries

---

<br>
<br>


### 6. logging.handlers.TimedRotatingFileHandler

Rotates log files based on time intervals.

**Use Case**: Daily/weekly log archiving, compliance requirements for time-based log retention.

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'timed_rotating_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/django/app.log',
            'when': 'midnight',  # Rotate at midnight
            'interval': 1,  # Every 1 day
            'backupCount': 30,  # Keep 30 days
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['timed_rotating_file'],
            'level': 'INFO',
        },
    },
}
```

**Time Options**:
- `'S'` - Seconds
- `'M'` - Minutes
- `'H'` - Hours
- `'D'` - Days
- `'midnight'` - Rotate at midnight
- `'W0'`-`'W6'` - Rotate on specific weekday (0=Monday)

**Pros**: Predictable log organization, easier to archive by date
**Cons**: Files can grow large if interval is too long

---

<br>
<br>
<br>
<br>  











## 2. Logging Formatters 

Formatters define how log messages appear. Django supports various attributes:

### Simple Format
```python
'formatters': {
    'simple': {
        'format': '{levelname} {message}',
        'style': '{',
    },
}
```
**Output**: `INFO User logged in`

---

### Verbose Format
```python
'formatters': {
    'verbose': {
        'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
        'style': '{',
    },
}
```
**Output**: `INFO 2025-11-20 10:30:45,123 views 12345 67890 User logged in`

---

### JSON Format
```python
'formatters': {
    'json': {
        'format': '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "module": "%(module)s"}',
    },
}
```
**Output**: `{"time": "2025-11-20 10:30:45", "level": "INFO", "message": "User logged in", "module": "views"}`

---

### Custom Format with Request Context
```python
'formatters': {
    'custom': {
        'format': '[{asctime}] {levelname} {name} - {message}',
        'style': '{',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    },
}
```

**Available Format Attributes**:
- `{levelname}` - Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `{asctime}` - Timestamp
- `{message}` - Log message
- `{name}` - Logger name
- `{module}` - Module name
- `{funcName}` - Function name
- `{lineno}` - Line number
- `{pathname}` - Full path
- `{process}` - Process ID
- `{thread}` - Thread ID

---

<br>
<br>
<br>
<br>















## 3. Django Settings Configuration

### Production-Ready Configuration

```python
# settings.py
import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'json': {
            'format': '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "module": "%(module)s", "path": "%(pathname)s"}',
        },
    },
    
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['require_debug_true'],
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join('logs', 'django.log'),
            'when': 'midnight',
            'backupCount': 30,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('logs', 'errors.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'CRITICAL',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['error_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'myapp': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
```

---

<br>
<br>
<br>
<br>


## 4. REST API Request Logging 

### Method 1: Custom Middleware

```python
# middleware.py
import logging
import time
import json

logger = logging.getLogger('api')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Before view execution
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.path}")
        
        if request.body:
            try:
                body = json.loads(request.body)
                logger.debug(f"Request Body: {body}")
            except:
                pass
        
        # Process request
        response = self.get_response(request)
        
        # After view execution
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {request.method} {request.path} "
            f"Status: {response.status_code} Duration: {duration:.2f}s"
        )
        
        return response

    def process_exception(self, request, exception):
        logger.error(
            f"Exception: {request.method} {request.path} "
            f"Error: {str(exception)}",
            exc_info=True
        )
```

**Add to settings.py**:
```python
MIDDLEWARE = [
    'myapp.middleware.RequestLoggingMiddleware',
    # ... other middleware
]
```

---

### Method 2: Django REST Framework Logging

```python
# middleware.py
import logging
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('api.requests')

class APILoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/api/'):
            request._log_data = {
                'method': request.method,
                'path': request.path,
                'user': str(request.user) if hasattr(request, 'user') else 'Anonymous',
                'ip': self.get_client_ip(request),
            }
            
            if request.body:
                try:
                    request._log_data['body'] = json.loads(request.body)
                except:
                    request._log_data['body'] = request.body.decode('utf-8')[:200]
    
    def process_response(self, request, response):
        if hasattr(request, '_log_data'):
            log_data = request._log_data
            log_data['status_code'] = response.status_code
            
            logger.info(json.dumps(log_data))
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

---

### Method 3: DRF Custom Logger Mixin

```python
# mixins.py
import logging

logger = logging.getLogger('api.views')

class LoggingMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        
        logger.info(
            f"{request.method} {request.path} - "
            f"User: {request.user} - "
            f"Status: {response.status_code}"
        )
        
        if response.status_code >= 400:
            logger.error(
                f"Error Response: {request.method} {request.path} - "
                f"Status: {response.status_code} - "
                f"Data: {response.data}"
            )
        
        return response

# Usage in views
from rest_framework.viewsets import ModelViewSet

class UserViewSet(LoggingMixin, ModelViewSet):
    # ... your viewset code
    pass
```

---

### Method 4: Decorator-Based Logging

```python
# decorators.py
import logging
import time
from functools import wraps

logger = logging.getLogger('api.decorators')

def log_api_request(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        start_time = time.time()
        
        logger.info(f"API Call: {func.__name__} - {request.method} {request.path}")
        
        try:
            response = func(request, *args, **kwargs)
            duration = time.time() - start_time
            
            logger.info(
                f"API Success: {func.__name__} - "
                f"Status: {response.status_code} - "
                f"Duration: {duration:.2f}s"
            )
            
            return response
        except Exception as e:
            logger.error(
                f"API Error: {func.__name__} - {str(e)}",
                exc_info=True
            )
            raise
    
    return wrapper

# Usage
from django.http import JsonResponse

@log_api_request
def my_api_view(request):
    return JsonResponse({'status': 'success'})
```

---

<br>
<br>
<br>
<br>
















## 5. Practical Use Cases 

### Use Case 1: User Authentication Logging

```python
# views.py
import logging

logger = logging.getLogger('auth')

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        login(request, user)
        logger.info(f"Successful login: {username} from {request.META.get('REMOTE_ADDR')}")
        return redirect('dashboard')
    else:
        logger.warning(f"Failed login attempt: {username} from {request.META.get('REMOTE_ADDR')}")
        return render(request, 'login.html', {'error': 'Invalid credentials'})
```

**Logging Configuration**:
```python
'loggers': {
    'auth': {
        'handlers': ['file', 'error_file'],
        'level': 'INFO',
        'propagate': False,
    },
}
```

---

### Use Case 2: Database Query Performance Logging

```python
# settings.py
LOGGING = {
    # ... other config
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

This logs all SQL queries executed by Django ORM.

---

### Use Case 3: Payment Processing Logging

```python
# payment_processor.py
import logging

logger = logging.getLogger('payments')

def process_payment(order_id, amount, card_token):
    logger.info(f"Payment initiated: Order {order_id}, Amount: ${amount}")
    
    try:
        # Process payment
        result = payment_gateway.charge(amount, card_token)
        
        if result.success:
            logger.info(
                f"Payment successful: Order {order_id}, "
                f"Transaction ID: {result.transaction_id}"
            )
            return True
        else:
            logger.error(
                f"Payment failed: Order {order_id}, "
                f"Reason: {result.error_message}"
            )
            return False
    except Exception as e:
        logger.critical(
            f"Payment exception: Order {order_id}, "
            f"Error: {str(e)}",
            exc_info=True
        )
        raise
```

**Configuration**:
```python
'loggers': {
    'payments': {
        'handlers': ['file', 'error_file', 'mail_admins'],
        'level': 'INFO',
        'propagate': False,
    },
}
```

---

### Use Case 4: Structured JSON Logging for Analysis

```python
# json_logger.py
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

# Usage
logger = logging.getLogger('myapp')
logger.info('User action', extra={'user_id': 123, 'request_id': 'abc-123'})
```

**Configuration**:
```python
'formatters': {
    'json': {
        '()': 'myapp.json_logger.JSONFormatter',
    },
},
'handlers': {
    'json_file': {
        'level': 'INFO',
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'filename': 'logs/app.json.log',
        'when': 'midnight',
        'formatter': 'json',
    },
},
```

---

### Use Case 5: Third-Party API Call Logging

```python
# api_client.py
import logging
import requests

logger = logging.getLogger('external_api')

def call_external_api(endpoint, payload):
    logger.info(f"Calling external API: {endpoint}")
    logger.debug(f"Payload: {payload}")
    
    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        
        logger.info(
            f"API Response: {endpoint} - "
            f"Status: {response.status_code} - "
            f"Duration: {response.elapsed.total_seconds()}s"
        )
        
        if response.status_code >= 400:
            logger.error(f"API Error Response: {response.text}")
        
        return response
    except requests.exceptions.Timeout:
        logger.error(f"API Timeout: {endpoint}")
        raise
    except Exception as e:
        logger.exception(f"API Exception: {endpoint} - {str(e)}")
        raise
```

---

<br>
<br>
<br>
<br>















## Complete Example: Multi-Handler Setup

```python
# settings.py - Production Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} {module}.{funcName}:{lineno} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    
    'handlers': {
        # Console output for development
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
        },
        
        # General application logs with daily rotation
        'app_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/app.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
            'formatter': 'verbose',
            'level': 'INFO',
        },
        
        # Error logs with size-based rotation
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/errors.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'level': 'ERROR',
        },
        
        # API request logs
        'api_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/api.log',
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'verbose',
            'level': 'INFO',
        },
        
        # Security logs
        'security_file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
            'formatter': 'verbose',
            'level': 'WARNING',
        },
        
        # Critical errors via email
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'CRITICAL',
            'formatter': 'verbose',
        },
    },
    
    'loggers': {
        # Django framework logs
        'django': {
            'handlers': ['console', 'app_file'],
            'level': 'INFO',
        },
        
        # Django request/response logs
        'django.request': {
            'handlers': ['error_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        
        # Security-related logs
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        
        # API logs
        'api': {
            'handlers': ['api_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        
        # Custom application logs
        'myapp': {
            'handlers': ['console', 'app_file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    
    'root': {
        'handlers': ['console', 'app_file'],
        'level': 'INFO',
    },
}
```

---



1. **Use appropriate log levels**:
   - DEBUG: Detailed diagnostic information
   - INFO: General informational messages
   - WARNING: Warning messages for potentially harmful situations
   - ERROR: Error messages for serious problems
   - CRITICAL: Critical messages for very serious errors
2. **Don't log sensitive data**: Passwords, credit cards, personal information
3. **Use structured logging**: JSON format for easy parsing and analysis
4. **Rotate logs**: Prevent disk space issues with rotating handlers
5. **Separate concerns**: Different loggers for different parts of your application
6. **Monitor performance**: Excessive logging can impact performance
7. **Use context**: Include user IDs, request IDs for tracing
8. **Test logging**: Ensure logs are being written correctly in different environments





--- 

> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)