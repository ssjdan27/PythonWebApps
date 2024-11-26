import os
from pathlib import Path

def build_code():
    """
    Generate views, templates, and URLs for project models.
    Primary entry point for code generation process.
    """
    print("🚀 Generating Project Code...")
    generate_message_board()

def generate_message_board():
    """
    Specifically generate components for Message model.
    Sets up project-specific code generation parameters.
    """
    project_path = Path(__file__).resolve().parent
    project_name = "Superhero"
    project_app = "messages"
    generate_data_type(
        project_path, 
        project_app, 
        "Message", 
        "message"
    )

def generate_data_type(
    project_path: Path, 
    app_name: str, 
    class_name: str, 
    object_name: str
):
    """
    Dynamically generate files and structure for a data type.

    Args:
        project_path: Root directory of the project
        app_name: Name of Django application
        class_name: Model class name
        object_name: Lowercase object identifier
    """
    app_path = project_path / app_name

    # Create required directory structure
    directories = [
        app_path / "templates" / object_name,
        app_path / "views",
        app_path / "urls"
    ]
    
    for directory in directories:
        create_directory(directory)

    # Generate project files
    generate_views(app_path, class_name, object_name)
    generate_urls(app_path, object_name)
    generate_templates(
        app_path / "templates" / object_name, 
        class_name, 
        object_name
    )

def create_directory(path: Path):
    """
    Safely create a directory if it doesn't exist.

    Args:
        path: Directory path to create
    """
    if not path.exists():
        path.mkdir(parents=True)
        print(f"📂 Created directory: {path}")

def generate_views(
    app_path: Path, 
    class_name: str, 
    object_name: str
):
    """
    Auto-generate Django class-based views for CRUD operations.

    Args:
        app_path: Path to Django application
        class_name: Model class name
        object_name: Lowercase object identifier
    """
    views_file = app_path / "views" / f"{object_name}_views.py"
    
    if not views_file.exists():
        views_content = f"""
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, 
    CreateView, UpdateView, 
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import {class_name}

class {class_name}ListView(ListView):
    model = {class_name}
    template_name = '{object_name}/{object_name}_list.html'

class {class_name}DetailView(DetailView):
    model = {class_name}
    template_name = '{object_name}/{object_name}_detail.html'

class {class_name}CreateView(LoginRequiredMixin, CreateView):
    model = {class_name}
    fields = ['title', 'text']
    template_name = '{object_name}/{object_name}_form.html'

class {class_name}UpdateView(LoginRequiredMixin, UpdateView):
    model = {class_name}
    fields = ['title', 'text']
    template_name = '{object_name}/{object_name}_form.html'

class {class_name}DeleteView(LoginRequiredMixin, DeleteView):
    model = {class_name}
    template_name = '{object_name}/{object_name}_confirm_delete.html'
    success_url = reverse_lazy('{object_name}_list')
"""
        views_file.write_text(views_content.strip())
        print(f"📄 Generated views: {views_file}")

def generate_urls(app_path: Path, object_name: str):
    """
    Create URL configuration for model views.

    Args:
        app_path: Path to Django application
        object_name: Lowercase object identifier
    """
    urls_file = app_path / "urls" / f"{object_name}_urls.py"
    
    if not urls_file.exists():
        urls_content = f"""
from django.urls import path
from .views.{object_name}_views import (
    {object_name.capitalize()}ListView,
    {object_name.capitalize()}DetailView,
    {object_name.capitalize()}CreateView,
    {object_name.capitalize()}UpdateView,
    {object_name.capitalize()}DeleteView,
)

urlpatterns = [
    path('', 
         {object_name.capitalize()}ListView.as_view(), 
         name='{object_name}_list'),
    path('<int:pk>/', 
         {object_name.capitalize()}DetailView.as_view(), 
         name='{object_name}_detail'),
    path('create/', 
         {object_name.capitalize()}CreateView.as_view(), 
         name='{object_name}_create'),
    path('<int:pk>/edit/', 
         {object_name.capitalize()}UpdateView.as_view(), 
         name='{object_name}_update'),
    path('<int:pk>/delete/', 
         {object_name.capitalize()}DeleteView.as_view(), 
         name='{object_name}_delete'),
]
"""
        urls_file.write_text(urls_content.strip())
        print(f"🔗 Generated URLs: {urls_file}")

def generate_templates(
    template_path: Path, 
    class_name: str, 
    object_name: str
):
    """
    Generate basic HTML templates for model operations.

    Args:
        template_path: Path to template directory
        class_name: Model class name
        object_name: Lowercase object identifier
    """
    templates = {
        f"{object_name}_list.html": f"""
<h1>{class_name} List</h1>
<ul>
    {{% for item in object_list %}}
    <li>
        <a href="{{% url '{object_name}_detail' item.pk %}}">
            {{{{ item.title }}}}
        </a>
    </li>
    {{% endfor %}}
</ul>
""",
        f"{object_name}_detail.html": f"""
<h1>{{{{ object.title }}}}</h1>
<p>{{{{ object.text }}}}</p>
<a href="{{% url '{object_name}_list' %}}">Back to List</a>
""",
        f"{object_name}_form.html": f"""
<h1>Create/Edit {class_name}</h1>
<form method="post">
    {{% csrf_token %}}
    {{% for field in form %}}
        <p>
            {{{{ field.label_tag }}}} 
            {{{{ field }}}}
        </p>
    {{% endfor %}}
    <button type="submit">Save</button>
</form>
""",
        f"{object_name}_confirm_delete.html": f"""
<h1>Delete {class_name}</h1>
<p>
    Are you sure you want to delete "{{{{ object.title }}}}"?
</p>
<form method="post">
    {{% csrf_token %}}
    <button type="submit">Confirm</button>
</form>
<a href="{{% url '{object_name}_list' %}}">Cancel</a>
"""
    }

    for filename, content in templates.items():
        template_file = template_path / filename
        if not template_file.exists():
            template_file.write_text(content.strip())
            print(f"🖼️ Generated template: {template_file}")

if __name__ == "__main__":
    build_code()