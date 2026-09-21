import json
import os
import random
import sqlite3
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database import get_db_connection, init_db

# ============================================================================
# 45 PILOT QUESTIONS  (Simple English, Easy-to-Medium Level)
#   - 15 Technical Knowledge  (mix of Descriptive + MCQ)
#   - 15 Workplace Scenarios  (mix of Descriptive + MCQ)
#   - 15 HR / Behavioural     (mix of Descriptive + MCQ)
# ============================================================================

PILOT_QUESTIONS = [

    # ---- TECHNICAL KNOWLEDGE (15 Questions) ----

    # TECH-01: Descriptive (Easy)
    {
        "id": "TECH-01",
        "pack_id": "pack-tech-01",
        "category": "Technical Knowledge",
        "difficulty": "Easy",
        "question_type": "descriptive",
        "question_text": "What is a database? Explain the difference between a table, a row, and a column with a simple example.",
        "rubric": [
            {"id": "c1", "name": "Basic Definition", "description": "Gives a clear, simple definition of a database as organized data storage.", "max_score": 4.0},
            {"id": "c2", "name": "Table / Row / Column", "description": "Explains that a table holds data, rows are records, and columns are fields.", "max_score": 3.0},
            {"id": "c3", "name": "Simple Example", "description": "Uses a real-life example like a student list or phone book.", "max_score": 3.0}
        ],
        "reference_material": "A database is an organized collection of data stored electronically. Data is kept in tables. Each table has columns (fields like Name, Age, City) and rows (individual records). For example, a 'Students' table might have columns: Roll_No, Name, Class. Each student is one row.",
        "keywords": ["database", "table", "row", "column", "record", "field", "organized", "data", "storage"],
        "options": None, "correct_option": None, "explanation": None
    },

    # TECH-02: MCQ (Easy)
    {
        "id": "TECH-02",
        "pack_id": "pack-tech-01",
        "category": "Technical Knowledge",
        "difficulty": "Easy",
        "question_type": "mcq",
        "question_text": "Which of the following is used to get data from a database table in SQL?",
        "rubric": [
            {"id": "c1", "name": "Correct Answer", "description": "Selects the correct SQL command.", "max_score": 10.0}
        ],
        "reference_material": "The SELECT statement is used to read or fetch data from a database table. INSERT adds new data, DELETE removes data, and UPDATE changes existing data.",
        "keywords": ["SELECT", "SQL", "query", "fetch", "data"],
        "options": ["INSERT", "SELECT", "DELETE", "UPDATE"],
        "correct_option": "SELECT",
        "explanation": "SELECT is the SQL command used to read and get data from a table. For example: SELECT * FROM Students;"
    },

    # TECH-03: Descriptive (Easy)
    {
        "id": "TECH-03",
        "pack_id": "pack-tech-01",
        "category": "Technical Knowledge",
        "difficulty": "Easy",
        "question_type": "descriptive",
        "question_text": "What is the difference between a compiler and an interpreter? Give one example of each.",
        "rubric": [
            {"id": "c1", "name": "Compiler Definition", "description": "Explains that a compiler converts the entire program into machine code at once before running.", "max_score": 3.5},
            {"id": "c2", "name": "Interpreter Definition", "description": "Explains that an interpreter runs the program line by line.", "max_score": 3.5},
            {"id": "c3", "name": "Examples", "description": "Gives correct examples like C/Java for compiler and Python for interpreter.", "max_score": 3.0}
        ],
        "reference_material": "A compiler translates the whole source code into machine code at one time, then the program runs. Example: C, C++. An interpreter translates and runs the code one line at a time. Example: Python, JavaScript. Compilers are faster at running but interpreters are easier for testing and debugging.",
        "keywords": ["compiler", "interpreter", "machine code", "line by line", "translate", "C", "Python"],
        "options": None, "correct_option": None, "explanation": None
    },

    # TECH-04: MCQ (Easy)
    {
        "id": "TECH-04",
        "pack_id": "pack-tech-01",
        "category": "Technical Knowledge",
        "difficulty": "Easy",
        "question_type": "mcq",
        "question_text": "What does HTML stand for?",
        "rubric": [
            {"id": "c1", "name": "Correct Answer", "description": "Selects the correct full form of HTML.", "max_score": 10.0}
        ],
        "reference_material": "HTML stands for HyperText Markup Language. It is the standard language used to create web pages. HTML uses tags like <h1>, <p>, <a> to structure content on a webpage.",
        "keywords": ["HTML", "HyperText", "Markup", "Language", "web"],
        "options": ["Hyper Transfer Markup Language", "HyperText Markup Language", "High Text Machine Language", "HyperText Managing Language"],
        "correct_option": "HyperText Markup Language",
        "explanation": "HTML stands for HyperText Markup Language. It is the basic building block of all websites."
    },

    # TECH-05: Descriptive (Easy)
    {
        "id": "TECH-05",
        "pack_id": "pack-tech-01",
        "category": "Technical Knowledge",
        "difficulty": "Easy",
        "question_type": "descriptive",
        "question_text": "What is an API? Explain in simple words why APIs are useful in software development.",
        "rubric": [
            {"id": "c1", "name": "Simple Definition", "description": "Defines API as a way for two software programs to talk to each other.", "max_score": 4.0},
            {"id": "c2", "name": "Why It Is Useful", "description": "Explains that APIs save time, allow reuse, and connect different services.", "max_score": 3.0},
            {"id": "c3", "name": "Real Example", "description": "Gives a simple example like weather app using a weather API.", "max_score": 3.0}
        ],
        "reference_material": "API stands for Application Programming Interface. It is a set of rules that allows one program to talk to another. For example, a weather app on your phone uses a weather API to get temperature data from a server. APIs save time because developers do not need to build everything from scratch.",
        "keywords": ["API", "Application Programming Interface", "connect", "software", "communication", "service", "request", "response"],
        "options": None, "correct_option": None, "explanation": None
    },

    # TECH-06: MCQ (Easy)
    {
        "id": "TECH-06",
        "pack_id": "pack-tech-01",
        "category": "Technical Knowledge",
        "difficulty": "Easy",
        "question_type": "mcq",
        "question_text": "Which data structure works on the principle of FIFO (First In, First Out)?",
        "rubric": [
            {"id": "c1", "name": "Correct Answer", "description": "Identifies Queue as the FIFO data structure.", "max_score": 10.0}
        ],
        "reference_material": "A Queue follows the FIFO principle, meaning the first item added is the first one removed, like a line at a ticket counter. A Stack follows LIFO (Last In, First Out). An Array is a simple list. A Tree is a hierarchical structure.",
        "keywords": ["Queue", "FIFO", "First In First Out", "data structure"],
        "options": ["Stack", "Queue", "Array", "Tree"],
        "correct_option": "Queue",
        "explanation": "A Queue follows FIFO. Think of a line at a shop: the person who comes first gets served first."
    },

    # TECH-07: Descriptive (Medium)
    {
        "id": "TECH-07",
        "pack_id": "pack-tech-01",
        "category": "Technical Knowledge",
        "difficulty": "Medium",
        "question_type": "descriptive",
        "question_text": "What is Object-Oriented Programming (OOP)? Name and briefly explain any three main concepts of OOP.",
        "rubric": [
            {"id": "c1", "name": "OOP Definition", "description": "Explains OOP as programming based on objects that contain data and methods.", "max_score": 3.0},
            {"id": "c2", "name": "Three Concepts", "description": "Names and explains at least three from: Encapsulation, Inheritance, Polymorphism, Abstraction.", "max_score": 4.0},
            {"id": "c3", "name": "Simple Example", "description": "Uses a real-world example like Car, Animal, or Student class.", "max_score": 3.0}
        ],
        "reference_material": "OOP is a way of writing programs using objects. An object has data (like name, age) and actions (like run, speak). Main concepts: 1. Encapsulation: hiding internal details and showing only what is needed. 2. Inheritance: a new class gets features from an existing class (like a Car class getting features from a Vehicle class). 3. Polymorphism: same action behaving differently (like 'speak' for a Dog says 'bark' but for a Cat says 'meow'). 4. Abstraction: showing only important details and hiding complexity.",
        "keywords": ["OOP", "object", "class", "encapsulation", "inheritance", "polymorphism", "abstraction", "method"],
        "options": None, "correct_option": None, "explanation": None
    },

    # TECH-08: MCQ (Easy)
    {
        "id": "TECH-08",
        "pack_id": "pack-tech-01",
        "category": "Technical Knowledge",
        "difficulty": "Easy",
        "question_type": "mcq",
        "question_text": "Which of the following is NOT a programming language?",
        "rubric": [
            {"id": "c1", "name": "Correct Answer", "description": "Identifies that HTML is a markup language, not a programming language.", "max_score": 10.0}
        ],
        "reference_material": "Python, Java, and C++ are programming languages that can perform calculations, make decisions, and run logic. HTML is a markup language used only to structure web page content. It cannot do calculations or run logic on its own.",
        "keywords": ["programming language", "HTML", "markup", "Python", "Java"],
        "options": ["Python", "Java", "HTML", "C++"],
        "correct_option": "HTML",
        "explanation": "HTML is a markup language, not a programming language. It is used to structure web pages but cannot run logic or calculations."
    },

    # TECH-09: Descriptive (Medium)
    {
        "id": "TECH-09",
        "pack_id": "pack-tech-01",
        "category": "Technical Knowledge",
        "difficulty": "Medium",
        "question_type": "descriptive",
        "question_text": "What is normalization in databases? Explain First Normal Form (1NF) and Second Normal Form (2NF) in simple words.",
        "rubric": [
            {"id": "c1", "name": "Normalization Purpose", "description": "Explains that normalization organizes data to reduce repetition and errors.", "max_score": 3.5},
            {"id": "c2", "name": "1NF Explanation", "description": "Each column has only one value per cell and each row is unique.", "max_score": 3.5},
            {"id": "c3", "name": "2NF Explanation", "description": "Table is in 1NF and every non-key column depends on the full primary key.", "max_score": 3.0}
        ],
        "reference_material": "Normalization means organizing a database to reduce repeated data and avoid errors. 1NF (First Normal Form): Each cell has only a single value (no lists), and every row is different. 2NF (Second Normal Form): The table is already in 1NF, and every column that is not part of the key depends on the whole key, not just part of it.",
        "keywords": ["normalization", "1NF", "2NF", "primary key", "redundancy", "single value", "organize"],
        "options": None, "correct_option": None, "explanation": None
    },

    # TECH-10: MCQ (Easy)
    {
        "id": "TECH-10",
        "pack_id": "pack-tech-01",
        "category": "Technical Knowledge",
        "difficulty": "Easy",
        "question_type": "mcq",
        "question_text": "What does CSS stand for in web development?",
        "rubric": [
            {"id": "c1", "name": "Correct Answer", "description": "Selects the correct full form of CSS.", "max_score": 10.0}
        ],
        "reference_material": "CSS stands for Cascading Style Sheets. It is used to control the look and design of a webpage, such as colors, fonts, spacing, and layout.",
        "keywords": ["CSS", "Cascading", "Style", "Sheets", "design"],
        "options": ["Computer Style Sheets", "Cascading Style Sheets", "Creative Style System", "Colorful Style Sheets"],
        "correct_option": "Cascading Style Sheets",
        "explanation": "CSS stands for Cascading Style Sheets. It is used alongside HTML to style and design web pages."
    },

    # TECH-11: Descriptive (Medium)
    {
        "id": "TECH-11",
        "pack_id": "pack-tech-01",
        "category": "Technical Knowledge",
        "difficulty": "Medium",
        "question_type": "descriptive",
        "question_text": "What is the difference between GET and POST methods in HTTP? When should you use each one?",
        "rubric": [
            {"id": "c1", "name": "GET Method", "description": "Explains that GET is used to request or read data and sends data in the URL.", "max_score": 3.5},
            {"id": "c2", "name": "POST Method", "description": "Explains that POST is used to send or submit data and sends data in the body.", "max_score": 3.5},
            {"id": "c3", "name": "When to Use", "description": "GET for loading pages or searching, POST for submitting forms or passwords.", "max_score": 3.0}
        ],
        "reference_material": "GET and POST are HTTP methods. GET asks the server for data and puts parameters in the URL (visible). Use GET for reading data, search, and loading pages. POST sends data to the server in the request body (hidden). Use POST for login forms, file uploads, and sending private data. POST is more secure for sensitive information.",
        "keywords": ["GET", "POST", "HTTP", "URL", "request", "body", "form", "submit", "secure"],
        "options": None, "correct_option": None, "explanation": None
    },

    # TECH-12: MCQ (Medium)
    {
        "id": "TECH-12",
        "pack_id": "pack-tech-01",
        "category": "Technical Knowledge",
        "difficulty": "Medium",
        "question_type": "mcq",
        "question_text": "In Python, what will be the output of: print(type(10.5))?",
        "rubric": [
            {"id": "c1", "name": "Correct Answer", "description": "Identifies that 10.5 is a float type in Python.", "max_score": 10.0}
        ],
        "reference_material": "In Python, numbers with decimal points like 10.5 are called 'float' (floating-point numbers). Whole numbers like 10 are 'int' (integers). Text like 'hello' is 'str' (string). True/False values are 'bool' (boolean).",
        "keywords": ["Python", "float", "type", "data type", "int", "str"],
        "options": ["<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'bool'>"],
        "correct_option": "<class 'float'>",
        "explanation": "10.5 has a decimal point, so Python treats it as a float (floating-point number)."
    },

    # TECH-13: Descriptive (Easy)
    {
        "id": "TECH-13",
        "pack_id": "pack-tech-01",
        "category": "Technical Knowledge",
        "difficulty": "Easy",
        "question_type": "descriptive",
        "question_text": "What is version control? Why do software developers use Git?",
        "rubric": [
            {"id": "c1", "name": "Version Control Definition", "description": "Explains that version control tracks changes to files over time.", "max_score": 4.0},
            {"id": "c2", "name": "Why Git Is Useful", "description": "Explains collaboration, tracking history, and undoing mistakes.", "max_score": 3.0},
            {"id": "c3", "name": "Basic Commands or Workflow", "description": "Mentions basic steps like clone, add, commit, push.", "max_score": 3.0}
        ],
        "reference_material": "Version control is a system that keeps track of every change made to files. Git is the most popular version control tool. It helps developers: 1) Work together on the same project without overwriting each other's work. 2) Go back to an older version if something breaks. 3) Keep a full history of all changes. Basic steps: git clone (download), git add (prepare changes), git commit (save changes), git push (upload to server).",
        "keywords": ["version control", "Git", "commit", "push", "clone", "history", "track", "collaborate"],
        "options": None, "correct_option": None, "explanation": None
    },

    # TECH-14: MCQ (Medium)
    {
        "id": "TECH-14",
        "pack_id": "pack-tech-01",
        "category": "Technical Knowledge",
        "difficulty": "Medium",
        "question_type": "mcq",
        "question_text": "Which SQL keyword is used to remove duplicate rows from query results?",
        "rubric": [
            {"id": "c1", "name": "Correct Answer", "description": "Identifies DISTINCT as the keyword to remove duplicates.", "max_score": 10.0}
        ],
        "reference_material": "DISTINCT is used in a SELECT statement to return only unique (non-duplicate) rows. Example: SELECT DISTINCT City FROM Students; gives each city name only once. WHERE filters rows. ORDER BY sorts rows. GROUP BY groups rows.",
        "keywords": ["DISTINCT", "SQL", "duplicate", "unique", "SELECT"],
        "options": ["WHERE", "DISTINCT", "ORDER BY", "GROUP BY"],
        "correct_option": "DISTINCT",
        "explanation": "DISTINCT removes duplicate values. For example, SELECT DISTINCT City FROM Students; shows each city only once."
    },

    # TECH-15: Descriptive (Medium)
    {
        "id": "TECH-15",
        "pack_id": "pack-tech-01",
        "category": "Technical Knowledge",
        "difficulty": "Medium",
        "question_type": "descriptive",
        "question_text": "What is cloud computing? Name three benefits of using cloud services for a business.",
        "rubric": [
            {"id": "c1", "name": "Cloud Definition", "description": "Explains cloud computing as using servers and services over the internet instead of your own computer.", "max_score": 4.0},
            {"id": "c2", "name": "Three Benefits", "description": "Lists benefits like saving cost, accessing from anywhere, easy scaling.", "max_score": 3.0},
            {"id": "c3", "name": "Examples of Cloud Services", "description": "Mentions services like AWS, Google Cloud, Microsoft Azure, or apps like Google Drive.", "max_score": 3.0}
        ],
        "reference_material": "Cloud computing means using computers and storage over the internet instead of your local machine. Benefits: 1) Cost saving: no need to buy expensive servers. 2) Access from anywhere: work from any location with internet. 3) Easy to grow: add more storage or power when needed. Popular services: AWS, Google Cloud, Microsoft Azure. Daily examples: Google Drive, Dropbox, Gmail.",
        "keywords": ["cloud computing", "internet", "server", "AWS", "Google Cloud", "scalable", "cost saving", "remote access"],
        "options": None, "correct_option": None, "explanation": None
    },

    # ---- WORKPLACE SCENARIOS (15 Questions) ----

    # WORK-01: Descriptive (Easy)
    {
        "id": "WORK-01",
        "pack_id": "pack-workplace-01",
        "category": "Workplace Scenarios",
        "difficulty": "Easy",
        "question_type": "descriptive",
        "question_text": "You find a bug in the application just before the deadline. What steps would you take to handle this situation?",
        "rubric": [
            {"id": "c1", "name": "Stay Calm and Report", "description": "First step is to stay calm and inform the team lead or manager right away.", "max_score": 4.0},
            {"id": "c2", "name": "Check How Serious It Is", "description": "Check if the bug is critical (app crashing) or minor (small UI issue).", "max_score": 3.0},
            {"id": "c3", "name": "Fix or Postpone", "description": "If it can be fixed quickly, fix it. If not, discuss with the team about a workaround or delay.", "max_score": 3.0}
        ],
        "reference_material": "When a bug is found near a deadline: 1) Stay calm and do not panic. 2) Tell your team lead or manager immediately. 3) Check how serious the bug is. 4) If it is a small fix, fix it and test it. 5) If it needs more time, discuss with the team whether to release with a known issue or delay the release.",
        "keywords": ["bug", "deadline", "inform", "team lead", "fix", "test", "communicate", "priority"],
        "options": None, "correct_option": None, "explanation": None
    },

    # WORK-02: MCQ (Easy)
    {
        "id": "WORK-02",
        "pack_id": "pack-workplace-01",
        "category": "Workplace Scenarios",
        "difficulty": "Easy",
        "question_type": "mcq",
        "question_text": "A team member is not completing their tasks on time, causing delays for everyone. What is the best first step?",
        "rubric": [
            {"id": "c1", "name": "Best Approach", "description": "Chooses a supportive, professional approach first.", "max_score": 10.0}
        ],
        "reference_material": "The best approach is to talk to the team member privately and politely to understand if they are facing any problems. They might be stuck on something, have personal issues, or need help understanding the task. Complaining to the boss first or ignoring the issue usually makes things worse.",
        "keywords": ["team", "communication", "support", "private conversation", "deadline"],
        "options": [
            "Talk to them privately and ask if they need help",
            "Complain about them to your manager immediately",
            "Ignore it and do their work yourself",
            "Send an angry email to the whole team"
        ],
        "correct_option": "Talk to them privately and ask if they need help",
        "explanation": "Always start with a friendly private conversation. They might need help, have too much work, or have a personal problem."
    },

    # WORK-03: Descriptive (Easy)
    {
        "id": "WORK-03",
        "pack_id": "pack-workplace-01",
        "category": "Workplace Scenarios",
        "difficulty": "Easy",
        "question_type": "descriptive",
        "question_text": "Your client asks for a new feature that was not part of the original plan, and the deadline is next week. How would you handle this?",
        "rubric": [
            {"id": "c1", "name": "Understand the Request", "description": "First listens to and clearly understands what the client wants.", "max_score": 3.5},
            {"id": "c2", "name": "Check Impact on Deadline", "description": "Checks how much time and work the new feature needs.", "max_score": 3.5},
            {"id": "c3", "name": "Discuss Options", "description": "Talks to client about extending the deadline or delivering the new feature later.", "max_score": 3.0}
        ],
        "reference_material": "When a client asks for extra work: 1) Listen carefully and understand what they need. 2) Check how much extra time and effort it will take. 3) Tell your manager about the request. 4) Discuss with the client: either extend the deadline, remove a less important feature to make room, or deliver the new feature in the next update.",
        "keywords": ["client", "new feature", "deadline", "scope", "negotiate", "discuss", "communicate"],
        "options": None, "correct_option": None, "explanation": None
    },

    # WORK-04: MCQ (Easy)
    {
        "id": "WORK-04",
        "pack_id": "pack-workplace-01",
        "category": "Workplace Scenarios",
        "difficulty": "Easy",
        "question_type": "mcq",
        "question_text": "You accidentally deleted an important file from the project. What should you do first?",
        "rubric": [
            {"id": "c1", "name": "Best Immediate Action", "description": "Chooses to check version control / backup first.", "max_score": 10.0}
        ],
        "reference_material": "If you accidentally delete a file: 1) Check if it is in the recycle bin or trash. 2) Check Git or version control for the latest saved version. 3) Ask your team if anyone has a copy. 4) Tell your manager honestly. Never try to hide mistakes.",
        "keywords": ["deleted file", "version control", "Git", "backup", "recover", "honest"],
        "options": [
            "Check version control (Git) or backup to recover the file",
            "Pretend nothing happened and hope nobody notices",
            "Blame another team member for the mistake",
            "Restart the entire project from scratch"
        ],
        "correct_option": "Check version control (Git) or backup to recover the file",
        "explanation": "Always check version control (Git) or backups first. The file can usually be recovered easily from there."
    },

    # WORK-05: Descriptive (Medium)
    {
        "id": "WORK-05",
        "pack_id": "pack-workplace-01",
        "category": "Workplace Scenarios",
        "difficulty": "Medium",
        "question_type": "descriptive",
        "question_text": "Two people in your team disagree about which technology to use for a project. How would you help resolve this?",
        "rubric": [
            {"id": "c1", "name": "Listen to Both Sides", "description": "Gives both people a fair chance to explain their reasons.", "max_score": 4.0},
            {"id": "c2", "name": "Compare Based on Facts", "description": "Suggests comparing options based on project needs, not personal preference.", "max_score": 3.0},
            {"id": "c3", "name": "Reach Agreement", "description": "Helps the team agree on a solution, possibly by involving the manager.", "max_score": 3.0}
        ],
        "reference_material": "When teammates disagree: 1) Let each person explain their choice calmly. 2) List the pros and cons of each option based on project needs (speed, cost, team skills). 3) Focus on what is best for the project, not who is right. 4) If they still cannot agree, involve the team lead for a final decision.",
        "keywords": ["disagreement", "listen", "pros and cons", "project needs", "resolve", "team lead", "consensus"],
        "options": None, "correct_option": None, "explanation": None
    },

    # WORK-06: MCQ (Easy)
    {
        "id": "WORK-06",
        "pack_id": "pack-workplace-01",
        "category": "Workplace Scenarios",
        "difficulty": "Easy",
        "question_type": "mcq",
        "question_text": "You finished your task early but your teammate is struggling with their work. What is the most professional thing to do?",
        "rubric": [
            {"id": "c1", "name": "Best Approach", "description": "Chooses to help the teammate.", "max_score": 10.0}
        ],
        "reference_material": "A good team member helps others when they can. If you finish early, offer to help your teammate. This builds trust, speeds up the project, and shows professionalism. Sitting idle or leaving early without checking is not good teamwork.",
        "keywords": ["teamwork", "help", "professional", "collaboration", "support"],
        "options": [
            "Offer to help your teammate with their task",
            "Leave early since your work is done",
            "Sit idle and browse the internet",
            "Tell the manager your teammate is slow"
        ],
        "correct_option": "Offer to help your teammate with their task",
        "explanation": "Good teamwork means helping each other. Offering help builds trust and keeps the project on track."
    },

    # WORK-07: Descriptive (Easy)
    {
        "id": "WORK-07",
        "pack_id": "pack-workplace-01",
        "category": "Workplace Scenarios",
        "difficulty": "Easy",
        "question_type": "descriptive",
        "question_text": "Your manager gives you a task but the instructions are not clear. What would you do?",
        "rubric": [
            {"id": "c1", "name": "Ask for Clarification", "description": "Goes back to the manager and asks specific questions politely.", "max_score": 4.0},
            {"id": "c2", "name": "Confirm Understanding", "description": "Repeats the task back in their own words to make sure they understood correctly.", "max_score": 3.0},
            {"id": "c3", "name": "Document Requirements", "description": "Writes down the requirements so there is no confusion later.", "max_score": 3.0}
        ],
        "reference_material": "If instructions are unclear: 1) Do not guess and start working blindly. 2) Go to your manager and politely ask specific questions about the task. 3) Repeat back what you understood to confirm. 4) Write down the key points. 5) If needed, ask for a small example or reference. This saves time and avoids doing the wrong work.",
        "keywords": ["clarification", "ask questions", "confirm", "write down", "understand", "requirements"],
        "options": None, "correct_option": None, "explanation": None
    },

    # WORK-08: MCQ (Medium)
    {
        "id": "WORK-08",
        "pack_id": "pack-workplace-01",
        "category": "Workplace Scenarios",
        "difficulty": "Medium",
        "question_type": "mcq",
        "question_text": "During a team meeting, your idea is rejected by the senior developer. What is the most mature response?",
        "rubric": [
            {"id": "c1", "name": "Professional Response", "description": "Accepts feedback gracefully and asks for the reason.", "max_score": 10.0}
        ],
        "reference_material": "When your idea is rejected: 1) Do not take it personally. 2) Listen to why it was rejected. 3) Ask politely what could be improved. 4) Learn from the feedback. Being defensive or arguing in front of everyone shows poor professionalism.",
        "keywords": ["feedback", "rejection", "professional", "listen", "learn", "mature"],
        "options": [
            "Accept it calmly and ask what approach they suggest instead",
            "Argue loudly in front of everyone",
            "Stop contributing ideas in future meetings",
            "Complain about it to other teammates after the meeting"
        ],
        "correct_option": "Accept it calmly and ask what approach they suggest instead",
        "explanation": "Accepting feedback gracefully and learning from it shows maturity and professionalism."
    },

    # WORK-09: Descriptive (Medium)
    {
        "id": "WORK-09",
        "pack_id": "pack-workplace-01",
        "category": "Workplace Scenarios",
        "difficulty": "Medium",
        "question_type": "descriptive",
        "question_text": "You are assigned multiple tasks with the same deadline, and you cannot finish all of them. How do you prioritize your work?",
        "rubric": [
            {"id": "c1", "name": "Assess Urgency and Importance", "description": "Sorts tasks by what is most urgent and most important to the project.", "max_score": 4.0},
            {"id": "c2", "name": "Communicate Early", "description": "Tells the manager early that all tasks cannot be done on time.", "max_score": 3.0},
            {"id": "c3", "name": "Work on High-Priority First", "description": "Starts with the most critical tasks and asks which ones can wait.", "max_score": 3.0}
        ],
        "reference_material": "When you have too many tasks: 1) Make a list of all tasks. 2) Sort them by urgency (how soon they are needed) and importance (how critical they are). 3) Talk to your manager and explain the situation honestly. 4) Ask which task should be done first. 5) Focus on the most important one and finish it before moving to the next.",
        "keywords": ["prioritize", "urgency", "importance", "communicate", "manager", "focus", "workload"],
        "options": None, "correct_option": None, "explanation": None
    },

    # WORK-10: MCQ (Medium)
    {
        "id": "WORK-10",
        "pack_id": "pack-workplace-01",
        "category": "Workplace Scenarios",
        "difficulty": "Medium",
        "question_type": "mcq",
        "question_text": "You notice a security issue in the codebase that could expose user data. What should you do?",
        "rubric": [
            {"id": "c1", "name": "Correct Action", "description": "Reports the security issue immediately to the team lead.", "max_score": 10.0}
        ],
        "reference_material": "Security issues are very serious. You should: 1) Report it to your team lead or security team right away. 2) Do not share the issue publicly. 3) Help fix it quickly. Never ignore security bugs because they can harm users and the company.",
        "keywords": ["security", "report", "user data", "team lead", "responsible", "fix"],
        "options": [
            "Report it immediately to the team lead or security team",
            "Ignore it because it is not your responsibility",
            "Post about it on social media to warn people",
            "Wait until the next sprint to mention it"
        ],
        "correct_option": "Report it immediately to the team lead or security team",
        "explanation": "Security issues must be reported immediately and privately to the team lead or security team to protect users."
    },

    # WORK-11 to WORK-15: More Workplace Scenarios
    {
        "id": "WORK-11",
        "pack_id": "pack-workplace-01",
        "category": "Workplace Scenarios",
        "difficulty": "Easy",
        "question_type": "descriptive",
        "question_text": "A new team member has joined your project. How would you help them get started and feel welcome?",
        "rubric": [
            {"id": "c1", "name": "Welcoming Attitude", "description": "Shows a friendly and supportive attitude toward the new person.", "max_score": 3.5},
            {"id": "c2", "name": "Practical Help", "description": "Helps with setup, shares project documents, and explains the workflow.", "max_score": 3.5},
            {"id": "c3", "name": "Regular Check-ins", "description": "Checks on them regularly to see if they have questions.", "max_score": 3.0}
        ],
        "reference_material": "To help a new team member: 1) Introduce yourself and be friendly. 2) Share project documents, codebase access, and tools setup guide. 3) Explain the team workflow and who does what. 4) Sit with them for the first few tasks. 5) Check on them daily and encourage them to ask questions.",
        "keywords": ["onboarding", "welcome", "introduce", "help", "documents", "questions", "support"],
        "options": None, "correct_option": None, "explanation": None
    },
    {
        "id": "WORK-12",
        "pack_id": "pack-workplace-01",
        "category": "Workplace Scenarios",
        "difficulty": "Medium",
        "question_type": "mcq",
        "question_text": "Your team is working overtime for 3 weeks and everyone looks tired. What should you suggest?",
        "rubric": [
            {"id": "c1", "name": "Best Approach", "description": "Suggests talking to the manager about workload and rest.", "max_score": 10.0}
        ],
        "reference_material": "Working too much without breaks leads to mistakes and burnout. The right step is to talk to the manager about reducing the workload or adjusting the deadline. Tired people make more errors and produce lower quality work.",
        "keywords": ["overtime", "burnout", "workload", "rest", "manager", "quality"],
        "options": [
            "Talk to the manager about reducing workload or adjusting deadlines",
            "Keep working without complaining",
            "Start coming late to get some rest",
            "Quit the job immediately"
        ],
        "correct_option": "Talk to the manager about reducing workload or adjusting deadlines",
        "explanation": "Continuous overtime leads to burnout and mistakes. It is professional to discuss workload concerns with the manager."
    },
    {
        "id": "WORK-13",
        "pack_id": "pack-workplace-01",
        "category": "Workplace Scenarios",
        "difficulty": "Easy",
        "question_type": "descriptive",
        "question_text": "You made a mistake in your code that caused a problem in the live website. How should you handle this?",
        "rubric": [
            {"id": "c1", "name": "Own the Mistake", "description": "Admits the mistake honestly without blaming others.", "max_score": 4.0},
            {"id": "c2", "name": "Fix It Quickly", "description": "Works to fix the issue as fast as possible.", "max_score": 3.0},
            {"id": "c3", "name": "Learn and Prevent", "description": "Adds testing or checks to prevent the same mistake from happening again.", "max_score": 3.0}
        ],
        "reference_material": "When you make a mistake: 1) Admit it honestly and tell the team immediately. 2) Focus on fixing the problem first. 3) After fixing, think about why it happened. 4) Add tests or review steps to prevent it from happening again. Everyone makes mistakes; what matters is how you respond.",
        "keywords": ["mistake", "honest", "fix", "test", "prevent", "learn", "accountability"],
        "options": None, "correct_option": None, "explanation": None
    },
    {
        "id": "WORK-14",
        "pack_id": "pack-workplace-01",
        "category": "Workplace Scenarios",
        "difficulty": "Medium",
        "question_type": "mcq",
        "question_text": "A client sends an angry email about a delayed feature. What is the best way to respond?",
        "rubric": [
            {"id": "c1", "name": "Professional Response", "description": "Chooses a calm, empathetic, and solution-focused reply.", "max_score": 10.0}
        ],
        "reference_material": "When handling an angry client: 1) Stay calm and professional. 2) Thank them for their patience. 3) Explain the reason for the delay briefly. 4) Give a clear new timeline. 5) Never argue or blame the client.",
        "keywords": ["client", "angry", "calm", "professional", "timeline", "empathy"],
        "options": [
            "Reply calmly, apologize for the delay, and share a clear updated timeline",
            "Ignore the email and hope they forget about it",
            "Reply with an equally angry email defending your team",
            "Forward the email to your manager without responding"
        ],
        "correct_option": "Reply calmly, apologize for the delay, and share a clear updated timeline",
        "explanation": "A professional reply with empathy, a brief explanation, and a clear timeline builds trust even in difficult situations."
    },
    {
        "id": "WORK-15",
        "pack_id": "pack-workplace-01",
        "category": "Workplace Scenarios",
        "difficulty": "Easy",
        "question_type": "descriptive",
        "question_text": "You are working from home and your internet connection is very slow. You have an important online meeting in 30 minutes. What do you do?",
        "rubric": [
            {"id": "c1", "name": "Quick Solutions", "description": "Tries immediate fixes like restarting router, mobile hotspot, or moving closer to router.", "max_score": 4.0},
            {"id": "c2", "name": "Inform the Team", "description": "Sends a message to the team about the situation before the meeting.", "max_score": 3.0},
            {"id": "c3", "name": "Backup Plan", "description": "Has a backup like joining by phone, or asking a colleague to share notes.", "max_score": 3.0}
        ],
        "reference_material": "When internet is slow before a meeting: 1) Restart your router. 2) Try using your mobile phone as a hotspot. 3) Close other apps using bandwidth. 4) Message the team that you might have connection issues. 5) Have a backup: join by phone call, turn off video, or ask someone to share the meeting summary.",
        "keywords": ["internet", "slow", "meeting", "hotspot", "backup", "inform", "plan"],
        "options": None, "correct_option": None, "explanation": None
    },

    # ---- HR / BEHAVIOURAL (15 Questions) ----

    {
        "id": "HR-01",
        "pack_id": "pack-hr-01",
        "category": "HR / Behavioural",
        "difficulty": "Easy",
        "question_type": "descriptive",
        "question_text": "Tell me about yourself. Share your background, your interests, and why you are interested in this job.",
        "rubric": [
            {"id": "c1", "name": "Clear Introduction", "description": "Gives a short, organized introduction covering education and skills.", "max_score": 3.5},
            {"id": "c2", "name": "Relevant Experience", "description": "Mentions projects or skills that match the job.", "max_score": 3.5},
            {"id": "c3", "name": "Enthusiasm", "description": "Shows genuine interest and motivation for the role.", "max_score": 3.0}
        ],
        "reference_material": "A good answer follows Present-Past-Future: 1) Present: I am currently studying MCA at [University] with a focus on [skill]. 2) Past: I have worked on projects like [project name] using [technology]. 3) Future: I want to join your company because [specific reason]. Keep it short, clear, and do not repeat your resume word by word.",
        "keywords": ["introduction", "education", "skills", "projects", "motivation", "interest"],
        "options": None, "correct_option": None, "explanation": None
    },
    {
        "id": "HR-02",
        "pack_id": "pack-hr-01",
        "category": "HR / Behavioural",
        "difficulty": "Easy",
        "question_type": "mcq",
        "question_text": "An interviewer asks about your biggest weakness. What is the best way to answer?",
        "rubric": [
            {"id": "c1", "name": "Best Approach", "description": "Mentions a real weakness and explains how they are working to improve it.", "max_score": 10.0}
        ],
        "reference_material": "The best answer is honest but shows self-awareness and growth. Pick a real weakness (like time management or public speaking) and explain what you are doing to improve it. Saying 'I have no weakness' sounds fake. Saying something too negative without improvement is also bad.",
        "keywords": ["weakness", "honest", "improve", "self-aware", "growth"],
        "options": [
            "Mention a real weakness and explain what you are doing to improve it",
            "Say you have no weakness at all",
            "Make up a fake weakness like 'I work too hard'",
            "List many weaknesses without any plan to improve"
        ],
        "correct_option": "Mention a real weakness and explain what you are doing to improve it",
        "explanation": "Being honest about a weakness and showing that you are working on it demonstrates maturity and self-awareness."
    },
    {
        "id": "HR-03",
        "pack_id": "pack-hr-01",
        "category": "HR / Behavioural",
        "difficulty": "Easy",
        "question_type": "descriptive",
        "question_text": "Tell me about a time when you worked in a team to complete a project. What was your role and what did you learn?",
        "rubric": [
            {"id": "c1", "name": "Situation and Task", "description": "Clearly describes the project and what the team had to do.", "max_score": 3.5},
            {"id": "c2", "name": "Your Contribution", "description": "Explains their specific role and actions in the team.", "max_score": 3.5},
            {"id": "c3", "name": "Learning Outcome", "description": "Shares what they learned from the experience.", "max_score": 3.0}
        ],
        "reference_material": "Use a simple structure: 1) Situation: We had a college project to build a [type of app]. 2) Task: My job was to [specific role like frontend, database, testing]. 3) Action: I created the [specific part] and helped my teammate with [something]. 4) Result: We finished on time and learned how to work together and divide tasks.",
        "keywords": ["teamwork", "project", "role", "contribution", "learning", "collaboration"],
        "options": None, "correct_option": None, "explanation": None
    },
    {
        "id": "HR-04",
        "pack_id": "pack-hr-01",
        "category": "HR / Behavioural",
        "difficulty": "Easy",
        "question_type": "mcq",
        "question_text": "You are given a task you have never done before and you do not know where to start. What should you do first?",
        "rubric": [
            {"id": "c1", "name": "Best First Step", "description": "Chooses to research and understand the task before asking for help.", "max_score": 10.0}
        ],
        "reference_material": "When facing an unfamiliar task: 1) Spend some time reading about it online or in documentation. 2) Try to understand the basic idea. 3) If you are still stuck after trying, ask a teammate or manager for guidance. Do not wait too long to ask, but also do not ask without trying first.",
        "keywords": ["new task", "research", "learn", "ask", "guidance", "try first"],
        "options": [
            "Research and try to understand it first, then ask for help if needed",
            "Immediately tell your manager you cannot do it",
            "Copy paste code from the internet without understanding it",
            "Wait for someone else to do it for you"
        ],
        "correct_option": "Research and try to understand it first, then ask for help if needed",
        "explanation": "A good approach is to try understanding it first (reading docs, watching tutorials), then ask for help with specific questions."
    },
    {
        "id": "HR-05",
        "pack_id": "pack-hr-01",
        "category": "HR / Behavioural",
        "difficulty": "Easy",
        "question_type": "descriptive",
        "question_text": "Tell me about a mistake you made in a project or assignment. What happened and what did you learn from it?",
        "rubric": [
            {"id": "c1", "name": "Honest Admission", "description": "Admits a real mistake without blaming others.", "max_score": 4.0},
            {"id": "c2", "name": "What They Did About It", "description": "Explains how they fixed or handled the situation.", "max_score": 3.0},
            {"id": "c3", "name": "Lesson Learned", "description": "Shares the lesson and what they do differently now.", "max_score": 3.0}
        ],
        "reference_material": "A good answer: 1) Pick a genuine mistake (like forgetting to back up data, not testing code, missing a deadline). 2) Own it honestly and do not blame others. 3) Explain how you fixed it. 4) Share what you learned and what you do differently now. Example: I forgot to save my work and lost a day's progress. Now I use Git to save my work regularly.",
        "keywords": ["mistake", "honest", "fix", "lesson", "improvement", "responsibility"],
        "options": None, "correct_option": None, "explanation": None
    },
    {
        "id": "HR-06",
        "pack_id": "pack-hr-01",
        "category": "HR / Behavioural",
        "difficulty": "Easy",
        "question_type": "mcq",
        "question_text": "During a group project, two team members are having a personal argument that is affecting the work. What would you do?",
        "rubric": [
            {"id": "c1", "name": "Best Response", "description": "Tries to calm the situation and focus on the work.", "max_score": 10.0}
        ],
        "reference_material": "In a team conflict: 1) Stay neutral and do not take sides. 2) Suggest focusing on the project goals. 3) If it continues, suggest they talk it out privately or involve the team leader. Do not spread gossip or add fuel to the argument.",
        "keywords": ["conflict", "neutral", "focus", "project goals", "team leader"],
        "options": [
            "Stay neutral and suggest focusing on the project goals first",
            "Take one person's side to end the argument quickly",
            "Tell everyone else about the drama",
            "Stop working on the project entirely"
        ],
        "correct_option": "Stay neutral and suggest focusing on the project goals first",
        "explanation": "Staying neutral and redirecting focus to the project shows maturity and keeps the work moving forward."
    },
    {
        "id": "HR-07",
        "pack_id": "pack-hr-01",
        "category": "HR / Behavioural",
        "difficulty": "Medium",
        "question_type": "descriptive",
        "question_text": "How do you handle pressure and stress when you have too much work and a tight deadline?",
        "rubric": [
            {"id": "c1", "name": "Practical Strategies", "description": "Mentions real strategies like making a list, breaking tasks down, or taking short breaks.", "max_score": 4.0},
            {"id": "c2", "name": "Staying Focused", "description": "Shows ability to focus on one task at a time instead of panicking.", "max_score": 3.0},
            {"id": "c3", "name": "Asking for Help", "description": "Is willing to ask for help or talk to the manager when needed.", "max_score": 3.0}
        ],
        "reference_material": "Handling stress: 1) Make a to-do list and sort tasks by urgency. 2) Break big tasks into small steps. 3) Focus on one thing at a time. 4) Take short breaks to clear your mind. 5) If it is too much, talk to your manager and ask for help or an extension. Panicking and multitasking usually make things worse.",
        "keywords": ["stress", "pressure", "prioritize", "to-do list", "breaks", "focus", "ask for help"],
        "options": None, "correct_option": None, "explanation": None
    },
    {
        "id": "HR-08",
        "pack_id": "pack-hr-01",
        "category": "HR / Behavioural",
        "difficulty": "Easy",
        "question_type": "mcq",
        "question_text": "Why do you want to work at our company? Which answer shows the best preparation?",
        "rubric": [
            {"id": "c1", "name": "Best Response", "description": "Shows research about the company and genuine interest.", "max_score": 10.0}
        ],
        "reference_material": "A strong answer shows you researched the company. Mention their products, technology, culture, or recent achievements. Explain how your skills can help them and how the role matches your career goals.",
        "keywords": ["company research", "interest", "goals", "skills match", "specific reasons"],
        "options": [
            "I researched your company and I like your products. My skills in [X] can add value to your team.",
            "I just need a job and your company was the first to call me back.",
            "I heard the salary is good here.",
            "My friend works here and he said it is easy."
        ],
        "correct_option": "I researched your company and I like your products. My skills in [X] can add value to your team.",
        "explanation": "Showing that you researched the company and connecting your skills to their work shows genuine interest and preparation."
    },
    {
        "id": "HR-09",
        "pack_id": "pack-hr-01",
        "category": "HR / Behavioural",
        "difficulty": "Medium",
        "question_type": "descriptive",
        "question_text": "Describe a time when you had to learn something new very quickly. How did you approach it?",
        "rubric": [
            {"id": "c1", "name": "Learning Method", "description": "Explains their approach like reading docs, watching tutorials, or practicing.", "max_score": 4.0},
            {"id": "c2", "name": "Time Management", "description": "Shows they managed their time and focused on the most important parts first.", "max_score": 3.0},
            {"id": "c3", "name": "Successful Result", "description": "Successfully learned and used the new skill to finish the task.", "max_score": 3.0}
        ],
        "reference_material": "Good answer: 1) Describe the situation (e.g. needed to learn React for a project in one week). 2) Explain your method: watched YouTube tutorials, read official docs, built a small practice app. 3) Focus on learning the most important 20% first. 4) Result: finished the project on time and now feel comfortable with the technology.",
        "keywords": ["learning", "quick", "tutorials", "practice", "focus", "result", "adapt"],
        "options": None, "correct_option": None, "explanation": None
    },
    {
        "id": "HR-10",
        "pack_id": "pack-hr-01",
        "category": "HR / Behavioural",
        "difficulty": "Easy",
        "question_type": "mcq",
        "question_text": "You disagree with your team leader's decision about a project approach. What is the best way to handle it?",
        "rubric": [
            {"id": "c1", "name": "Professional Response", "description": "Chooses to share their view respectfully and support the final decision.", "max_score": 10.0}
        ],
        "reference_material": "If you disagree with your leader: 1) Share your view politely in private, not in front of everyone. 2) Explain your reasons with facts. 3) Listen to their reasoning. 4) If they still decide differently, support their decision and work with the team.",
        "keywords": ["disagree", "respectful", "private", "facts", "support", "team"],
        "options": [
            "Share your view respectfully in private and support the final decision",
            "Argue with the team leader in front of everyone",
            "Say nothing and silently do the work your own way",
            "Complain about the decision to other team members"
        ],
        "correct_option": "Share your view respectfully in private and support the final decision",
        "explanation": "Sharing your opinion respectfully and then supporting the team's final decision shows maturity and professionalism."
    },
    {
        "id": "HR-11",
        "pack_id": "pack-hr-01",
        "category": "HR / Behavioural",
        "difficulty": "Easy",
        "question_type": "descriptive",
        "question_text": "What are your strengths that make you a good fit for a software development role?",
        "rubric": [
            {"id": "c1", "name": "Relevant Strengths", "description": "Lists strengths that matter for the job like problem-solving, learning fast, or coding skills.", "max_score": 4.0},
            {"id": "c2", "name": "Examples", "description": "Gives at least one real example of when they used this strength.", "max_score": 3.0},
            {"id": "c3", "name": "Confidence Without Arrogance", "description": "Speaks confidently but remains humble.", "max_score": 3.0}
        ],
        "reference_material": "Good strengths for a developer: problem-solving, willingness to learn, attention to detail, teamwork, and coding skills. Give a short example: 'I am good at problem-solving. In my last project, I fixed a difficult bug by reading logs carefully and tracing the error step by step.' Be confident but not boastful.",
        "keywords": ["strengths", "problem-solving", "learning", "coding", "example", "confidence"],
        "options": None, "correct_option": None, "explanation": None
    },
    {
        "id": "HR-12",
        "pack_id": "pack-hr-01",
        "category": "HR / Behavioural",
        "difficulty": "Easy",
        "question_type": "mcq",
        "question_text": "You receive tough feedback on your code during a code review. What is the best reaction?",
        "rubric": [
            {"id": "c1", "name": "Mature Response", "description": "Takes feedback positively and uses it to improve.", "max_score": 10.0}
        ],
        "reference_material": "Code reviews are normal and help everyone write better code. When you get tough feedback: 1) Do not take it personally. 2) Read the comments carefully and understand them. 3) Ask questions if something is unclear. 4) Fix the issues and learn from them.",
        "keywords": ["feedback", "code review", "positive", "learn", "improve", "not personal"],
        "options": [
            "Thank the reviewer, learn from the feedback, and fix the issues",
            "Get upset and refuse to change your code",
            "Delete all comments without reading them",
            "Stop sharing your code with anyone in the future"
        ],
        "correct_option": "Thank the reviewer, learn from the feedback, and fix the issues",
        "explanation": "Taking feedback positively and using it to improve your skills shows a growth mindset and professionalism."
    },
    {
        "id": "HR-13",
        "pack_id": "pack-hr-01",
        "category": "HR / Behavioural",
        "difficulty": "Medium",
        "question_type": "descriptive",
        "question_text": "Where do you see yourself in 3 to 5 years? What are your career goals?",
        "rubric": [
            {"id": "c1", "name": "Realistic Goals", "description": "Sets achievable career goals like becoming a senior developer or learning new technologies.", "max_score": 3.5},
            {"id": "c2", "name": "Skill Growth Plan", "description": "Mentions specific skills or areas they want to develop.", "max_score": 3.5},
            {"id": "c3", "name": "Company Alignment", "description": "Shows how their goals align with growing in the company.", "max_score": 3.0}
        ],
        "reference_material": "A good answer: In 3-5 years, I want to grow into a mid-level or senior software developer. I plan to learn cloud computing, improve my system design skills, and eventually mentor junior team members. I want to grow with a company where I can contribute meaningfully and take on bigger responsibilities.",
        "keywords": ["career goals", "growth", "skills", "senior developer", "learning", "company"],
        "options": None, "correct_option": None, "explanation": None
    },
    {
        "id": "HR-14",
        "pack_id": "pack-hr-01",
        "category": "HR / Behavioural",
        "difficulty": "Medium",
        "question_type": "mcq",
        "question_text": "You notice a teammate is feeling sad and not talking to anyone at work. What should you do?",
        "rubric": [
            {"id": "c1", "name": "Empathetic Response", "description": "Checks on the teammate privately and with kindness.", "max_score": 10.0}
        ],
        "reference_material": "If you notice a teammate is not doing well: 1) Check on them privately with genuine concern. 2) Ask if they are okay and if you can help. 3) Listen without judging. 4) Do not force them to talk if they do not want to. 5) If it seems serious, suggest they talk to HR or a trusted person.",
        "keywords": ["empathy", "check on", "listen", "support", "kindness", "private"],
        "options": [
            "Check on them privately and ask if they are okay or need any help",
            "Ignore it since it is their personal matter",
            "Talk about it with other colleagues",
            "Tell the manager that they are not working properly"
        ],
        "correct_option": "Check on them privately and ask if they are okay or need any help",
        "explanation": "Showing empathy by checking on them privately and listening with kindness shows you care about your team."
    },
    {
        "id": "HR-15",
        "pack_id": "pack-hr-01",
        "category": "HR / Behavioural",
        "difficulty": "Easy",
        "question_type": "descriptive",
        "question_text": "Why should we hire you? What makes you different from other candidates?",
        "rubric": [
            {"id": "c1", "name": "Unique Value", "description": "Highlights what makes them unique: specific skills, project experience, or attitude.", "max_score": 4.0},
            {"id": "c2", "name": "Connection to Role", "description": "Connects their skills and experience to the specific job requirements.", "max_score": 3.0},
            {"id": "c3", "name": "Eagerness to Contribute", "description": "Shows willingness to learn, grow, and contribute from day one.", "max_score": 3.0}
        ],
        "reference_material": "Good answer: You should hire me because I have hands-on experience with [technology], I learn quickly, and I am eager to contribute from day one. In my MCA project, I built a complete web application using Python and Flask, which shows I can deliver real products. I also enjoy working in teams and I am always looking for ways to improve.",
        "keywords": ["unique", "skills", "experience", "contribute", "learn", "eager", "value"],
        "options": None, "correct_option": None, "explanation": None
    },
]


