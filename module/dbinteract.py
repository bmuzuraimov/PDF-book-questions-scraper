import sqlite3
import os
import sys
import traceback
from contextlib import closing

class DBQuery():
  def __init__(self, dbname):
    self.__c_dir = os.path.dirname(os.path.dirname(__file__))
    self.__db_path = './database/' + dbname
    self.__abs_db_path = self.__c_dir + '/database/' + dbname
    self.__connection = sqlite3.connect(self.__abs_db_path)
    self.__cursor = self.__connection.cursor()
    self.__q_tables = []
    self.__o_tables = []
    self.__get_tables()

  def __get_tables(self):
    tables = self.__cursor.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
    tables = self.__cursor.fetchall()
    self.__q_tables = [table[0] for table in tables if table[0][0] == 'q']
    self.__q_tables = [table[0] for table in tables if table[0][0] == 'o']

  def fetch_data(self, table_name):
    sql_statement = "SELECT * FROM {}".format(table_name)
    rows = self.__cursor.execute(sql_statement).fetchall()
    return rows

  def setup_tables(self):
    self.__query("""CREATE TABLE IF NOT EXISTS students(sid INTEGER PRIMARY KEY, 
                            name TEXT);""")

    self.__query("""CREATE TABLE IF NOT EXISTS courses(cid INTEGER PRIMARY KEY, 
                            code TEXT, name TEXT);""")

    self.__query("""CREATE TABLE IF NOT EXISTS enrolled(sid INTEGER, 
                            cid INTEGER, current_score INTEGER, PRIMARY KEY(sid, cid), 
                            FOREIGN KEY(sid) REFERENCES students(sid), 
                            FOREIGN KEY(cid) REFERENCES courses(cid));""")

    self.__query("""CREATE TABLE IF NOT EXISTS topics(tid INTEGER, 
                            cid INTEGER, name TEXT, PRIMARY KEY(tid), 
                            FOREIGN KEY(cid) REFERENCES courses(cid));""")

    self.__query("""CREATE TABLE IF NOT EXISTS topic_weaknesses(twid INTEGER, 
                            sid INTEGER, cid INTEGER, tid INTEGER, PRIMARY KEY(twid), 
                            FOREIGN KEY(sid) REFERENCES enrolled(sid),
                            FOREIGN KEY(cid) REFERENCES enrolled(cid),
                            FOREIGN KEY(tid) REFERENCES topics(tid));""")

  def create_exercises_table(self, q_table, o_table):
    sql_statement = """CREATE TABLE IF NOT EXISTS {table_name}(id INTEGER PRIMARY KEY, 
                      question_no INTEGER, question TEXT, is_mcq BOOLEAN);""".format(table_name=q_table)
    self.__query(sql_statement)
    sql_statement = """CREATE TABLE IF NOT EXISTS {table}(id INTEGER PRIMARY KEY, qid INTEGER, letter TEXT, 
                    option TEXT, FOREIGN KEY(qid) REFERENCES {ref_table}(question_no));""".format(table=o_table, ref_table=q_table)
    self.__query(sql_statement)

  def add_topic(self, ex_table, o_table, exercises_obj):
    pass

  def add_exercises(self, ex_table, o_table, exercises_obj):
    for ex in exercises_obj.questions:
      sql_statement = ex.insert_question_query(ex_table)
      self.__query(sql_statement, (ex.question_no, ex.question, ex.is_mcq))
      if(ex.is_mcq):
        for letter, option in ex.options.items():
          sql_statement = ex.insert_options_query(o_table)
          self.__query(sql_statement, (ex.question_no, letter, option))

  def fill_basic_data(self):
    user_query = ["INSERT INTO students(name) VALUES ('Baiel');",
                      "INSERT INTO students(name) VALUES ('Destiny');",
                      "INSERT INTO students(name) VALUES ('Eric');"]
    course_query = ["INSERT INTO courses(code, name) VALUES ('math1205', 'Discrete Math');",
                      "INSERT INTO courses(code, name) VALUES ('comp2006', 'Computer Organization');",
                      "INSERT INTO courses(code, name) VALUES ('gfvm1047', 'Philosophy of China');"]
    enrolled_query = ["INSERT INTO enrolled(sid, cid, current_score) VALUES (1, 1, 100);",
                      "INSERT INTO enrolled(sid, cid, current_score) VALUES (1, 2, 100);",
                      "INSERT INTO enrolled(sid, cid, current_score) VALUES (2, 2, 100);",
                      "INSERT INTO enrolled(sid, cid, current_score) VALUES (2, 3, 100);",
                      "INSERT INTO enrolled(sid, cid, current_score) VALUES (3, 1, 100);",
                      "INSERT INTO enrolled(sid, cid, current_score) VALUES (3, 3, 100);"]

    topics_query = ["INSERT INTO topics(cid, name) VALUES (2, '1.1 Propositional Logic');",
                "INSERT INTO topics(cid, name) VALUES (2, '1.2 Applications of Propositional Logic');",
                "INSERT INTO topics(cid, name) VALUES (2, '1.3 Propositional Equivalences');",
                "INSERT INTO topics(cid, name) VALUES (2, '1.4 Predicates and Quantifiers');",
                "INSERT INTO topics(cid, name) VALUES (2, '1.5 Nested Quantifiers');",
                "INSERT INTO topics(cid, name) VALUES (2, '1.6 Rules of Inference');",
                "INSERT INTO topics(cid, name) VALUES (2, '1.7 Introduction to Proofs');",
                "INSERT INTO topics(cid, name) VALUES (2, '1.8 Proof Methods and Strategy');",
                "INSERT INTO topics(cid, name) VALUES (2, '2.1 Sets');",
                "INSERT INTO topics(cid, name) VALUES (2, '2.2 Set Operations');",
                "INSERT INTO topics(cid, name) VALUES (2, '2.3 Functions');",
                "INSERT INTO topics(cid, name) VALUES (2, '2.4 Sequences and Summations');",
                "INSERT INTO topics(cid, name) VALUES (2, '2.5 Cardinality of Sets');",
                "INSERT INTO topics(cid, name) VALUES (2, '2.6 Matrices');",
                "INSERT INTO topics(cid, name) VALUES (2, '3.1 Algorithms');",
                "INSERT INTO topics(cid, name) VALUES (2, '3.2 The Growth of Functions');",
                "INSERT INTO topics(cid, name) VALUES (2, '3.3 Complexity of Algorithms');",
                "INSERT INTO topics(cid, name) VALUES (2, '4.1 Divisibility and Modular Arithmetic');",
                "INSERT INTO topics(cid, name) VALUES (2, '4.2 Integer Representations and Algorithms');",
                "INSERT INTO topics(cid, name) VALUES (2, '4.3 Primes and Greatest Common Divisors');",
                "INSERT INTO topics(cid, name) VALUES (2, '4.4 Solving Congruences');",
                "INSERT INTO topics(cid, name) VALUES (2, '4.5 Applications of Congruences');",
                "INSERT INTO topics(cid, name) VALUES (2, '4.6 Cryptography');",
                "INSERT INTO topics(cid, name) VALUES (2, '5.1 Mathematical Induction');",
                "INSERT INTO topics(cid, name) VALUES (2, '5.2 Strong Induction andWell-Ordering');",
                "INSERT INTO topics(cid, name) VALUES (2, '5.3 Recursive Definitions and Structural Induction');",
                "INSERT INTO topics(cid, name) VALUES (2, '5.4 Recursive Algorithms');",
                "INSERT INTO topics(cid, name) VALUES (2, '5.5 Program Correctness');",
                "INSERT INTO topics(cid, name) VALUES (2, '6.1 The Basics of Counting');",
                "INSERT INTO topics(cid, name) VALUES (2, '6.2 The Pigeonhole Principle');",
                "INSERT INTO topics(cid, name) VALUES (2, '6.3 Permutations and Combinations');",
                "INSERT INTO topics(cid, name) VALUES (2, '6.4 Binomial Coefficients and Identities');",
                "INSERT INTO topics(cid, name) VALUES (2, '6.5 Generalized Permutations and Combinations');",
                "INSERT INTO topics(cid, name) VALUES (2, '6.6 Generating Permutations and Combinations');",
                "INSERT INTO topics(cid, name) VALUES (2, '7.1 An Introduction to Discrete Probability');",
                "INSERT INTO topics(cid, name) VALUES (2, '7.2 Probability Theory');",
                "INSERT INTO topics(cid, name) VALUES (2, '7.3 Bayes’ Theorem');",
                "INSERT INTO topics(cid, name) VALUES (2, '7.4 Expected Value and Variance');",
                "INSERT INTO topics(cid, name) VALUES (2, '8.1 Applications of Recurrence Relations');",
                "INSERT INTO topics(cid, name) VALUES (2, '8.2 Solving Linear Recurrence Relations');",
                "INSERT INTO topics(cid, name) VALUES (2, '8.3 Divide-and-Conquer Algorithms and Recurrence Relations');",
                "INSERT INTO topics(cid, name) VALUES (2, '8.4 Generating Functions');",
                "INSERT INTO topics(cid, name) VALUES (2, '8.5 Inclusion–Exclusion');",
                "INSERT INTO topics(cid, name) VALUES (2, '8.6 Applications of Inclusion–Exclusion');",
                "INSERT INTO topics(cid, name) VALUES (2, '9.1 Relations and Their Properties');",
                "INSERT INTO topics(cid, name) VALUES (2, '9.2 n-ary Relations and Their Applications');",
                "INSERT INTO topics(cid, name) VALUES (2, '9.3 Representing Relations');",
                "INSERT INTO topics(cid, name) VALUES (2, '9.4 Closures of Relations');",
                "INSERT INTO topics(cid, name) VALUES (2, '9.5 Equivalence Relations');",
                "INSERT INTO topics(cid, name) VALUES (2, '9.6 Partial Orderings');",
                "INSERT INTO topics(cid, name) VALUES (2, '10.1 Graphs and Graph Models');",
                "INSERT INTO topics(cid, name) VALUES (2, '10.2 Graph Terminology and Special Types of Graphs');",
                "INSERT INTO topics(cid, name) VALUES (2, '10.3 Representing Graphs and Graph Isomorphism');",
                "INSERT INTO topics(cid, name) VALUES (2, '10.4 Connectivity');",
                "INSERT INTO topics(cid, name) VALUES (2, '10.5 Euler and Hamilton Paths');",
                "INSERT INTO topics(cid, name) VALUES (2, '10.6 Shortest-Path Problems');",
                "INSERT INTO topics(cid, name) VALUES (2, '10.7 Planar Graphs');",
                "INSERT INTO topics(cid, name) VALUES (2, '10.8 Graph Coloring');",
                "INSERT INTO topics(cid, name) VALUES (2, '11.1 Introduction to Trees');",
                "INSERT INTO topics(cid, name) VALUES (2, '11.2 Applications of Trees');",
                "INSERT INTO topics(cid, name) VALUES (2, '11.3 Tree Traversal');",
                "INSERT INTO topics(cid, name) VALUES (2, '11.4 Spanning Trees');",
                "INSERT INTO topics(cid, name) VALUES (2, '11.5 Minimum Spanning Trees');",
                "INSERT INTO topics(cid, name) VALUES (2, '12.1 Boolean Functions');",
                "INSERT INTO topics(cid, name) VALUES (2, '12.2 Representing Boolean Functions');",
                "INSERT INTO topics(cid, name) VALUES (2, '12.3 Logic Gates');",
                "INSERT INTO topics(cid, name) VALUES (2, '12.4 Minimization of Circuits');",
                "INSERT INTO topics(cid, name) VALUES (2, '13.1 Languages and Grammars');",
                "INSERT INTO topics(cid, name) VALUES (2, '13.2 Finite-State Machines with Output');",
                "INSERT INTO topics(cid, name) VALUES (2, '13.3 Finite-State Machines with No Output');",
                "INSERT INTO topics(cid, name) VALUES (2, '13.4 Language Recognition');",
                "INSERT INTO topics(cid, name) VALUES (2, '13.5 Turing Machines');"]  

    self.__query(user_query)
    self.__query(course_query)
    self.__query(enrolled_query)
    self.__query(topics_query)

  def __query(self, sql_statement, sql_data=()):
    try:
      if(isinstance(sql_statement, list)):
        for query in sql_statement:
          self.__cursor.execute(query, sql_data)
          self.__connection.commit()
      elif(isinstance(sql_statement, str)):
          self.__cursor.execute(sql_statement, sql_data)
          self.__connection.commit()
    except sqlite3.Error as er:
      print('SQLite error: %s' % (' '.join(er.args)))
      print("Exception class is: ", er.__class__)
      print('SQLite traceback: ')
      exc_type, exc_value, exc_tb = sys.exc_info()
      print(traceback.format_exception(exc_type, exc_value, exc_tb))
