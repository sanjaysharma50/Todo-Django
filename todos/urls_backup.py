from django.urls import path

from . import views


urlpatterns = [

    # Dashboard
    path(
        '',
        views.todo_list,
        name='todo_list'
    ),

    path(
    'calendar/',
    views.calendar_view,
    name='calendar'
    ),

    # Authentication
    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # Todo actions
    path(
        'todo/<int:todo_id>/toggle/',
        views.toggle_todo,
        name='toggle_todo'
    ),

    path(
        'todo/<int:todo_id>/edit/',
        views.edit_todo,
        name='edit_todo'
    ),

    path(
        'todo/<int:todo_id>/delete/',
        views.delete_todo,
        name='delete_todo'
    ),

]