def generate_sample_answers():
    """Generate 180 varied sample answers (4 per question x 45 questions)."""
    samples = []
    for q_idx, q in enumerate(PILOT_QUESTIONS):
        qid = q["id"]
        cat = q["category"]
        kws = q["keywords"]
        ref = q["reference_material"]
        q_type = q["question_type"]

        # For MCQ questions, generate answer variants differently
        if q_type == "mcq":
            options = q["options"]
            correct = q["correct_option"]
            wrong_opts = [o for o in options if o != correct]

            # Excellent: correct answer with explanation
            samples.append({
                "sample_id": f"SAMPLE-{(q_idx*4)+1:03d}", "question_id": qid, "category": cat,
                "performance_level": "Excellent", "source_type": "Synthetic - Correct + Explained",
                "answer_text": f"The correct answer is: {correct}. {q.get('explanation', '')}",
                "notes": "Correct MCQ answer with clear reasoning."
            })
            # Proficient: correct answer, short
            samples.append({
                "sample_id": f"SAMPLE-{(q_idx*4)+2:03d}", "question_id": qid, "category": cat,
                "performance_level": "Proficient", "source_type": "Student Pilot Submission",
                "answer_text": f"I think the answer is: {correct}.",
                "notes": "Correct answer but without detailed explanation."
            })
            # Developing: wrong answer
            samples.append({
                "sample_id": f"SAMPLE-{(q_idx*4)+3:03d}", "question_id": qid, "category": cat,
                "performance_level": "Developing", "source_type": "Synthetic - Wrong Choice",
                "answer_text": f"I would say: {wrong_opts[0]}.",
                "notes": "Incorrect MCQ choice. Shows partial or confused understanding."
            })
            # Inadequate: random wrong + no explanation
            samples.append({
                "sample_id": f"SAMPLE-{(q_idx*4)+4:03d}", "question_id": qid, "category": cat,
                "performance_level": "Inadequate", "source_type": "Synthetic - Off Topic",
                "answer_text": f"Maybe {wrong_opts[1] if len(wrong_opts)>1 else wrong_opts[0]}. I am not sure about this topic.",
                "notes": "Incorrect answer with no reasoning. Shows lack of knowledge."
            })
        else:
            # Descriptive questions: 4 levels
            # Excellent
            if cat == "Technical Knowledge":
                ans_exc = (f"In simple terms, {q['question_text'].split('?')[0].lower()} is about {kws[0]} and {kws[1]}. "
                           f"{ref[:160]}... The key things to remember are {kws[2] if len(kws)>2 else kws[0]} and "
                           f"{kws[3] if len(kws)>3 else kws[1]}. In real projects, this helps us build better and faster software.")
            elif cat == "Workplace Scenarios":
                ans_exc = (f"In this situation, my first step would be to {kws[0]} and {kws[1]}. "
                           f"I would talk to my team and explain the situation clearly. "
                           f"Then I would work on a solution together. After that, I would make sure we have steps to prevent this from happening again.")
            else:
                ans_exc = (f"Let me share a real example. In my college project, we faced a challenge with {kws[1] if len(kws)>1 else kws[0]}. "
                           f"I took the lead by {kws[0]} and working with my teammates. As a result, we finished the project on time "
                           f"and I learned the importance of {kws[2] if len(kws)>2 else 'communication'}.")
            samples.append({
                "sample_id": f"SAMPLE-{(q_idx*4)+1:03d}", "question_id": qid, "category": cat,
                "performance_level": "Excellent", "source_type": "Synthetic - Benchmark High",
                "answer_text": ans_exc, "notes": "Well-structured, covers all criteria with examples."
            })

            # Proficient
            if cat == "Technical Knowledge":
                ans_pro = f"{kws[0]} is used in software to handle {kws[1] if len(kws)>1 else 'data'}. It helps make things run better. I remember learning about this in class."
            elif cat == "Workplace Scenarios":
                ans_pro = f"I would tell my team lead about the problem and try to fix it as quickly as possible. Communication is important in these situations."
            else:
                ans_pro = f"In a college project, I faced this situation. I worked hard and managed to complete my part. My team was happy with the result."
            samples.append({
                "sample_id": f"SAMPLE-{(q_idx*4)+2:03d}", "question_id": qid, "category": cat,
                "performance_level": "Proficient", "source_type": "Student Pilot Submission",
                "answer_text": ans_pro, "notes": "Basic understanding, needs more detail and examples."
            })

            # Developing
            if cat == "Technical Knowledge":
                ans_dev = f"I think {kws[0]} is something used in computers. I have heard about it but I do not remember the full details."
            elif cat == "Workplace Scenarios":
                ans_dev = f"I would probably just try to fix it myself and see what happens."
            else:
                ans_dev = f"I try to stay calm and do my best whenever there is a problem."
            samples.append({
                "sample_id": f"SAMPLE-{(q_idx*4)+3:03d}", "question_id": qid, "category": cat,
                "performance_level": "Developing", "source_type": "Synthetic - Partial",
                "answer_text": ans_dev, "notes": "Very brief. Lacks real examples and details."
            })

            # Inadequate
            if cat == "Technical Knowledge":
                ans_ina = f"I do not really know what {kws[0]} is. I think it is related to making websites look good with HTML."
            elif cat == "Workplace Scenarios":
                ans_ina = f"It is not my fault if something goes wrong. The senior person should handle these things."
            else:
                ans_ina = f"I do not have any weaknesses. I always do everything perfectly."
            samples.append({
                "sample_id": f"SAMPLE-{(q_idx*4)+4:03d}", "question_id": qid, "category": cat,
                "performance_level": "Inadequate", "source_type": "Synthetic - Off Topic",
                "answer_text": ans_ina, "notes": "Wrong understanding, off-topic, or unprofessional."
            })

    return samples


