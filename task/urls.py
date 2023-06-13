from django.urls import path

from . import views

urlpatterns = [

	path('get-tasks/', views.task_list, name="get-tasks"),
	path('get-task/<str:pk>/', views.task_detail, name="get-task"),
	path('create-task/', views.create_task, name="create-task"),
	path('delete-task/<str:id>/', views.delete_task, name="delete-task"),
	path('update-task/<str:id>/', views.update_task, name="update-task"),

	path('create-team/', views.create_team, name="new_team"),
	path('get-teams/', views.get_teams, name="get_teams"),
	path('get-team/<str:id>/', views.get_team, name="get_team"),
	path('add-user-to-team/', views.add_user_to_team, name="add_to_team"),
	path('get-team-tasks/', views.teamTasks, name="team_tasks"),
	path('get-team-members/<str:id>/', views.get_teammates, name="team_members"),
	path('leave-team/<str:id>/', views.leave_team, name="leave_team")
]
