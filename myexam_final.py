import mysql.connector as ms
from tabulate import tabulate
import os, csv, random

prnt_dir = os.getcwd()
if not os.path.exists(os.path.join(prnt_dir, "time_tables")):
    os.makedirs(os.path.join(prnt_dir, "time_tables"))

if not os.path.exists(os.path.join(prnt_dir, "text_files")):
    os.makedirs(os.path.join(prnt_dir, "text_files"))

if not os.path.exists(os.path.join(prnt_dir, "sample_papers")):
    os.makedirs(os.path.join(prnt_dir, "sample_papers"))

pwd = input('enter mysql password:')
mydb = ms.connect(host='localhost', user='root', passwd=pwd)

if mydb.is_connected():
    print('CONNECTION ESTABLISHED')

else:
    print('CONNECTION UNSUCCESSFUL')

mc = mydb.cursor()
mc.execute('CREATE DATABASE IF NOT EXISTS MYEXAM;')
mc.execute('USE MYEXAM;')

# master table
mc.execute('''

    CREATE TABLE IF NOT EXISTS SubjectCode (

        subject_code VARCHAR(255) PRIMARY KEY,

        subject_name VARCHAR(255)

    )

''')
mc.execute('''

    CREATE TABLE IF NOT EXISTS ClassCode (

        class_code VARCHAR(255) PRIMARY KEY,

        class_name VARCHAR(255)

    )

''')
mc.execute('''

    CREATE TABLE IF NOT EXISTS Exams (

        exam_code VARCHAR(255) PRIMARY KEY,

        exam_name VARCHAR(255)

    )

''')
mc.execute('''

    CREATE TABLE IF NOT EXISTS QuestionPaper (

        ecode VARCHAR(255),

        ccode VARCHAR(255),

        scode VARCHAR(255),

        marks_5 INTEGER,

        marks_4 INTEGER,

        marks_3 INTEGER,

        marks_2 INTEGER,

        marks_1 INTEGER
        
    )

''')
mc.execute('''

    CREATE TABLE IF NOT EXISTS PFILES(

        SCODE INT NOT NULL,

        ECODE INT NOT NULL,

        CCODE INT NOT NULL,

        FILES VARCHAR(100)

    )

''')
mydb.commit()  ##change it for all


# SYLLABUS MANAGEMENT
def manual():
    mc.execute('SELECT * FROM EXAMS ORDER BY EXAM_CODE')
    examdata = mc.fetchall()
    mc.execute('SELECT * FROM CLASSCODE ORDER BY CLASS_CODE')
    classdata = mc.fetchall()
    mc.execute('SELECT * FROM SUBJECTCODE ORDER BY SUBJECT_CODE')
    subjectdata = mc.fetchall()

    print(tabulate(examdata, headers=['EXAM_CODE', 'EXAM_NAME'], tablefmt="fancy_grid"))
    print(tabulate(classdata, headers=['CLASS_CODE', 'CLASS_NAME'], tablefmt="fancy_grid"))
    print(tabulate(subjectdata, headers=['SUBJECT_CODE', 'SUBJECT_NAME'], tablefmt="fancy_grid"))
    ecode = input('ENTER THE EXAM CODE\n(AS GIVEN IN THE ABOVE TABLE):')
    ccode = input('ENTER THE CLASS CODE\n(AS GIVEN IN THE ABOVE TABLE):')
    scode = input('ENTER THE SUBJECT CODE\n(AS GIVEN IN THE ABOVE TABLE):')
    return [scode, ecode, ccode]


def addpor(scode, ecode, std):
    if int(std) <= 112 and len(scode) == 3:
        f_name = std + ecode + scode + '.txt'
        add = 'INSERT INTO PFILES(SCODE,ECODE,CCODE,FILES) VALUES(%s,%s,%s,%s)'
        mc.execute(add, (scode, ecode, std, f_name))
        f_path = os.path.join(prnt_dir, "text_files", f_name)
        try:
            f = open(f_path, 'a')
            input('''NOW YOU WILL BE GIVEN A NOTEPAD, WHERE YOU CAN ENTER THE SYLLABUS 
AND HIT CTRL+S TO SAVE THE FILE
PRESS ENTER TO CONTINUE :''')
            os.startfile(f_path)
            input('IF YOU ARE DONE ENTERING THE INFORMATION HIT [ENTER] : ')
            print('PROCESS SUCCESSFUL')
            f.close()
        except ms.Error as err:
            print(f"Error: {err}")
        mydb.commit()
    else:
        print('INVALID STANDARD')


