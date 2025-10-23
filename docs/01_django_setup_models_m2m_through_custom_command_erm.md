### Django Custom Management Command Explained  

**Date:** 22 October 2025  
**Video Title**: SETUP AND MODELS 

---

## Topics Covered  

##  1. `model.ManyToManyField`  
- The **`through`** parameter in a `ManyToManyField` is used in Django to customize the **intermediate (bridge) table or class**.  
- It allows you to add extra fields or control the relationship model between two tables.

<br>
<br>
<br>
<br>


## 2. Generate ERM (Entity Relationship Model) Diagram in Django

This guide explains how to **generate and visualize an ERM diagram** from your Django project using the `graph_models` command.
 

### **Step 1: Install Dependencies**

Before generating the ERM diagram, install **django-extensions** and **pygraphviz**.

```bash
pip install django-extensions pygraphviz
```

Then, add `'django_extensions'` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'django_extensions',
]
```

---

### **Step 2: Generate the DOT File**

Run this command inside your Django project directory:

```bash
python manage.py graph_models core > models.dot
```

This generates a `.dot` file representing your **app’s models and their relationships**.

* Example output file: `models.dot`
* This file contains all model relations (ForeignKey, ManyToMany, OneToOne, etc.)

---

### **Step 3: Visualize the ERM Diagram Online**

You can visualize your generated `.dot` file online:

1. Go to **[Graphviz Online](https://dreampuf.github.io/GraphvizOnline/)**
2. Open or paste the content of your `models.dot` file
3. The tool will convert it into a **clear ERM diagram** showing all models and their relationships.
 

### **Generate Diagrams for Multiple Apps**

You can also generate ERM diagrams for multiple apps together:

```bash
python manage.py graph_models app1 app2 > output.dot
```

This command will include all models and relationships from both apps (`app1` and `app2`).
 
### **Notes**
 
The `.dot` extension comes from Graphviz DOT language, where DOT stands for **graph description language**.
*  It’s a plain text file format used to describe graphs — nodes, edges, and their relationships.
*  Graphviz tools read .dot files and render them into visual diagrams like ER diagrams, flowcharts, and network graphs.
*  So basically, .dot files contain the structure of a graph in text, not the image itself. You then use Graphviz or online tools to convert it into an actual diagram.




<br>
<br>
<br>
<br>



## 3. Custom Management Command in Django
 
Custom management commands in Django allow you to create **custom scripts** that can be executed via the `manage.py` command. They are useful for performing **automated tasks**, batch operations, or maintenance scripts directly from the terminal.

**Use Cases:**
- Cleaning up expired or unused records in the database.
- Populating the database with initial or test data.
- Running automated tasks such as sending emails, generating reports, or syncing data.


## Directory Structure
To create a custom management command, the app directory structure should look like this:
```shell
your_app/
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       └── clean_expired_students.py
│       └── populate_db.py
```
**Explanation:**
- `management/` → Required folder for custom commands.
- `commands/` → Contains the Python scripts for each command.
- Each file inside `commands/` represents a separate management command.

<br>

### Example: Clean Expired Students Command
> Create a file `clean_expired_students.py`:
```python
from django.core.management.base import BaseCommand
from apps.students.models import Student
from datetime import date

class Command(BaseCommand):
    help = 'Delete students whose enrollment has expired'

    def handle(self, *args, **kwargs):
        expired_students = Student.objects.filter(enrollment_end__lt=date.today())
        count = expired_students.count()
        expired_students.delete()
        self.stdout.write(self.style.SUCCESS(f'{count} expired students deleted successfully.'))
```
- BaseCommand is imported from django.core.management.base.
- handle() method contains the logic executed when the command runs.
- self.stdout.write() is used to print messages to the console.

<br>

### Example: Populate Database Command
> Create a file `populate_db.py`:
```py
from django.core.management.base import BaseCommand
from apps.students.models import Student
from faker import Faker

class Command(BaseCommand):
    help = 'Populate the database with dummy student data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(10):
            Student.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email()
            )
        self.stdout.write(self.style.SUCCESS('10 dummy students added successfully.'))
``` 
- Faker library is used to generate fake data.
- Loop creates multiple Student objects in the database.
- `self.stdout.write()` confirms completion in the terminal.



### Running Custom Commands
> To execute a custom command, use:
`python manage.py <command_name>` 
```shell
python manage.py clean_expired_students
python manage.py populate_db
```