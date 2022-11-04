class Question():
  def __init__(self, source, question_no, question, options):
    self.question_source = source
    self.question_no = question_no
    self.question = question
    self.options = options
    self.is_mcq = True if(len(self.options) > 0) else False

  def __str__(self):
    result = "Question #{}\n".format(self.question_no)
    result += "{}\n".format(self.question)
    for letter, option in self.options.items():
      result += "{} {}\n".format(letter, option)
    return result

  def insert_question_query(self, table_name):
    return """INSERT INTO {table_name}(question_no, question, is_mcq) VALUES (?, ?, ?);
                          """.format(table_name=table_name)

  def insert_options_query(self, table_name):
    return """INSERT INTO {table_name}(qid, letter, option) VALUES (?, ?, ?);
                        """.format(table_name=table_name)