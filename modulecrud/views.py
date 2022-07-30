from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Semester, User_role, CustomUser, Faculty, Department, Course_status, Course, Session, Chapter, Classwork, Quiz, Exam
from .serializers import SemesterSerializer, UserRoleSerializer, UserSerializer, FacultySerializer, DepartmentSerializer, CourseStatusSerializer, CourseSerializer, SessionSerializer, ChapterSerializer, ClassworkSerializer, QuizSerializer, ExamSerializer
from django.http import FileResponse, JsonResponse, request
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view

from modulecrud import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
# from django.contrib.auth.models import User 
# index view
def index(request):
    return render(request, 'modulecrud/index.html')
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id'] = user.id
        token['email'] = user.email
        token['firstName'] = user.firstName
        token['lastName'] = user.lastName
        token['role'] = user.role.name
        token['phoneNumber'] = user.phoneNumber
        token['department'] = user.department
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    print(serializer)
    return Response(serializer.data)


# register user
@api_view(['POST'])
def registerUser(request):
    data = request.data
    user = CustomUser.objects.create(
                firstName = data['firstName'],
                lastName = data['lastName'],
                email = data['email'],
                password = make_password(data['password']),
                phoneNumber = data['phoneNumber'],
                role_id = data['role'],
                department = data['department']
            )
    serializer = UserSerializer(user, many=False)
    return Response({"message":"User registration has been successful", "data":serializer.data})

@api_view(['GET'])
def retreiveUsers(request):
    users = CustomUser.objects.exclude(role=1)
    serializer = UserSerializer(users, many=True)
    return Response({"message":"Users returned successfully", "data":serializer.data})