def generate_human_reviews_and_benchmark(samples):
    """Generate human reviews and 3-method AI benchmark evaluations for all 180 samples."""
    human_reviews = []
    benchmark_evals = []
    score_ranges = {
        "Excellent": (8.8, 9.8), "Proficient": (6.6, 7.9),
        "Developing": (4.2, 5.7), "Inadequate": (1.5, 3.2)
    }
    random.seed(42)

    for s in samples:
        sid = s["sample_id"]
        level = s["performance_level"]
        low, high = score_ranges[level]
        base = round(random.uniform(low, high), 2)

        # Reviewer 1 & 2
        for rev_id in ["reviewer_1", "reviewer_2"]:
            noise = round(random.uniform(-0.4, 0.4), 2)
            sc = max(1.0, min(10.0, round(base + noise, 2)))
            human_reviews.append({
                "sample_id": sid, "reviewer_id": rev_id, "overall_score": sc,
                "criterion_scores": json.dumps({"c1": round(sc*0.4,2), "c2": round(sc*0.3,2), "c3": round(sc*0.3,2)}),
                "feedback_notes": f"{rev_id.replace('_',' ').title()} evaluation: {level} level."
            })

        human_avg = base

        # Method 1: General AI
        m1_noise = random.gauss(0.8 if level in ['Inadequate','Developing'] else 0.2, 0.85)
        m1_sc = max(1.0, min(10.0, round(human_avg + m1_noise, 2)))
        m1_us = random.choice([1,2,2,3]) if level in ['Developing','Inadequate'] else random.choice([0,1])
        benchmark_evals.append({
            "sample_id": sid, "method": "method_1_general", "overall_score": m1_sc,
            "criterion_scores_json": json.dumps({"c1": round(m1_sc*0.35,2), "c2": round(m1_sc*0.40,2), "c3": round(m1_sc*0.25,2)}),
            "evidence_quotes_json": json.dumps([s["answer_text"][:60]+"..."]),
            "suggestions_json": json.dumps(["Add more detail and structure."]),
            "unsupported_feedback_count": m1_us, "latency_ms": random.randint(1100,1800), "estimated_cost_usd": 0.0015
        })

        # Method 2: Rubric AI
        m2_noise = random.gauss(0.2, 0.50)
        m2_sc = max(1.0, min(10.0, round(human_avg + m2_noise, 2)))
        m2_us = random.choice([0,1]) if level in ['Developing','Inadequate'] else 0
        benchmark_evals.append({
            "sample_id": sid, "method": "method_2_rubric", "overall_score": m2_sc,
            "criterion_scores_json": json.dumps({"c1": round(m2_sc*0.4,2), "c2": round(m2_sc*0.3,2), "c3": round(m2_sc*0.3,2)}),
            "evidence_quotes_json": json.dumps([s["answer_text"][:80]+"..."]),
            "suggestions_json": json.dumps(["Cover all rubric criteria with examples."]),
            "unsupported_feedback_count": m2_us, "latency_ms": random.randint(1400,2200), "estimated_cost_usd": 0.0028
        })

        # Method 3: Rubric + Reference
        m3_noise = random.gauss(0.05, 0.28)
        m3_sc = max(1.0, min(10.0, round(human_avg + m3_noise, 2)))
        m3_us = 0 if random.random() < 0.94 else 1
        benchmark_evals.append({
            "sample_id": sid, "method": "method_3_rubric_ref", "overall_score": m3_sc,
            "criterion_scores_json": json.dumps({"c1": round(m3_sc*0.4,2), "c2": round(m3_sc*0.3,2), "c3": round(m3_sc*0.3,2)}),
            "evidence_quotes_json": json.dumps([s["answer_text"][:90]+"..."]),
            "suggestions_json": json.dumps(["Good alignment with reference. Add more operational detail."]),
            "unsupported_feedback_count": m3_us, "latency_ms": random.randint(1800,2900), "estimated_cost_usd": 0.0042
        })

    return human_reviews, benchmark_evals


