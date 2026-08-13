from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from django.contrib import messages

from django.db.models import Q

from .models import Todo

from .forms import TodoForm


# =========================================================
# TODO DASHBOARD
# =========================================================

def todo_list(request):

    # Login required
    if not request.user.is_authenticated:
        return redirect('login')


    # Current user's todos
    todos = Todo.objects.filter(
        user=request.user
    ).order_by('-created_at')


    # =====================================================
    # SEARCH
    # =====================================================

    search = request.GET.get(
        'search',
        ''
    ).strip()


    if search:

        todos = todos.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )


    # =====================================================
    # PRIORITY FILTER
    # =====================================================

    selected_priority = request.GET.get(
        'priority',
        ''
    )


    if selected_priority:

        todos = todos.filter(
            priority=selected_priority
        )


    # =====================================================
    # STATUS FILTER
    # =====================================================

    selected_status = request.GET.get(
        'status',
        ''
    )


    if selected_status == 'completed':

        todos = todos.filter(
            completed=True
        )


    elif selected_status == 'pending':

        todos = todos.filter(
            completed=False
        )


    # =====================================================
    # ADD TODO
    # =====================================================

    if request.method == 'POST':

        form = TodoForm(
            request.POST
        )


        if form.is_valid():

            todo = form.save(
                commit=False
            )

            todo.user = request.user

            todo.save()


            messages.success(
                request,
                'Todo added successfully!'
            )


            return redirect(
                'todo_list'
            )


    else:

        form = TodoForm()


    # =====================================================
    # STATISTICS
    # =====================================================

    user_todos = Todo.objects.filter(
        user=request.user
    )


    total_tasks = user_todos.count()


    completed_tasks = user_todos.filter(
        completed=True
    ).count()


    pending_tasks = user_todos.filter(
        completed=False
    ).count()


    high_priority = user_todos.filter(
        priority='high'
    ).count()


    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        'todos/home.html',
        {
            'todos': todos,

            'form': form,

            'total_tasks': total_tasks,

            'completed_tasks': completed_tasks,

            'pending_tasks': pending_tasks,

            'high_priority': high_priority,

            'search': search,

            'selected_priority': selected_priority,

            'selected_status': selected_status,
        }
    )


# =========================================================
# REGISTER
# =========================================================

def register_view(request):

    if request.user.is_authenticated:

        return redirect(
            'todo_list'
        )


    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()


        email = request.POST.get(
            'email',
            ''
        ).strip()


        password = request.POST.get(
            'password',
            ''
        )


        confirm_password = request.POST.get(
            'confirm_password',
            ''
        )


        # Required fields

        if not username or not password:

            messages.error(
                request,
                'Username and password are required.'
            )

            return redirect(
                'register'
            )


        # Password match

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect(
                'register'
            )


        # Username exists

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect(
                'register'
            )


        # Create user

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )


        # Login automatically

        login(
            request,
            user
        )


        messages.success(
            request,
            'Account created successfully!'
        )


        return redirect(
            'todo_list'
        )


    return render(
        request,
        'todos/register.html'
    )


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:

        return redirect(
            'todo_list'
        )


    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()


        password = request.POST.get(
            'password',
            ''
        )


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            login(
                request,
                user
            )


            messages.success(
                request,
                f'Welcome, {user.username}!'
            )


            return redirect(
                'todo_list'
            )


        messages.error(
            request,
            'Invalid username or password.'
        )


    return render(
        request,
        'todos/login.html'
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(
        request
    )


    messages.success(
        request,
        'You have been logged out successfully.'
    )


    return redirect(
        'login'
    )


# =========================================================
# TOGGLE TODO
# =========================================================

def toggle_todo(
    request,
    todo_id
):

    if not request.user.is_authenticated:

        return redirect(
            'login'
        )


    todo = get_object_or_404(
        Todo,
        id=todo_id,
        user=request.user
    )


    todo.completed = not todo.completed

    todo.save()


    if todo.completed:

        messages.success(
            request,
            'Todo marked as completed.'
        )

    else:

        messages.info(
            request,
            'Todo marked as pending.'
        )


    return redirect(
        'todo_list'
    )


# =========================================================
# EDIT TODO
# =========================================================

def edit_todo(
    request,
    todo_id
):

    if not request.user.is_authenticated:

        return redirect(
            'login'
        )


    todo = get_object_or_404(
        Todo,
        id=todo_id,
        user=request.user
    )


    if request.method == 'POST':

        form = TodoForm(
            request.POST,
            instance=todo
        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                'Todo updated successfully!'
            )


            return redirect(
                'todo_list'
            )


    else:

        form = TodoForm(
            instance=todo
        )


    return render(
        request,
        'todos/edit_todo.html',
        {
            'form': form,
            'todo': todo,
        }
    )


# =========================================================
# DELETE TODO
# =========================================================

def delete_todo(
    request,
    todo_id
):

    if not request.user.is_authenticated:

        return redirect(
            'login'
        )


    todo = get_object_or_404(
        Todo,
        id=todo_id,
        user=request.user
    )


    if request.method == 'POST':

        todo.delete()


        messages.success(
            request,
            'Todo deleted successfully!'
        )


        return redirect(
            'todo_list'
        )


    return render(
        request,
        'todos/delete_todo.html',
        {
            'todo': todo,
        }
    )