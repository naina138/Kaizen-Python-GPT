import json
from rapidfuzz import process

# Sample JSON database with predefined answers
data = {
    "Python?": "Python is a high-level, interpreted programming language known for its simplicity and readability.",
    "What are key features of Python?": "Python features include easy syntax, dynamic typing, garbage collection, high-level data structures, and support for multiple paradigms.",
    "What is variable?": "A variable is a named memory location used to store data.",
    "What are data types?": "Python has various data types such as int, float, str, list, tuple, dict, and set.",
    "What is list?": "A list is an ordered, mutable collection of items defined using square brackets [].",
    "What is tuple?": "A tuple is an ordered, immutable collection of items defined using parentheses ().",
    "What is dictionary?": "A dictionary is an unordered collection of key-value pairs defined using curly brackets {}.",
    "What is set?": "A set is an unordered collection of unique elements defined using curly brackets {}.",
    "What is function?": "A function is a reusable block of code that performs a specific task.",
    "What is lambda function?": "A lambda function is an anonymous function defined using the lambda keyword.",
    "What is if statement?": "An if statement is used for conditional execution of code.",
    "What is loop?": "Loops (for, while) allow repeated execution of code blocks.",
    "What is difference between break and continue?": "break exits a loop entirely, while continue skips the current iteration and moves to the next one.",
    "What is OOP?": "OOP (Object-Oriented Programming) is a paradigm based on objects and classes.",
    "What are classes and objects?": "A class is a blueprint for objects, and an object is an instance of a class.",
    "What is inheritance?": "Inheritance is a mechanism that allows a class to inherit properties and methods from another class.",
    "What is polymorphism?": "Polymorphism allows a function or method to have different behaviors based on the object calling it.",
    "What is exception?": "An exception is an error that occurs during program execution and can be handled using try-except blocks.",
    "What is module?": "A module is a file containing Python code that can be imported and reused in other programs.",
    "What is package?": "A package is a collection of related modules organized in a directory.",
    "What is multithreading?": "Multithreading allows concurrent execution of multiple threads to improve performance.",
    "What is decorator?": "A decorator is a function that modifies the behavior of another function or method.",
    "What is generator?": "A generator is a function that yields values lazily using the yield keyword.",
    "What is list comprehension?": "List comprehension is a concise way to create lists.",
    "What is difference between deep copy and shallow copy?": "A deep copy creates a new copy of an object and its nested elements, while a shallow copy only copies references.",
    "What are built-in data structures?": "Built-in data structures include lists, tuples, sets, and dictionaries.",
    "What is difference between mutable and immutable types?": "Mutable types (lists, dictionaries) can be changed after creation, whereas immutable types (tuples, strings) cannot.",
    "What is purpose of __init__ method?": "The __init__ method initializes a newly created object in a class.",
    "What is virtual environment?": "A virtual environment is an isolated workspace for projects to manage dependencies separately.",
    "What is pip?": "pip is Python's package manager used to install and manage libraries.",
    "What are built-in functions?": "Built-in functions include print(), len(), type(), input(), and range().",
    "What is recursion?": "Recursion is a programming technique where a function calls itself to solve a problem.",
    "What is difference between == and is operator?": "== checks for value equality, while is checks for object identity.",
    "What is difference between list and tuple?": "A list is mutable, while a tuple is immutable.",
    "What is difference between static method and class method?": "A static method does not depend on instance variables, whereas a class method can modify class variables.",
    "What is difference between local and global variable?": "A local variable is declared inside a function and accessible only there, whereas a global variable is accessible throughout the program.",
    "What is purpose of self keyword?": "self represents the instance of the class and allows access to its attributes and methods.",
    "What is docstring?": "A docstring is a multi-line string used to document a module, function, or class.",
    "What is map function?": "The map function applies a function to each item in an iterable and returns an iterator.",
    "What is filter function?": "The filter function returns an iterator containing elements that satisfy a given condition.",
    "What is zip function?": "The zip function combines multiple iterables into tuples.",
    "What is enumerate function?": "The enumerate function adds an index to an iterable and returns it as an iterator.",
    "What is difference between args and kwargs?": "*args is used for variable-length positional arguments, while **kwargs is used for variable-length keyword arguments.",
    "What is f-string?": "An f-string is a formatted string literal introduced in Python 3.6 to simplify string interpolation.",
    " Time complexity of searching in a dictionary?": "The average time complexity for searching in a dictionary is O(1).",
    "What is difference between del, pop and remove?": "del removes an element by index, pop removes and returns an element by index, and remove deletes an element by value.",
    "What is metaclass?": "A metaclass is a class that defines the behavior of other classes.",
    "What is use of pass statement?": "The pass statement is a placeholder used when a statement is syntactically required but no code needs to be executed.",
    "What is string?": "String is a data type which contains characters.",
    "What is data science?": "It deals with data to find insights.",
      "What is Object-Oriented Programming (OOP)?": "OOP is a programming paradigm based on objects containing data and behavior.",
    "What are the four main principles of OOP?": "Encapsulation, Inheritance, Polymorphism, and Abstraction.",
    "Why is OOP important?": "OOP improves code reusability, maintainability, and scalability by structuring programs around objects.",
    "What are objects in OOP?": "Objects are instances of a class that contain attributes and behaviors.",
    "What is a class in Python?": "A class is a blueprint for creating objects, defining their properties and behaviors.",
    "How do you create a class in Python?": "Use the 'class' keyword, e.g., 'class Car: pass'.",
    "How do you create an object in Python?": "Instantiate a class: 'my_car = Car()'.",
    "What is an instance variable?": "A variable specific to an instance of a class, defined using 'self.var_name'.",
    "What is a class variable?": "A variable shared across all instances of a class, defined within the class but outside methods.",
    "What is the difference between instance and class variables?": "Instance variables are unique to each object, while class variables are shared across all instances.",
    "What is encapsulation in OOP?": "Encapsulation restricts direct access to object data and allows modification through methods.",
    "How do you achieve encapsulation in Python?": "By defining private (_var) or protected (__var) attributes.",
    "What is the purpose of the __init__ method?": "The __init__ method initializes an object's attributes when created.",
    "What is a getter method?": "A method that retrieves the value of a private variable.",
    "What is a setter method?": "A method that modifies the value of a private variable.",
    "How do you implement getters and setters in Python?": "Using property decorators @property and @setter.",
    "What is the difference between private and protected attributes?": "Private (__var) attributes are not directly accessible, whereas protected (_var) attributes can be accessed in subclasses.",
    "Why should we use encapsulation?": "Encapsulation improves security, data integrity, and modularity in code.",
    "What is the difference between data hiding and encapsulation?": "Data hiding restricts access to attributes, while encapsulation includes controlled access via methods.",
    "Can private attributes be accessed outside the class?": "No, but they can be accessed using name mangling (_ClassName__var).",
    "What is inheritance in Python?": "Inheritance allows a class to inherit properties and methods from another class.",
    "What are the types of inheritance?": "Single, multiple, multilevel, hierarchical, and hybrid inheritance.",
    "How do you implement single inheritance in Python?": "class Child(Parent): pass",
    "What is multiple inheritance?": "A class inheriting from multiple parent classes.",
    "What is multilevel inheritance?": "A child class inheriting from another derived class.",
    "What is hierarchical inheritance?": "Multiple child classes inheriting from a single parent class.",
    "What is hybrid inheritance?": "A combination of multiple types of inheritance.",
    "How do you use the super() function?": "super() is used to call a method from a parent class.",
    "What happens if two parent classes have the same method in multiple inheritance?": "The method resolution order (MRO) determines which method is used.",
    "What is the Method Resolution Order (MRO)?": "MRO defines the order in which base classes are searched for methods.",
    "What is the difference between composition and inheritance?": "Composition uses objects of other classes, while inheritance derives new classes from existing ones.",
    "What is polymorphism in OOP?": "Polymorphism allows objects of different classes to be treated as the same type.",
    "What is method overloading?": "Defining multiple methods with the same name but different parameters (not directly supported in Python).",
    "What is method overriding?": "Redefining a method in a subclass that exists in a parent class.",
    "What is operator overloading?": "Defining custom behavior for operators like +, -, *, etc., using special methods.",
    "How do you overload the + operator in Python?": "By defining the __add__ method in a class.",
    "What is duck typing?": "A concept where an object's behavior determines its type rather than explicit inheritance.",
    "What is dynamic method dispatch?": "A process where a call to an overridden method is resolved at runtime.",
    "What is the difference between static and dynamic polymorphism?": "Static polymorphism (overloading) is determined at compile time, while dynamic polymorphism (overriding) occurs at runtime.",
    "Can Python support method overloading?": "Not directly, but it can be simulated using default arguments or *args.",
    "Why is polymorphism useful?": "Polymorphism promotes code flexibility and reusability.",
    "What is abstraction in OOP?": "Abstraction hides implementation details and shows only necessary functionalities.",
    "How do you achieve abstraction in Python?": "Using abstract classes and methods with the abc module.",
    "What is an abstract class?": "A class that cannot be instantiated and contains at least one abstract method.",
    "What is an abstract method?": "A method declared in a class but implemented in a subclass.",
    "What module is used for abstraction in Python?": "The 'abc' module.",
    "Can abstract classes have concrete methods?": "Yes, abstract classes can have both abstract and concrete methods.",
    "What is the difference between an interface and an abstract class?": "An interface only contains method signatures, while an abstract class can contain method implementations.",
    "Can a class be abstract without an abstract method?": "Yes, but it cannot be instantiated.",
    "Why is abstraction important in OOP?": "Abstraction simplifies complex systems by exposing only necessary details.",
    "What is the difference between abstraction and encapsulation?": "Encapsulation hides data, while abstraction hides implementation details.",
    "What is a static method?": "A method that does not depend on class or instance attributes, defined using @staticmethod.",
    "What is a class method?": "A method that works on class attributes, defined using @classmethod.",
    "What is the difference between static and class methods?": "A static method does not access class data, while a class method does.",
    "What is the self parameter?": "A reference to the current instance of a class.",
    "What is the difference between self and cls?": "self refers to instance attributes, while cls refers to class attributes.",
    "What is multiple dispatch?": "A technique where method selection depends on multiple argument types.",
    "What is a singleton class?": "A class that allows only one instance to exist.",
    "What is the difference between association, aggregation, and composition?": "Association is a general relationship, aggregation is a weak relationship, and composition is a strong relationship.",
    "How do you prevent a class from being inherited?": "By raising an exception in the __init__ method or using metaclasses.",
    "What is the difference between procedural and OOP programming?": "Procedural programming follows a sequence, while OOP organizes code into objects.",
    "How is OOP used in real-world applications?": "OOP is used in game development, GUI applications, data science, and enterprise software.",
    "Can OOP be used in machine learning?": "Yes, OOP helps structure machine learning models using objects and classes.",
    "Is Python a fully OOP language?": "Python supports OOP but also allows procedural and functional programming.",

    "What is a data structure?": "A data structure is a way to store and organize data efficiently.",
    "What are the types of data structures?": "Linear (arrays, lists, stacks, queues) and Non-linear (trees, graphs).",
    "What is the difference between linear and non-linear data structures?": "Linear structures store data sequentially, whereas non-linear structures organize data hierarchically.",
    "What are the primary operations on data structures?": "Insertion, deletion, traversal, searching, and sorting.",
    "Why are data structures important?": "They optimize data processing, improve efficiency, and make algorithms scalable.",
    "What is a list in Python?": "A list is an ordered, mutable collection of elements.",
    "How do you create a list in Python?": "Using square brackets: my_list = [1, 2, 3].",
    "What is the time complexity of list operations?": "Appending: O(1), Insertion/Deletion: O(n), Access: O(1).",
    "How does slicing work in lists?": "List slicing extracts a subset: my_list[start:end:step].",
    "What is the difference between list and tuple?": "Lists are mutable, while tuples are immutable.",

    "What is a stack?": "A stack is a linear data structure following the LIFO (Last In, First Out) principle.",
    "What are the main operations of a stack?": "Push (insert), Pop (remove), Peek (view top element).",
    "How can a stack be implemented?": "Using lists or the collections.deque module.",
    "What is the time complexity of stack operations?": "Push and pop operations are O(1).",
    "What are some real-world applications of stacks?": "Undo/redo, function call stack, browser history.",

    "What is a queue?": "A queue is a linear data structure following the FIFO (First In, First Out) principle.",
    "What are the main operations of a queue?": "Enqueue (insert), Dequeue (remove), Front (view first element).",
    "How can a queue be implemented?": "Using lists, collections.deque, or queue.Queue.",
    "What is the time complexity of queue operations?": "Enqueue and dequeue operations are O(1).",
    "What are some real-world applications of queues?": "Task scheduling, print spooling, messaging systems.",

    "What is a tree?": "A tree is a hierarchical data structure with nodes connected by edges.",
    "What are the components of a tree?": "Root, parent, child, siblings, leaves, edges, height, depth.",
    "What is a binary tree?": "A tree where each node has at most two children.",
    "What is a binary search tree (BST)?": "A binary tree where the left child < parent < right child.",
    "What is tree traversal?": "Visiting all nodes in a tree using methods like inorder, preorder, and postorder.",
    "What is the time complexity of searching in a BST?": "O(log n) for balanced trees, O(n) for skewed trees.",
    "What are AVL trees?": "Self-balancing BSTs where height difference between subtrees is ≤1.",
    "What is a heap?": "A specialized tree-based structure satisfying the heap property.",
    "What is the difference between min-heap and max-heap?": "Min-heap: Parent ≤ children. Max-heap: Parent ≥ children.",
    "What are some real-world applications of trees?": "Databases, file systems, hierarchical data representation.",

    "What is a graph?": "A graph is a collection of vertices (nodes) and edges (connections).",
    "What are the types of graphs?": "Directed, undirected, weighted, unweighted, cyclic, acyclic.",
    "What is an adjacency matrix?": "A 2D array representing graph connections (O(n²) space).",
    "What is an adjacency list?": "A list-based representation of graph connections (O(V+E) space).",
    "What are graph traversal techniques?": "Depth-First Search (DFS) and Breadth-First Search (BFS).",
    "What is DFS?": "Depth-First Search explores as far as possible before backtracking.",
    "What is BFS?": "Breadth-First Search explores all neighbors before moving deeper.",
    "What is Dijkstra’s algorithm?": "An algorithm to find the shortest path in weighted graphs.",
    "What is the time complexity of Dijkstra’s algorithm?": "O((V+E) log V) using a priority queue.",
    "What is the Bellman-Ford algorithm?": "A shortest path algorithm that works for graphs with negative weights.",

    # Sorting Algorithms
    "What is sorting?": "Sorting arranges elements in a specific order (ascending/descending).",
    "What is the time complexity of bubble sort?": "O(n²) in worst and average cases.",
    "What is selection sort?": "A sorting algorithm that repeatedly selects the smallest element.",
    "What is insertion sort?": "A sorting algorithm that inserts elements in their correct position.",
    "What is merge sort?": "A divide-and-conquer sorting algorithm with O(n log n) complexity.",
    "What is quicksort?": "A sorting algorithm that uses partitioning for sorting (O(n log n) avg).",
    "What is counting sort?": "A non-comparative sorting algorithm with O(n + k) complexity.",
    "What is radix sort?": "A non-comparative sorting algorithm sorting numbers digit by digit.",
    "What is bucket sort?": "A sorting algorithm that distributes elements into buckets and sorts them.",
    "What is the difference between stable and unstable sorting?": "Stable sorting maintains the order of equal elements, unstable does not.",

    # Searching Algorithms
    "What is searching?": "Finding an element in a data structure.",
    "What is linear search?": "A simple search algorithm with O(n) complexity.",
    "What is binary search?": "An efficient search algorithm with O(log n) complexity, requiring sorted data.",
    "What is ternary search?": "A divide-and-conquer search algorithm similar to binary search.",
    "What is jump search?": "A search algorithm that jumps fixed steps before linear search.",
    "What is exponential search?": "A search algorithm that finds the range before applying binary search.",
    "What is interpolation search?": "A search algorithm optimized for uniformly distributed sorted data.",
    "What is hash-based searching?": "A searching technique using hash tables (O(1) average time).",
    "What is the best searching algorithm?": "Depends on the data; for sorted arrays, binary search is best.",
    "What is the worst-case complexity of binary search?": "O(log n), when the element is not found.",

    # Miscellaneous DSA Topics
    "What is recursion?": "A function calling itself to solve smaller subproblems.",
    "What is dynamic programming?": "A method to solve problems by breaking them into overlapping subproblems.",
    "What is memoization?": "A technique to store previously computed results to avoid redundancy.",
    "What is greedy algorithm?": "An algorithm that makes the best local choice at each step.",
    "What is backtracking?": "An algorithm that explores all possibilities and backtracks when needed.",
    "What is Big O notation?": "A mathematical notation to describe algorithm complexity.",
    "What is time complexity?": "The measure of the number of operations in an algorithm.",
    "What is space complexity?": "The measure of memory used by an algorithm.",
    "What is a hash table?": "A data structure that stores key-value pairs for quick lookups.",
    "What is amortized analysis?": "An average-case performance analysis over a sequence of operations.",

    # Basics of Regular Expressions
    "What is a regular expression?": "A regular expression (regex) is a sequence of characters that defines a search pattern.",
    "What is the use of regular expressions?": "Regular expressions are used for pattern matching, validation, and string manipulation.",
    "How do you define a regex pattern in Python?": "Using the re module, e.g., `re.match(r'pattern', text)`.",
    "What is the difference between re.match() and re.search()?": "match() checks only the beginning of a string, while search() checks the entire string.",
    "What is the purpose of re.findall()?": "It returns all occurrences of a pattern in a string.",
    
    # Meta Characters
    "What does the dot (.) match in regex?": "It matches any single character except a newline.",
    "What does the caret (^) do in regex?": "It matches the start of a string.",
    "What does the dollar sign ($) do in regex?": "It matches the end of a string.",
    "What does the asterisk (*) do in regex?": "It matches 0 or more occurrences of the preceding character.",
    "What does the plus (+) do in regex?": "It matches 1 or more occurrences of the preceding character.",
    "What does the question mark (?) do in regex?": "It matches 0 or 1 occurrence of the preceding character.",
    "What does the pipe (|) do in regex?": "It acts as an OR operator, matching either pattern.",
    
    # Character Classes
    "What is a character class in regex?": "A character class matches any one character from a set.",
    "What does [abc] match?": "It matches either 'a', 'b', or 'c'.",
    "What does [0-9] match?": "It matches any digit from 0 to 9.",
    "What does [A-Za-z] match?": "It matches any uppercase or lowercase letter.",
    "What does [^0-9] match?": "It matches any character except digits.",
    "What does \d match in regex?": "It matches any digit (0-9), equivalent to [0-9].",
    "What does \D match in regex?": "It matches any non-digit character, equivalent to [^0-9].",
    "What does \w match in regex?": "It matches any word character (letters, digits, underscore).",
    "What does \W match in regex?": "It matches any non-word character.",
    "What does \s match in regex?": "It matches any whitespace character (space, tab, newline).",
    "What does \S match in regex?": "It matches any non-whitespace character.",
    
    # Quantifiers
    "What does {n} mean in regex?": "It matches exactly 'n' occurrences of the preceding character.",
    "What does {n,} mean in regex?": "It matches at least 'n' occurrences of the preceding character.",
    "What does {n,m} mean in regex?": "It matches between 'n' and 'm' occurrences of the preceding character.",
    "What is the difference between greedy and lazy matching?": "Greedy matching tries to match as much as possible, while lazy matching matches the shortest possible string.",
    "How do you make a quantifier lazy?": "By adding a '?' after it, e.g., `.*?` matches the shortest possible match.",
    
    # Grouping and Capturing
    "What are capturing groups in regex?": "Groups allow part of a match to be extracted and referenced.",
    "How do you define a capturing group?": "Using parentheses, e.g., `(ab)+` matches 'ab' one or more times.",
    "How do you refer to a captured group in regex?": "Using backreferences, e.g., `\\1` refers to the first captured group.",
    "What does (?:...) do in regex?": "It defines a non-capturing group, which groups without storing the match.",
    "How do you name a capturing group?": "Using `(?P<name>pattern)`, e.g., `(?P<year>\d{4})`.",
    
    # Lookaheads and Lookbehinds
    "What is a lookahead in regex?": "A lookahead ensures a pattern follows without including it in the match.",
    "How do you write a positive lookahead?": "Using `(?=...)`, e.g., `\d(?=px)` matches digits before 'px'.",
    "What is a negative lookahead in regex?": "It ensures a pattern does not follow without including it in the match.",
    "How do you write a negative lookahead?": "Using `(?!...)`, e.g., `\d(?!px)` matches digits not followed by 'px'.",
    "What is a lookbehind in regex?": "A lookbehind ensures a pattern precedes without including it in the match.",
    "How do you write a positive lookbehind?": "Using `(?<=...)`, e.g., `(?<=\$)\d+` matches digits preceded by '$'.",
    "What is a negative lookbehind in regex?": "It ensures a pattern does not precede without including it in the match.",
    "How do you write a negative lookbehind?": "Using `(?<!...)`, e.g., `(?<!\$)\d+` matches digits not preceded by '$'.",
    
    # String Manipulation
    "How do you replace a pattern in a string?": "Using `re.sub(pattern, replacement, text)`.",
    "How do you split a string using regex?": "Using `re.split(pattern, text)`.",
    "How do you extract email addresses using regex?": "Using `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b`.",
    "How do you validate a phone number using regex?": "Using `^\+?[1-9]\d{1,14}$` for international formats.",
    "How do you remove extra spaces from a string using regex?": "Using `re.sub(r'\s+', ' ', text)`.",
    
    # Advanced Regex
    "What is regex backreference?": "It refers to a previous capture group within the same regex.",
    "What does \b mean in regex?": "It matches a word boundary (start or end of a word).",
    "What does \B mean in regex?": "It matches a position that is not a word boundary.",
    "How do you use regex in Python?": "Using the `re` module, e.g., `re.match()`, `re.search()`.",
    "How do you use regex in JavaScript?": "Using `RegExp` objects, e.g., `/pattern/.test(string)`. ",
    "What is the purpose of re.compile()?": "It compiles a regex pattern for faster matching in repeated use.",
    "What is regex greedy matching?": "It matches as much as possible before backtracking.",
    "What is regex lazy matching?": "It matches the shortest possible string before stopping.",
    "What does re.IGNORECASE or re.I do?": "It makes regex case-insensitive.",
    "What does re.MULTILINE or re.M do?": "It allows `^` and `$` to match start and end of lines.",
    
    # Practical Applications
    "How is regex used in web scraping?": "It extracts data from web pages, like emails, phone numbers.",
    "How is regex used in log file analysis?": "It helps filter and analyze log entries based on patterns.",
    "How is regex used in data validation?": "It validates input like email, phone numbers, and dates.",
    "How is regex used in text processing?": "It performs tasks like search, replace, and data extraction.",
    "How can regex improve search engines?": "It allows advanced searching with pattern-based queries.",
    "How do you test regex patterns online?": "Using tools like regex101.com or regexr.com.",
    "What are common pitfalls in regex?": "Greedy matches, incorrect character classes, backtracking issues.",

    # Introduction to Flask
    "What is Flask?": "Flask is a lightweight, micro web framework for Python.",
    "Why use Flask?": "Flask is simple, flexible, and requires minimal setup.",
    "How do you install Flask?": "Using `pip install flask`.",
    "How do you create a basic Flask app?": "By creating `app.py` with `from flask import Flask; app = Flask(__name__)`.",
    "How do you run a Flask app?": "Using `flask run` or `python app.py`.",
    
    # Flask Routes
    "What is a route in Flask?": "A route maps URLs to functions in Flask.",
    "How do you define a route in Flask?": "Using `@app.route('/')` decorator.",
    "How do you pass parameters in Flask routes?": "Using `<parameter>` in routes, e.g., `@app.route('/user/<name>')`.",
    "What is the difference between GET and POST methods?": "GET retrieves data, POST submits data to the server.",
    "How do you handle POST requests in Flask?": "Using `request.form['key']` in a POST route.",
    
    # Flask Templates
    "What are Flask templates?": "Templates allow rendering HTML dynamically using Jinja2.",
    "How do you use templates in Flask?": "Using `render_template('template.html', data=value)`.",
    "What is Jinja2 in Flask?": "Jinja2 is a templating engine for dynamic HTML rendering.",
    "How do you loop in Jinja2?": "Using `{% for item in list %} ... {% endfor %}`.",
    "How do you include one template inside another in Flask?": "Using `{% include 'file.html' %}`.",
    
    # Flask Forms and Requests
    "How do you handle form data in Flask?": "Using `request.form.get('fieldname')`.",
    "How do you handle JSON data in Flask?": "Using `request.get_json()`.",
    "How do you redirect in Flask?": "Using `redirect(url_for('function_name'))`.",
    "How do you handle file uploads in Flask?": "Using `request.files['file']`.",
    "What is Flask-WTF?": "A Flask extension for working with web forms using WTForms.",
    
    # Flask Responses
    "What is a response in Flask?": "A response is the data returned to the client.",
    "How do you return JSON in Flask?": "Using `jsonify({'key': 'value'})`.",
    "How do you set HTTP status codes in Flask?": "Using `return 'Message', 404`.",
    "What is the default port for Flask?": "Port 5000.",
    "How do you set cookies in Flask?": "Using `response.set_cookie('key', 'value')`.",
    
    # Introduction to Django
    "What is Django?": "Django is a high-level Python web framework.",
    "Why use Django?": "Django follows the 'batteries-included' philosophy and provides built-in features.",
    "How do you install Django?": "Using `pip install django`.",
    "How do you create a new Django project?": "Using `django-admin startproject projectname`.",
    "How do you create a new Django app?": "Using `python manage.py startapp appname`.",
    
    # Django Views and URLs
    "What is a view in Django?": "A view is a function that handles HTTP requests.",
    "How do you define a view in Django?": "By writing a function in `views.py`.",
    "How do you map URLs to views in Django?": "Using `urlpatterns` in `urls.py`.",
    "How do you pass parameters in Django URLs?": "Using `<int:id>` or `<str:name>` in `path()`.",
    "What is a class-based view in Django?": "A class-based view (CBV) is an object-oriented way of handling requests.",
    
    # Django Templates
    "What are Django templates?": "Django templates allow dynamic HTML rendering.",
    "How do you use Django templates?": "Using `render(request, 'template.html', context)`.",
    "How do you loop in Django templates?": "Using `{% for item in list %} ... {% endfor %}`.",
    "How do you extend templates in Django?": "Using `{% extends 'base.html' %}`.",
    "How do you include one template inside another in Django?": "Using `{% include 'file.html' %}`.",
    
    # Django Forms and Requests
    "What is Django Forms?": "Django Forms handle HTML form generation and validation.",
    "How do you create a form in Django?": "By defining a class that inherits from `forms.Form`.",
    "How do you handle form submissions in Django?": "Using `request.POST.get('fieldname')`.",
    "How do you validate forms in Django?": "Using `form.is_valid()`.",
    "How do you handle file uploads in Django?": "Using `request.FILES['file']`.",
    
    # Django Models and Database
    "What is a Django model?": "A Django model is a representation of a database table.",
    "How do you create a Django model?": "By defining a class in `models.py` that inherits from `models.Model`.",
    "How do you apply database migrations in Django?": "Using `python manage.py makemigrations` and `migrate`.",
    "How do you query data in Django?": "Using `Model.objects.filter(condition)`.",
    "What is Django ORM?": "Django ORM (Object-Relational Mapping) allows interaction with the database using Python.",
    
    # Django Authentication
    "How does Django handle authentication?": "Using Django's built-in authentication system.",
    "How do you create a user in Django?": "Using `User.objects.create_user(username, email, password)`.",
    "How do you check user authentication in Django?": "Using `request.user.is_authenticated`.",
    "How do you implement login in Django?": "Using `authenticate()` and `login()` functions.",
    "How do you implement logout in Django?": "Using `logout(request)`.",
    
    # Django Middleware
    "What is middleware in Django?": "Middleware processes requests before reaching the view.",
    "How do you add middleware in Django?": "By adding it to `MIDDLEWARE` in `settings.py`.",
    "How do you create custom middleware in Django?": "By creating a class that implements `__call__()`.",
    "What are common middleware classes in Django?": "AuthenticationMiddleware, SecurityMiddleware, etc.",
    "How do you disable middleware in Django?": "By removing it from `MIDDLEWARE` in `settings.py`.",
    
    # Deployment and Security
    "How do you deploy a Flask app?": "Using services like Gunicorn, uWSGI, or Flask's built-in server.",
    "How do you deploy a Django app?": "Using services like Heroku, AWS, or DigitalOcean.",
    "What is the purpose of `DEBUG` in Django settings?": "To enable/disable debug mode.",
    "How do you configure allowed hosts in Django?": "Using `ALLOWED_HOSTS` in `settings.py`.",
    "How do you handle environment variables in Django?": "Using `os.environ.get('VAR_NAME')`.",
    
    # Miscellaneous
    "How do you enable CORS in Flask?": "Using `Flask-CORS` extension.",
    "How do you enable CORS in Django?": "Using `django-cors-headers` package.",
    "What is REST API?": "A REST API is a web service that follows REST principles.",
    "How do you create a REST API in Flask?": "Using `Flask-RESTful` or `Flask-RESTX`.",
    "How do you create a REST API in Django?": "Using Django REST Framework (DRF).",
    "What is the difference between Flask and Django?": "Flask is lightweight and flexible, while Django is full-featured and structured.",

    # Introduction to Databases
    "What is a database?": "A database is an organized collection of data that allows easy access, management, and updating.",
    "What are relational databases?": "Relational databases store data in tables with predefined relationships between them.",
    "What is SQL?": "SQL (Structured Query Language) is used to interact with relational databases.",
    "What are the types of databases?": "Databases include relational (SQL) and non-relational (NoSQL) databases.",
    "What is a database management system (DBMS)?": "A DBMS is software that allows users to create, read, update, and delete data in databases.",
    
    # SQLite Basics
    "What is SQLite?": "SQLite is a lightweight, serverless, self-contained SQL database engine.",
    "Why use SQLite?": "SQLite is easy to set up, requires no server, and is suitable for small applications.",
    "How do you create a SQLite database?": "Using `sqlite3 database_name.db` in the command line.",
    "How do you create a table in SQLite?": "Using `CREATE TABLE table_name (column1 datatype, column2 datatype);`.",
    "How do you insert data into a SQLite table?": "Using `INSERT INTO table_name (column1, column2) VALUES (value1, value2);`.",
    
    # MySQL Basics
    "What is MySQL?": "MySQL is an open-source relational database management system (RDBMS).",
    "Why use MySQL?": "MySQL is scalable, secure, and widely used in web applications.",
    "How do you start a MySQL server?": "Using `sudo service mysql start` or `mysqld`.",
    "How do you connect to MySQL?": "Using `mysql -u username -p` in the terminal.",
    "How do you create a database in MySQL?": "Using `CREATE DATABASE database_name;`.",
    
    # PostgreSQL Basics
    "What is PostgreSQL?": "PostgreSQL is an advanced, open-source relational database known for its extensibility.",
    "Why use PostgreSQL?": "PostgreSQL supports complex queries, large datasets, and advanced features.",
    "How do you start a PostgreSQL server?": "Using `sudo service postgresql start`.",
    "How do you connect to PostgreSQL?": "Using `psql -U username -d database_name`.",
    "How do you create a database in PostgreSQL?": "Using `CREATE DATABASE database_name;`.",
    
    # CRUD Operations - Create
    "What is CRUD?": "CRUD stands for Create, Read, Update, and Delete operations in a database.",
    "How do you insert data into a MySQL table?": "Using `INSERT INTO table_name (column1, column2) VALUES (value1, value2);`.",
    "How do you insert data into a PostgreSQL table?": "Using `INSERT INTO table_name (column1, column2) VALUES (value1, value2);`.",
    "What is an auto-increment column?": "An auto-increment column automatically generates unique values.",
    "How do you add an auto-increment column in MySQL?": "Using `AUTO_INCREMENT` in the column definition.",
    
    # CRUD Operations - Read
    "How do you retrieve data from a table?": "Using `SELECT * FROM table_name;`.",
    "How do you filter data in a SELECT query?": "Using `WHERE` clause, e.g., `SELECT * FROM users WHERE age > 18;`.",
    "How do you sort query results?": "Using `ORDER BY column_name ASC|DESC;`.",
    "How do you limit query results?": "Using `LIMIT n;` to return only n rows.",
    "How do you retrieve unique values?": "Using `SELECT DISTINCT column_name FROM table_name;`.",
    
    # CRUD Operations - Update
    "How do you update a record in a table?": "Using `UPDATE table_name SET column1 = value WHERE condition;`.",
    "How do you update multiple records?": "Using `UPDATE table_name SET column1 = value1, column2 = value2 WHERE condition;`.",
    "What happens if you forget the WHERE clause in an UPDATE query?": "All records in the table will be updated.",
    "How do you prevent accidental updates?": "Always use a `WHERE` clause and test with `SELECT` before updating.",
    "How do you update a specific column in MySQL?": "Using `SET column_name = new_value WHERE condition;`.",
    
    # CRUD Operations - Delete
    "How do you delete a record from a table?": "Using `DELETE FROM table_name WHERE condition;`.",
    "How do you delete all records from a table?": "Using `DELETE FROM table_name;`.",
    "What is the difference between DELETE and TRUNCATE?": "DELETE removes rows with a condition, TRUNCATE removes all rows and resets indexes.",
    "How do you delete a table?": "Using `DROP TABLE table_name;`.",
    "How do you delete a database?": "Using `DROP DATABASE database_name;`.",
    
    # Joins
    "What is a join in SQL?": "A join combines rows from two or more tables based on a related column.",
    "What are the types of joins?": "INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL JOIN.",
    "What is an INNER JOIN?": "An INNER JOIN returns only matching rows from both tables.",
    "What is a LEFT JOIN?": "A LEFT JOIN returns all rows from the left table and matching rows from the right.",
    "What is a RIGHT JOIN?": "A RIGHT JOIN returns all rows from the right table and matching rows from the left.",
    
    # Indexes and Performance
    "What is an index in SQL?": "An index speeds up data retrieval in a database.",
    "How do you create an index?": "Using `CREATE INDEX index_name ON table(column);`.",
    "What is a primary key?": "A primary key uniquely identifies each record in a table.",
    "What is a foreign key?": "A foreign key links a column in one table to the primary key in another.",
    "How do indexes improve performance?": "Indexes allow faster searches by reducing the number of scanned rows.",
    
    # Transactions
    "What is a transaction in SQL?": "A transaction is a sequence of SQL statements executed as a single unit.",
    "What are the properties of a transaction?": "ACID: Atomicity, Consistency, Isolation, Durability.",
    "How do you start a transaction?": "Using `BEGIN TRANSACTION;`.",
    "How do you commit a transaction?": "Using `COMMIT;` to save changes.",
    "How do you roll back a transaction?": "Using `ROLLBACK;` to undo changes.",
    
    # Security and Best Practices
    "What is SQL injection?": "SQL injection is an attack where malicious SQL code is inserted into queries.",
    "How do you prevent SQL injection?": "By using parameterized queries or prepared statements.",
    "What is a database schema?": "A schema defines the structure of a database, including tables and relationships.",
    "What is data normalization?": "Normalization organizes data to reduce redundancy and improve integrity.",
    "What is a stored procedure?": "A stored procedure is a reusable SQL script stored in the database.",
    
    # Advanced SQL Features
    "What is a trigger in SQL?": "A trigger is an automatic action executed when a specific event occurs.",
    "What is a view in SQL?": "A view is a virtual table based on a SELECT query.",
    "What is a materialized view?": "A materialized view stores query results for faster access.",
    "What is a CTE (Common Table Expression)?": "A CTE is a temporary result set used in complex queries.",
    "How do you handle large datasets efficiently?": "By using indexing, partitioning, and optimized queries.",

    # Introduction to APIs
    "What is an API?": "An API (Application Programming Interface) allows different software applications to communicate with each other.",
    "What are the types of APIs?": "Types of APIs include REST, SOAP, GraphQL, and WebSockets.",
    "What is a REST API?": "A REST API follows Representational State Transfer principles for communication.",
    "What is a SOAP API?": "A SOAP API (Simple Object Access Protocol) uses XML for structured messaging.",
    "What is GraphQL?": "GraphQL is a query language that allows clients to request only the data they need.",
    "What is an HTTP request?": "An HTTP request is a message sent by a client to a server to perform an action.",
    "What are HTTP methods?": "HTTP methods include GET, POST, PUT, DELETE, PATCH, OPTIONS, and HEAD.",
    "What is the purpose of a GET request?": "A GET request retrieves data from a server.",
    "What is the purpose of a POST request?": "A POST request sends data to the server to create a resource.",
    "What is the purpose of a PUT request?": "A PUT request updates a resource by replacing it entirely.",
    
    # API Endpoints and Requests
    "What is an API endpoint?": "An API endpoint is a URL where clients can access resources.",
    "How do you structure API endpoints?": "API endpoints should be clear, consistent, and follow RESTful principles.",
    "What is a query parameter in an API?": "A query parameter is a key-value pair appended to a URL for filtering or customization.",
    "What is a request header?": "A request header contains metadata such as authentication tokens and content type.",
    "What is a request body?": "A request body contains data sent to the API, usually in JSON or XML format.",
    "What is JSON?": "JSON (JavaScript Object Notation) is a lightweight data format used for API communication.",
    "What is XML?": "XML (Extensible Markup Language) is another format used for data exchange in APIs.",
    "What is the difference between JSON and XML?": "JSON is more lightweight and widely used, while XML is more structured and supports schemas.",
    "What is an API key?": "An API key is a unique identifier used to authenticate API requests.",
    "How do you pass an API key in a request?": "API keys are passed in the request headers, query parameters, or request body.",
    
    # API Responses and Status Codes
    "What is an API response?": "An API response is the data returned by the server after processing a request.",
    "What is an HTTP status code?": "An HTTP status code indicates the outcome of an API request.",
    "What does status code 200 mean?": "Status code 200 means the request was successful.",
    "What does status code 201 mean?": "Status code 201 means a resource was successfully created.",
    "What does status code 400 mean?": "Status code 400 indicates a bad request due to client errors.",
    "What does status code 401 mean?": "Status code 401 means unauthorized access, usually due to missing authentication.",
    "What does status code 403 mean?": "Status code 403 means the request is forbidden due to insufficient permissions.",
    "What does status code 404 mean?": "Status code 404 means the requested resource was not found.",
    "What does status code 500 mean?": "Status code 500 indicates an internal server error.",
    "What does status code 503 mean?": "Status code 503 means the service is unavailable due to overload or maintenance.",
    
    # API Authentication and Security
    "What is API authentication?": "API authentication verifies the identity of clients accessing an API.",
    "What are common authentication methods for APIs?": "Common methods include API keys, OAuth, JWT, and Basic Authentication.",
    "What is OAuth?": "OAuth is an authorization framework that allows secure API access without exposing user credentials.",
    "What is JWT?": "JWT (JSON Web Token) is a compact, self-contained token used for authentication.",
    "How does JWT authentication work?": "JWT contains encoded user information and is validated using a secret key.",
    "What is Basic Authentication?": "Basic Authentication uses a username and password encoded in the request header.",
    "What is token-based authentication?": "Token-based authentication uses access tokens instead of passwords for secure access.",
    "What is API rate limiting?": "Rate limiting restricts the number of API requests a client can make in a given time.",
    "Why is rate limiting important?": "Rate limiting prevents abuse, protects server resources, and ensures fair usage.",
    "What is an API gateway?": "An API gateway is a management layer that handles authentication, rate limiting, and routing.",
    
    # API Design Best Practices
    "What are best practices for designing APIs?": "APIs should be RESTful, use clear endpoints, follow versioning, and ensure security.",
    "What is RESTful API design?": "RESTful APIs follow principles such as statelessness, resource-based URLs, and proper HTTP methods.",
    "Why is API versioning important?": "API versioning ensures backward compatibility when making updates.",
    "How can you implement API versioning?": "API versioning can be done using URL paths, headers, or query parameters.",
    "What is pagination in APIs?": "Pagination limits the number of results returned in a single request for large datasets.",
    "How do you implement pagination?": "Using query parameters like `?page=1&limit=10` to fetch paginated results.",
    "What is CORS?": "CORS (Cross-Origin Resource Sharing) controls how resources are shared across different domains.",
    "Why is CORS needed?": "CORS prevents unauthorized cross-origin API requests and enhances security.",
    "How do you enable CORS in an API?": "By setting the `Access-Control-Allow-Origin` header in the API response.",
    "What is HATEOAS in REST APIs?": "HATEOAS (Hypermedia as the Engine of Application State) allows APIs to provide links for navigation.",
    
    # Working with APIs in Python
    "How do you make an API request in Python?": "Using the `requests` library: `requests.get('https://api.example.com')`.",
    "How do you send a POST request in Python?": "Using `requests.post(url, json=data)`.",
    "How do you handle API responses in Python?": "Using `response.json()` to parse JSON responses.",
    "How do you handle API errors in Python?": "By checking `response.status_code` and using exception handling.",
    "How do you authenticate an API request in Python?": "By passing an API key in headers: `requests.get(url, headers={'Authorization': 'Bearer token'})`.",
    
    # API Testing and Monitoring
    "What is API testing?": "API testing ensures an API functions correctly and meets its requirements.",
    "What tools are used for API testing?": "Common tools include Postman, Curl, and automated testing frameworks like Pytest.",
    "How do you test an API with Postman?": "By sending requests, validating responses, and automating test cases.",
    "What is API mocking?": "API mocking creates fake API responses for testing without real API calls.",
    "What is API monitoring?": "API monitoring tracks API performance, availability, and response times.",
    
    # Advanced API Concepts
    "What is a WebSocket API?": "WebSockets allow real-time, bidirectional communication between client and server.",
    "What is a webhook?": "A webhook is an automated callback triggered by an event in another system.",
    "What is an RPC API?": "RPC (Remote Procedure Call) APIs allow clients to execute functions remotely.",
    "What is an API contract?": "An API contract defines the expected request and response structure of an API.",
    "What is API orchestration?": "API orchestration coordinates multiple API calls into a single workflow.",
    
    # API Trends and Future
    "What is serverless API architecture?": "Serverless APIs run on cloud services without managing infrastructure.",
    "What is an OpenAPI specification?": "OpenAPI defines a standard way to describe RESTful APIs.",
    "What is API-first development?": "API-first development focuses on designing APIs before building applications.",
    "What is API monetization?": "API monetization involves charging users for API usage through subscription models.",
    "What are microservices and how do they relate to APIs?": "Microservices are small, independent services that communicate via APIs.",

    # Introduction to Data Visualization
    "What is data visualization?": "Data visualization is the graphical representation of information and data.",
    "Why is data visualization important?": "It helps in identifying patterns, trends, and insights from data easily.",
    "What are common Python libraries for data visualization?": "Matplotlib, Seaborn, and Plotly are widely used for data visualization in Python.",
    "What is Matplotlib?": "Matplotlib is a popular Python library used for creating static, animated, and interactive plots.",
    "What is Seaborn?": "Seaborn is a Python library built on top of Matplotlib that provides a high-level interface for drawing attractive statistical graphics.",
    "What is Plotly?": "Plotly is a Python library for creating interactive plots and dashboards.",
    
    # Matplotlib Basics
    "How do you install Matplotlib?": "Use `pip install matplotlib` to install Matplotlib.",
    "How do you import Matplotlib?": "Use `import matplotlib.pyplot as plt` to import the pyplot module of Matplotlib.",
    "How do you create a simple line plot in Matplotlib?": "Use `plt.plot(x, y)` followed by `plt.show()` to display the plot.",
    "How do you add labels to a Matplotlib plot?": "Use `plt.xlabel('X-axis')` and `plt.ylabel('Y-axis')`.",
    "How do you add a title to a Matplotlib plot?": "Use `plt.title('Plot Title')`.",
    "How do you change the figure size in Matplotlib?": "Use `plt.figure(figsize=(width, height))`.",
    "How do you add a legend in Matplotlib?": "Use `plt.legend(['Label 1', 'Label 2'])`.",
    "How do you save a Matplotlib figure?": "Use `plt.savefig('filename.png')`.",
    "What is a subplot in Matplotlib?": "A subplot is a way to create multiple plots in a single figure using `plt.subplot()` or `plt.subplots()`.",
    "How do you create multiple subplots in Matplotlib?": "Use `fig, ax = plt.subplots(rows, cols)`.",

    # Matplotlib Plot Types
    "How do you create a bar plot in Matplotlib?": "Use `plt.bar(x, y)`.",
    "How do you create a scatter plot in Matplotlib?": "Use `plt.scatter(x, y)`.",
    "How do you create a histogram in Matplotlib?": "Use `plt.hist(data, bins=10)`.",
    "How do you create a pie chart in Matplotlib?": "Use `plt.pie(sizes, labels=labels)`.",
    "How do you create a box plot in Matplotlib?": "Use `plt.boxplot(data)`.",
    "How do you change line style in Matplotlib?": "Use `plt.plot(x, y, linestyle='--')`.",
    "How do you change marker style in Matplotlib?": "Use `plt.plot(x, y, marker='o')`.",
    "How do you change color in Matplotlib plots?": "Use `plt.plot(x, y, color='red')`.",
    
    # Seaborn Basics
    "How do you install Seaborn?": "Use `pip install seaborn` to install Seaborn.",
    "How do you import Seaborn?": "Use `import seaborn as sns` to import Seaborn.",
    "How do you load built-in datasets in Seaborn?": "Use `sns.load_dataset('dataset_name')`.",
    "How do you create a line plot in Seaborn?": "Use `sns.lineplot(x='column1', y='column2', data=df)`.",
    "How do you create a scatter plot in Seaborn?": "Use `sns.scatterplot(x='column1', y='column2', data=df)`.",
    "How do you create a histogram in Seaborn?": "Use `sns.histplot(data=df, x='column')`.",
    "How do you create a bar plot in Seaborn?": "Use `sns.barplot(x='category', y='values', data=df)`.",
    "How do you create a box plot in Seaborn?": "Use `sns.boxplot(x='category', y='values', data=df)`.",
    "How do you create a violin plot in Seaborn?": "Use `sns.violinplot(x='category', y='values', data=df)`.",
    "How do you create a heatmap in Seaborn?": "Use `sns.heatmap(df.corr(), annot=True, cmap='coolwarm')`.",
    
    # Seaborn Customization
    "How do you change the theme in Seaborn?": "Use `sns.set_theme(style='darkgrid')`.",
    "How do you change color palettes in Seaborn?": "Use `sns.set_palette('pastel')`.",
    "How do you add titles to Seaborn plots?": "Use `plt.title('Title')`.",
    "How do you customize axis labels in Seaborn?": "Use `plt.xlabel('X Label')`, `plt.ylabel('Y Label')`.",
    
    # Plotly Basics
    "How do you install Plotly?": "Use `pip install plotly`.",
    "How do you import Plotly?": "Use `import plotly.express as px`.",
    "How do you create an interactive scatter plot in Plotly?": "Use `px.scatter(df, x='column1', y='column2')`.",
    "How do you create an interactive line plot in Plotly?": "Use `px.line(df, x='column1', y='column2')`.",
    "How do you create an interactive bar plot in Plotly?": "Use `px.bar(df, x='category', y='values')`.",
    "How do you create an interactive pie chart in Plotly?": "Use `px.pie(df, names='category', values='values')`.",
    "How do you create an interactive histogram in Plotly?": "Use `px.histogram(df, x='column')`.",
    
    # Advanced Plotly Features
    "How do you create a 3D scatter plot in Plotly?": "Use `px.scatter_3d(df, x='x', y='y', z='z')`.",
    "How do you create a choropleth map in Plotly?": "Use `px.choropleth(df, locations='country', color='values')`.",
    "How do you create a bubble chart in Plotly?": "Use `px.scatter(df, x='x', y='y', size='size_column')`.",
    
    # Comparison of Libraries
    "What are the differences between Matplotlib, Seaborn, and Plotly?": "Matplotlib provides basic plots, Seaborn enhances statistical visualization, and Plotly provides interactive graphs.",
    "Which library is best for statistical analysis?": "Seaborn is best for statistical analysis as it provides built-in functions for statistical plots.",
    "Which library is best for interactive visualizations?": "Plotly is the best choice for interactive visualizations.",
    "Which library is best for simple plotting?": "Matplotlib is best for simple static plots.",
    
    # Miscellaneous
    "How do you display multiple plots in one figure?": "Use `plt.subplots(rows, cols)` in Matplotlib.",
    "How do you save a figure in Seaborn?": "Use `plt.savefig('filename.png')`.",
    "What is the difference between a bar plot and a histogram?": "A bar plot compares categories, while a histogram shows frequency distribution.",
    "How do you create an animated plot in Matplotlib?": "Use `matplotlib.animation` module.",
    "How do you add annotations to a plot?": "Use `plt.annotate('text', (x, y))`.",

    # Introduction to Machine Learning
    "What is Machine Learning?": "Machine Learning is a field of AI that enables systems to learn from data and make predictions without explicit programming.",
    "What are the types of Machine Learning?": "The main types are Supervised Learning, Unsupervised Learning, and Reinforcement Learning.",
    "What is Supervised Learning?": "Supervised Learning is a type of ML where a model learns from labeled data.",
    "What is Unsupervised Learning?": "Unsupervised Learning is a type of ML where a model identifies patterns in unlabeled data.",
    "What is Reinforcement Learning?": "Reinforcement Learning is a type of ML where an agent learns by interacting with an environment and receiving rewards or penalties.",
    "What is the difference between AI, ML, and Deep Learning?": "AI is the broader concept, ML is a subset of AI that learns from data, and Deep Learning is a subset of ML that uses neural networks.",
    "What is scikit-learn?": "scikit-learn is a Python library for machine learning, providing simple and efficient tools for data analysis and modeling.",
    "How do you install scikit-learn?": "Use `pip install scikit-learn` to install scikit-learn.",
    "How do you import scikit-learn?": "Use `import sklearn` to import the scikit-learn library.",
    
    # Supervised Learning
    "What is classification in ML?": "Classification is a supervised learning task where the goal is to assign labels to input data.",
    "What is regression in ML?": "Regression is a supervised learning task where the goal is to predict continuous values.",
    "What is an example of classification?": "Spam detection, where emails are classified as spam or not spam.",
    "What is an example of regression?": "Predicting house prices based on features like size and location.",
    "What is a training set in ML?": "A training set is the dataset used to train a machine learning model.",
    "What is a test set in ML?": "A test set is a separate dataset used to evaluate the model's performance.",
    "What is a validation set?": "A validation set is used to fine-tune model hyperparameters before testing.",
    "What is overfitting?": "Overfitting occurs when a model learns noise in the training data and fails to generalize.",
    "What is underfitting?": "Underfitting occurs when a model is too simple and fails to capture the underlying pattern in data.",
    "What is a decision tree?": "A decision tree is a tree-like model used for classification and regression tasks.",
    "What is a random forest?": "A random forest is an ensemble learning method that uses multiple decision trees.",
    "What is logistic regression?": "Logistic regression is a classification algorithm used to model the probability of a categorical outcome.",
    "What is linear regression?": "Linear regression is a regression algorithm used to predict continuous values.",
    "What is the difference between logistic regression and linear regression?": "Linear regression is used for continuous outcomes, while logistic regression is used for categorical outcomes.",
    "What is a support vector machine (SVM)?": "SVM is a supervised learning algorithm used for classification and regression by finding the optimal hyperplane.",
    
    # Unsupervised Learning
    "What is clustering in ML?": "Clustering is an unsupervised learning task that groups similar data points together.",
    "What is an example of clustering?": "Customer segmentation, where customers are grouped based on purchasing behavior.",
    "What is K-Means clustering?": "K-Means is an unsupervised algorithm that partitions data into K clusters.",
    "What is hierarchical clustering?": "Hierarchical clustering builds a hierarchy of clusters without specifying the number of clusters beforehand.",
    "What is DBSCAN?": "DBSCAN (Density-Based Spatial Clustering) is an unsupervised algorithm that groups data based on density.",
    "What is dimensionality reduction?": "Dimensionality reduction reduces the number of features in a dataset while preserving information.",
    "What is Principal Component Analysis (PCA)?": "PCA is a technique for reducing dimensionality by transforming features into principal components.",
    "What is feature engineering?": "Feature engineering involves creating new features or modifying existing ones to improve model performance.",
    
    # Model Evaluation and Performance Metrics
    "What is accuracy in ML?": "Accuracy is the percentage of correctly predicted labels in classification tasks.",
    "What is precision?": "Precision measures the proportion of true positive predictions among all positive predictions.",
    "What is recall?": "Recall measures the proportion of actual positive cases that were correctly identified.",
    "What is F1-score?": "F1-score is the harmonic mean of precision and recall.",
    "What is confusion matrix?": "A confusion matrix is a table used to evaluate classification model performance.",
    "What is RMSE?": "Root Mean Squared Error (RMSE) measures the difference between actual and predicted values in regression.",
    
    # Feature Selection and Data Preprocessing
    "What is feature selection?": "Feature selection is the process of selecting the most relevant features for a model.",
    "What is feature scaling?": "Feature scaling normalizes data to improve model performance.",
    "What is normalization?": "Normalization scales data to a range of [0,1] or [-1,1].",
    "What is standardization?": "Standardization scales data to have a mean of 0 and a standard deviation of 1.",
    "What is data augmentation?": "Data augmentation generates new training samples by applying transformations like rotation or flipping.",
    "What is missing data imputation?": "Missing data imputation is the process of replacing missing values in a dataset.",
    
    # Advanced ML Concepts
    "What is cross-validation?": "Cross-validation splits data into multiple subsets to validate model performance.",
    "What is hyperparameter tuning?": "Hyperparameter tuning optimizes model parameters for better performance.",
    "What is grid search?": "Grid search is a method for finding the best hyperparameters by testing all possible combinations.",
    "What is random search?": "Random search selects random hyperparameter combinations for optimization.",
    "What is transfer learning?": "Transfer learning reuses pre-trained models for new tasks to improve learning efficiency.",
    
    # Model Deployment
    "What is model deployment?": "Model deployment is the process of integrating a trained model into a production environment.",
    "What is Flask in ML deployment?": "Flask is a lightweight Python framework used for serving ML models as APIs.",
    "What is FastAPI?": "FastAPI is a high-performance framework used for deploying ML models with REST APIs.",
    "What is a model pipeline in ML?": "A pipeline automates data preprocessing, training, and prediction steps in ML.",
    
    # Miscellaneous
    "What is deep learning?": "Deep Learning is a subset of ML that uses neural networks with multiple layers.",
    "What is a neural network?": "A neural network is a computational model inspired by the human brain for learning patterns in data.",
    "What is a perceptron?": "A perceptron is a basic unit of a neural network used for binary classification.",
    "What is the difference between ML and Deep Learning?": "ML uses traditional algorithms, while Deep Learning relies on neural networks.",
    "What is an activation function?": "An activation function introduces non-linearity in neural networks.",
    "What is a loss function?": "A loss function measures the difference between predicted and actual values.",
    "What is backpropagation?": "Backpropagation is a method used in training neural networks to adjust weights based on error.",

    # Introduction to Excel and Pandas
    "What is Pandas in Python?": "Pandas is a Python library used for data manipulation and analysis, particularly useful for handling structured data like Excel files.",
    "How do you install Pandas?": "Use `pip install pandas` to install Pandas.",
    "How do you import Pandas?": "Use `import pandas as pd` to import the Pandas library.",
    "What is an Excel file?": "An Excel file is a spreadsheet document used to store, organize, and analyze data, typically saved as .xls or .xlsx.",
    "What is the difference between .xls and .xlsx?": ".xls is an older Excel format, while .xlsx is a newer format that supports more features and larger file sizes.",
    "How do you read an Excel file in Pandas?": "Use `pd.read_excel('file.xlsx')` to read an Excel file.",
    "How do you write a DataFrame to an Excel file?": "Use `df.to_excel('file.xlsx', index=False)` to save a DataFrame to an Excel file.",
    "What is the default engine used by Pandas to read Excel files?": "Pandas uses the `openpyxl` engine for .xlsx files and `xlrd` for .xls files.",
    
    # Reading and Writing Excel Files
    "How do you read multiple sheets from an Excel file?": "Use `pd.read_excel('file.xlsx', sheet_name=None)` to read all sheets into a dictionary of DataFrames.",
    "How do you specify a sheet while reading an Excel file?": "Use `pd.read_excel('file.xlsx', sheet_name='Sheet1')` to read a specific sheet.",
    "How do you read only specific columns from an Excel file?": "Use `pd.read_excel('file.xlsx', usecols=['Column1', 'Column2'])` to read specific columns.",
    "How do you skip rows while reading an Excel file?": "Use `pd.read_excel('file.xlsx', skiprows=5)` to skip the first 5 rows.",
    "How do you skip blank lines while reading an Excel file?": "Use `skip_blank_lines=True` in `pd.read_excel()`.",
    "How do you read an Excel file without headers?": "Use `pd.read_excel('file.xlsx', header=None)` to read without headers.",
    "How do you set a specific column as an index when reading an Excel file?": "Use `pd.read_excel('file.xlsx', index_col='Column1')` to set a column as an index.",
    "How do you save a Pandas DataFrame to a specific sheet in an Excel file?": "Use `df.to_excel('file.xlsx', sheet_name='Sheet1', index=False)`. ",
    "How do you append data to an existing Excel file?": "Use `ExcelWriter` with `mode='a'` to append data to an existing file.",
    
    # Manipulating DataFrames from Excel
    "How do you display the first few rows of a DataFrame?": "Use `df.head()` to display the first 5 rows.",
    "How do you display the last few rows of a DataFrame?": "Use `df.tail()` to display the last 5 rows.",
    "How do you get basic information about a DataFrame?": "Use `df.info()` to get a summary of the DataFrame.",
    "How do you get summary statistics of a DataFrame?": "Use `df.describe()` to get statistical summaries.",
    "How do you rename columns in a DataFrame?": "Use `df.rename(columns={'old_name': 'new_name'})`.",
    "How do you drop a column in a DataFrame?": "Use `df.drop(columns=['Column1'])` to remove a column.",
    "How do you filter data in a DataFrame?": "Use `df[df['Column1'] > 10]` to filter rows.",
    "How do you replace missing values in a DataFrame?": "Use `df.fillna(value)` to replace missing values.",
    "How do you remove rows with missing values?": "Use `df.dropna()` to remove rows with NaN values.",
    
    # Working with Multiple Sheets
    "How do you write multiple DataFrames to an Excel file?": "Use `ExcelWriter` with `df.to_excel(writer, sheet_name='Sheet1')`.",
    "How do you read multiple sheets from an Excel file?": "Use `pd.read_excel('file.xlsx', sheet_name=None)`.",
    "How do you copy a sheet in Excel using Pandas?": "You need to use `openpyxl` or `xlrd` to copy a sheet.",
    
    # Formatting and Styling
    "How do you format a column in an Excel file using Pandas?": "Use `df.style.format({'Column1': '{:.2f}'})`.",
    "How do you set column width in an Excel file?": "Use `openpyxl` to adjust column width.",
    "How do you set font style in an Excel file using Pandas?": "Use `xlsxwriter` with `workbook.add_format()` to style text.",
    
    # Advanced Excel Operations
    "How do you merge two DataFrames from an Excel file?": "Use `pd.merge(df1, df2, on='key')` to merge on a common column.",
    "How do you concatenate DataFrames from an Excel file?": "Use `pd.concat([df1, df2])` to concatenate DataFrames.",
    "How do you pivot a DataFrame from an Excel file?": "Use `df.pivot(index='Column1', columns='Column2', values='Column3')`.",
    "How do you group data in an Excel file using Pandas?": "Use `df.groupby('Column1').sum()` to group and aggregate data.",
    
    # Writing Data to Excel
    "How do you write a dictionary to an Excel file?": "Convert it to a DataFrame and use `df.to_excel('file.xlsx')`.",
    "How do you export data from Pandas to an Excel file?": "Use `df.to_excel('file.xlsx', index=False)`.",
    
    # Working with Dates and Time
    "How do you parse dates while reading an Excel file?": "Use `pd.read_excel('file.xlsx', parse_dates=['date_column'])`.",
    "How do you format dates in an Excel file using Pandas?": "Use `df['date_column'].dt.strftime('%Y-%m-%d')` to format dates.",
    
    # Error Handling and Debugging
    "What error occurs when reading an Excel file with missing dependencies?": "A `ModuleNotFoundError` occurs if `openpyxl` or `xlrd` is not installed.",
    "How do you handle missing values while reading an Excel file?": "Use `na_values=['missing']` in `pd.read_excel()`.",
    "What error occurs when writing to an open Excel file?": "A `PermissionError` occurs if the file is open.",
    
    # Miscellaneous
    "What is the best format for storing large datasets?": "For large datasets, `parquet` or `csv` is preferred over `xlsx`.",
    "What is the difference between Pandas and OpenPyXL?": "Pandas is for data manipulation, while OpenPyXL is for Excel file modifications.",
    "What is XlsxWriter?": "XlsxWriter is a Python module for creating Excel files with advanced formatting.",

    # Introduction to Networking
    "What is computer networking?": "Computer networking is the practice of connecting computers and devices to share resources and information.",
    "What is a network socket?": "A network socket is an endpoint for sending or receiving data across a network.",
    "What are the types of network sockets?": "The two main types of sockets are stream sockets (TCP) and datagram sockets (UDP).",
    "What is the difference between TCP and UDP?": "TCP is connection-oriented and reliable, while UDP is connectionless and faster but less reliable.",
    "What is an IP address?": "An IP address is a unique identifier assigned to each device on a network.",
    "What is the difference between IPv4 and IPv6?": "IPv4 uses 32-bit addresses, while IPv6 uses 128-bit addresses, allowing for more unique addresses.",
    "What is a port number?": "A port number is a numerical identifier for network services on a device.",
    "What are well-known ports?": "Well-known ports range from 0 to 1023 and are assigned to standard services like HTTP (80) and HTTPS (443).",
    "What is a protocol in networking?": "A protocol is a set of rules that define how data is transmitted over a network.",
    "What are common networking protocols?": "Common protocols include TCP, UDP, HTTP, FTP, and ICMP.",
    
    # Introduction to Sockets in Python
    "What is the Python socket module?": "The `socket` module in Python provides functions for network communication using sockets.",
    "How do you create a socket in Python?": "Use `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` to create a TCP socket.",
    "What are the types of socket families in Python?": "`AF_INET` for IPv4 and `AF_INET6` for IPv6.",
    "What are the types of socket types in Python?": "`SOCK_STREAM` for TCP and `SOCK_DGRAM` for UDP.",
    "How do you bind a socket to an address?": "Use `socket.bind(('hostname', port))`.",
    "How do you put a socket in listening mode?": "Use `socket.listen()` to make a socket listen for incoming connections.",
    "How do you accept a connection on a socket?": "Use `socket.accept()` to accept an incoming connection.",
    "How do you connect to a server socket?": "Use `socket.connect(('hostname', port))` to establish a connection.",
    "How do you send data through a socket?": "Use `socket.send(data)` for sending data.",
    "How do you receive data from a socket?": "Use `socket.recv(buffer_size)` to receive data.",

    # TCP Programming
    "How does TCP establish a connection?": "TCP uses a three-way handshake: SYN, SYN-ACK, and ACK.",
    "What is a TCP handshake?": "A process used to establish a TCP connection between a client and a server.",
    "How do you implement a TCP client in Python?": "Use `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`, connect to the server, and send/receive data.",
    "How do you implement a TCP server in Python?": "Create a socket, bind to an address, listen, accept connections, and communicate.",
    "What is the purpose of `socket.shutdown()`?": "It disables further send/receive operations on a socket.",
    "How do you close a socket?": "Use `socket.close()` to close a socket.",
    "How do you handle multiple clients in a TCP server?": "Use threading or `select` to handle multiple clients.",
    "What is `select` in socket programming?": "`select` allows monitoring multiple sockets for activity.",
    "How do you set a timeout for a socket?": "Use `socket.settimeout(seconds)`.",
    
    # UDP Programming
    "What is UDP?": "UDP (User Datagram Protocol) is a connectionless transport protocol.",
    "How is UDP different from TCP?": "UDP is faster and connectionless but does not guarantee delivery or order of packets.",
    "How do you create a UDP socket in Python?": "Use `socket.socket(socket.AF_INET, socket.SOCK_DGRAM)`.",
    "How do you send data using UDP?": "Use `socket.sendto(data, (host, port))`.",
    "How do you receive data using UDP?": "Use `socket.recvfrom(buffer_size)`.",
    "Why is UDP preferred for real-time applications?": "Because it has lower latency and does not require a connection handshake.",
    
    # Advanced Socket Programming
    "What is a non-blocking socket?": "A non-blocking socket does not wait for operations to complete before continuing execution.",
    "How do you make a socket non-blocking?": "Use `socket.setblocking(False)`.",
    "What is a raw socket?": "A raw socket allows direct access to lower network layers.",
    "What is multicast?": "Multicast is a one-to-many communication method over a network.",
    "What is broadcasting?": "Broadcasting sends data to all devices in a network segment.",
    "What is a socket timeout?": "A socket timeout is the maximum time a socket will wait for data before timing out.",
    
    # Network Utilities and Debugging
    "How do you find your IP address in Python?": "Use `socket.gethostbyname(socket.gethostname())`.",
    "How do you resolve a hostname to an IP?": "Use `socket.gethostbyname('hostname')`.",
    "How do you get the local hostname in Python?": "Use `socket.gethostname()`.",
    "What is netcat?": "Netcat is a command-line tool for testing network connections.",
    "What is Wireshark?": "Wireshark is a network packet analyzer.",
    "What is ping?": "Ping tests connectivity between devices using ICMP.",
    "How do you check open ports on a server?": "Use `nmap` or `netstat -an`.",
    
    # Security in Network Programming
    "What is SSL/TLS?": "SSL/TLS is a protocol for securing network communications.",
    "How do you enable SSL/TLS in Python sockets?": "Use `ssl.wrap_socket()` or `ssl.SSLContext().wrap_socket()`.",
    "What is a firewall?": "A firewall is a security system that monitors and controls network traffic.",
    "What is a VPN?": "A VPN (Virtual Private Network) encrypts internet traffic to secure data transmission.",
    
    # Miscellaneous
    "What is a proxy server?": "A proxy server acts as an intermediary between a client and the internet.",
    "What is NAT?": "Network Address Translation (NAT) maps private IPs to a public IP for internet access.",
    "What is DNS?": "The Domain Name System (DNS) translates domain names to IP addresses.",
    "What is DHCP?": "The Dynamic Host Configuration Protocol (DHCP) assigns IP addresses dynamically.",
    "What is ICMP?": "ICMP is used for error messages and network diagnostics, like ping.",
    "What is a VPN tunnel?": "A VPN tunnel encrypts and secures traffic between endpoints.",
    "What is a load balancer?": "A load balancer distributes traffic across multiple servers.",
    "What is an API gateway?": "An API gateway manages API requests and security.",
    "What is a CDN?": "A Content Delivery Network (CDN) speeds up content delivery by caching data globally.",
    
    # Conclusion
    "Why is network programming important?": "Network programming enables communication between devices over the internet and local networks.",
    "What are common challenges in network programming?": "Latency, packet loss, security, and connection reliability are common challenges.",
    "What are common applications of socket programming?": "Chat applications, file transfer, web servers, IoT, and multiplayer games use socket programming.",

    # Introduction to Cryptography
    "What is cryptography?": "Cryptography is the practice of securing information by converting it into an unreadable format.",
    "What are the main goals of cryptography?": "The main goals are confidentiality, integrity, authentication, and non-repudiation.",
    "What is plaintext?": "Plaintext is the original, readable message before encryption.",
    "What is ciphertext?": "Ciphertext is the encrypted, unreadable version of plaintext.",
    "What is encryption?": "Encryption is the process of converting plaintext into ciphertext using an algorithm and a key.",
    "What is decryption?": "Decryption is the process of converting ciphertext back into plaintext using a key.",
    "What is a cryptographic key?": "A cryptographic key is a piece of information used in encryption and decryption.",
    "What is the difference between symmetric and asymmetric encryption?": "Symmetric encryption uses one key for encryption and decryption, while asymmetric encryption uses a pair of public and private keys.",
    "What is a cipher?": "A cipher is an algorithm used for encryption and decryption.",
    "What is a cryptographic algorithm?": "A cryptographic algorithm is a set of rules for encrypting and decrypting data.",

    # Symmetric Encryption
    "What is symmetric encryption?": "Symmetric encryption uses the same key for both encryption and decryption.",
    "What are examples of symmetric encryption algorithms?": "Examples include AES, DES, and Blowfish.",
    "What is AES encryption?": "AES (Advanced Encryption Standard) is a widely used, secure encryption algorithm.",
    "What is DES encryption?": "DES (Data Encryption Standard) is an older encryption algorithm, now considered weak.",
    "What is Blowfish encryption?": "Blowfish is a symmetric encryption algorithm known for its speed and flexibility.",
    "What is the key size of AES?": "AES supports key sizes of 128, 192, and 256 bits.",
    "Why is AES preferred over DES?": "AES is more secure and supports larger key sizes than DES.",
    "What is an encryption key?": "An encryption key is a secret value used in encryption algorithms to secure data.",
    "What is key distribution?": "Key distribution is the process of securely sharing encryption keys between parties.",
    "What is the biggest challenge in symmetric encryption?": "The biggest challenge is securely sharing the key between parties.",

    # Asymmetric Encryption
    "What is asymmetric encryption?": "Asymmetric encryption uses a public key for encryption and a private key for decryption.",
    "What are examples of asymmetric encryption algorithms?": "Examples include RSA, ECC, and Diffie-Hellman.",
    "What is RSA encryption?": "RSA (Rivest-Shamir-Adleman) is a widely used asymmetric encryption algorithm.",
    "What is ECC encryption?": "ECC (Elliptic Curve Cryptography) is an efficient asymmetric encryption method with smaller keys.",
    "What is Diffie-Hellman key exchange?": "Diffie-Hellman is a method for securely exchanging cryptographic keys over a public channel.",
    "How does public-key cryptography work?": "A public key is used to encrypt data, and only the corresponding private key can decrypt it.",
    "What is the advantage of asymmetric encryption?": "It eliminates the need for secure key sharing, as only the private key must be kept secret.",
    "What is the disadvantage of asymmetric encryption?": "It is slower than symmetric encryption due to complex computations.",
    "What is a digital signature?": "A digital signature is a cryptographic method for verifying the authenticity of a message or document.",
    "How does a digital signature work?": "A sender signs a message with their private key, and the recipient verifies it using the sender's public key.",

    # Hashing
    "What is hashing in cryptography?": "Hashing converts data into a fixed-length string using a mathematical function.",
    "What are common hashing algorithms?": "Common algorithms include MD5, SHA-1, and SHA-256.",
    "What is MD5?": "MD5 (Message Digest 5) is a hashing algorithm that produces a 128-bit hash value.",
    "What is SHA-1?": "SHA-1 (Secure Hash Algorithm 1) produces a 160-bit hash value but is no longer secure.",
    "What is SHA-256?": "SHA-256 is a widely used, secure hashing algorithm that produces a 256-bit hash value.",
    "What is a cryptographic hash function?": "A hash function maps data to a fixed-length output and is designed to be irreversible.",
    "What is a hash collision?": "A hash collision occurs when two different inputs produce the same hash value.",
    "What is salting in cryptography?": "Salting is adding a random value to a password before hashing to increase security.",
    "What is a checksum?": "A checksum is a value used to verify the integrity of data.",
    "How is hashing used in password storage?": "Passwords are hashed before being stored to prevent them from being stolen in plaintext form.",

    # Cryptographic Protocols
    "What is SSL/TLS?": "SSL/TLS are cryptographic protocols used for securing communication over the internet.",
    "What is HTTPS?": "HTTPS is the secure version of HTTP that uses SSL/TLS encryption.",
    "What is a VPN?": "A VPN (Virtual Private Network) encrypts internet traffic for secure communication.",
    "What is PGP encryption?": "PGP (Pretty Good Privacy) is a cryptographic program used for secure email communication.",
    "What is the purpose of a cryptographic nonce?": "A nonce is a random value used once in encryption to prevent replay attacks.",
    "What is end-to-end encryption?": "End-to-end encryption ensures that only the sender and receiver can read a message.",
    "What is a certificate authority (CA)?": "A CA issues digital certificates to verify the authenticity of websites and entities.",
    "What is a digital certificate?": "A digital certificate is an electronic document that verifies an entity's identity.",
    "What is the purpose of public key infrastructure (PKI)?": "PKI manages digital certificates and encryption keys.",
    "What is two-factor authentication (2FA)?": "2FA requires two forms of verification to enhance security.",

    # Cryptanalysis and Security
    "What is cryptanalysis?": "Cryptanalysis is the study of breaking cryptographic algorithms and ciphers.",
    "What is brute force attack?": "A brute force attack tries all possible key combinations to decrypt data.",
    "What is a dictionary attack?": "A dictionary attack tries common passwords to guess credentials.",
    "What is a man-in-the-middle attack?": "A MITM attack intercepts and alters communication between two parties.",
    "What is side-channel attack?": "A side-channel attack exploits physical properties of a system to gain information.",
    "What is quantum cryptography?": "Quantum cryptography uses quantum mechanics to secure communication.",
    "What is forward secrecy?": "Forward secrecy ensures that past communications remain secure even if encryption keys are compromised.",
    "What is homomorphic encryption?": "Homomorphic encryption allows computation on encrypted data without decrypting it.",
    "What is zero-knowledge proof?": "A zero-knowledge proof allows one party to prove knowledge of information without revealing it.",
    "What is blockchain cryptography?": "Blockchain cryptography secures transactions using cryptographic hashing and digital signatures.",

    # Miscellaneous
    "What is steganography?": "Steganography hides messages within other data, such as images or audio files.",
    "What is the difference between encoding and encryption?": "Encoding is for data representation, while encryption is for security.",
    "What is the future of cryptography?": "Post-quantum cryptography is being developed to resist quantum computing threats.",
    "Why is cryptography important?": "Cryptography protects sensitive information from unauthorized access and cyber threats.",

    # Introduction to Game Development
    "What is game development?": "Game development is the process of designing, creating, and programming video games.",
    "What are the main stages of game development?": "The main stages are concept, design, development, testing, and release.",
    "What programming languages are commonly used in game development?": "Common languages include Python, C++, C#, and Java.",
    "What is a game engine?": "A game engine is software that provides tools for game development, such as graphics rendering and physics.",
    "What are examples of popular game engines?": "Examples include Unity, Unreal Engine, and Godot.",
    "What is Pygame?": "Pygame is a Python library for game development that provides tools for graphics, sound, and input handling.",
    "Why is Python used for game development?": "Python is easy to learn and has libraries like Pygame for simple game creation.",
    "What are the main components of a game?": "Components include graphics, physics, input handling, AI, and sound.",
    "What is a game loop?": "A game loop continuously updates the game state and renders graphics to keep the game running.",
    "Why is the game loop important?": "The game loop ensures smooth gameplay by updating and rendering frames continuously.",

    # Getting Started with Pygame
    "How do you install Pygame?": "Use the command `pip install pygame` in a terminal or command prompt.",
    "How do you initialize Pygame?": "Use `pygame.init()` to initialize all Pygame modules before using them.",
    "How do you create a Pygame window?": "Use `pygame.display.set_mode((width, height))` to create a game window.",
    "What is the purpose of `pygame.display.flip()`?": "It updates the entire game window with the latest frame.",
    "What does `pygame.time.Clock()` do?": "It helps control the game's frame rate to maintain smooth performance.",
    "How do you set a frame rate in Pygame?": "Use `clock.tick(FPS)` inside the game loop to limit frames per second.",
    "How do you handle events in Pygame?": "Use `pygame.event.get()` to capture and process player inputs and events.",
    "How do you detect key presses in Pygame?": "Use `pygame.KEYDOWN` and `pygame.KEYUP` events to detect key presses.",
    "How do you load an image in Pygame?": "Use `pygame.image.load('filename.png')` to load an image.",
    "How do you display an image in Pygame?": "Use `screen.blit(image, (x, y))` to draw an image on the screen.",

    # Drawing and Graphics
    "How do you fill the screen with color in Pygame?": "Use `screen.fill((R, G, B))` to fill the window with a color.",
    "How do you draw a rectangle in Pygame?": "Use `pygame.draw.rect(screen, color, (x, y, width, height))`.",
    "How do you draw a circle in Pygame?": "Use `pygame.draw.circle(screen, color, (x, y), radius)`.",
    "What is a sprite in game development?": "A sprite is a 2D image or animation representing a character or object in a game.",
    "How do you create a sprite in Pygame?": "Use `pygame.sprite.Sprite` to create and manage sprites.",
    "How do you move a sprite in Pygame?": "Update its position in the game loop using `sprite.rect.x += speed`.",
    "What is collision detection?": "Collision detection checks if two objects in a game are touching.",
    "How do you detect collisions in Pygame?": "Use `pygame.sprite.collide_rect(sprite1, sprite2)` to check if two sprites collide.",
    "What is alpha transparency in Pygame?": "Alpha transparency allows images to have transparent parts for smoother blending.",
    "How do you rotate an image in Pygame?": "Use `pygame.transform.rotate(image, angle)` to rotate an image.",

    # Handling User Input
    "How do you detect mouse clicks in Pygame?": "Use `pygame.MOUSEBUTTONDOWN` to check if a mouse button is clicked.",
    "How do you get the mouse position in Pygame?": "Use `pygame.mouse.get_pos()` to get the current mouse coordinates.",
    "How do you handle keyboard input in Pygame?": "Use `pygame.KEYDOWN` events to detect key presses.",
    "How do you quit a Pygame program?": "Detect `pygame.QUIT` and use `pygame.quit()` to close the game window.",
    "How do you add sound effects in Pygame?": "Use `pygame.mixer.Sound('sound.wav')` to load a sound effect.",
    "How do you play background music in Pygame?": "Use `pygame.mixer.music.load('music.mp3')` and `pygame.mixer.music.play(-1)`.",
    "How do you stop background music in Pygame?": "Use `pygame.mixer.music.stop()` to stop playing music.",
    "What is an event queue in Pygame?": "The event queue stores user inputs like key presses and mouse clicks.",
    "How do you detect if a key is held down in Pygame?": "Use `pygame.key.get_pressed()` to check if a key is being held.",
    "What is `pygame.event.poll()` used for?": "It checks for the next event in the event queue without removing it.",

    # Game Physics and AI
    "What is game physics?": "Game physics simulates real-world forces like gravity and collisions.",
    "How do you add gravity in Pygame?": "Increase an object's downward velocity over time to simulate gravity.",
    "What is AI in game development?": "AI controls non-player characters (NPCs) to make them act intelligently.",
    "What is pathfinding in AI?": "Pathfinding helps NPCs find the shortest path to a target in a game.",
    "What is the A* algorithm?": "A* is a common pathfinding algorithm used in games to navigate environments.",
    "How do you implement AI enemies in Pygame?": "Create enemy sprites that move, detect collisions, and respond to the player.",
    "How do you implement physics in Pygame?": "Use velocity and acceleration variables to move and animate objects.",
    "What is collision response?": "Collision response determines what happens after two objects collide.",
    "How do you simulate jumping in Pygame?": "Apply an upward force to a character and gradually reduce it to simulate gravity.",
    "How do you create a platformer in Pygame?": "Use gravity, collision detection, and player controls to create movement on platforms.",

    # Advanced Game Development
    "How do you create animations in Pygame?": "Use sprite sheets and update images over time to create animations.",
    "What is a game state?": "A game state manages different phases of the game, such as menus and gameplay.",
    "What is procedural generation?": "Procedural generation creates game content dynamically, like random terrain.",
    "How do you optimize a Pygame game?": "Reduce unnecessary calculations, optimize images, and use efficient loops.",
    "What is a game HUD?": "A Heads-Up Display (HUD) shows game information like health and score.",
    "What is a game engine loop?": "A loop that continuously updates and renders the game.",
    "What is a save system in games?": "A system that stores player progress so they can resume later.",
    "How do you export a Pygame game?": "Use `pyinstaller` to package the game into an executable file.",
    "How do you add multiplayer to a game?": "Use networking libraries like `socket` or Pygame's networking features.",
    "How do you publish a Pygame game?": "Package the game and distribute it via platforms like itch.io or Steam.",

    # Introduction to Image Processing
    "What is image processing?": "Image processing involves manipulating or analyzing images to improve or extract information.",
    "What is Pillow in Python?": "Pillow is a Python library for opening, manipulating, and saving images in different formats.",
    "How do you install Pillow?": "Use the command `pip install Pillow` to install the library.",
    "What image formats does Pillow support?": "Pillow supports formats like JPEG, PNG, BMP, GIF, and TIFF.",
    "How do you open an image in Pillow?": "Use `Image.open('image.jpg')` to load an image.",
    "How do you display an image using Pillow?": "Use `image.show()` to open the image with the default image viewer.",
    "How do you get the size of an image in Pillow?": "Use `image.size` to get the (width, height) of an image.",
    "How do you get the format of an image in Pillow?": "Use `image.format` to check the image format.",
    "How do you save an image in a different format?": "Use `image.save('new_image.png')` to save an image in a new format.",
    "How do you convert an image to grayscale in Pillow?": "Use `image.convert('L')` to convert an image to grayscale.",

    # Image Manipulation Basics
    "How do you resize an image using Pillow?": "Use `image.resize((new_width, new_height))`.",
    "How do you crop an image using Pillow?": "Use `image.crop((left, upper, right, lower))` to extract a region.",
    "How do you rotate an image using Pillow?": "Use `image.rotate(degrees)` to rotate an image.",
    "How do you flip an image horizontally?": "Use `image.transpose(Image.FLIP_LEFT_RIGHT)`.",
    "How do you flip an image vertically?": "Use `image.transpose(Image.FLIP_TOP_BOTTOM)`.",
    "How do you create a thumbnail of an image?": "Use `image.thumbnail((width, height))` to resize while maintaining aspect ratio.",
    "How do you draw on an image using Pillow?": "Use `ImageDraw` from Pillow to draw shapes or text.",
    "How do you add text to an image in Pillow?": "Use `ImageDraw.text((x, y), 'Text', fill=color, font=font)`.",
    "How do you change the color mode of an image?": "Use `image.convert('RGB')` or `image.convert('CMYK')`.",
    "How do you get pixel values from an image?": "Use `image.getpixel((x, y))` to retrieve a pixel's RGB values.",

    # Advanced Image Processing
    "How do you paste one image onto another in Pillow?": "Use `image.paste(image2, (x, y))`.",
    "How do you blend two images in Pillow?": "Use `Image.blend(image1, image2, alpha)` for transparency blending.",
    "How do you apply a Gaussian blur to an image?": "Use `image.filter(ImageFilter.GaussianBlur(radius))`.",
    "How do you apply a sharpen filter to an image?": "Use `image.filter(ImageFilter.SHARPEN)`.",
    "How do you apply an edge enhancement filter?": "Use `image.filter(ImageFilter.EDGE_ENHANCE)`.",
    "How do you apply a contour filter?": "Use `image.filter(ImageFilter.CONTOUR)`.",
    "What is an alpha channel in images?": "An alpha channel controls transparency in an image.",
    "How do you split an image into its RGB channels?": "Use `r, g, b = image.split()`.",
    "How do you merge RGB channels back into an image?": "Use `Image.merge('RGB', (r, g, b))`.",
    "How do you adjust image brightness?": "Use `ImageEnhance.Brightness(image).enhance(factor)`.",

    # Image File Handling
    "How do you check if an image file exists?": "Use `os.path.exists('image.jpg')` to check if a file exists.",
    "How do you delete an image file in Python?": "Use `os.remove('image.jpg')` to delete an image file.",
    "How do you get a list of image files in a folder?": "Use `glob.glob('*.jpg')` to list all JPG files.",
    "How do you open multiple images in Pillow?": "Use a loop with `Image.open()` to open multiple files.",
    "How do you extract EXIF metadata from an image?": "Use `image._getexif()` to retrieve metadata like camera settings.",
    "How do you compress an image using Pillow?": "Use `image.save('compressed.jpg', quality=50)` to reduce file size.",
    "How do you convert an image to black and white?": "Use `image.convert('1')` to create a binary image.",
    "How do you check if an image is in RGB mode?": "Use `image.mode` to check the current color mode.",
    "How do you add a watermark to an image?": "Overlay a transparent image or text using `paste()`.",
    "How do you convert an image to a NumPy array?": "Use `np.array(image)` to convert an image for further processing.",

    # Working with Animated GIFs
    "How do you load an animated GIF in Pillow?": "Use `image = Image.open('animation.gif')`.",
    "How do you get the number of frames in a GIF?": "Use `image.n_frames` to check the number of frames.",
    "How do you extract frames from a GIF?": "Use `image.seek(frame_number)` to navigate through frames.",
    "How do you create a GIF from multiple images?": "Use `image.save('output.gif', save_all=True, append_images=[...])`.",
    "How do you loop a GIF animation?": "Set `loop=0` when saving the GIF.",
    "How do you control the speed of a GIF?": "Adjust the `duration` parameter in `save()`.",
    "How do you resize all frames of a GIF?": "Loop through frames and apply `resize()` to each.",
    "How do you add transparency to a GIF?": "Use `convert('RGBA')` and modify the alpha channel.",
    "How do you save an animated GIF with compression?": "Use `optimize=True` in `save()` to reduce file size.",
    "How do you extract text from an image?": "Use `pytesseract.image_to_string(image)` from Tesseract OCR.",

    # Combining Pillow with Other Libraries
    "How do you integrate Pillow with NumPy?": "Convert images using `np.array(image)` and `Image.fromarray(array)`.",
    "How do you use OpenCV with Pillow?": "Convert images between Pillow and OpenCV using `cv2.cvtColor()`.",
    "How do you apply custom filters using NumPy?": "Modify pixel values in a NumPy array and convert back to an image.",
    "How do you use Matplotlib to display Pillow images?": "Use `plt.imshow(image)` from Matplotlib.",
    "How do you combine Pillow with Tkinter?": "Use `ImageTk.PhotoImage(image)` for GUI applications.",
    "How do you integrate Pillow with Flask?": "Use `request.files['file']` to upload and process images in Flask.",
    "How do you detect faces in an image?": "Use OpenCV’s `cv2.CascadeClassifier` on a Pillow image.",
    "How do you apply a mask to an image?": "Use `image.putalpha(mask)` to apply an alpha mask.",
    "How do you generate QR codes using Pillow?": "Use `qrcode.make('text')` to generate QR codes.",
    "How do you create a meme generator with Pillow?": "Overlay text on an image using `ImageDraw.text()`.",

    # Final Concepts
    "How do you create a transparent image?": "Use `Image.new('RGBA', size, (0, 0, 0, 0))`.",
    "How do you generate an image from scratch?": "Use `Image.new('RGB', (width, height), color)`.",
    "What is dithering in image processing?": "Dithering reduces color depth while maintaining image quality.",
    "What is anti-aliasing in images?": "Anti-aliasing smooths edges by blending colors.",
    "How do you create pixel art with Pillow?": "Resize a small image with `NEAREST` interpolation to create pixelated art.",
    "How do you generate a gradient image?": "Loop through pixels and set colors based on position.",

    # Introduction to PyAudio
    "What is PyAudio?": "PyAudio is a Python library that provides bindings for PortAudio, allowing audio recording and playback.",
    "How do you install PyAudio?": "Use `pip install pyaudio`. On Windows, you may need precompiled binaries.",
    "What is PortAudio?": "PortAudio is a cross-platform audio library used by PyAudio for handling audio streams.",
    "What are the key features of PyAudio?": "PyAudio supports real-time audio streaming, reading and writing audio files, and interacting with audio devices.",
    "How do you check if PyAudio is installed correctly?": "Run `import pyaudio` in Python. If there are no errors, it is installed correctly.",
    
    # Recording Audio with PyAudio
    "How do you record audio with PyAudio?": "Open an input stream and use `stream.read(CHUNK)` to capture audio frames.",
    "How do you save recorded audio to a file?": "Use the `wave` module to write the recorded frames to a `.wav` file.",
    "What is the recommended buffer size for recording?": "A buffer size of 1024 or 2048 samples is commonly used.",
    "How do you stop a recording in PyAudio?": "Use `stream.stop_stream()` and `stream.close()`.",
    "How do you record audio for a fixed duration?": "Use a loop to capture frames for `DURATION * RATE / CHUNK` iterations.",
    
    # Playing Audio with PyAudio
    "How do you play an audio file using PyAudio?": "Open an output stream and write frames using `stream.write()`.",
    "How do you play a WAV file in Python?": "Use the `wave` module to read the file and `pyaudio` to play it.",
    "Can PyAudio play MP3 files?": "No, PyAudio only supports WAV. Use `pydub` or `ffmpeg` to convert MP3 to WAV.",
    "How do you adjust playback speed?": "Resample the audio using `scipy.signal.resample()`.",
    "How do you loop an audio file in PyAudio?": "Read the file and replay the frames in a loop.",
    
    # Audio File Manipulation
    "How do you convert an MP3 file to WAV in Python?": "Use `pydub` with `AudioSegment.from_mp3('file.mp3').export('file.wav', format='wav')`.",
    "How do you extract metadata from an audio file?": "Use `mutagen` or `pydub` to read metadata like artist, title, and duration.",
    "How do you change the sample rate of an audio file?": "Use `librosa.resample(y, orig_sr, target_sr)` to change the sample rate.",
    "How do you trim an audio file?": "Use `pydub` with `audio[start_time:end_time]` to extract a segment.",
    "How do you merge multiple audio files?": "Use `pydub` with `combined = audio1 + audio2` to concatenate audio files.",
    
    
    "How do you stream live audio from a microphone?": "Open an input stream and continuously read frames using `stream.read()`.",
    "How do you apply real-time audio processing?": "Capture audio with PyAudio, process it using `numpy` or `scipy`, and play it back.",
    "How do you detect silence in an audio stream?": "Analyze the amplitude of the waveform using `numpy` or `scipy.signal`.",
    "How do you visualize an audio waveform in Python?": "Use `matplotlib` with `plt.plot(audio_data)` to plot the waveform.",
    "How do you perform speech recognition on an audio file?": "Use `speech_recognition` library with `recognizer.recognize_google(audio)`.",
      "How to print 'Hello, World!' in Python?": "print('Hello, World!')",
    "How to declare a variable in Python?": "x = 10\ny = 'Hello'\nprint(x, y)",
    "How to use an if statement in Python?": "x = 5\nif x > 0:\n    print('Positive number')",
    "How to use a for loop in Python?": "for i in range(5):\n    print(i)",
    "How to define a function in Python?": "def greet(name):\n    return 'Hello ' + name\nprint(greet('Alice'))",
    "How to create a list in Python?": "fruits = ['apple', 'banana', 'cherry']\nprint(fruits)",
    "How to create a tuple in Python?": "numbers = (1, 2, 3, 4)\nprint(numbers)",
    "How to create a dictionary in Python?": "student = {'name': 'John', 'age': 20}\nprint(student)",
    "How to create a set in Python?": "unique_numbers = {1, 2, 3, 4, 4, 2}\nprint(unique_numbers)",
    "How to manipulate strings in Python?": "text = 'Hello, Python'\nprint(text.upper())",
    "How to check if a number is even or odd?": "x = 10\nif x % 2 == 0:\n    print('Even')\nelse:\n    print('Odd')",
    "How to find the factorial of a number using recursion?": "def factorial(n):\n    return 1 if n == 0 else n * factorial(n-1)\nprint(factorial(5))",
    "How to reverse a list in Python?": "numbers = [1, 2, 3, 4]\nnumbers.reverse()\nprint(numbers)",
    "How to sort a list in Python?": "numbers = [4, 2, 8, 1]\nnumbers.sort()\nprint(numbers)",
    "How to merge two dictionaries in Python?": "dict1 = {'a': 1, 'b': 2}\ndict2 = {'c': 3, 'd': 4}\nmerged_dict = {**dict1, **dict2}\nprint(merged_dict)",
    "How to iterate over a dictionary?": "student = {'name': 'Alice', 'age': 25}\nfor key, value in student.items():\n    print(key, value)",
    "How to remove an item from a dictionary?": "student = {'name': 'Alice', 'age': 25}\ndel student['age']\nprint(student)",
    "How to convert a string to a list?": "text = 'hello'\nchar_list = list(text)\nprint(char_list)",
    "How to check if a key exists in a dictionary?": "student = {'name': 'Alice', 'age': 25}\nif 'name' in student:\n    print('Key exists')",
    "How to find the length of a list?": "numbers = [1, 2, 3, 4]\nprint(len(numbers))",
    "How to append an item to a list?": "numbers = [1, 2, 3]\nnumbers.append(4)\nprint(numbers)",
    "How to remove duplicates from a list?": "numbers = [1, 2, 2, 3, 4, 4]\nunique_numbers = list(set(numbers))\nprint(unique_numbers)",
    "How to convert a tuple to a list?": "numbers = (1, 2, 3)\nnumber_list = list(numbers)\nprint(number_list)",
    "How to find the maximum value in a list?": "numbers = [1, 5, 3, 9]\nprint(max(numbers))",
    "How to concatenate two lists?": "list1 = [1, 2, 3]\nlist2 = [4, 5, 6]\nmerged_list = list1 + list2\nprint(merged_list)",
    "How to swap two variables in Python?": "a, b = 5, 10\na, b = b, a\nprint(a, b)",
    "How to check if a string contains a substring?": "text = 'Hello, Python'\nif 'Python' in text:\n    print('Substring found')",
    "How to find the index of an element in a list?": "numbers = [10, 20, 30]\nprint(numbers.index(20))",
    "How to use a while loop in Python?": "x = 5\nwhile x > 0:\n    print(x)\n    x -= 1",
    "Hello World": "print('Hello, World!')",
    "Variables and Data Types": "x = 10\ny = 3.14\nz = 'Hello'",
    "Conditional Statements": "if x > 5:\n    print('x is greater than 5')\nelse:\n    print('x is 5 or less')",
    "Loops": "for i in range(5):\n    print(i)\n\nwhile x > 0:\n    print(x)\n    x -= 1",
    "Functions": "def greet(name):\n    return f'Hello, {name}'\n\nprint(greet('Alice'))",
    "Lists": "my_list = [1, 2, 3, 4]\nmy_list.append(5)\nprint(my_list)",
    "Tuples": "my_tuple = (1, 2, 3)\nprint(my_tuple[1])",
    "Dictionaries": "my_dict = {'name': 'Alice', 'age': 25}\nprint(my_dict['name'])",
    "Sets": "my_set = {1, 2, 3}\nmy_set.add(4)\nprint(my_set)",
    "Strings": "my_string = 'Hello'\nprint(my_string.upper())",
    "Async/Await": "import asyncio\nasync def main():\n    print('Hello')\n    await asyncio.sleep(1)\n    print('World')\nasyncio.run(main())",
    "Web Development with Flask": "from flask import Flask\napp = Flask(__name__)\n@app.route('/')\ndef home():\n    return 'Hello, Flask!'\nif __name__ == '__main__':\n    app.run(debug=True)",
    "Web Development with Django": "# Install Django: pip install django\n# Create project: django-admin startproject mysite",
    "Data Science with Pandas": "import pandas as pd\ndf = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})\nprint(df.head())",
    "Data Science with NumPy": "import numpy as np\na = np.array([1, 2, 3])\nprint(np.mean(a))",
    "Machine Learning with Scikit-learn": "from sklearn.linear_model import LinearRegression\nmodel = LinearRegression()\nX = [[1], [2], [3]]\ny = [2, 4, 6]\nmodel.fit(X, y)\nprint(model.predict([[4]]))",
    "Deep Learning with TensorFlow": "import tensorflow as tf\nmodel = tf.keras.models.Sequential([tf.keras.layers.Dense(1)])\nmodel.compile(optimizer='sgd', loss='mse')",
    "Natural Language Processing (NLP)": "from nltk.tokenize import word_tokenize\ntext = 'Hello, how are you?'\nprint(word_tokenize(text))",
    "Computer Vision": "import cv2\nimg = cv2.imread('image.jpg')\ngray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)\ncv2.imshow('Gray', gray)\ncv2.waitKey(0)",
    "Robotics": "from gpiozero import Robot\nrobot = Robot(left=(4, 14), right=(17, 18))\nrobot.forward()",
        "Async/Await": """
import asyncio

async def main():
    print('Hello')
    await asyncio.sleep(1)
    print('World')

asyncio.run(main())
    """,
    "Web Development with Flask": """
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
    """,
    "Web Development with Django": """
# Install Django using 'pip install django'
# Create a project: django-admin startproject myproject
# Run the development server: python manage.py runserver
    """,
    "Data Science with Pandas": """
import pandas as pd

data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
df = pd.DataFrame(data)
print(df)
    """,
    "Data Science with NumPy": """
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])
print(np.mean(arr, axis=0))
    """,
    "Machine Learning with Scikit-learn": """
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

model = LinearRegression()
model.fit(X, y)
print(model.predict([[6]]))
    """,
    "Deep Learning with TensorFlow": """
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mse')
    """,
    "Natural Language Processing (NLP)": """
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')
text = "Natural Language Processing with Python."
print(word_tokenize(text))
    """,
    "Computer Vision": """
import cv2

img = cv2.imread('image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray Image', gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
    """,
    "Robotics": """
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        hello_str = "Hello Robot!"
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
    """,
      "Async/Await in Python": """
import asyncio

async def say_hello():
    await asyncio.sleep(1)
    print("Hello, Async World!")

asyncio.run(say_hello())
    """,
    "Web Development with Flask": """
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
    """,
    "Web Development with Django": """
# Install Django and run the following commands
# django-admin startproject myproject
# cd myproject
# python manage.py runserver
    """,
    "Data Science with Pandas": """
import pandas as pd

data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
df = pd.DataFrame(data)
print(df.head())
    """,
    "Data Science with NumPy": """
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])
print(np.mean(arr, axis=0))
    """,
    "Machine Learning with Scikit-learn": """
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1], [2], [3], [4]])
y = np.array([2, 4, 6, 8])
model = LinearRegression().fit(X, y)
print(model.predict([[5]]))
    """,
    "Deep Learning with TensorFlow": """
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(1)
])
model.compile(optimizer='adam', loss='mse')
print(model.summary())
    """,
    "Natural Language Processing (NLP)": """
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

text = "Natural Language Processing is amazing!"
print(word_tokenize(text))
    """,
    "Computer Vision with OpenCV": """
import cv2

img = cv2.imread('image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Grayscale Image', gray)
cv2.waitKey(0)
    """,
    "Robotics with ROS": """
# Install ROS and create a package
# roslaunch my_robot world.launch
    """,
    "What is an array?": "An array is a data structure that stores elements of the same type in contiguous memory locations.",
    "How to declare an array in Python?": "In Python, you can declare an array using the array module: `from array import array; arr = array('i', [1, 2, 3])`.",
    "How to declare an array in C?": "In C, you can declare an array as `int arr[] = {1, 2, 3, 4};`.",
    "How to declare an array in Java?": "In Java, you can declare an array as `int[] arr = {1, 2, 3, 4};`.",
    "How to access elements in an array?": "You can access elements using indexing, e.g., `arr[0]` in Python.",
    "How to modify elements in an array?": "Modify an element by assigning a new value, e.g., `arr[1] = 50` in Python.",
    "How to find the length of an array?": "Use `len(arr)` in Python to get the number of elements in an array.",
    "How to loop through an array?": "Use a for-loop, e.g., `for i in arr: print(i)` in Python.",
    "How to sort an array?": "Use `arr.sort()` in Python or `Arrays.sort(arr)` in Java.",
    "How to search for an element in an array?": "Use `element in arr` in Python or a loop to search manually.",
    "What is a 2D array?": "A 2D array is an array of arrays, used for matrix representation.",
    "How to create a 2D array in Python?": "Use nested lists, e.g., `arr = [[1, 2], [3, 4]]`.",
    "How to traverse a 2D array?": "Use nested loops, e.g., `for row in arr: for elem in row: print(elem)`.",
    "How to reverse an array?": "Use `arr[::-1]` in Python or `reverse()` method.",
    "How to rotate an array?": "Use slicing in Python, e.g., `arr = arr[-k:] + arr[:-k]`.",
    "How to remove duplicates from an array?": "Convert to a set and back to a list: `arr = list(set(arr))`.",
    "How to merge two arrays?": "Use `+` operator in Python or `extend()` method.",
    "What is an associative array?": "An associative array is a dictionary-like structure that maps keys to values.",
    "How to check if an array is empty?": "Use `if not arr:` in Python.",
    "How to copy an array?": "Use `arr.copy()` or `arr[:]` in Python.",
    "How to remove an element from an array?": "Use `arr.remove(value)` or `del arr[index]` in Python.",
    "What is a dynamic array?": "A dynamic array can resize itself automatically, like Python’s list.",
    "How to create a dynamic array in Python?": "Use `list` instead of `array` module.",
    "What is a jagged array?": "A jagged array is an array of arrays where each row can have a different length.",
    "How to check if an element exists in an array?": "Use `if value in arr:` in Python.",
    "How to convert an array to a string?": "Use `''.join(arr)` for character arrays in Python.",
    "How to convert a string to an array?": "Use `list(string)` in Python.",
    "What is a sparse array?": "A sparse array is an array where most elements are zero or empty.",
    "How to initialize an array with default values?": "Use list comprehension, e.g., `[0] * 10` in Python.",
    "How to insert an element at a specific position?": "Use `arr.insert(index, value)` in Python.",
    "What is a circular array?": "A circular array wraps around when accessing elements beyond its length.",
    "How to implement a circular array?": "Use `arr[index % len(arr)]` for circular indexing.",
    "How to split an array?": "Use slicing, e.g., `arr[:mid]` and `arr[mid:]`.",
    "How to concatenate two arrays?": "Use `+` in Python, e.g., `arr1 + arr2`.",
    "How to remove the last element from an array?": "Use `arr.pop()` in Python.",
    "How to remove the first element from an array?": "Use `arr.pop(0)` in Python.",
    "How to clear an array?": "Use `arr.clear()` in Python.",
    "What is a bit array?": "A bit array is an array that stores bits compactly.",
    "How to shuffle an array?": "Use `random.shuffle(arr)` in Python.",
    "What is an immutable array?": "An immutable array cannot be changed after creation, like a tuple.",
    "How to implement an immutable array?": "Use tuples instead of lists in Python.",
    "How to find the max element in an array?": "Use `max(arr)` in Python.",
    "How to find the min element in an array?": "Use `min(arr)` in Python.",
    "How to find the sum of elements in an array?": "Use `sum(arr)` in Python.",
    "How to find the average of an array?": "Use `sum(arr) / len(arr)` in Python.",
    "What is an array index out of bounds error?": "It occurs when accessing an index beyond the array size.",
    "How to avoid array index out of bounds?": "Check `index < len(arr)` before accessing elements.",
    "What is a multi-dimensional array?": "An array with more than one dimension, like 2D or 3D arrays.",
    "How to flatten a multi-dimensional array?": "Use `numpy.flatten()` or list comprehension.",
    "How to slice an array?": "Use `arr[start:end:step]` in Python.",
    "How to find unique elements in an array?": "Use `set(arr)` in Python.",
    "How to get the frequency of elements?": "Use `collections.Counter(arr)` in Python.",
    "How to find the median of an array?": "Use `statistics.median(arr)` in Python.",
    "How to implement a stack using an array?": "Use `append()` for push and `pop()` for pop in Python.",
    "How to implement a queue using an array?": "Use `append()` for enqueue and `pop(0)` for dequeue in Python.",
    "How to implement a priority queue using an array?": "Use `heapq` module in Python.",
    "How to generate a random array?": "Use `random.sample(range(1, 100), 10)` in Python.",
    "How to find the second largest element in an array?": "Use `sorted(arr)[-2]` in Python.",
    "What is an XOR array trick?": "XOR is used for finding missing elements in number sequences.",
    "How to remove all occurrences of a value?": "Use `arr = [x for x in arr if x != value]`.",
    "What is a permutation of an array?": "A permutation is a reordering of array elements.",
    "How to generate all permutations of an array?": "Use `itertools.permutations(arr)` in Python.",
    "How to check if an array is sorted?": "Compare `arr` with `sorted(arr)`.",
    "How to get the first N elements of an array?": "Use `arr[:N]` in Python.",
    "What is a difference array?": "A difference array is used to perform range updates efficiently.",
    "What is a Fenwick Tree (Binary Indexed Tree)?": "A data structure for fast prefix sum queries.",
    "What is a segment tree?": "A tree data structure for range queries and updates.",
    "Difference between list and tuple?": "Lists are mutable, whereas tuples are immutable. Lists use square brackets [], while tuples use parentheses ().",
    "Difference between set and list?": "Sets are unordered and contain unique elements, while lists are ordered and can contain duplicates.",
    "Difference between dictionary and list?": "Dictionaries store key-value pairs, while lists store elements in a sequence.",
    "Difference between Python 2 and Python 3?": "Python 3 supports Unicode by default, has print() as a function, and uses `//` for floor division.",
    "Difference between deep copy and shallow copy?": "A shallow copy creates references to the original object, while a deep copy creates a new independent object.",
    "Difference between is and ==?": "`is` checks object identity, while `==` checks value equality.",
    "Difference between append() and extend()?": "`append()` adds a single element, whereas `extend()` adds multiple elements from an iterable.",
    "Difference between remove() and pop()?": "`remove(value)` deletes a specific value, while `pop(index)` removes an element at a given index.",
    "Difference between sort() and sorted()?": "`sort()` modifies the list in place, while `sorted()` returns a new sorted list.",
    "Difference between del and remove()?": "`del` deletes by index or slices, while `remove()` removes by value.",
    "Difference between None and False?": "`None` represents the absence of a value, while `False` is a boolean value.",
    "Difference between break and continue?": "`break` exits the loop, while `continue` skips the current iteration.",
    "Difference between pass and continue?": "`pass` does nothing and moves to the next statement, while `continue` skips to the next iteration.",
    "Difference between global and nonlocal?": "`global` is used to modify a global variable inside a function, while `nonlocal` modifies a variable in the nearest enclosing scope.",
    "Difference between return and yield?": "`return` ends the function and returns a value, while `yield` returns a generator that can be iterated.",
    "Difference between args and kwargs?": "`*args` collects positional arguments, while `**kwargs` collects keyword arguments.",
    "Difference between class and instance variables?": "Class variables are shared across all instances, while instance variables are specific to each object.",
    "Difference between static method and class method?": "Static methods don’t use `self` or `cls`, while class methods operate on the class level using `cls`.",
    "Difference between instance method and class method?": "Instance methods use `self` and operate on instances, while class methods use `cls` and operate on the class itself.",
    "Difference between mutable and immutable types?": "Mutable types can be changed after creation (lists, dictionaries), while immutable types cannot (tuples, strings).",
    "Difference between Python and Java?": "Python is dynamically typed and interpreted, while Java is statically typed and compiled.",
    "Difference between list comprehension and map()?": "List comprehension is more readable, while `map()` is faster for large data sets.",
    "Difference between filter() and map()?": "`filter()` removes elements based on a condition, while `map()` applies a function to each element.",
    "Difference between range() and xrange()?": "`xrange()` existed in Python 2 and was memory efficient, while `range()` in Python 3 behaves like `xrange()`.",
    "Difference between == and is not?": "`==` checks for equality, while `is not` checks for object identity.",
    "Difference between input() and raw_input()?": "`raw_input()` existed in Python 2, whereas `input()` in Python 3 behaves like `raw_input()` in Python 2.",
    "Difference between HashMap and Dictionary?": "Python’s dictionary is implemented as a HashMap but provides additional features.",
    "Difference between Python and JavaScript?": "Python is a general-purpose language, while JavaScript is mainly used for web development.",
    "Difference between compile-time and runtime errors?": "Compile-time errors occur before execution, while runtime errors occur during execution.",
    "Difference between functional and object-oriented programming?": "Functional programming focuses on pure functions, while OOP focuses on objects and classes.",
    "Difference between import and from-import?": "`import module` imports the whole module, while `from module import x` imports only `x`.",
    "Difference between shallow and deep copy in dictionary?": "A shallow copy copies references, while a deep copy creates a new independent dictionary.",
    "Difference between NumPy array and Python list?": "NumPy arrays are faster and support vectorized operations, while lists do not.",
    "Difference between NumPy and Pandas?": "NumPy is used for numerical operations, while Pandas is used for data manipulation and analysis.",
    "Difference between Pandas DataFrame and Series?": "A Series is a single column, while a DataFrame is a 2D table.",
    "Difference between JSON and pickle?": "JSON is human-readable and cross-platform, while pickle is Python-specific and faster.",
    "Difference between CSV and JSON?": "CSV is simple and human-readable, while JSON supports nested data structures.",
    "Difference between recursion and iteration?": "Recursion uses function calls, while iteration uses loops.",
    "Difference between while and for loop?": "`while` loops run until a condition is false, while `for` loops iterate over a sequence.",
    "Difference between finally and else in try-except?": "`finally` always executes, while `else` executes only if no exceptions occur.",
    "Difference between AssertionError and Exception?": "AssertionError occurs when `assert` fails, while Exception is a base class for all exceptions.",
    "Difference between open() and with open()?": "`with open()` ensures proper file closure, while `open()` requires explicit closure.",
    "Difference between TCP and UDP in Python?": "TCP is connection-oriented, while UDP is connectionless and faster.",
    "Difference between re.match() and re.search()?": "`match()` checks at the start of a string, while `search()` checks anywhere in the string.",
    "Difference between str() and repr()?": "`str()` is user-friendly, while `repr()` is developer-friendly and used for debugging.",
    "Difference between multiprocessing and threading?": "Multiprocessing creates separate processes, while threading runs in the same process.",
    "Difference between synchronous and asynchronous programming?": "Synchronous code runs sequentially, while asynchronous code allows tasks to run concurrently.",
    "Difference between LIFO and FIFO?": "LIFO (Last In, First Out) is used in stacks, while FIFO (First In, First Out) is used in queues.",
    "Difference between private and protected variables?": "Private variables are prefixed with `__`, while protected variables are prefixed with `_`.",
    "Difference between datetime and time modules?": "`datetime` handles both date and time, while `time` focuses on time-related functions.",
    "Difference between __str__ and __repr__?": "`__str__()` is used for user-friendly output, while `__repr__()` is used for debugging and logging.",
    "Difference between *args and **kwargs?": "`*args` handles positional arguments, while `**kwargs` handles keyword arguments.",
    "Difference between synchronized and non-synchronized collections in Python?": "Synchronized collections use locking mechanisms, while non-synchronized ones do not.",
    "Difference between @staticmethod and @classmethod?": "`@staticmethod` does not access class variables, while `@classmethod` does.",
    "Difference between method overloading and method overriding?": "Python does not support method overloading but supports method overriding in subclasses.",
    "What is a string in Python?": "A string is a sequence of characters enclosed in single, double, or triple quotes.",
    "How to create a string in Python?": "Strings can be created using single (' '), double (\" \"), or triple (''' ''' or \"\"\" \"\"\").",
    "How to access characters in a string?": "Characters in a string can be accessed using indexing, e.g., `s[0]` for the first character.",
    "How to slice a string in Python?": "Use slicing syntax `s[start:end:step]` to extract parts of a string.",
    "Difference between indexing and slicing?": "Indexing retrieves a single character, while slicing extracts a substring.",
    "How to find the length of a string?": "Use `len(string)` to get the number of characters in a string.",
    "How to check if a string contains a substring?": "Use `substring in string` to check for the presence of a substring.",
    "How to convert a string to uppercase?": "Use `string.upper()` to convert all characters to uppercase.",
    "How to convert a string to lowercase?": "Use `string.lower()` to convert all characters to lowercase.",
    "How to capitalize the first letter of a string?": "Use `string.capitalize()` to make the first letter uppercase.",
    "How to title-case a string?": "Use `string.title()` to capitalize the first letter of each word.",
    "How to swap case in a string?": "Use `string.swapcase()` to switch uppercase to lowercase and vice versa.",
    "How to check if a string starts with a specific substring?": "Use `string.startswith(substring)`.",
    "How to check if a string ends with a specific substring?": "Use `string.endswith(substring)`.",
    "How to replace a substring in a string?": "Use `string.replace(old, new)`.",
    "How to remove whitespace from a string?": "Use `string.strip()` to remove leading and trailing whitespace.",
    "How to remove only leading whitespace from a string?": "Use `string.lstrip()`.",
    "How to remove only trailing whitespace from a string?": "Use `string.rstrip()`.",
    "How to split a string into a list?": "Use `string.split(delimiter)`.",
    "How to join a list of strings into a single string?": "Use `'delimiter'.join(list)`.",
    "How to count occurrences of a substring?": "Use `string.count(substring)`.",
    "How to find the index of a substring?": "Use `string.find(substring)` or `string.index(substring)`.",
    "Difference between find() and index()?": "`find()` returns -1 if not found, while `index()` raises an error.",
    "How to check if a string is numeric?": "Use `string.isdigit()`.",
    "How to check if a string is alphabetic?": "Use `string.isalpha()`.",
    "How to check if a string is alphanumeric?": "Use `string.isalnum()`.",
    "How to check if a string is in uppercase?": "Use `string.isupper()`.",
    "How to check if a string is in lowercase?": "Use `string.islower()`.",
    "How to check if a string is a valid identifier?": "Use `string.isidentifier()`.",
    "How to format a string using f-strings?": "Use `f\"Hello, {name}!\"`.",
    "How to format a string using format()?": "Use `\"Hello, {}\".format(name)`.",
    "How to format a string using % operator?": "Use `\"Hello, %s\" % name`.",
    "Difference between f-string, format(), and % operator?": "F-strings are the fastest, `format()` is more flexible, `%` is older.",
    "How to escape characters in a string?": "Use a backslash `\\` before special characters.",
    "How to use raw strings in Python?": "Prefix with `r`, e.g., `r\"C:\\new_folder\\file.txt\"`.",
    "How to reverse a string?": "Use slicing `string[::-1]`.",
    "How to check if a string is palindrome?": "Compare the string with its reverse `string == string[::-1]`.",
    "How to remove digits from a string?": "Use `''.join(c for c in string if not c.isdigit())`.",
    "How to remove punctuation from a string?": "Use `string.translate(str.maketrans('', '', string.punctuation))`.",
    "How to concatenate strings?": "Use `+` operator or `join()`.",
    "How to repeat a string multiple times?": "Use `string * n`.",
    "How to convert a string to a list of characters?": "Use `list(string)`.",
    "How to encode a string?": "Use `string.encode(encoding)`.",
    "How to decode a byte string?": "Use `byte_string.decode(encoding)`.",
    "How to convert a string to a set of characters?": "Use `set(string)`.",
    "How to remove duplicate characters from a string?": "Use `''.join(set(string))`.",
    "How to check if a string contains only whitespace?": "Use `string.isspace()`.",
    "How to check if a string follows title case?": "Use `string.istitle()`.",
    "How to format a string to a fixed width?": "Use `string.ljust(width)`, `string.rjust(width)`, or `string.center(width)`.",
    "How to remove all vowels from a string?": "Use `''.join(c for c in string if c.lower() not in 'aeiou')`.",
    "How to extract digits from a string?": "Use `''.join(c for c in string if c.isdigit())`.",
    "How to extract alphabets from a string?": "Use `''.join(c for c in string if c.isalpha())`.",
    "How to extract words from a string?": "Use `re.findall(r'\b\w+\b', string)`.",
    "How to replace multiple spaces with a single space?": "Use `re.sub(r'\\s+', ' ', string)`.",
    "How to check if two strings are anagrams?": "Sort both and compare: `sorted(str1) == sorted(str2)`.",
    "How to find the most common character in a string?": "Use `collections.Counter(string).most_common(1)`.",
    "How to split a string at capital letters?": "Use `re.findall('[A-Z][^A-Z]*', string)`.",
    "How to check if a string is in CamelCase?": "Use `re.match(r'[A-Z][a-z]+(?:[A-Z][a-z]+)*', string)`.",
    "How to convert CamelCase to snake_case?": "Use `re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()`.",
    "How to convert snake_case to CamelCase?": "Use `''.join(word.title() for word in string.split('_'))`.",
    "How to remove special characters from a string?": "Use `re.sub(r'[^A-Za-z0-9]', '', string)`.",
    "How to count words in a string?": "Use `len(string.split())`.",
    "How to extract hashtags from a string?": "Use `re.findall(r'#\\w+', string)`.",
    "How to find all email addresses in a string?": "Use `re.findall(r'[\\w.]+@[\\w.]+', string)`.",
    "How to mask part of a string (e.g., credit card numbers)?": "Use `string[:-4] + '****'`.",
    "How to check if a string is a valid URL?": "Use `re.match(r'^https?://[\\w./]+$', string)`.",
    "How to count frequency of characters in a string?": "Use `collections.Counter(string)`.",

    "What are basic arithmetic operators in Python?": "Python supports + (addition), - (subtraction), * (multiplication), / (division), % (modulus), ** (exponentiation), and // (floor division).",
    "How to add two numbers in Python?": "Use the `+` operator, e.g., `a + b`.",
    "How to subtract two numbers in Python?": "Use the `-` operator, e.g., `a - b`.",
    "How to multiply two numbers in Python?": "Use the `*` operator, e.g., `a * b`.",
    "How to divide two numbers in Python?": "Use the `/` operator, e.g., `a / b`.",
    "What is floor division in Python?": "Floor division `//` returns the largest integer quotient, e.g., `7 // 2` results in `3`.",
    "What is modulus operator in Python?": "The `%` operator returns the remainder of division, e.g., `7 % 2` results in `1`.",
    "What is exponentiation in Python?": "Use `**` for power calculation, e.g., `2 ** 3` gives `8`.",
    "How to find the square of a number?": "Use `num ** 2` or `pow(num, 2)`.",
    "How to find the cube of a number?": "Use `num ** 3` or `pow(num, 3)`.",
    "How to calculate square root in Python?": "Use `math.sqrt(num)` or `num ** 0.5`.",
    "How to calculate cube root in Python?": "Use `num ** (1/3)`.",
    "How to find absolute value of a number?": "Use `abs(num)`.",
    "How to round a number in Python?": "Use `round(num, decimals)`, where `decimals` is optional.",
    "How to perform integer division in Python?": "Use `//` for floor division.",
    "How to check if a number is even?": "Use `num % 2 == 0`.",
    "How to check if a number is odd?": "Use `num % 2 != 0`.",
    "How to check if a number is positive?": "Use `num > 0`.",
    "How to check if a number is negative?": "Use `num < 0`.",
    "How to check if a number is zero?": "Use `num == 0`.",
    "How to calculate factorial of a number?": "Use `math.factorial(num)`.",
    "How to calculate logarithm of a number?": "Use `math.log(num)` for natural log, or `math.log10(num)` for base 10 log.",
    "How to find greatest common divisor (GCD)?": "Use `math.gcd(a, b)`.",
    "How to find least common multiple (LCM)?": "Use `math.lcm(a, b)` (Python 3.9+).",
    "How to convert degrees to radians?": "Use `math.radians(degrees)`.",
    "How to convert radians to degrees?": "Use `math.degrees(radians)`.",
    "How to calculate sine of an angle?": "Use `math.sin(angle_in_radians)`.",
    "How to calculate cosine of an angle?": "Use `math.cos(angle_in_radians)`.",
    "How to calculate tangent of an angle?": "Use `math.tan(angle_in_radians)`.",
    "How to calculate arc sine in Python?": "Use `math.asin(value)`.",
    "How to calculate arc cosine in Python?": "Use `math.acos(value)`.",
    "How to calculate arc tangent in Python?": "Use `math.atan(value)`.",
    "How to find maximum of two numbers?": "Use `max(a, b)`.",
    "How to find minimum of two numbers?": "Use `min(a, b)`.",
    "How to check if a number is a prime?": "Loop from `2` to `sqrt(n)` and check divisibility.",
    "How to generate a random number?": "Use `random.randint(a, b)` for integers, `random.uniform(a, b)` for floats.",
    "How to shuffle a list randomly?": "Use `random.shuffle(list)`.",
    "How to get a random choice from a list?": "Use `random.choice(list)`.",
    "How to generate a random float?": "Use `random.random()` for a value between `0` and `1`.",
    "How to calculate permutation in Python?": "Use `math.perm(n, r)` (Python 3.8+).",
    "How to calculate combination in Python?": "Use `math.comb(n, r)` (Python 3.8+).",
    "How to check if two numbers are equal?": "Use `a == b`.",
    "How to check if a number is greater than another?": "Use `a > b`.",
    "How to check if a number is less than another?": "Use `a < b`.",
    "How to check if a number is greater than or equal to another?": "Use `a >= b`.",
    "How to check if a number is less than or equal to another?": "Use `a <= b`.",
    "How to convert an integer to a float?": "Use `float(num)`.",
    "How to convert a float to an integer?": "Use `int(num)`.",
    "How to convert a string to an integer?": "Use `int(string)` if valid.",
    "How to convert a string to a float?": "Use `float(string)` if valid.",
    "How to check if a number is NaN (Not a Number)?": "Use `math.isnan(num)`.",
    "How to perform bitwise AND operation?": "Use `a & b`.",
    "How to perform bitwise OR operation?": "Use `a | b`.",
    "How to perform bitwise XOR operation?": "Use `a ^ b`.",
    "How to perform bitwise NOT operation?": "Use `~a`.",
    "How to perform left shift operation?": "Use `a << n`.",
    "How to perform right shift operation?": "Use `a >> n`.",
    "How to find the binary representation of a number?": "Use `bin(num)`.",
    "How to find the hexadecimal representation of a number?": "Use `hex(num)`.",
    "How to find the octal representation of a number?": "Use `oct(num)`.",
    "How to generate Fibonacci series in Python?": "Use a loop or recursion to calculate `F(n) = F(n-1) + F(n-2)`.",
    "How to check if a number is an Armstrong number?": "Sum of its digits raised to power `n` equals the number.",
    "How to convert Celsius to Fahrenheit?": "Use `F = (C * 9/5) + 32`.",
    "How to convert Fahrenheit to Celsius?": "Use `C = (F - 32) * 5/9`.",
    "How to find the sum of digits of a number?": "Use `sum(int(digit) for digit in str(num))`.",
    "How to count digits in a number?": "Use `len(str(num))` or `math.log10(num) + 1`.",
    "How to calculate the area of a circle?": "Use `math.pi * r**2`.",
    "How to calculate the area of a rectangle?": "Use `length * width`.",
    "How to calculate the area of a triangle?": "Use `0.5 * base * height`.",
    "How to calculate the perimeter of a square?": "Use `4 * side`.",
    "How to check if a number is divisible by another?": "Use `num % divisor == 0`.",
    "How to swap two numbers without using a third variable?": "Use `a, b = b, a`.",
    "How to solve a quadratic equation in Python?": "Use `(-b ± sqrt(b² - 4ac)) / 2a`.",
    "How to find the percentage of a number?": "Use `(part / total) * 100`.",
    "How to round up a number?": "Use `math.ceil(num)`.",
    "How to round down a number?": "Use `math.floor(num)`.",

    "What is indentation in Python?": "Indentation in Python refers to the spaces or tabs used at the beginning of a line to define code blocks.",
    "Why is indentation important in Python?": "Python uses indentation to determine the structure of the code, unlike other languages that use braces `{}`.",
    "How many spaces should be used for indentation in Python?": "The standard indentation in Python is 4 spaces.",
    "Can tabs be used instead of spaces for indentation in Python?": "Yes, but it is recommended to use spaces for consistency as per PEP 8 guidelines.",
    "What happens if indentation is incorrect in Python?": "Python will raise an `IndentationError` if the indentation is incorrect or inconsistent.",
    "What is the difference between indentation in Python and other languages?": "Languages like C, Java, and JavaScript use curly braces `{}` for code blocks, whereas Python relies on indentation.",
    "Is indentation mandatory in Python?": "Yes, indentation is mandatory in Python to indicate code blocks.",
    "What is an `IndentationError`?": "An `IndentationError` occurs when the indentation is incorrect or inconsistent in Python.",
    "How to fix an `IndentationError` in Python?": "Ensure that all code blocks use a consistent number of spaces (preferably 4 spaces per indentation level).",
    "Does Python allow mixing spaces and tabs for indentation?": "No, mixing spaces and tabs in the same script will result in an `IndentationError`.",
    "How does indentation affect loops in Python?": "Indentation is used to define the body of loops such as `for` and `while`.",
    "How does indentation affect conditional statements in Python?": "Indentation is used to define the code block executed when a condition in `if`, `elif`, or `else` statements is met.",
    "How does indentation affect functions in Python?": "The body of a function must be indented to indicate where the function starts and ends.",
    "How does indentation affect classes in Python?": "The body of a class must be indented to define its attributes and methods.",
    "Can indentation affect code readability?": "Yes, proper indentation improves readability and makes the code more maintainable.",
    "What is PEP 8's recommendation for indentation?": "PEP 8 recommends using 4 spaces per indentation level.",
    "What tool can help maintain proper indentation in Python?": "Linters like `flake8` or formatters like `black` can help maintain proper indentation.",
    "How to set Python indentation settings in VS Code?": "Go to `Settings` → `Editor: Tab Size` and set it to 4 spaces.",
    "How to convert tabs to spaces in Python?": "Use the `expandtabs()` method or configure your editor to replace tabs with spaces.",
    "What are common indentation mistakes in Python?": "Common mistakes include inconsistent indentation, missing indentation, or using the wrong number of spaces.",
    "Does indentation affect execution time in Python?": "No, indentation does not affect execution time but affects the correctness of the program.",
    "Can Python code work without indentation?": "No, Python relies on indentation to define code blocks, and removing indentation will cause an error.",
    "What is block indentation in Python?": "Block indentation refers to the use of spaces or tabs to define a block of code, such as inside functions, loops, or conditionals.",
    "Can indentation be used for multiline statements in Python?": "Yes, Python allows indentation for multiline statements using parentheses, brackets, or backslashes.",
    "How does indentation work with `try-except` in Python?": "The `try` block and corresponding `except` blocks must be indented properly to handle exceptions correctly.",
    "How does indentation work with `with` statements in Python?": "The block of code inside the `with` statement must be indented.",
    "What is an indentation block in Python?": "An indentation block is a group of indented lines that belong together as part of a loop, function, or class.",
    "How to handle indentation errors in Jupyter Notebook?": "Ensure consistent use of spaces and avoid mixing spaces and tabs in different cells.",
    "How to handle indentation errors in PyCharm?": "Use `Code` → `Reformat Code` to automatically fix indentation issues.",
    "How to fix inconsistent indentation in Python?": "Use `autopep8` or manually ensure that all indentation uses 4 spaces.",
    "Can indentation be used for alignment in Python?": "Yes, indentation can be used to align elements in lists, dictionaries, and function arguments.",
    "How does indentation work with nested loops in Python?": "Each inner loop should be indented further to indicate its nested level.",
    "How does indentation work with nested functions in Python?": "A nested function should be indented inside its enclosing function.",
    "How does indentation work with nested conditionals in Python?": "Each nested condition should be indented further to indicate its level of nesting.",
    "How does indentation work in list comprehensions?": "Indentation is not needed within list comprehensions unless spanning multiple lines.",
    "How does indentation work with decorators in Python?": "Decorators are placed before function definitions without extra indentation.",
    "Can indentation be skipped in one-liner if statements?": "Yes, a one-liner if statement does not require explicit indentation, e.g., `if x > 0: print('Positive')`.",
    "How does indentation work with class inheritance?": "Methods inside a class must be indented, including those inherited from a parent class.",
    "How does indentation work in docstrings?": "Docstrings should be properly indented within functions, classes, or modules.",
    "How does indentation work with `async` and `await`?": "Async functions and await statements must follow normal indentation rules.",
    "Does indentation matter in Python comments?": "No, comments do not require indentation, but they should align with the code they describe.",
    "Can indentation be enforced in Python?": "Yes, using tools like `black` and `flake8` can enforce indentation rules automatically.",
    "Does indentation affect Python's performance?": "No, indentation does not affect performance but is crucial for correct syntax.",
    "How to convert improper indentation to proper indentation?": "Use a text editor or an IDE with automatic indentation correction.",
    "How does indentation work with `elif` and `else`?": "`elif` and `else` should be at the same indentation level as `if`.",
    "What is hanging indentation in Python?": "Hanging indentation is used when breaking long lines for readability.",
    "How to check indentation in Python code?": "Use `flake8` or `pylint` to detect indentation issues.",
    "How to format indentation in Sublime Text?": "Use `Edit` → `Line` → `Convert Indentation to Spaces`.",
    "How to format indentation in Notepad++?": "Use `Edit` → `Blank Operations` → `Tab to Space`.",
    "How to format indentation in Atom?": "Use `Packages` → `Whitespace` → `Convert Tabs to Spaces`.",
    "What happens if indentation levels are inconsistent?": "Python throws an `IndentationError` or unexpected behavior occurs.",
    "What is vertical alignment in Python indentation?": "Vertical alignment helps keep related elements visually organized.",
    "How to change indentation width in Python?": "Modify the editor settings to change indentation width (default is 4 spaces).",
    "How to prevent indentation issues in Python?": "Always use spaces instead of tabs and maintain consistent indentation levels.",
    "Can Python indentation be different for different blocks?": "No, all indentation in a script should be consistent.",
    "How does indentation affect function calling?": "Function calls do not require indentation unless spanning multiple lines.",
    "What is hanging indent in Python?": "A hanging indent is used when a function call or definition spans multiple lines.",
    "How to visualize indentation in an editor?": "Enable 'Show Indentation Guides' in most code editors.",
    "Can indentation affect string formatting?": "No, indentation does not impact string formatting directly.",
    "How to quickly fix indentation errors?": "Use an autoformatter like `black` or `autopep8`.",
    "Why does Python use indentation?": "Python uses indentation for readability and to enforce clean coding practices.",

 "How to swap two numbers in Python?": "You can swap two numbers using tuple unpacking: \n\na, b = 5, 10\na, b = b, a\nprint(a, b)  # Output: 10 5",
    
    "How to check if a number is even or odd?": "Use the modulus operator: \n\nnum = 7\nif num % 2 == 0:\n    print('Even')\nelse:\n    print('Odd')",
    
    "How to find the factorial of a number?": "Use recursion: \n\ndef factorial(n):\n    return 1 if n == 0 else n * factorial(n - 1)\nprint(factorial(5))  # Output: 120",
    
    "How to reverse a string?": "Use slicing: \n\nstring = 'hello'\nprint(string[::-1])  # Output: 'olleh'",
    
    "How to check if a string is a palindrome?": "Compare the string with its reverse: \n\ndef is_palindrome(s):\n    return s == s[::-1]\nprint(is_palindrome('madam'))  # Output: True",
    
    "How to find the largest number in a list?": "Use max(): \n\nnumbers = [3, 8, 1, 5]\nprint(max(numbers))  # Output: 8",
    
    "How to remove duplicates from a list?": "Convert to a set: \n\nnums = [1, 2, 2, 3, 4, 4]\nunique_nums = list(set(nums))\nprint(unique_nums)  # Output: [1, 2, 3, 4]",
    
    "How to merge two dictionaries?": "Use the update() method: \n\ndict1 = {'a': 1, 'b': 2}\ndict2 = {'c': 3, 'd': 4}\ndict1.update(dict2)\nprint(dict1)  # Output: {'a': 1, 'b': 2, 'c': 3, 'd': 4} ",
    
    "How to check if a key exists in a dictionary?": "Use the 'in' keyword: \n\nd = {'name': 'Alice', 'age': 25}\nprint('name' in d)  # Output: True",
    
    "How to sort a list in Python?": "Use sorted() or sort(): \n\nnumbers = [4, 2, 9, 1]\nnumbers.sort()\nprint(numbers)  # Output: [1, 2, 4, 9]",
    
    "How to read a file in Python?": "Use open() function: \n\nwith open('file.txt', 'r') as file:\n    content = file.read()\nprint(content)",
    
    "How to write to a file in Python?": "Use open() in write mode: \n\nwith open('file.txt', 'w') as file:\n    file.write('Hello, World!')",
    
    "How to handle exceptions in Python?": "Use try-except block: \n\ntry:\n    x = 10 / 0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero!')",
    
    "How to import a module in Python?": "Use the import statement: \n\nimport math\nprint(math.sqrt(16))  # Output: 4.0",
    
    "How to use a lambda function?": "Use the lambda keyword: \n\nsquare = lambda x: x ** 2\nprint(square(5))  # Output: 25",
    
    "How to filter elements from a list?": "Use the filter() function: \n\nnumbers = [1, 2, 3, 4, 5]\neven_numbers = list(filter(lambda x: x % 2 == 0, numbers))\nprint(even_numbers)  # Output: [2, 4]",
    
    "How to get the current date and time?": "Use datetime module: \n\nfrom datetime import datetime\nnow = datetime.now()\nprint(now)",
    
    "How to create a class in Python?": "Use the class keyword: \n\nclass Person:\n    def __init__(self, name):\n        self.name = name\np = Person('Alice')\nprint(p.name)  # Output: Alice",
    
    "How to create a list comprehension?": "Use square brackets: \n\nnumbers = [x**2 for x in range(5)]\nprint(numbers)  # Output: [0, 1, 4, 9, 16]",

 "Swap two numbers": "def swap(a, b):\n    a, b = b, a\n    return a, b\n\nnum1, num2 = 5, 10\nnum1, num2 = swap(num1, num2)\nprint(num1, num2)",
    
    "Check if number is even or odd": "def check_even_odd(num):\n    return 'Even' if num % 2 == 0 else 'Odd'\n\nprint(check_even_odd(10))\nprint(check_even_odd(7))",
    
    "Find factorial of a number": "def factorial(n):\n    return 1 if n == 0 else n * factorial(n-1)\n\nprint(factorial(5))",
    
    "Find Fibonacci series up to n terms": "def fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        print(a, end=' ')\n        a, b = b, a + b\n\nfibonacci(10)",
    
    "Reverse a string": "def reverse_string(s):\n    return s[::-1]\n\nprint(reverse_string('Python'))",
    
    "Check if a number is prime": "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n ** 0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n\nprint(is_prime(7))\nprint(is_prime(10))",
    
    "Find the largest number in a list": "def find_largest(lst):\n    return max(lst)\n\nprint(find_largest([1, 5, 3, 9, 2]))",
    
    "Check if a string is a palindrome": "def is_palindrome(s):\n    return s == s[::-1]\n\nprint(is_palindrome('radar'))\nprint(is_palindrome('hello'))",
    
    "Sort a list of numbers": "def sort_list(lst):\n    return sorted(lst)\n\nprint(sort_list([4, 2, 9, 1, 5]))",
    
    "Merge two sorted lists": "def merge_sorted_lists(lst1, lst2):\n    return sorted(lst1 + lst2)\n\nprint(merge_sorted_lists([1, 3, 5], [2, 4, 6]))",
    
    "Find the sum of digits of a number": "def sum_of_digits(n):\n    return sum(int(digit) for digit in str(n))\n\nprint(sum_of_digits(1234))",
    
    "Find the greatest common divisor (GCD)": "import math\ndef gcd(a, b):\n    return math.gcd(a, b)\n\nprint(gcd(48, 18))",
    
    "Find the least common multiple (LCM)": "def lcm(a, b):\n    return abs(a * b) // math.gcd(a, b)\n\nprint(lcm(4, 6))",
    
    "Find the square root of a number": "import math\ndef sqrt(n):\n    return math.sqrt(n)\n\nprint(sqrt(16))",
    
    "Convert Celsius to Fahrenheit": "def celsius_to_fahrenheit(c):\n    return (c * 9/5) + 32\n\nprint(celsius_to_fahrenheit(30))",
    
    "Convert Fahrenheit to Celsius": "def fahrenheit_to_celsius(f):\n    return (f - 32) * 5/9\n\nprint(fahrenheit_to_celsius(86))",
    
    "Find the sum of n natural numbers": "def sum_natural(n):\n    return n * (n + 1) // 2\n\nprint(sum_natural(10))",
    
    "Generate a random number": "import random\ndef generate_random():\n    return random.randint(1, 100)\n\nprint(generate_random())",
    
    "Find the ASCII value of a character": "def ascii_value(char):\n    return ord(char)\n\nprint(ascii_value('A'))",

    
    "How to implement a binary search algorithm in Python?": """ 
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
    """,

    "How to find the factorial of a number using recursion?": """
def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)
    """,

    "How to check if a number is prime?": """
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
    """,

    "How to reverse a linked list in Python?": """
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_linked_list(head):
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev
    """,

    "How to implement a decorator in Python?": """
def my_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@my_decorator
def say_hello():
    print("Hello, World!")
    """,

    "How to use multithreading in Python?": """
import threading

def print_numbers():
    for i in range(5):
        print(i)

t1 = threading.Thread(target=print_numbers)
t1.start()
t1.join()
    """,

    "How to use multiprocessing in Python?": """
from multiprocessing import Process

def worker():
    print("Worker function")

if __name__ == "__main__":
    p = Process(target=worker)
    p.start()
    p.join()
    """,

    "How to use asyncio for asynchronous programming?": """
import asyncio

async def say_hello():
    await asyncio.sleep(1)
    print("Hello, Asyncio!")

asyncio.run(say_hello())
    """,

    "How to use a priority queue in Python?": """
import heapq

pq = []
heapq.heappush(pq, (1, "Task 1"))
heapq.heappush(pq, (3, "Task 3"))
heapq.heappush(pq, (2, "Task 2"))

while pq:
    print(heapq.heappop(pq)[1])
    """,

    "How to use the itertools module for permutations?": """
from itertools import permutations

perm = permutations([1, 2, 3])
for p in perm:
    print(p)
    """,

    "How to implement a trie (prefix tree)?": """
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
    """,

    "How to use metaclasses in Python?": """
class Meta(type):
    def __new__(cls, name, bases, dct):
        print(f"Creating class {name}")
        return super().__new__(cls, name, bases, dct)

class MyClass(metaclass=Meta):
    pass
    """,

    "How to create a context manager using the 'with' statement?": """
class MyContextManager:
    def __enter__(self):
        print("Entering")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting")

with MyContextManager():
    print("Inside context")
    """,

    "How to serialize and deserialize objects using pickle?": """
import pickle

data = {"name": "Alice", "age": 25}
serialized = pickle.dumps(data)
deserialized = pickle.loads(serialized)
print(deserialized)
    """,

    "How to implement a singleton class in Python?": """
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

s1 = Singleton()
s2 = Singleton()
print(s1 is s2)  # True
    """,

    "How to use the functools module for memoization?": """
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
    """,

    "How to use regular expressions in Python?": """
import re

pattern = r"\d+"
matches = re.findall(pattern, "The numbers are 12, 34, and 56.")
print(matches)
    """,

    "How to handle memory management with weak references?": """
import weakref

class MyClass:
    pass

obj = MyClass()
weak_obj = weakref.ref(obj)
print(weak_obj())  # Access the object
del obj
print(weak_obj())  # None (object is garbage collected)
    """,

    "How to implement method chaining in Python?": """
class Person:
    def __init__(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age
        return self

    def set_city(self, city):
        self.city = city
        return self

p = Person("Alice").set_age(25).set_city("New York")
    """,

    "How to create a Python program that reads and processes large files efficiently?": """
def read_large_file(file_path):
    with open(file_path, "r") as f:
        for line in f:
            process(line)  # Replace with actual processing

read_large_file("large_file.txt")
    """,

    "How to implement an LRU cache manually?": """
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1

    def put(self, key: int, value: int):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
    """,

    "How to implement the observer pattern in Python?": """
class Observer:
    def update(self, message):
        pass

class Subject:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify(self, message):
        for observer in self.observers:
            observer.update(message)

class ConcreteObserver(Observer):
    def update(self, message):
        print(f"Received message: {message}")

subject = Subject()
observer = ConcreteObserver()
subject.add_observer(observer)
subject.notify("Hello, Observer!")
    """,
    "How to get the current date and time in Python?": """
import datetime
now = datetime.datetime.now()
print(now)
    """,

    "How to format a datetime object as a string?": """
import datetime
now = datetime.datetime.now()
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted)
    """,

    "How to parse a string into a datetime object?": """
import datetime
date_string = "2025-03-13 14:30:00"
dt = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
print(dt)
    """,

    "How to get the difference between two dates in Python?": """
import datetime
date1 = datetime.date(2025, 3, 1)
date2 = datetime.date(2025, 3, 13)
delta = date2 - date1
print(delta.days)
    """,

    "How to add days to a date?": """
import datetime
today = datetime.date.today()
future_date = today + datetime.timedelta(days=10)
print(future_date)
    """,

    "How to get the current time?": """
import datetime
now = datetime.datetime.now().time()
print(now)
    """,

    "How to compare two datetime objects?": """
import datetime
dt1 = datetime.datetime(2025, 3, 13, 10, 0, 0)
dt2 = datetime.datetime(2025, 3, 13, 15, 0, 0)
print(dt1 < dt2)
    """,

    "How to get the day of the week from a date?": """
import datetime
today = datetime.date.today()
print(today.strftime("%A"))  # Outputs day name
    """,

    "How to measure the execution time of a function?": """
import time
start = time.time()
sum(range(1000000))  # Example operation
end = time.time()
print(f"Execution time: {end - start} seconds")
    """,

    "How to get the UNIX timestamp of the current time?": """
import time
timestamp = time.time()
print(timestamp)
    """,
    "How to create a simple Flask application?": """
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)
    """,

    "How to create an API endpoint in Flask?": """
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello, API!"})

if __name__ == "__main__":
    app.run(debug=True)
    """,

    "How to use request parameters in Flask?": """
from flask import Flask, request

app = Flask(__name__)

@app.route('/greet')
def greet():
    name = request.args.get('name', 'Guest')
    return f"Hello, {name}!"

if __name__ == "__main__":
    app.run(debug=True)
    """,

    "How to create a simple HTML form in Flask?": """
from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form.get("name")
        return f"Hello, {name}!"
    return '''
        <form method="post">
            Name: <input type="text" name="name">
            <input type="submit">
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
    """
}




# Save to a JSON file
with open("python_faq.json", "w") as file:
    json.dump(data, file, indent=4)

# Function to load JSON data
def load_data():
    with open("python_faq.json", "r") as file:
        return json.load(file)

# Function to get the best-matching answer
def get_answer(query):
    faq_data = load_data()
    questions = list(faq_data.keys())

    # Get top 3 matches
    matches = process.extract(query, questions, limit=10)

    if matches:
        best_match, score = matches[0][0], matches[0][1]  # Select the highest scoring match
        if score > 80:  # Use a threshold to avoid wrong matches
            return faq_data[best_match]

    return "Sorry, I don't have an answer for that."

# Main loop to interact with the user
if __name__ == "__main__":
    while True:
        user_query = input("Ask a Python-related question (or type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            print("Goodbye!")
            break
        print(get_answer(user_query))