def delpor(mod, ecode, ccode):
    try:
        mc.execute(f'SELECT FILES FROM PFILES WHERE CCODE={ccode} AND ECODE={ecode} AND SCODE={mod}')
        lst = mc.fetchall()
        print(lst[0][0])
        f_modpath = os.path.join(prnt_dir, "text_files", lst[0][0])
        os.remove(f_modpath)
        mc.execute(f'DELETE FROM PFILES WHERE CCODE={ccode} AND ECODE={ecode} AND SCODE={mod}')
        print('Deleted Successful...')
    except ms.Error as err:
        print(f"Error: {err}")


def modpor(mod, ecode, ccode):
    try:
        mc.execute(f'SELECT FILES FROM PFILES WHERE CCODE={ccode} AND ECODE={ecode} AND SCODE={mod}')
        lst = mc.fetchall()
        f_modpath = os.path.join(prnt_dir, "text_files", lst[0][0])
        f = open(f_modpath, 'a')
        input(
            'NOW YOU WILL BE GIVEN A NOTEPAD, WHERE YOU CAN CHANGE \n'
            'THE SYLLABUS AND HIT CTRL+S TO SAVE THE FILE '
            '\nPRESS ENTER TO CONTINUE : ')

        os.startfile(f_modpath)
        input('If you are done changing the information hit [ENTER] : ')
        f.close()
        print('Process succesful')
        print('*' * 50)
    except ms.Error as err:
        print(f"Error: {err}")


def see_whole_por(cls):
    try:
        finder = f'SELECT FILES FROM PFILES WHERE CCODE={cls}+"%"'
        mc.execute(finder)
        d_names = mc.fetchall()
        d_names_lst = []
        new_fo = open(os.path.join(prnt_dir, "text_files", 'whole_syl.txt'), 'a+')
        for i in d_names:
            d_names_lst.append(i[0])
        for j in d_names_lst:
            path = os.path.join(prnt_dir, "text_files", j)
            with open(path) as sub_file:
                data = sub_file.read()
                new_fo.writelines([data, '\n', '\n', '~' * 100, '-' * 100])
        new_fo.seek(0)
        final_syl = new_fo.read()
        print('The entire syllabus of standard', cls, 'is here --->')
        print(final_syl)
        new_fo.close()
        os.remove(os.path.join(prnt_dir, "text_files", 'whole_syl.txt'))
    except ms.Error as err:
        print(f"Error: {err}")


def see_specific_por(mod, ecode, ccode):
    try:
        mc.execute(f'SELECT FILES FROM PFILES WHERE CCODE={ccode} AND ECODE={ecode} AND SCODE={mod}')
        lst = mc.fetchall()
        f_modpath = os.path.join(prnt_dir, "text_files", lst[0][0])
        f = open(f_modpath, 'r')
        data = f.read()
        print('The syllabus of the subject is here--->')
        print(data)
        print('\n', "~" * 100, '\n', '-' * 100)
        f.close()
    except ms.Error as err:
        print(f"Error: {err}")


def admin():
    try:
        mc.execute('SELECT CCODE,SCODE,ECODE,FILES FROM PFILES ORDER BY CCODE')
        data = mc.fetchall()
        print('The following table contains the list of subjects \n'
              'which have the syllabus information filled---> ')
        print(tabulate(data, headers=['Standard', 'Subjects'], tablefmt="fancy_grid"))
        print('\n', '\n', '~' * 100, '\n', '-' * 100)
    except ms.Error as err:
        print(f"Error: {err}")


# attendence login
def create_attendance_record(student_id, student_name, adate, status):
    try:
        sql = """CREATE TABLE IF NOT EXISTS  attendance
        (student_id INTEGER NOT NULL ,adate DATE,  student_name TEXT,  status TEXT, PRIMARY KEY(student_id,adate)  )"""
        mc.execute(sql)
        sql = "INSERT INTO attendance (student_id, student_name, adate, status) VALUES (%s, %s, %s, %s)"
        values = (student_id, student_name, adate, status)
        mc.execute(sql, values)
        mydb.commit()
        print("Attendance record created successfully.")
    except ms.Error as err:
        print(f"Error: {err}")


def read_attendance_records():
    try:
        sql = "SELECT * FROM attendance"
        mc.execute(sql)
        records = mc.fetchall()
        for record in records:
            print(record)
    except ms.Error as err:
        print(f"Error: {err}")


