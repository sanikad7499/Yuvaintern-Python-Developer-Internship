name = input("Enter student name: ")

marks = []

for i in range(3):
    mark = float(input("Enter subject marks: "))
    marks.append(mark)

total = sum(marks)
average = total / 3

print("\nStudent Name:", name)
print("Total Marks:", total)
print("Average Marks:", average)

if average >= 75:
    print("Grade: Distinction")
elif average >= 60:
    print("Grade: First Class")
elif average >= 40:
    print("Grade: Pass")
else:
    print("Grade: Fail")