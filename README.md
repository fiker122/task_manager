# Task Manager (Django)

A simple, user-friendly **Task Manager** built with Django.  
This project includes full task CRUD operations, tagging, search, and authentication features—perfect for ALX projects or personal learning.

---

## 📌 Features

### 🔐 User Authentication
- Login & logout using Django’s built-in auth system.
- Each user can only see **their own** tasks.

### 📝 Task Management
- Create, edit, update, and view tasks.
- Mark tasks as completed or not completed.
- Auto timestamps (created & updated).

### 🏷 Tagging System
- Add multiple tags (comma-separated).
- Click on any tag to filter tasks.
- Automatically prevents duplicate tags.

### 🔍 Search Functionality
Search tasks by:
- Title  
- Description  
- Tags  

Example: searching **“school”** returns all tasks containing that keyword.

---

## 🗂 Project Structure

task_manager/
│── manage.py
│── task_manager/
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
│
└── tasks/
├── models.py
├── views.py
├── forms.py
├── urls.py
├── admin.py
├── templates/
│ └── tasks/
│ ├── base.html
│ ├── task_list.html
│ ├── task_detail.html
│ ├── task_form.html
│ └── search_results.html
└── static/
└── tasks/
└── style.css
