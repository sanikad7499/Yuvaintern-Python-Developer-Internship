print("STUDENT GRADE CALCULATOR")

name = input("Enter student name: ")

subjects = ["Python", "Mathematics", "Computer Science"]
marks = []

for subject in subjects:
    mark = float(input("Enter marks for " + subject + ": "))
    marks.append(mark)

total = sum(marks)
percentage = total / len(subjects)

print("\n----- RESULT -----")
print("Student:", name)
print("Total Marks:", total)
print("Percentage:", percentage, "%")

if percentage >= 75:
    print("Grade: A")
elif percentage >= 60:
    print("Grade: B")
elif percentage >= 40:
    print("Grade: C")
else:
    print("Grade: Fail")