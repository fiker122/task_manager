from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Task, Tag
from .forms import TaskForm

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).prefetch_related('tags')
    q = request.GET.get('q')
    tag = request.GET.get('tag')
    if q:
        tasks = tasks.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct()
    if tag:
        tasks = tasks.filter(tags__name=tag)
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'query': q, 'tag': tag})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            tags_field = form.cleaned_data.get('tags', '')
            tag_names = [t.strip() for t in tags_field.split(',') if t.strip()]
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name})
                # get_or_create with case-insensitive attempt; ensure tag is Tag instance
                if isinstance(tag, tuple):
                    tag = tag[0]
                task.tags.add(tag)
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            task.tags.clear()
            tags_field = form.cleaned_data.get('tags', '')
            tag_names = [t.strip() for t in tags_field.split(',') if t.strip()]
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name})
                if isinstance(tag, tuple):
                    tag = tag[0]
                task.tags.add(tag)
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'task': task})

@login_required
def tasks_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    tasks = tag.tasks.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'tag': tag})

@login_required
def search_view(request):
    q = request.GET.get('q', '')
    tasks = Task.objects.none()
    if q:
        tasks = Task.objects.filter(user=request.user).filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct()
    return render(request, 'tasks/search_results.html', {'tasks': tasks, 'query': q})
