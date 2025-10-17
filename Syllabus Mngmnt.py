import os
import mysql.connector as sql
from tabulate import tabulate

prnt_dir = os.getcwd()
if not os.path.exists(os.path.join(prnt_dir, "text_files")):
    os.makedirs(os.path.join(prnt_dir, "text_files"))
link = sql.connect(host='localhost', user='root', password='20225186')

if link.is_connected():
    print('Connection established')

else:
    print('Connection unsuccessful')

mypen = link.cursor()
mypen.execute('create database if not exists pmanagement')
mypen.execute('use pmanagement')
mypen.execute('create table if not exists Classes(Standard varchar(10) primary key,Subjects varchar(900) not null)')
mypen.execute("create table if not exists pfiles(scode int primary key,files varchar(100))")
link.commit()
print('HI THERE , YOU ARE NOW GOING TO WORK WITH SYLLABUS MANAGEMENT SYSTEM')
print('~' * 70)
input('Press enter to continue')


def manual_writer(n):
    for i in range(n):
        try:
            stand = int(input('Enter the standard : '))
            z = int(input('Number of subjects you wish to enter : '))
            subj = '('
            for k in range(z):
                subs = input('Enter the subject : ')
                subcode = input('Enter the subject code : ')
                subj = subj + subs + '(' + subcode + ')' '  '
            subj = subj + ')'
            work = 'insert into classes(standard ,subjects) values(%s,%s)'
            mypen.execute(work, (stand, subj))
            print('Successfully entered')
            link.commit()
        except Exception as aiio:
            print(aiio)


def manual_editor(std):
    if int(std) <= 12:
        manual()
        try:
            z = int(input('Number of subjects you wish to enter : '))
            subj = '('
            for k in range(z):
                subs = input('Enter the subject : ')
                subcode = input('Enter the subject code : ')
                subj = subj + subs + '(' + subcode + ')' '  '
            subj = subj + ')'
            print(subj)
            chngr = 'update classes set subjects = %s where standard = %s '
            mypen.execute(chngr, (subj, std))
            link.commit()
            manual()
            print('Successfully updated')
        except Exception as aiio:
            print(aiio)
    else:
        print('Invalid standard given')


def manual():
    mypen.execute('select * from classes')
    data = mypen.fetchall()
    print(tabulate(data, headers=['Standard', 'Subjects'], tablefmt="fancy_grid"))


def addpor(sub, std, scode):
    if int(std) <= 12 and len(scode) == 3:
        f_name = std + sub + '.txt'
        add = 'insert into pfiles(scode,files) values(%s,%s)'
        mypen.execute(add, (scode, f_name))
        f_path = os.path.join(prnt_dir, "text_files", f_name)
        f = open(f_path, 'a')
        input('''Now you will be given a Notepad, where you can enter the syllabus 
    and hit Ctrl+s to save the file
    Press enter to continue :''')
        os.startfile(f_path)
        input('If you are done entering the information hit enter : ')
        print('Process successful')
        f.close()
        link.commit()
    else:
        print('Invalid standard')


def delpor(thooku):
    mypen.execute('select * from pfiles')
    lst = mypen.fetchall()
    n = len(lst)
    scode_list = []

    for i in range(n):
        scode_list.append(lst[i][0])

    if thooku in scode_list:
        index_of_del = scode_list.index(thooku)
        f_delpath = os.path.join(prnt_dir, "text_files", lst[index_of_del][1])
        os.remove(f_delpath)
        for i in lst:
            if i[0] == thooku:
                thookukairu = 'delete from pfiles where scode = %s'
                mypen.execute(thookukairu, (thooku,))
                link.commit()
                print('Deletion Successful...')

    elif thooku not in scode_list:
        print('Incorrect entry..'
              'syllabus does mot exist.. '
              'scode not found...')

    elif not lst != []:
        print('Underflow')


def modpor(mod):
    mypen.execute('select * from pfiles')
    lst = mypen.fetchall()
    n = len(lst)
    scode_list = []

    for i in range(n):
        scode_list.append(lst[i][0])

    if mod in scode_list:
        index_of_mod = scode_list.index(mod)
        f_modpath = os.path.join(prnt_dir, "text_files", lst[index_of_mod][1])
        f = open(f_modpath, 'a')
        input(
            'Now you will be given a Notepad, where you can change \n'
            'the syllabus and hit Ctrl+s to save the file '
            '\nPress enter to continue : ')
        os.startfile(f_modpath)
        input('If you are done changing the information hit enter : ')
        f.close()
        print('Process succesful')
        print('*' * 50)

    if mod not in scode_list:
        print('Incorrect entry.. scode not found...')