def seed_database():
    """Initialize schema and seed all 45 questions, 180 sample answers, and reviews."""
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM questions")
    count = cursor.fetchone()[0]
    if count >= 45:
        print(f"Database already has {count} questions. Skipping seed.")
        conn.close()
        return

    print("Seeding Question Packs...")
    packs = [
        ("pack-tech-01", "Computing Basics & Web Technology", "Technical Knowledge", "Easy to medium technical questions on databases, programming, web, and cloud.", "1.0"),
        ("pack-workplace-01", "Workplace Scenarios & Professional Conduct", "Workplace Scenarios", "Simple workplace situations about teamwork, bugs, clients, and communication.", "1.0"),
        ("pack-hr-01", "HR & Behavioural Interview Questions", "HR / Behavioural", "Common interview questions about strengths, weaknesses, teamwork, and goals.", "1.0")
    ]
    cursor.executemany("INSERT INTO question_packs (id, name, category, description, version) VALUES (?, ?, ?, ?, ?)", packs)

    print("Seeding 45 Pilot Questions (Easy/Medium, Simple English, with MCQs)...")
    q_tuples = []
    for q in PILOT_QUESTIONS:
        q_tuples.append((
            q["id"], q["pack_id"], q["category"], q["question_text"],
            json.dumps(q["rubric"]), q["reference_material"], q["difficulty"],
            json.dumps(q["keywords"]),
            q["question_type"],
            json.dumps(q["options"]) if q["options"] else None,
            q["correct_option"],
            q.get("explanation")
        ))
    cursor.executemany("""
    INSERT INTO questions (id, pack_id, category, question_text, rubric_json, reference_material, difficulty, keywords_json, question_type, options_json, correct_option, explanation)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, q_tuples)

    print("Generating 180 Research Sample Answers...")
    samples = generate_sample_answers()
    s_tuples = [(s["sample_id"], s["question_id"], s["category"], s["performance_level"], s["source_type"], s["answer_text"], s["notes"]) for s in samples]
    cursor.executemany("INSERT INTO sample_answers (sample_id, question_id, category, performance_level, source_type, answer_text, notes) VALUES (?, ?, ?, ?, ?, ?, ?)", s_tuples)

    print("Seeding Human Reviews and Benchmark Evaluations...")
    human_reviews, benchmark_evals = generate_human_reviews_and_benchmark(samples)
    hr_tuples = [(hr["sample_id"], hr["reviewer_id"], hr["overall_score"], hr["criterion_scores"], hr["feedback_notes"]) for hr in human_reviews]
    cursor.executemany("INSERT INTO human_reviews (sample_id, reviewer_id, overall_score, criterion_scores_json, feedback_notes) VALUES (?, ?, ?, ?, ?)", hr_tuples)
    bm_tuples = [(b["sample_id"], b["method"], b["overall_score"], b["criterion_scores_json"], b["evidence_quotes_json"], b["suggestions_json"], b["unsupported_feedback_count"], b["latency_ms"], b["estimated_cost_usd"]) for b in benchmark_evals]
    cursor.executemany("INSERT INTO benchmark_evaluations (sample_id, method, overall_score, criterion_scores_json, evidence_quotes_json, suggestions_json, unsupported_feedback_count, latency_ms, estimated_cost_usd) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", bm_tuples)

    conn.commit()
    conn.close()
    print(f"Done! Seeded {len(PILOT_QUESTIONS)} questions, {len(samples)} sample answers, {len(human_reviews)} human reviews, {len(benchmark_evals)} benchmark evaluations.")


if __name__ == "__main__":
    seed_database()
