from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Todo
from .forms import TodoForm
# Create your views here.
class TodoListView(View):
    def get(self, request):
        todos = Todo.objects.all()
        return render(request, 'todos/todo_list.html', {'todos': todos})
    
class TodoCreateList(View):
    def get(self, request):
        form = TodoForm()
        return render(request, 'todos/todo_form.html', {'form': form})
    
    def post(self, request):
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo-list')
        return render(request, 'todos/todo_form.html', {'form': form})
    
class TodoUpdateView(View):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        form = TodoForm(instance=todo)
        return render(request, 'todos/todo_form.html', {'form': form, 'todo': todo})
    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo-list')
        return render(request, 'todos/todo_form,html', {'form': form, 'todo' : todo})
        
class TodoDeleteView(View):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        return render(request, 'todos/todo_confirm_delete.html', {'todo': todo})
    
    def post(self, _, pk):
        todo = get_object_or_404(Todo, pk=pk)
        todo.delete()
        return redirect('todo-list')