def update_attendance_record(student_id, adate, new_status):
    try:
        sql = "UPDATE attendance SET status = %s WHERE student_id = %s and adate=%s"
        values = (new_status, student_id, adate)
        mc.execute(sql, values)
        mydb.commit()
        print("Attendance record updated successfully.")
    except ms.Error as err:
        print(f"Error: {err}")


def delete_attendance_record(student_id, adate):
    try:
        sql = "DELETE FROM attendance WHERE student_id = %s and adate=%s"
        values = (student_id, adate)
        mc.execute(sql, values)
        mydb.commit()
        print("Attendance record deleted successfully.")
    except ms.Error as err:
        print(f"Error: {err}")


def read_specific_records(student_id):
    try:
        sql = f'''SELECT * FROM attendance WHERE student_id = '{student_id}'
'''
        mc.execute(sql)
        records = mc.fetchall()
        for record in records:
            print(record)
    except ms.Error as err:
        print(f"Error: {err}")


##QP pattern
def add_subject_code():
    print('inserting into subjectcode')
    while True:

        subject_code = input("Enter the subject code: ")

        subject_name = input("Enter the subject name: ")

        str1 = f'''

            INSERT INTO SubjectCode (subject_code, subject_name)

            VALUES ('{subject_code}', '{subject_name}')
            

        '''

        mc.execute(str1)

        mydb.commit()
        ask = input('do you want to continue(y/n)')
        if ask == 'y':
            continue
        elif ask == 'n':
            break
        else:
            print('invalid choice')


def add_class_code():
    print('inserting into classcode')
    while True:

        class_code = input("Enter the class code: ")

        class_name = input("Enter the class name: ")
        str2 = f'''

            INSERT INTO ClassCode (class_code, class_name)

            VALUES ('{class_code}', '{class_name}')

        '''
        mc.execute(str2)

        mydb.commit()
        ask = input('do you want to continue(y/n)')
        if ask == 'y':
            continue
        elif ask == 'n':
            break
        else:
            print('invalid choice')


def add_exam():
    print('inserting into exams')
    while True:

        exam_code = input("Enter the exam code: ")

        exam_name = input("Enter the exam name: ")
        str3 = f'''

            INSERT INTO Exams (exam_code, exam_name)

            VALUES ('{exam_code}', '{exam_name}')

        '''

        mc.execute(str3)

        mydb.commit()
        ask = input('do you want to continue(y/n)')
        if ask == 'y':
            continue
        elif ask == 'n':
            break
        else:
            print('invalid choice')


def update_subjectcode():
    while True:
        subject_code = int(input('enter the subject code to be updated'))
        subject_name = input('enter the subject name to bve updated')
        str5 = f'''UPDATE subjectcode set subject_name='{subject_name}' WHERE subject_code='{subject_code}'
'''
        mc.execute(str5)
        mydb.commit()
        ask = input('do you want to continue(y/n)')
        if ask == 'y':
            continue
        elif ask == 'n':
            break
        else:
            print('invalid choice')


def update_classcode():
    while True:
        class_code = int(input('enter the class code to be updated'))
        class_name = input('enter the class name to be updated')
        str6 = f'''UPDATE classcode set class_name='{class_name}' WHERE class_code='{class_code}'
'''
        mc.execute(str6)
        mydb.commit()
        ask = input('do you want to continue(y/n)')
        if ask == 'y':
            continue
        elif ask == 'n':
            break
        else:
            print('invalid choice')


def update_exams():
    while True:
        exam_code = int(input('enter the exam code to be updated'))
        exam_name = input('enter the exam name to be updated')
        str7 = f'''UPDATE exams set exam_name='{exam_name}' WHERE exam_code='{exam_code}'
'''
        mc.execute(str7)
        mydb.commit()
        ask = input('do you want to continue(y/n)')
        if ask == 'y':
            continue
        elif ask == 'n':
            break
        else:
            print('invalid choice')


def delete_subjectcode():
    while True:
        subject_code = int(input('enter subject code to be deleted'))
        mc.execute(f'''delete from subjectcode where subject_code='{subject_code}'
''')
        mydb.commit()
        ask = input('do you want to continue(y/n)')
        if ask == 'y':
            continue
        elif ask == 'n':
            break
        else:
            print('invalid choice')


def delete_classcode():
    while True:
        class_code = int(input('enter class code to be deleted'))
        mc.execute(f'''delete from classcode where class_code='{class_code}'
''')
        mydb.commit()
        ask = input('do you want to continue(y/n)')
        if ask == 'y':
            continue
        elif ask == 'n':
            break
        else:
            print('invalid choice')


