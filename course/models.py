from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + ' ' + self.second_name


class Course(models.Model):
    name = models.CharField(max_length=300)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