@api_view(['PUT'])
def updateUser(request, id):
    user = CustomUser.objects.get(pk=id)
    
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"User update has been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['DELETE']) 
def deleteUser(request, id):
    user = CustomUser.objects.get(pk=id)
    user.delete()
    return Response({"message": "User has been deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# Faculty views
@api_view(['GET'])
def retreiveFaculties(request):
    faculties = Faculty.objects.all().order_by("-id")
    serializer = FacultySerializer(faculties, many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
def createFaculty(request):
    serializer = FacultySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Faculty registration has been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['PUT'])
def updateFaculty(request, id):
    faculty = Faculty.objects.get(pk=id)
    serializer = FacultySerializer(faculty, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Faculty update has been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['DELETE']) 
def deleteFaculty(request, id):
    faculty = Faculty.objects.get(pk=id)
    faculty.delete()
    return Response({"message":"Faculty has been deleted successful"})
    

# User role views
@api_view(['GET'])
def retreiveUserRoles(request):
    user_roles = User_role.objects.all()
    serializer = UserRoleSerializer(user_roles, many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
def createUserRole(request):
    serializer = UserRoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"User role registration has been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['PUT'])
def updateUserRole(request, id):
    user_role = User_role.objects.get(pk=id)
    serializer = UserRoleSerializer(user_role, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"User role update has been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['DELETE']) 
def deleteUserRole(request, id):
    user_role = User_role.objects.get(pk=id)
    user_role.delete()
    return Response({"message":"User role has been deleted successful"})

# Department views
@api_view(['GET'])
def retreiveDepartments(request):
    departments = Department.objects.all().order_by("-id")
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
def createDepartment(request):
    serializer = DepartmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Department registration has been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['PUT'])
def updateDepartment(request, id):
    department = Department.objects.get(pk=id)
    serializer = DepartmentSerializer(department, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Department update has been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['DELETE']) 
def deleteDepartment(request, id):
    department = Department.objects.get(pk=id)
    department.delete()
    return Response({"message":"Department has been deleted successful"})

# Course Status Views
@api_view(['GET'])
def retreiveCourseStatus(request):
    course_status = Course_status.objects.all()
    serializer = CourseStatusSerializer(course_status, many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
def createCourseStatus(request):
    serializer = CourseStatusSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['PUT'])
def updateCourseStatus(request, id):
    course_status = Course_status.objects.get(pk=id)
    serializer = CourseStatusSerializer(course_status, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE']) 
def deleteCourseStatus(request, id):
    course_status = Course_status.objects.get(pk=id)
    course_status.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Course views
@api_view(['GET'])
def adminretreiveCourses(request):
    courses= Course.objects.all().order_by('-id')
    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(courses, request)
    serializer = CourseSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def representerRetreiveCourses(request, id):
    courses= Course.objects.filter(class_representer_id=id).order_by('-id')
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def retreiveCourses(request, id):
    courses= Course.objects.filter(user=id).order_by('-id')
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def retOneCourses(request, id):
    courses= Course.objects.get(pk=id)
    serializer = CourseSerializer(courses, many=False)
    return Response({"message":"Course retrieved successfully", "data":serializer.data})

@api_view(['GET'])
def retCoursesByStatus(request, id):
    courses= Course.objects.filter(status=id).order_by('-id')
    serializer = CourseSerializer(courses, many=True)
    return Response({"message":"Course retrieved successfully", "data":serializer.data})
    
@api_view(['POST'])
def createCourse(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Course registration has been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['PUT'])
def updateCourse(request, id):
    course = Course.objects.get(pk=id)
    serializer = CourseSerializer(course, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Course update has been successful", "data":serializer.data})
    return Response(serializer.errors)

def uploadCourseFile(request, id):
    # parser_classes = (MultiPartParser, FormParser)
    course = Course.objects.get(pk=id)
    file = request.FILES['file']
    print(file)
    serializer = CourseSerializer(course, data=request.FILES, partial=True)
    if serializer.is_valid():
        serializer.save()
        if 'file' not in request.FILES:
            print('course file not found')
        return Response({"message":"Course update has been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['DELETE']) 
def deleteCourse(request, id):
    course = Course.objects.get(pk=id)
    course.delete()
    return Response({"message":"Course has been deleted successful"})

    # Chapter views
def retreiveChapter(request, courseId):
    chapter = Chapter.objects.filter(course=courseId)
    serializer = ChapterSerializer(chapter, many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
def createChapter(request):
    serializer = ChapterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Chapters registration have been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['PUT'])
def updateChapter(request, id):
    chapter = Chapter.objects.get(pk=id)
    serializer = ChapterSerializer(chapter, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Chapter update has been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['PUT'])
def checkChapter(request, id):
    chapter = Chapter.objects.get(pk=id)
    serializer = ChapterSerializer(chapter, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Chapter has been completed successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['DELETE']) 
def deleteChapter(request, id):
    chapter = Chapter.objects.get(pk=id)
    chapter.delete()
    return Response({"message":"Chapter has been deleted successful"})


    # Session views
def retreiveSession(request, courseId):
    session = Session.objects.filter(course=courseId)
    serializer = SessionSerializer(session, many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
def createSession(request):
    serializer = SessionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Session rhegistration have been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['PUT'])
def updateSession(request, id):
    session = Session.objects.get(pk=id)
    serializer = SessionSerializer(session, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Session update has been successful", "data":serializer.data})
    return Response(serializer.errors)

# @api_view(['PUT'])
# def checkChapter(request, id):
#     chapter = Session.objects.get(pk=id)
#     serializer = SessionSerializer(chapter, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message":"Session has been completed successful", "data":serializer.data})
#     return Response(serializer.errors)

@api_view(['DELETE']) 
def deleteSession(request, id):
    session = Session.objects.get(pk=id)
    session.delete()
    return Response({"message":"Session has been deleted successful"})

        # Classwork views
def retreiveClasswork(request, courseId):
    classwork = Classwork.objects.filter(course=courseId)
    serializer = ClassworkSerializer(classwork, many=True)
    return Response({"message": "quizes were retrieved successfully", "data": serializer.data})
    
@api_view(['POST'])
def createClasswork(request):
    serializer = ClassworkSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Classwork registration has been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['PUT'])
def updateClasswork(request, id):
    classwork = Classwork.objects.get(pk=id)
    serializer = ClassworkSerializer(classwork, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Classwork update has been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['DELETE']) 
def deleteClasswork(request, id):
    classwork = Classwork.objects.get(pk=id)
    classwork.delete()
    return Response({"message":"Classwork has been deleted successful"})

        # Quiz views
def retreiveQuiz(request, courseId):
    quiz = Quiz.objects.filter(course=courseId)
    serializer = QuizSerializer(quiz, many=True)
    return Response({"message": "quizes were retrieved successfully", "data": serializer.data})
    
@api_view(['POST'])
def createQuiz(request):
    serializer = QuizSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Quiz registration has been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['PUT'])
def updateQuiz(request, id):
    quiz = Quiz.objects.get(pk=id)
    serializer = QuizSerializer(quiz, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Quiz update has been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['DELETE']) 
def deleteQuiz(request, id):
    quiz = Quiz.objects.get(pk=id)
    quiz.delete()
    return Response({"message":"Quiz has been deleted successful"})


class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  def put(self, request, id, *args, **kwargs):
    course = Course.objects.get(pk=id)
    file = request.FILES
    print(file)
    serializer = CourseSerializer(course, data=request.FILES, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET']) 
def download(request, id):
    obj = Course.objects.get(id=id)
    filename = obj.course_file.path
    response = FileResponse(open(filename, 'rb'), filename)
    print(response)
    return response

@api_view(['GET']) 
def getCourseReport(request):
    print (request.GET.get('department'))
    report = Session.objects.filter(Q(isFinished=True) & Q(department=request.GET.get('department'))).order_by('-id')
    serializer = SessionSerializer(report, many=True)
    return Response({"message":"Courses report retrieved successfully", "data": serializer.data})

@api_view(['GET']) 
def getRegistraReport(request):
    users = CustomUser.objects.all().count()
    faculties = Faculty.objects.all().count()
    departments = Department.objects.all().count()
    courses = Course.objects.all().count()
    return Response({"message":"Registra report retrieved successfully", "data": {
        "users": users,
        "faculties": faculties,
        "departments": departments,
        "courses": courses
    }})

@api_view(['GET'])
def retrieveSemesters(request):
    semester = Semester.objects.all().order_by("-id")
    serializer = SemesterSerializer(semester, many=True)
    return Response({"message": "Semesters retreived successfully", "data": serializer.data})

@api_view(['POST'])
def createSemester(request):
    serializer = SemesterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Semester registration has been successful", "data":serializer.data})
    return Response(serializer.errors)

@api_view(['PUT'])
def updateSemester(request, id):
    semester = Semester.objects.get(pk=id)
    serializer = SemesterSerializer(semester, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Semester update has been successful", "data":serializer.data})
    return Response(serializer.errors)