def delete_exams():
    while True:
        exam_code = int(input('enter exam code to be deleted'))
        mc.execute(f'''delete from exams where exam_code='{exam_code}'
''')
        mydb.commit()
        ask = input('do you want to continue(y/n)')
        if ask == 'y':
            continue
        elif ask == 'n':
            break
        else:
            print('invalid choice')


def add_question_paper_pattern(subject_code, exam_code, class_code):
    print('adding qp pattern')

    marks_5 = input("Enter marks for 5 marks questions (press Enter if not applicable): ")

    marks_4 = input("Enter marks for 4 marks questions (press Enter if not applicable): ")

    marks_3 = input("Enter marks for 3 marks questions (press Enter if not applicable): ")

    marks_2 = input("Enter marks for 2 marks questions (press Enter if not applicable): ")

    marks_1 = input("Enter marks for 1 mark questions (press Enter if not applicable): ")

    # Check if any of the marks is entered before inserting into the database

    if marks_5 or marks_4 or marks_3 or marks_2 or marks_1:
        str4 = f'''

            INSERT INTO QuestionPaper (ecode, ccode, scode, marks_5, marks_4, marks_3, marks_2, marks_1)

            VALUES ('{exam_code}', '{class_code}', '{subject_code}', '{marks_5 or 'NULL'}', '{marks_4 or 'NULL'}', '{marks_3 or 'NULL'}', '{marks_2 or 'NULL'}', '{marks_1 or 'NULL'}')

        '''

        mc.execute(str4)

        mydb.commit()

    else:

        print("No marks entered. Question paper pattern not added.")

    mc.execute(f'''

        SELECT * FROM QuestionPaper

        WHERE ecode='{exam_code}' AND ccode='{class_code}' AND scode='{subject_code}'

    ''')

    pattern = mc.fetchone()

    if pattern:

        print(f"\nQuestion Paper Pattern for {exam_code}, Class {class_code}, Subject {subject_code}:")

        if pattern[3] is not None:
            print(f"5 Marks: {pattern[3]}")

        if pattern[4] is not None:
            print(f"4 Marks: {pattern[4]}")

        if pattern[5] is not None:
            print(f"3 Marks: {pattern[5]}")

        if pattern[6] is not None:
            print(f"2 Marks: {pattern[6]}")

        if pattern[7] is not None:
            print(f"1 Mark: {pattern[7]}")

    else:

        print("Question paper pattern not found.")


def read_question_paper_pattern(subject_code, exam_code, class_code):
    print('read the qp pattern')

    mc.execute(f'''

        SELECT * FROM QuestionPaper

        WHERE ecode='{exam_code}' AND ccode='{class_code}' AND scode='{subject_code}'

    ''')

    pattern = mc.fetchone()

    if pattern:

        print(f"\nQuestion Paper Pattern for {exam_code}, Class {class_code}, Subject {subject_code}:")

        if pattern[3] is not None:
            print(f"5 Marks: {pattern[3]}")

        if pattern[4] is not None:
            print(f"4 Marks: {pattern[4]}")

        if pattern[5] is not None:
            print(f"3 Marks: {pattern[5]}")

        if pattern[6] is not None:
            print(f"2 Marks: {pattern[6]}")

        if pattern[7] is not None:
            print(f"1 Mark: {pattern[7]}")

    else:

        print("Question paper pattern not found.")


##sample question paper
mc.execute('''
    create table if not exists samplepaper(
    
        scode int not null,
        
        ecode int not null,
        
        ccode int not null,
        
        qppdf varchar(111) unique,
        
        anspdf varchar(111) unique

)
''')


def add_sample_paper(scode, ecode, ccode, fpath, qppdf, anspdf):
    try:
        qppdf = ecode + scode + ccode + 'qp'
        anspdf = ecode + scode + ccode + 'ap'
        add = 'insert into samplepaper values(%s,%s,%s,%s,%s)'
        mc.execute(add, (scode, ecode, ccode, qppdf, anspdf))
        g1_path = os.path.join(fpath, qppdf)
        g2_path = os.path.join(fpath, anspdf)
        f1_path = os.path.join(prnt_dir, "sample_papers", qppdf)
        f2_path = os.path.join(prnt_dir, "sample_papers", anspdf)
        os.rename(g1_path, f1_path)
        os.rename(g2_path, f2_path)
        print('Process successful')
        mydb.commit()
    except ms.Error as err:
        print(f"Error: {err}")


