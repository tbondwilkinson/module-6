#!/usr/bin/python

import sys


class Student:
    def __init__(self):
        self.firstName = ""
        self.lastName = ""
        self.examGrades = []
        self.labGrades = []
        self.finalGrade = 0.0
        self.finalLetter = ""

f = open('./grades.txt')
firstLine = f.readline().split(",")
numLabs = int(firstLine[0])
numExams = int(firstLine[1])
labWeight = float(firstLine[2])

grades = {}

# Read in all of the students
line = f.readline()
while line > "":
    parsedLine = line.split("\t")
    # Check to make sure we have a well formatted line
    if len(parsedLine) < 4:
        line = f.readline()
        continue
    if parsedLine[1] in grades:
        student = grades[parsedLine[1]]
    else:
        student = Student()
        student.firstName = parsedLine[0]
        student.lastName = parsedLine[1]
        grades[parsedLine[1]] = student

    parsedLine[3] = parsedLine[3].rstrip()
    if parsedLine[3] == 'lab':
        student.labGrades.append(float(parsedLine[2]))
    elif parsedLine[3] == 'exam':
        student.examGrades.append(float(parsedLine[2]))

    line = f.readline()

# Calculate grades
for student in grades.itervalues():
    for labGrade in student.labGrades:
        student.finalGrade += labGrade * labWeight / numLabs
    for examGrade in student.examGrades:
        student.finalGrade += examGrade * (1 - labWeight) / numExams

    if student.finalGrade >= 90.0:
        student.finalLetter = "A"
    elif student.finalGrade >= 80.0:
        student.finalLetter = "B"
    elif student.finalGrade >= 70.0:
        student.finalLetter = "C"
    elif student.finalGrade >= 60.0:
        student.finalLetter = "D"
    else:
        student.finalLetter = "F"

gradesByLastName = sorted(grades.itervalues(),
    key=lambda student: student.lastName)

limit = False
limiter = ""
if len(sys.argv) > 1:
    limit = True
    limiter = sys.argv[1]

for student in gradesByLastName:
    if not limit or limiter in student.firstName or limiter in student.lastName:
        print '{0} {1} recieves a {2} ({3})'.format(student.lastName,
            student.firstName, student.finalLetter, student.finalGrade)
