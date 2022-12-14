from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

urlpatterns = [
    path('home/', views.index),
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/signup/', views.registerUser, name='signup'),
    path('users/profile/', views.getUserProfile, name='user-profile'),
    path('users/all/', views.retreiveUsers, name='user-all'),
    path('users/update/<int:id>/', views.updateUser, name='user-update'),
    path('users/delete/<int:id>/', views.deleteUser, name='user-delete'),
    path('user_role/', views.retreiveUserRoles, name='user-role-list'),
    path('user_role/', views.createUserRole, name='user-role-create'),
    path('user_role/update/<int:id>', views.updateUserRole, name='user-role-update'),
    path('user_role/<int:id>/delete', views.deleteUserRole, name='user-role-delete'),
    path('faculty/', views.retreiveFaculties, name='get-faculties'),
    path('faculty', views.createFaculty, name='create-faculty'),
    path('faculty/update/<int:id>', views.updateFaculty, name='update-faculty'),
    path('faculty/delete/<int:id>', views.deleteFaculty, name='delete-faculty'),
    path('department/', views.retreiveDepartments, name='get-departments'),
    path('department', views.createDepartment, name='create-department'),
    path('department/update/<int:id>', views.updateDepartment, name='update-department'),
    path('department/delete/<int:id>', views.deleteDepartment, name='delete-department'),
    path('course-status/', views.retreiveCourseStatus, name='get-course-status'),
    path('course-status/', views.createCourseStatus, name='create-course-status'),
    path('course/', views.createCourse, name='create-course'),
    path('course/<int:id>', views.retOneCourses, name='get-a-course'),
    path('course/all/', views.adminretreiveCourses, name='get-all-courses'),
    path('course/statuses/<int:id>', views.retCoursesByStatus, name='get-users-courses-status'),
    path('course/all/<int:id>', views.retreiveCourses, name='get-users-courses'),
    path('course/update/<int:id>', views.updateCourse, name='update-course'),
    path('course/upload/<int:id>', views.FileView.as_view(), name='upload-course-file'),
    path('course/download/<int:id>', views.download, name='course-file-download'),
    path('course/delete/<int:id>', views.deleteCourse, name='delete-course'),
    path('course/representer/<int:id>', views.representerRetreiveCourses, name='representer-courses'),
    path('course/report', views.getCourseReport, name='course-report'),
    path('registra/report', views.getRegistraReport, name='registra-report'),
    path('session/', views.createSession, name="create-session"),
    path('session/update/<int:id>', views.updateSession, name='update-session'),
    path('session/delete/<int:id>', views.deleteSession, name='delete-session'),
    path('chapter/', views.createChapter, name="create-chapter"),
    path('chapter/update/<int:id>', views.updateChapter, name='update-chapter'),
    path('chapter/delete/<int:id>', views.deleteChapter, name='delete-chapter'),
    path('classwork/', views.createClasswork, name="create-classwork"),
    path('classwork/update/<int:id>', views.updateClasswork, name='update-classwork'),
    path('classwork/delete/<int:id>', views.deleteClasswork, name='delete-classwork'),
    path('quiz/', views.createQuiz, name="create-quiz"),
    path('quiz/update/<int:id>', views.updateQuiz, name='update-quiz'),
    path('quiz/delete/<int:id>', views.deleteQuiz, name='delete-quiz'),
    path('semester/all/', views.retrieveSemesters, name="get-semester"),
    path('semester/', views.createSemester, name="create-semester"),
    path('semester/update/<int:id>', views.updateSemester, name='update-semester'),
]