def open_sample_paper(scode, ecode, ccode):
    try:
        mc.execute(f'select qppdf,anspdf from samplepaper where ccode={ccode} and ecode={ecode} and scode={scode}')
        lst = mc.fetchall()
        f1_modpath = os.path.join(prnt_dir, "sample_papers", lst[0][0])
        f2_modpath = os.path.join(prnt_dir, "sample_papers", lst[0][1])
        print('1-CHECK SAMPLE QUESTION PAPER\n2-CHECK SAMPLE ANSWER PAPER\n3-EXIT')
        ch11 = int(input('ENTER YOUR CHOICE:'))
        if ch11 == 1:
            input('press [ENTER] to open question paper for {ecode}')
            f = open(f1_modpath, 'a')
            os.startfile(f1_modpath)
            f.close()
        elif ch11 == 1:
            input('press [ENTER] to open answer paper for {ecode}')
            f1 = open(f2_modpath, 'a')
            os.startfile(f2_modpath)
            f1.close()
        else:
            return
    except ms.Error as err:
        print(f"Error: {err}")


##time_table_retrival
def create_TB(tn):
    tn = 'TB' + str(tn)
    tc = f'''create table if not exists {str(tn)}(

             date date primary key,

             IX varchar(50),

             X varchar(50),

             XI varchar(50),

             XII varchar(50)

        )'''
    mc.execute(tc)
    mydb.commit()
    try:
        d = eval(input('ENTER 5 EXAM DATES(eg:"2006-09-26","2006-09-27","2006-09-28","2006-09-29","2006-09-30"):'))
    except Exception as a:
        print('\n', a, '\n')

    try:
        cix = ['english', 'mathematics', 'science', 'social science', 'tamil/hindi']
        cx = ['english', 'mathematics', 'science', 'social science', 'tamil/hindi']
        cxi = ['english', 'mathematics/bussiness', 'physics/economics', 'chemistry/accountancy',
               'biology/computer/applied maths']
        cxii = ['english', 'mathematics/applied maths', 'physics/bussiness', 'chemistry/accountancy',
                'biology/economics', 'computer']

        ni = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]
        rn = random.randint(0, 4)

        xiio = cxii.pop(random.randint(0, 4))

        vi = "insert into " + str(tn) + " values('" + str(d[0]) + "','','','','" + str(xiio) + "');"
        for i in range(1, 5):
            mc.execute("insert into " + tn + " values('" + str(d[i]) + "','" + str(cix[ni[rn]]) + "','" + str(
                cx[ni[rn + 1]]) + "','" + str(cxi[ni[rn + 2]]) + "','" + str(cxii[ni[rn + 3]]) + "');")
            rn += 1

        mc.execute(vi)
        mydb.commit()

        print('\nTIME TABLE SUCCESSFULLY CREATED\n\n')
    except Exception as a:
        print('\n', a, '\n')

    try:
        mc.execute('select * from ' + str(tn) + ';')
        fn = os.path.join(prnt_dir, "time_tables", str(tn) + '.csv')

        f = open(fn, 'w', newline='')
        w = csv.writer(f)
        w.writerow(['DATE', 'IX', 'X', 'XI', 'XII', ])

        for k in mc:
            w.writerow(list(k))
        f.close()
    except Exception as a:
        print('\n', a, '\n')
    try:
        mc.execute('select * from ' + str(tn) + ';')
        data = mc.fetchall()
        print('\n\n', '  ' * 20, tn)
        print(tabulate(data, headers=['date', 'IX', 'X', 'XI', 'XII'], tablefmt="fancy_grid"))
    except Exception as a:
        print('\n', a, '\n')


def readI_TB(tn):
    tn = 'TB' + str(tn)
    try:
        fn = os.path.join(prnt_dir, "time_tables", str(tn) + '.csv')
        fd = open(fn, 'r')
        a = input(f'\nPRESS [ENTER] TO OPEN TIME TABLE {tn} IN EXCEL:')
        os.startfile(fn)
        fd.close()
    except Exception as a:
        print('\n', a, '\n')


def readII_TB(tn):
    tn = 'TB' + str(tn)
    try:
        mc.execute('select * from ' + str(tn) + ';')
        data = mc.fetchall()
        print('\n\n', '  ' * 20, tn)
        print(tabulate(data, headers=['date', 'IX', 'X', 'XI', 'XII'], tablefmt="fancy_grid"))
    except Exception as a:
        print('\n', a, '\n')


