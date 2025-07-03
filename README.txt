This file contains useful information about the quiz software and how to use it
The log file should contain any errors that may need to be addressed when run, without changing code
It is a good idea to check the log file whenever you see it has been written to as errors may be supressed during runtime, written to the log, and still continue to run despite the error

Quizzes:

Any files in the quizzes folder beginning with # will not be made into quizzes at runtime
If an invalid file in this folder is loaded at runtime, it will state "error loading quiz on (date) at (time)" in the log

var -  quizzes[desiredlesson][desiredquestion][part]
file structure: /subjects/subjectname.txt

Must have a minimum of 2 answers (obviously) and while it won't crash with over 5 answers, any answers after 5 will never be shown to a student.



To get the current unix timestamp   int(datetime.now().timestamp())
To get the date from a unix timestamp datetime.fromtimestamp(unix)

May be added back to loadquizzes(), first line after the first for:
        if subject.startswith('#'):
            continue

Beep Boop Beep Boop?