def see_whole_por(cls):
    finder = "select files from pfiles where scode like %s "
    mypen.execute(finder, (cls + '%',))
    d_names = mypen.fetchall()
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


def see_specific_por(to_see):
    mypen.execute('select * from pfiles')
    lst = mypen.fetchall()
    n = len(lst)
    scode_list = []

    for i in range(n):
        scode_list.append(lst[i][0])

    if to_see in scode_list:
        index_of_see = scode_list.index(to_see)
        f_seepath = os.path.join(prnt_dir, "text_files", lst[index_of_see][1])
        f = open(f_seepath, 'r')
        data = f.read()
        print('The syllabus of the subject is here--->')
        print(data)
        print('\n', '\n', "~" * 100, '\n', '-' * 100)
        f.close()

    if to_see not in scode_list:
        print('No such syllabus found')


def admin():
    mypen.execute('select * from pfiles')
    data = mypen.fetchall()
    print('The following table contains the list of subjects \n'
          'which have the syllabus information filled---> ')
    print(tabulate(data, headers=['Standard', 'Subjects'], tablefmt="fancy_grid"))
    print('\n', '\n', '~' * 100, '\n', '-' * 100)


while True:
    print('''1-ADD SYLLABUS FOR A SUBJECT 
2-DELETE THE SYLLABUS FOR A SUBJECT 
3-CHANGE THE SYLLABUS FOR A SUBJECT 
4-VIEW THE SYLLABUS FOR A SUBJECT 
5-MANUAL OPERATIONS
6-SUBJECTS WHICH HAVE SYLLABUS INFO FILLED
7-EXIT''')
    try:
        ch = int(input('Enter your choice: '))

        if ch == 1:
            manual()
            try:
                std = input('Enter the standard(just the number, like 12 or 11): ')
                sub = input('Enter the subject :')
                scode = input('Enter the subject code as given in the above table: ')
                addpor(sub, std, scode)
            except Exception as aiio:
                print(aiio)

        elif ch == 2:
            manual()
            try:
                thooku = int(input('Enter the scode of the syllabus which\n'
                                   'needs to be deleted (as given in the above table): '))
                t = int(input('Do you really wanna delete the syllabus\n'
                              '1-YES\n2-NO'))
                if t == 1:
                    delpor(thooku)
                else:
                    pass
            except Exception as aiio:
                print(aiio)

        elif ch == 3:
            manual()
            try:
                mod = int(input('Enter the scode of the syllabus in which\n'
                                'you want to make changes (as given in the above table): '))
                modpor(mod)
            except Exception as aiio:
                print(aiio)

        elif ch == 4:
            print(
                '1-TO VIEW WHOLE SYLLABUS OF A SPECIFIC STANDARD \n'
                '2-TO VIEW THE SYLLABUS FOR SPECIFIC SUBJECT IN A CLASS')
            try:
                x = int(input('Enter your choice : '))
                if x == 1:
                    cls = input('Enter the standard : ')
                    see_whole_por(cls)
                elif x == 2:
                    manual()
                    to_see = int(input('Enter the scode of the syllabus\n'
                                       'which you want ( as given in the above table): '))
                    see_specific_por(to_see)
                else:
                    print('Invalid entry')
            except Exception as aiio:
                print(aiio)

        elif ch == 5:
            print('1-ADD NEW STANDARDS TO MANUAL\n'
                  '2-TO EDIT THE SUBJECTS')
            try:
                v: int = int(input('Enter your choice : '))
            except Exception:
                print('Invalid entry')
            if v == 1:
                n = int(input('Enter the number of entries : '))
                manual_writer(n)
            elif v == 2:
                std = input('Enter the standard in which you want to make changes : ')
                manual_editor(std)
            else:
                print('Invalid entry')

        elif ch == 6:
            admin()

        elif ch == 7:
            print('Program Terminated')
            break

        else:
            print('Invalid entry')
            input('Press enter to re-enter the option : ')
    except Exception as aiio:
        print(aiio)