def delete_TB(tn):
    tn = 'TB' + str(tn)
    try:
        mc.execute('drop table ' + str(tn) + ';')
        file_path = os.path.join(prnt_dir, "time_tables", str(tn) + '.csv')
        os.remove(file_path)
        print("\n\nDELETED SUCCESSFULLY.\n")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except PermissionError:
        print(f"Permission error: Unable to delete file '{file_path}'.")
    except Exception as a:
        print('\n', a, '\n')

    # master table


def display():
    try:
        mc.execute('SELECT * FROM EXAMS ORDER BY EXAM_CODE')
        examdata = mc.fetchall()
        mc.execute('SELECT * FROM CLASSCODE ORDER BY CLASS_CODE')
        classdata = mc.fetchall()
        mc.execute('SELECT * FROM SUBJECTCODE ORDER BY SUBJECT_CODE')
        subjectdata = mc.fetchall()
        a1 = [];
        n = len(subjectdata)
        for j in range(n - len(examdata)):
            examdata.append(('', ''))
        for j in range(n - len(classdata)):
            classdata.append(('', ''))
        for i in range(n):
            a1.append(examdata[i] + subjectdata[i] + classdata[i])
        print(
            tabulate(a1, headers=['EXAM_CODE', 'EXAM_NAME', 'SUBJECT_CODE', 'SUBJECT_NAME', 'CLASS_CODE', 'CLASS_NAME'],
                     tablefmt="fancy_grid"))
    except ms.Error as err:
        print(f"Error: {err}")


# checking if required data filled
def check(scode, ecode, ccode):
    try:
        mc.execute(f'''
            select scode,ecode,ccode
                from pfiles
                where ccode={ccode} and ecode={ecode} and scode={scode}''')
        lst1 = mc.fetchall()
        mc.execute(f'''
            select scode,ecode,ccode
                from samplepaper
                where ccode={ccode} and ecode={ecode} and scode={scode}''')
        lst2 = mc.fetchall()
        mc.execute(f'''
            select scode,ecode,ccode
                from questionpaper
                where ccode={ccode} and ecode={ecode} and scode={scode}''')
        lst3 = mc.fetchall()
        mydb.commit()
        if lst1 != [] and lst2 != [] and lst3 != []:
            return True
        elif lst1 != [] or lst2 != [] or lst3 != []:
            print('still exam details are need to be uploaded....')
            return False
        elif lst1 == [] and lst2 == [] and lst3 == []:
            print('no such exam found:(...')
            return False
        else:
            print('INVALID INPUTS')
    except ms.Error as err:
        print(f"Error: {err}")


