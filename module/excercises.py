from .questions import Question
import re

class Exercise():
  def __init__(self, content):
    QUESTION_NUMERIC_DEL = '.'
    QUESTION_DEL = r'\n+\∗?(\d+\.)'
    OPTION_NUMBERIC_DEL = ')'
    OPTION_DEL = r'([a-h]\))'
    self.questions = []
    content = content.replace('-\n', '')
    self.excercises_tok_raw = re.split(QUESTION_DEL, content)
    for index in range(len(self.excercises_tok_raw)):
      if(self.excercises_tok_raw[index] == ''):
        continue
      if(self.excercises_tok_raw[index][0].isnumeric() and self.excercises_tok_raw[index][-1] == QUESTION_NUMERIC_DEL):
        question_no = self.excercises_tok_raw[index][:-1]
        index += 1
        question_body = self.excercises_tok_raw[index]
        question_tok = re.split(OPTION_DEL, question_body)
        question_statement = question_tok[0].strip()
        question_statement = question_statement.replace('\n', ' ')
        options_raw = question_tok[1:]
        options_filtered = {}
        for index in range(len(options_raw)):
          if(len(options_raw[index]) == 2 and options_raw[index][-1] == OPTION_NUMBERIC_DEL):
            option_letter = options_raw[index]
            index += 1
            option_statement = options_raw[index].replace('\n', '').strip()
            options_filtered[option_letter] = option_statement
        self.add_question('Exercises', question_no, question_statement, options_filtered)

  def add_question(self, source, question_no, question, options):
    self.questions.append(Question(source, question_no, question, options))