#File/Folder Path Config
TEAMS_FILE = "teams.txt"
PLAYERS_FILE = "players.txt"
GAMES_FILE = "games.txt"

from os import popen
from os import listdir
from datetime import datetime
from random import randint
#tfr = open(TEAMS_FILE, "r") #tfr - teams file, read
#tfa = open(TEAMS_FILE, "a") #tfa - teams file, append
#pfr = open(PLAYERS_FILE, "r") #pfr - players file, read
#pfa = open(PLAYERS_FILE, "a") #pfa - players file, append
teams = {}

def modifyplayer(team): #player creation screen, a non existent player can be given
    #Needs attributes' name, attack, defense, needs to save/load team attribute but not use it because team is parent dict and better memory usage
    while True:
        name = input("Please enter their name ").lower().strip()
        atk = input("Please enter their attack (0-10) ").strip()
        dfn = input("Please enter their defense (0-7) ").strip()
        if name.isalpha() and atk.isdecimal() and dfn.isdecimal():
            if int(atk) <= 10 and int(atk) >= 0 and int(dfn) <= 7 and int(dfn) >= 0:
                atk = int(atk)
                dfn = int(dfn)
                break
            else:
                print("Invalid attack/defense value")
        else:
            print("Invalid name/atk/dfn, contained numbers/letters or symbols.")
    tfr.seek(0) #make sure tfr is at beginning
    tfa.write(name + "|" + str(atk) + "|" + str(dfn) + "|\n")
    print("Player '" + name + "' created")
    tfa.close() #they shouldnt need to be used after this point
    tfr.close()

def selectplayer(): #player selection screen
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

def loadgames():
    global games
    games = {}
    gfr = open(GAMES_FILE, "r") #gfr - games file, read
    for line in gfr.readlines():
        line = line.strip()
        if line.startswith('#'):  #allow comments in reports file
            continue
        parts = line.split('|') #team, dfn, atk, num, name
        #game = parts[0].strip()
        games[team1]
        games[team]['player' + parts[3].strip()] = {}
        teams[team]['player' + parts[3].strip()]['name'] = parts[4].strip()
        teams[team]['player' + parts[3].strip()]['dfn'] = parts[1].strip()
        teams[team]['player' + parts[3].strip()]['atk'] = parts[2].strip()
    gfr.close()

loadgames()
print(games)

def loadteams():
    global teams
    tfr = open(TEAMS_FILE, "r") #tfr - teams file, read
    for line in tfr.readlines():
        line = line.strip()
        if line.startswith('#'):  #allow comments in reports file
            continue
        parts = line.split('|')
        team = parts[0].strip()
        #teams['num'] += 1
        try:
            if teams[team] == {}:
                pass
        except:
            teams[team] = {}
        teams[team]['wins'] = parts[1].strip()
        teams[team]['draws'] = parts[2].strip()
        teams[team]['losses'] = parts[3].strip()
        teams[team]['letin'] = parts[4].strip()
    tfr.close()

def loadplayers(): #loadplayers() and loadteams() must both be called for full team data but can be called independently
    global teams
    pfr = open(PLAYERS_FILE, "r") #pfr - players file, read
    for line in pfr.readlines():
        line = line.strip()
        if line.startswith('#'):  #allow comments in reports file
            continue
        parts = line.split('|') #team, dfn, atk, num, name
        team = parts[0].strip()
        try:
            if teams[team] == {}:
                pass
        except:
            teams[team] = {}
        teams[team]['player' + parts[3].strip()] = {}
        teams[team]['player' + parts[3].strip()]['name'] = parts[4].strip()
        teams[team]['player' + parts[3].strip()]['dfn'] = parts[1].strip()
        teams[team]['player' + parts[3].strip()]['atk'] = parts[2].strip()
    pfr.close()

#loadplayers()
#print(teams, "\n")
#loadteams()
#loadplayers()
#print(teams)
#print(teams[input("input a team ")]['player' + input("input a player number ")][input("input data field")])

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

#preloginscreen()
#loadteams()

#could add the times to report lookup but cba
#make it so in reportlookup (student) it displays what quizzes are available to view the reports of by looking through the reports file and seeing which quizzes that user has completed
