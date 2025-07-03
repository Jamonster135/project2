#File/Folder Path Config
USER_ACCOUNTS_FILE = "useraccounts.txt"
QUIZ_FOLDER = "quizzes"
REPORTS_FILE = "reports.txt"

from os import popen
from os import listdir
from datetime import datetime
from random import randint
uar = open(USER_ACCOUNTS_FILE, "r") #uar - user accounts, read
uaa = open(USER_ACCOUNTS_FILE, "a") #uaa - user accounts, append
username = "uf-error" #in case a username doesn't get set before use, to prevent crashes

def makepassword(name):
        global password
        password = input("Please enter your password ")
        if name in password:
            print("Invalid password, must not contain your name")
            makepassword(name)
        elif len(password) >= 5 and any(char.isdigit() for char in password): #check to make sure its equal/more than 5 characters and has at least 1 number for security
            pass
        else:
            print("Invalid password, your password must consist of at least 5 characters and 1 number")
            makepassword()

def acccreatescreen(): #account creation screen
    global age
    global username
    while True:
        name = input("Please enter your name ").lower().strip()
        age = input("Please enter your age ").strip()
        if name.isalpha() and age.isdecimal():
            if int(age) < 100:
                age = int(age)
                break
            else:
                print("Invalid age, over 100")
        else:
            print("Invalid name/age, contained numbers/letters or symbols.")
    makepassword(name)
    uar.seek(0) #make sure uar is at beginning
    suffixneeded = 0 #if this is more than 0, a - then this number is added onto the end
    for line in uar:
        usernameinfile = line.split('|')[0].strip() #split the line by | for username part
        if usernameinfile[:5] == name[:3] + str(age):
            suffixneeded = suffixneeded+1
    if suffixneeded == 0:
        username = name[:3] + str(age)
    else:
        username = name[:3] + str(age) + "-" + str(suffixneeded)
    print("Your username is", username, "and your password is", password)
    uaa.write(username + "|" + name + "|" + str(age) + "|" + password + "|\n")
    uaa.close() #they shouldnt need to be used after this point
    uar.close()

def accloginscreen(): #account login screen
    global username
    global age
    loginusername = input("Please enter your username ").lower()
    uar.seek(0) #make sure uar is at beginning
    for line in uar:
        usernameinfile = line.split('|')[0].strip() #split line by '|' and get the first (username) part
        if usernameinfile == loginusername: #check if the first part is the same username
            username = line.split('|')[0].strip() #make username that line (formatted correctly)
            filepassword = line.split('|')[3].strip()
                    
            break
    if username != "uf-error":
        #print("Found line with entered username:", username) #only used for debugging
        loginpassword = input("Please enter your password ")
        if filepassword == loginpassword:
            print("Login Successful ")
            del filepassword
            del loginpassword
            age = int(line.split('|')[2].strip())
            uaa.close() #they shouldnt need to be used after this point
            uar.close()
        else:
            print("Password Incorrect ")
            accloginscreen()
    else:
        print("Invalid Username")
        preloginscreen()

def preloginscreen():
    logcre = input("Do you want to create an account or login? ").lower().strip() #logcre - login/create
    if logcre == "create":
        acccreatescreen()
    elif logcre == "login":
        accloginscreen()
    else:
        print("Invalid input, please enter a valid input")
        preloginscreen()

def postloginscreen():
    quizrep = input("Do you want to take a quiz or see reports? ").lower().strip()
    if quizrep == "take" or quizrep == "quiz":
        takequiz()
    elif quizrep.lower().strip() == "see" or quizrep.lower().strip() == "report":
        loadreports(username)
        reportlookup()
    else:
        print("Invalid input, please enter a valid input")
        postloginscreen()


