### Django Custom Management Command Explained  

**Date:** 22 October 2025  
**Video Title**: SETUP AND MODELS 

---

## Topics Covered  

### 1. `model.ManyToManyField`  
- The **`through`** parameter in a `ManyToManyField` is used in Django to customize the **intermediate (bridge) table or class**.  
- It allows you to add extra fields or control the relationship model between two tables.
  
<br>
<br>

### 2. How to Create an ERM Diagram from an Existing Database
Creating an ERM (Entity-Relationship Model) diagram helps visualize the structure of your database, including tables, fields, and relationships. This is especially useful for understanding complex Django models.

**Step 1: Documentation**  
- Refer to Django Extensions: [Graph Models Documentation](https://django-extensions.readthedocs.io/en/latest/graph_models.html)

**Step 2: Generate the DOT file**  
Run this command in your terminal inside the Django project:  
```bash
python manage.py graph_models core > models.dot
```
This generates a .dot file representing your app’s models and relationships.

 
**Step 3: Visualize the ERM Diagram Online**
- Open the .dot file using [Graphviz Online](https://dreampuf.github.io/GraphvizOnline/)
- The tool converts the DOT file into a clear ERM diagram showing all models and relationships.

You can generate diagrams for multiple apps by adding app names:
```py
python manage.py graph_models app1 app2 > output.dot
```

<br>
<br>

### 3. Custom Management Command in Django  
- Custom management commands allow you to run **custom scripts** using the Django `manage.py` command.  
- These commands can be used to perform automated database actions directly from the terminal.


```
your_app/
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       └── clean_expired_students.py
│       └── populate_db.py
```

**Example Command:**  
```bash
python manage.py <command_name>
python manage.py clean_expired_students
python manage.py populate_db
```



