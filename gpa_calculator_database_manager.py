import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user='root',
    password='root',
    database='studentGrades',
    port=3306
)

cursor = mydb.cursor()


def add_account(email, password, name, school):
    command = 'insert into students(email, studentPassword, name, school) values(%s, %s, %s, %s)'
    values = (email, password, name, school)
    cursor.execute(command, values)
    mydb.commit()


def add_grade(student_id, subject, grade, weighted, studentGrade):
    command = 'insert into grades(studentID, subject, grade, weighted, studentGrade) values(%s, %s, %s, %s, %s)'
    values = (student_id, subject, grade, weighted, studentGrade)
    cursor.execute(command, values)
    mydb.commit()


def update_grade(student_id, subject, grade):
    command = 'update grades set grade = %s where (subject = %s and studentID = %s)'
    values = (grade, subject, student_id)
    cursor.execute(command, values)
    mydb.commit()


def update_student_grade(studentID, grade):
    command = 'update students set studentGrade = %s where (studentID = %s)'
    values = (grade, studentID)
    cursor.execute(command, values)
    mydb.commit()


def delete_grade(student_id, subject):
    command = 'delete from grades where (studentID = %s and subject = %s)'
    values = (student_id, subject)
    cursor.execute(command, values)
    mydb.commit()


def get_all_grades(student_id):
    command = 'select * from grades where studentID = %s'
    values = (student_id,)
    cursor.execute(command, values)
    result = cursor.fetchall()

    accounts = []

    for row in result:
        grade_data = {
            "subject": row[2],
            "grade": row[3],
            "weighted": row[4],
            "lastUpdate": row[5]
        }

        grade = int(row[6])

        found_grade = None
        for account in accounts:
            if account["grade"] == grade:
                found_grade = account
                break

        if found_grade is None:
            accounts.append({"grade": grade, "subjects": [grade_data]})
        else:
            found_grade["subjects"].append(grade_data)

    # Calculate GPA for each grade
    for account in accounts:
        total_subjects = len(account["subjects"])

        unweighted_sum = 0
        weighted_sum = 0

        for subject in account["subjects"]:
            if subject["grade"] > 90:
                unweighted_sum += 4
                weighted_sum += 5
            else:
                unweighted_sum += subject["grade"] / 25
                weighted_sum += subject["grade"] / 20

        account["unweighted_gpa"] = unweighted_sum / total_subjects
        account["weighted_gpa"] = weighted_sum / total_subjects

    # Calculate overall GPAs based on the average of all subjects
    total_accounts = len(accounts)
    overall_unweighted_gpa = sum(account["unweighted_gpa"] for account in accounts) / total_accounts
    overall_weighted_gpa = sum(account["weighted_gpa"] for account in accounts) / total_accounts

    accounts.append({"overall": {"unweighted_gpa": overall_unweighted_gpa, "weighted_gpa": overall_weighted_gpa}})
    return accounts


def login(email, password):
    command = 'select * from students where email LIKE %s and studentPassword LIKE %s'
    values = (email, password)
    cursor.execute(command, values)
    result = cursor.fetchall()

    if not result == []:
        return result[0]
