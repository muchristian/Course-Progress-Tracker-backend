from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import tree
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

# Create your models here.
class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User_role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=100, blank=True)
    role = models.ForeignKey(User_role, on_delete=models.CASCADE, default=1)
    address = models.CharField(max_length=100, null=True)
    department = models.CharField(max_length=100, null=True)
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email



# class User(models.Model):
#     firstName = models.CharField(max_length=100)
#     lastName = models.CharField(max_length=100)
#     email = models.EmailField(max_length=254)
#     password = models.CharField(max_length=100)
#     phoneNumber = models.CharField(max_length=100)
#     role = models.ForeignKey(User_role, on_delete=models.CASCADE)
#     address = models.CharField(max_length=100)
    
#     def __str__(self):
#         return self.email

class Faculty(models.Model):
    faculty_name = models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.faculty_name

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.department_name

class Semester(models.Model):
    title = models.CharField(max_length=255)
    startDate = models.DateField(auto_now=False, auto_now_add=False)
    endDate = models.DateField(auto_now=False, auto_now_add=False)
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.title

class Course_status(models.Model):
    name = models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=30)
    course_credits = models.IntegerField(default=0)
    startDate = models.DateField(auto_now=False, auto_now_add=False)
    endDate = models.DateField(auto_now=False, auto_now_add=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(Course_status, on_delete=models.CASCADE, default=1)
    status_at = models.DateField(auto_now_add=True)
    class_representer_id = models.IntegerField(null=True)
    class_representer_name = models.CharField(max_length=100, default="none")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    enroll_key = models.CharField(max_length=30, null=True)
    course_file = models.FileField(blank=True, default="")
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.course_name

class Session(models.Model):
    title = models.CharField(max_length=100)
    isFinished = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="session_list", null=True)
    department = models.CharField(max_length=100, null=True)
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    course_name = models.CharField(max_length=100, null=True, blank=True)
    course_code = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return self.title

class Chapter(models.Model):
    title = models.CharField(max_length=100)
    isFinished = models.BooleanField(default=False)
    text = models.TextField(null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="chapter_list")
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return self.title

class Classwork(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(default=now)
    type = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="classwork_list", null=True)
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return self.title

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(default=now)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quiz_list", null=True)
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return self.title

class Exam(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(default=now)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="exam_list", null=True)
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.title

