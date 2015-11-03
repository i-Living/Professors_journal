from django.db import models

class Professor(models.Model):
    name = models.TextField()
    
    def __str__(self):
        return self.name
    
class Subject(models.Model):
    professor = models.ForeignKey('Professor')
    title = models.TextField()
    
    def __str__(self):
        return self.title
    
class Subsection(models.Model):
    subject = models.ForeignKey('Subject')
    title = models.TextField()
    
    def __str__(self):
        return str(self.title)
    
class Lesson(models.Model):
    subsection = models.ForeignKey('Subsection')
    lesson_type = models.BooleanField()
    date = models.DateField()

    def subsection_subject(self):
        return self.subsection.subject

    def __str__(self):
        return str(self.date) + '|' + str(self.subsection)
    
class Student(models.Model):
    name = models.TextField()
    
    def __str__(self):
        return self.name
    
class StudentLesson(models.Model):
    student = models.ForeignKey('Student')
    lesson = models.ForeignKey('Lesson')
    
    class Meta:
        unique_together = (('student', 'lesson'),)

    def __str__(self):
        return str(self.lesson) + ', ' + str(self.student)