def loadquizzes():
    global quizzes
    global quizlist
    quizlist = None
    quizzes = {}
    for subject in listdir(QUIZ_FOLDER): #loop all subject files in folder
        try:
            subject_name = subject.split('.')[0]
            sfr = open(QUIZ_FOLDER + "/" + subject, 'r') #sfr - subject file, read
            questions = {}
            qnum = 1 #qnum - question number
            for line in sfr.readlines():
                line = line.strip()
                if line.startswith('#'):  #allow comments in question files
                    continue
                parts = line.split('|')
                question_data = {'question': parts[0].strip('"')}
                for i in range(1, len(parts) - 1): #dynamically add each answer as answer1 answer2 etc
                    question_data["answer[" + str(i) + "]"] = parts[i].strip('"')
                question_data['cans'] = int(parts[-1]) #store the correct answer number
                questions[qnum] = question_data
                qnum += 1  #increment the question number    
            quizzes[subject_name] = questions
        except:
            print("error loading quiz on", popen('echo %date%').read().strip(), "at", popen('echo %time%').read().strip() + "\n")
    for quiz in quizzes:
        if quizlist == None:
            quizlist = quiz
        else:
            quizlist = quizlist + ", " + quiz
                

def loadreports(name):
    global reports
    reports = {}
    rfr = open(REPORTS_FILE, 'r') #rfr - reports file, read
    rnum = 0
    for line in rfr.readlines():
        line = line.strip()
        if line.startswith('#'):  #allow comments in reports file
            continue
        if line.split('|')[0] == name:
            parts = line.split('|')
            report_data = {'username': parts[0].strip()}
            report_data['quiz'] = parts[1].strip()
            report_data['rnum'] = parts[2].strip()
            report_data['act'] = parts[3].strip()
            report_data['difficulty'] = parts[4].strip()
            report_data['time'] = parts[5]
            reports[rnum] = report_data
            rnum += 1
    rfr.close()

def quizlookup():
    print("Here, you can lookup quizzes, their questions and their answers")
    print("Quizzes:", quizlist)
    desiredlesson = input("What quiz would you like to inspect? ")
    if desiredlesson in quizzes:
        desiredquestion = input("What question number? (Press Enter to see all questions) ").strip() #ask for the question number
        if desiredquestion.isdigit(): #if the user provided a question number
            desiredquestion = int(desiredquestion)
            if desiredquestion in quizzes[desiredlesson]: #check if the specific question exists in the selected lesson
                question_data = quizzes[desiredlesson][desiredquestion]
                print("Question", str(desiredquestion) + ":", question_data['question'])
                for i in range(1, len(question_data) - 1):  #loop through all the answers
                    print("Answer", str(i) + ":", question_data["answer[" + str(i) + "]"])
                print("Correct Answer:", question_data['cans'])
            else:
                print("Question", desiredquestion, "not found in the lesson", desiredlesson + ".")
        else: #if the user did not specify a question number
            print("Question number, Question, Answers, Correct answer")
            for qnum, question_data in quizzes[desiredlesson].items(): #got me confused, quizzes[desiredlesson] contains all questions
                for i in range(1, len(question_data) - 1):
                    answers = " | ".join([question_data["answer[" + str(i) + "]"]])
                print("Question", str(qnum) + ":", question_data['question'], "|", answers, "|", question_data['cans'])
    else:
        print("Lesson", desiredlesson, "not found.")
    teacherscreen()

def takequiz():
    print("Here, you can take quizzes")
    print("Quizzes:", quizlist)
    act = 0
    difficulty = None
    quiz = input("What quiz would you like to take? ")
    while difficulty == None or difficulty < 2 or difficulty > 5:
        if difficulty != None:
            print("Invalid input, please enter a valid input")
        difficulty = int(input("How many possible answers would you like to choose from? (Min 2, max 5) ").strip())
    if quiz in quizzes:
        for question in range(1, len(quizzes[quiz])+1):
            random = randint(1, difficulty)
            question_data = quizzes[quiz][question]
            cans = question_data['cans']
            print("Question", str(question) + ":", question_data['question'])
            try: #tries to do all answers user wants but if there are not enough it will error or access bad data so instead does all answers
                if question_data["answer[" + str(difficulty+1) + "]"] != str(cans):
                    for i in range(1, difficulty+1):  #loop through all the answers
                        if cans > difficulty and i == random:
                            print("Answer", str(i) + ":", question_data["answer[" + str(cans) + "]"])
                            cans = i
                        else:
                            print("Answer", str(i) + ":", question_data["answer[" + str(i) + "]"])
            except:
                for i in range(1, len(question_data) - 1):  #loop through all the answers
                    print("Answer", str(i) + ":", question_data["answer[" + str(i) + "]"])
                #print("Correct Answer:", question_data['cans'])
            inans = input() # inans - inputted answer
            if inans == str(cans):
                print("Correct!")
                act = act+1 #act - answered correctly
            else:
                print("Incorrect!")
        percentage = str(act/len(quizzes[quiz])*100)[:5]
        #postquiz               amount correctly answered, out of total number of questions (percentage to 1 decimal place), grade, quiz name, difficulty answers
        print("You achieved a score of", str(act) + "/" + str(len(quizzes[quiz])), "(" + percentage + "%)", "for", getgradepostquiz(int(float(percentage))), "in '" + quiz + "' with", str(difficulty), "answers provided")
        writereport(quiz, act, difficulty) #calls the report function and passes the quiz name, how many questions were answered correctly, and the amount of answers available
        postloginscreen()
    else:
        print("Quiz '" + quiz + "' not found.")

