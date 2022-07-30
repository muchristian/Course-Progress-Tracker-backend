from django.db.models import fields
from modulecrud.models import CustomUser, Semester, User_role, Faculty, Department, Course_status, Course, Session, Chapter, Classwork, Quiz, Exam
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import User


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_role
        fields = "__all__"

        def create(self, validated_data):
            return User_role.objects.create(**validated_data)
        
        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.save()
            return instance

class UserSerializer(serializers.ModelSerializer):
    role = UserRoleSerializer(many=False)
    class Meta:
        model = CustomUser
        exclude = ["password"]

        def create(self, validated_data):
            return User_role.objects.create(**validated_data)

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CustomUser,
        exclude = ["password"]


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"
        
        def create(self, validated_data):
            return Faculty.objects.create(**validated_data)

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
        
        def create(self, validated_data):
            return Department.objects.create(**validated_data)
        
        def update(self, instance, validated_data):
            instance.department_name = validated_data.get('department_name', instance.department_name)
            instance.faculty = validated_data.get('faculty', instance.faculty)
            instance.save()
            return instance

    def to_representation(self, instance):
        self.fields['faculty'] =  FacultySerializer(read_only=True)
        return super(DepartmentSerializer, self).to_representation(instance)

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = "__all__"

class CourseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course_status
        fields = "__all__"

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = "__all__"

        def create(self, validated_data):
            return Chapter.objects.create(**validated_data)

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"

    def to_representation(self, instance):
        self.fields['chapter_list'] = ChapterSerializer(many=True)
        return super(SessionSerializer, self).to_representation(instance)

class ClassworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classwork
        fields = "__all__"

        def create(self, validated_data):
            return Chapter.objects.create(**validated_data)

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"

        def create(self, validated_data):
            return Chapter.objects.create(**validated_data)

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"

        def create(self, validated_data):
            return Chapter.objects.create(**validated_data)
            

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

    def to_representation(self, instance):
        self.fields['session_list'] = SessionSerializer(many=True)
        self.fields['classwork_list'] = ClassworkSerializer(many=True)
        self.fields['quiz_list'] = QuizSerializer(many=True)
        self.fields['faculty'] = FacultySerializer(many=False)
        self.fields['department'] = DepartmentSerializer(many=False)
        self.fields['semester'] = SemesterSerializer(many=False)
        self.fields['user'] = UserSerializer(many=False)
        self.fields['exam_list'] = ExamSerializer(many=True)
        return super(CourseSerializer, self).to_representation(instance)