# MAIN PROGRAM
while True:
    print('''
      MENU
1-ADMINISTRATIVE LOGIN
2-TEACHER LOGIN
3-STUDENT LOGIN
4-EXIT''')
    ch = int(input('ENTER YOUR CHOICE :'))
    if ch == 1:
        while True:
            print('''1-SPECIFY EXAM DETIALS
2-UPDATE EXAM DETIALS
3-DELETE EXAM DETIALS
4-EXIT''')
            ch1 = int(input('ENTER YOUR CHOICE :'))
            if ch1 == 1:
                print('''1-CREATE EXAM TIME TABLE
2-ADD NEW  SUBJECT CODE IN MASTER TABLE
3-ADD NEW CLASS CODE IN MASTER TABLE
4-ADD NEW EXAM CODE IN MASTER TABLE
5-TO VIEW WHOLE SYLLABUS OF A SPECIFIC STANDARD' 
6-TO DISPLAY THE SUBJECTS WHICH HAVE PORTION FILLED
7-ADD SAMPLE PAPER
8-VIEW SAMPLE PAPER
9-TO DISPLAY MASTER TABLES
10-EXIT''')
                ch5 = int(input('ENTER YOUR CHOICE :'))
                if ch5 == 1:
                    l = manual()
                    create_TB(l[1])
                elif ch5 == 2:
                    add_subject_code()
                elif ch5 == 3:
                    add_class_code()
                elif ch5 == 4:
                    add_exam()
                elif ch5 == 5:
                    l = manual()
                    see_whole_por(l[2])
                elif ch5 == 6:
                    admin()
                elif ch5 == 7:
                    l = manual()
                    fpath = input('ENTER FILE PATH(eg-E:\python programs\pdfs):')
                    qppdf = input('ENTER QP NAME(eg-qp.pdf):')
                    anspdf = input('ENTER ANS NAME(eg-ans.pdf):')
                    add_sample_paper(l[0], l[1], l[2], fpath, qppdf, anspdf)
                elif ch5 == 8:
                    l = manual()
                    open_sample_paper(l[0], l[1], l[2])
                elif ch5 == 9:
                    display()
                elif ch5 == 10:
                    print('EXITING TO HOME PAGE')
                    break
            if ch1 == 2:
                while True:
                    print('''1-UPDATE SUBJECT CODE MASTER TABLE
2-UPDATE CLASS CODE MASTER TABLE
3-UPDATE EXAM CODE MASTER TABLE
4-EXIT TO HOME PAGE''')
                    ch6 = int(input('ENTER YOUR CHOICE :'))
                    if ch6 == 1:
                        update_subjectcode()
                    elif ch6 == 2:
                        update_classcode()
                    elif ch6 == 3:
                        update_exams()
                    elif ch6 == 4:
                        print('EXITING TO HOME PAGE')
                        break
            if ch1 == 3:
                print('''1-DELETE TIME TABLE
2-DELETE FROM SUBJECT CODE MASTER TABLE
3-DELETE FROM CLASS CODE MASTER TABLE
4-DELETE FROM EXAM CODE MASTER TABLE
5-EXIT''')
                ch8 = int(input('ENTER YOUR CHOICE :'))
                if ch8 == 1:
                    l = manual()
                    delete_TB(l[1])
                elif ch8 == 2:
                    delete_subjectcode()
                elif ch8 == 3:
                    delete_classcode()
                elif ch8 == 4:
                    delete_exams()
                elif ch8 == 5:
                    print('EXITING TO HOME PAGE')
                    break
            if ch1 == 4:
                print('EXITING TO HOME PAGE')
                break

    elif ch == 2:
        while True:
            print('''1-ATTENDENCE
2-UPLOAD EXAM DETAILS
3-EXIT''')
            ch2 = int(input('ENTER YOUR CHOICE :'))
            if ch2 == 1:
                while True:
                    print('''1-CREATE ATTENDANCE RECORD
2-READ ATTENDANCE RECORD
3-READ SPECIFIC RECORDS
4-UPDATE ATTENDANCE RECORD
5-DELETE ATTENDANCE RECORD
6-EXIT''')
                    ch3 = int(input('ENTER YOUR CHOICE :'))
                    if ch3 == 1:
                        student_id = input("Enter student id: ")
                        student_name = input("Enter student name: ")
                        adate = input("Enter date (YYYY-MM-DD): ")
                        status = input("Enter status (Present/Absent): ")
                        create_attendance_record(student_id, student_name, adate, status)

                    elif ch3 == 2:
                        read_attendance_records()

                    elif ch3 == 3:
                        student_id = input("Enter student id: ")
                        read_specific_records(student_id)

                    elif ch3 == 4:
                        student_id = input("Enter student ID to update: ")
                        adate = input("Enter date to update: ")
                        new_status = input("Enter new status (Present/Absent): ")
                        update_attendance_record(student_id, adate, new_status)

                    elif ch3 == 5:
                        student_id = input("Enter student ID to delete: ")
                        adate = input("Enter date to be deleted: ")
                        delete_attendance_record(student_id, adate)

                    elif ch3 == 6:
                        print('EXITING TO HOME PAGE')
                        break

            elif ch2 == 2:
                while True:
                    print('''1-UPLOAD PORTION FOR EXAM
2-CHANGE PORTION FOR EXAM
3-DELETE PORTION FOR EXAM
4-CHECK PORTION FOR SPECIFIC SUBJECT 
5-UPLOAD SAMPLE PAPER FOR EXAM
6-ADD QUESTION PAPER PATTERN
7-DISPLAY QUESTION PAPER PATTERN
8-DISPLAY TIME TABLE
9-EXIT''')
                    ch7 = int(input('ENTER YOUR CHOICE :'))
                    if ch7 == 1:
                        l = manual()
                        try:
                            addpor(l[0], l[1], l[2])
                        except Exception as aiio:
                            print(aiio)

                    elif ch7 == 2:
                        l = manual()
                        try:
                            modpor(l[0], l[1], l[2])
                        except Exception as aiio:
                            print(aiio)

                    elif ch7 == 3:
                        l = manual()
                        try:
                            t = input('Do you really wanna delete the syllabus'
                                      'Y/n:')
                            if t == 'y':
                                delpor(l[0], l[1], l[2])
                            else:
                                pass
                        except Exception as aiio:
                            print(aiio)

                    elif ch7 == 4:
                        l = manual()
                        see_specific_por(l[0], l[1], l[2])

                    elif ch7 == 5:
                        l = manual()
                        fpath = input('ENTER FILE PATH(eg:-E:\python programs\pdfs):')
                        qppdf = input('ENTER QP NAME(eg:-qp.pdf):')
                        anspdf = input('ENTER ANS NAME(eg:-ans.pdf):')
                        add_sample_paper(l[0], l[1], l[2], fpath, qppdf, anspdf)

                    elif ch7 == 6:
                        l = manual()
                        add_question_paper_pattern(l[0], l[1], l[2])

                    elif ch7 == 7:
                        l = manual()
                        read_question_paper_pattern(l[0], l[1], l[2])

                    elif ch7 == 8:
                        print('''
1-DISPLAY TIME TABLE IN MSEXCEL
2-DISPLAY TIME TABLE IN PYTHON
3-EXIT''')
                        ch9 = int(input('ENTER YOUR CHOICE :'))
                        if ch9 == 1:
                            l = manual()
                            readI_TB(l[1])
                        elif ch9 == 2:
                            l = manual()
                            readII_TB(l[1])
                        elif ch9 == 3:
                            print('EXITING TO HOME PAGE')
                            break
                    elif ch7 == 9:
                        print('EXITING TO HOME PAGE')
                        break

            elif ch2 == 3:
                print('EXITING TO HOME PAGE')
                break

    elif ch == 3:
        while True:
            print('''1-CHECK EXAM DETAILS
2-CHECK ATTENDENCE
3-EXIT''')
            ch4 = int(input('Enter your choice :'))
            if ch4 == 1:
                try:
                    l = manual()
                    if check(l[0], l[1], l[2]):
                        print('EXAM DETIALS')
                        readII_TB(l[1])
                        read_question_paper_pattern(l[0], l[1], l[2])
                        see_specific_por(l[0], l[1], l[2])
                        open_sample_paper(l[0], l[1], l[2])
                except ms.Error as err:
                    print(f"Error: {err}")
            elif ch4 == 2:
                try:
                    student_id = input("Enter student id: ")
                    read_specific_records(student_id)
                except ms.Error as err:
                    print(f"Error: {err}")
            elif ch4 == 3:
                print('EXITING TO HOME PAGE')
                break

    elif ch == 4:
        print('EXITING...:)')
        break
    else:
        break


