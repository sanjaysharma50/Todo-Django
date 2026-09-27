from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from .models import Todo
from .forms import TodoForm


# =========================================================
# TODO DASHBOARD
# =========================================================

def todo_list(request):

    # Login required
    if not request.user.is_authenticated:
        return redirect('login')

    today = timezone.localdate()

    # =====================================================
    # CURRENT USER'S TODOS
    # =====================================================

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
    # CATEGORY FILTER
    # =====================================================

    selected_category = request.GET.get(
        'category',
        ''
    )

    if selected_category:

        todos = todos.filter(
            category=selected_category
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

    elif selected_status == 'overdue':

        todos = todos.filter(
            completed=False,
            due_date__lt=today
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
    # ALL USER TASKS FOR STATISTICS
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

    overdue_tasks = user_todos.filter(
        completed=False,
        due_date__lt=today
    ).count()

    # =====================================================
    # COMPLETION PERCENTAGE
    # =====================================================

    if total_tasks > 0:

        completion_percentage = round(
            (completed_tasks / total_tasks) * 100
        )

    else:

        completion_percentage = 0

    # =====================================================
    # TODAY'S TASKS
    # =====================================================

    today_tasks = user_todos.filter(
        due_date=today
    ).count()

    # =====================================================
    # UPCOMING TASKS
    # Next 7 days, excluding today
    # =====================================================

    next_seven_days = today + timedelta(days=7)

    upcoming_tasks = user_todos.filter(
        completed=False,
        due_date__gt=today,
        due_date__lte=next_seven_days
    ).count()

    # =====================================================
    # CATEGORY STATISTICS
    # =====================================================

    work_tasks = user_todos.filter(
        category='work'
    ).count()

    study_tasks = user_todos.filter(
        category='study'
    ).count()

    personal_tasks = user_todos.filter(
        category='personal'
    ).count()

    shopping_tasks = user_todos.filter(
        category='shopping'
    ).count()

    ideas_tasks = user_todos.filter(
        category='ideas'
    ).count()

    other_tasks = user_todos.filter(
        category='other'
    ).count()

    # =====================================================
    # PRODUCTIVITY SCORE
    # =====================================================

    if total_tasks == 0:

        productivity_score = 0

    else:

        productivity_score = min(
            100,
            round(
                (
                    (completed_tasks / total_tasks) * 70
                )
                +
                (
                    max(
                        0,
                        (pending_tasks - overdue_tasks)
                    )
                    / total_tasks
                    * 30
                )
            )
        )

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        'todos/home.html',
        {
            # Tasks
            'todos': todos,
            'form': form,

            # Basic statistics
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'high_priority': high_priority,
            'overdue_tasks': overdue_tasks,

            # Productivity
            'completion_percentage': completion_percentage,
            'productivity_score': productivity_score,

            # Date statistics
            'today_tasks': today_tasks,
            'upcoming_tasks': upcoming_tasks,

            # Category statistics
            'work_tasks': work_tasks,
            'study_tasks': study_tasks,
            'personal_tasks': personal_tasks,
            'shopping_tasks': shopping_tasks,
            'ideas_tasks': ideas_tasks,
            'other_tasks': other_tasks,

            # Filters
            'search': search,
            'selected_priority': selected_priority,
            'selected_category': selected_category,
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

        if not username or not password:

            messages.error(
                request,
                'Username and password are required.'
            )

            return redirect(
                'register'
            )

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect(
                'register'
            )

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

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

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

    logout(request)

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
    # =========================================================
# CALENDAR
# =========================================================
 
def calendar_view(request):

    if not request.user.is_authenticated:
        return redirect('login')

    import calendar

    today = timezone.localdate()

    year = int(
        request.GET.get(
            'year',
            today.year
        )
    )

    month = int(
        request.GET.get(
            'month',
            today.month
        )
    )

    # Previous / next month protection
    if month < 1:
        month = 12
        year -= 1

    elif month > 12:
        month = 1
        year += 1

    # Calendar weeks
    cal = calendar.Calendar(
        firstweekday=6
    )

    raw_weeks = cal.monthdayscalendar(
        year,
        month
    )

    # Get tasks for this month
    month_tasks = Todo.objects.filter(
        user=request.user,
        due_date__year=year,
        due_date__month=month
    ).order_by(
        'due_date'
    )

    # Put tasks by day
    tasks_by_date = {}

    for todo in month_tasks:

        day = todo.due_date.day

        if day not in tasks_by_date:
            tasks_by_date[day] = []

        tasks_by_date[day].append(todo)

    # Build template-friendly calendar
    weeks = []

    for raw_week in raw_weeks:

        week = []

        for day in raw_week:

            if day == 0:

                week.append({
                    'day': 0,
                    'tasks': [],
                })

            else:

                week.append({
                    'day': day,
                    'tasks': tasks_by_date.get(
                        day,
                        []
                    ),
                })

        weeks.append(week)

    # Previous month
    if month == 1:

        previous_month = 12
        previous_year = year - 1

    else:

        previous_month = month - 1
        previous_year = year

    # Next month
    if month == 12:

        next_month = 1
        next_year = year + 1

    else:

        next_month = month + 1
        next_year = year

    return render(
        request,
        'todos/calendar.html',
        {
            'weeks': weeks,

            'year': year,

            'month': month,

            'month_name': calendar.month_name[month],

            'today': today,

            'previous_month': previous_month,

            'previous_year': previous_year,

            'next_month': next_month,

            'next_year': next_year,
        }
    )