def writereport(quiz, act, difficulty): #should be passed quiz, act, and difficulty as seen above ^^^
    rfa = open(REPORTS_FILE, "a") #rfa - reports file, append
    rfr = open(REPORTS_FILE, "r") #rfr - reports file, read
    rnum = 0
    for line in rfr: #its possible to loop the file backwards, look for the last entry of this user's reportnum and add 1 but could be more susceptible to corruption and duplicate entries
        if line.split('|')[0] == username:
            rnum = rnum+1
    rfa.write(username + '|' + quiz + '|' + str(rnum) + '|' + str(act) + '|' + str(difficulty) + '|' + str(int(datetime.now().timestamp())) + '\n') #username|quiz|rnum|act|difficulty|date\n
    loadreports(username) #(line above) turns the date into a unix timestamp (float) into an integer (to remove the miliseconds (decimals)) then string ^^^

def getgradepostquiz(percentage): #can only be used for after the quiz as it includes the a/an, because of this, i thought it easier to just have 2 different functions for the different use cases
    if percentage >= 90:
        return "an A"
    elif percentage >= 80:
        return "a B"
    elif percentage >= 65:
        return "a C"
    elif percentage >= 50:
        return "a D"
    elif percentage >= 35:
        return "an E"
    else:
        return "an F"

def reportlookup():
    quiz = input("What quiz's reports would you like to view? ")
    reversedreports = {key: reports[key] for key in reversed(sorted(reports.keys()))}
    #print(reversedreports)
    count = 0
    print("These are your last 10 '" + quiz + "' reports:")
    for i in reversedreports:
        if count >= 10:
            break
        if reversedreports[i]['quiz'] == quiz:
            percentage = str(int(reversedreports[i]['act']) / len(quizzes[quiz]) * 100)[:5]
            print(str(count+1) + ".", "You got", reversedreports[i]['act'] + "/" + str(len(quizzes[quiz])), "(" + percentage + "%)", "for", getgradepostquiz(int(float(percentage))), "with", reversedreports[i]['difficulty'], "answers provided")
            count += 1
    postloginscreen()

def reportlookupteacher():
    reversedreports = {key: reports[key] for key in reversed(sorted(reports.keys()))}
    count = 0
    #print(reversedreports)
    print("These are their last 10 reports:")
    for i in reversedreports:
        if count >= 10:
            break
        percentage = str(int(reversedreports[i]['act']) / len(quizzes[reports[i]['quiz']]) * 100)[:5]
        print(str(count+1) + ".", reports[i]['quiz'] + ": They got", reversedreports[i]['act'] + "/" + str(len(quizzes[reports[i]['quiz']])), "(" + percentage + "%)", "for", getgradepostquiz(int(float(percentage))), "with", reversedreports[i]['difficulty'], "answers provided")
        count += 1
    teacherscreen()

def teacherscreen():
    userorquiz = input("Do you want to view a user or a quiz report? ") #userorquiz - user or quiz
    if userorquiz == "user" or userorquiz == "student":
        wanteduser = input("Which user's reports would you like to see? ")
        loadreports(wanteduser)
        reportlookupteacher()
    elif userorquiz == "lesson" or userorquiz == "quiz":
        quizlookup()
    else:
        print("Invalid input!")
        teacherscreen()

preloginscreen()
loadquizzes()
if age < 18:
    postloginscreen()
else:
    teacherscreen()

#could add the times to report lookup but cba
#make it so in reportlookup (student) it displays what quizzes are available to view the reports of by looking through the reports file and seeing which quizzes that user has completed