def remove():
    mc.execute('''
    drop table  classcode        ;
    drop table  subjectcode      ;
    drop table  exams            ;
    ''')
    print('PROCESS SUCCESSFUL')
    if input('do u really want to drop important tables  y/n:') == 'y':
        mc.execute('''drop table  QuestionPaper    ;
                    drop table  pfiles             ;
                    drop table  samplepaper        ;''')
        print('PROCESS SUCCESSFUL')


def drop():
    if input('do u really want to drop database y/n:') == 'y':
        mc.execute('''
    drop database myexam''')
        mydb.commit()
        print('PROCESS SUCCESSFUL')


def insert():
    t1 = 'ClassCode'
    a = '109', '110', '111', '112'
    b = 'NINE_TH', 'TEN_TH', 'ELEVEN_TH', 'TWELVE_TH'
    for i in range(len(a)):
        mc.execute(f"insert into {t1} values('{a[i]}','{b[i]}')")
    mydb.commit()

    t1 = 'SubjectCode'
    a = '041', '042', '043', '044', '301', '106', '083', '027', '029'
    b = 'MATHS', 'PHYSICS', 'CHEMISRY', 'BIOLOGY', 'ENGLISH_CORE', 'TAMIL', 'COMPUTER_SCIENCE', 'HISTORY', 'GEOGRAPHY'
    for i in range(len(a)):
        mc.execute(f"insert into {t1} values('{a[i]}','{b[i]}')")
    mydb.commit()

    t1 = 'EXAMS'
    a = '201', '202', '203', '204', '205', '206', '207', '208', '209', '210'
    b = 'SET_I', 'SET_II', 'MID_TERM', 'SET_III', 'SET_IV', 'QUATERLY', 'SET_V', 'SET_VI', 'HALF_YEARLY', 'REVISION_I'
    for i in range(len(a)):
        mc.execute(f"insert into {t1} values('{a[i]}','{b[i]}')")
    mydb.commit()
    print('PROCESS SUCCESSFUL')


if ch == 100:
    insert()
elif ch == 1234:
    drop()
elif ch == 101:
    remove()
