import py_stringmatching as sm
import re
from PyPDF2 import PdfReader
import math
import os
import sys
from .dbinteract import DBQuery
from .excercises import Exercise


class ContentExtractor():
  def __init__(self, in_file):
      self.__c_dir = os.path.dirname(os.path.dirname(__file__))
      self.__sql_obj = DBQuery('aihk.db')
      self.exercises_obj = None
      self.topic_name = ''
      self.__table_name = ''
      self.__in_file = '.' + in_file
      self.__abs_in_file = self.__c_dir + in_file
      self.__out_file_dir = './docs/'
      self.__abs_out_file_dir = self.__c_dir + '/docs/'
      self.__keyword_offset = {}
      self.__font_types = {}
      self.__content_types = []
      self.__outline_arr = []
      self.__reader_obj = None
      self.__text_parts = []
      self.__ex_start_keyword = None
      self.__ex_stop_keyword = ''
      self.__pdf_stop_keyword = '"Appendixes"'
      self.text_body = ''
      # Used for __reader_windows(self) only
      self.__is_start = False
      self.__is_stop = False
      # Used for get_outline(self) only
      self.first_page = 0
      self.last_page = 0
      # ==============================
      self.read_pdf()
      self.get_outline()

  def set_topic(self, topic):
    self.topic_name = topic
    self.__table_name = self.topic2table(topic).lower()

  def print_outline(self):
    for topic in self.__outline_arr:
      if(topic[0].split(".")[0].isnumeric() and not topic[2]):
        print(topic[0])

  def add_keyword_offset(self, key, value):
    self.__keyword_offset[key] = value

  def add_font_types(self, key, value):
    self.__font_types[key] = value

  def add_content_type(self, *content_type, **kwargs):
    for item in content_type:
      self.__content_types.append(item)
    self.__ex_start_keyword = kwargs['start_keyword']

  def read_pdf(self):
    try:
      self.__reader_obj = PdfReader(self.__in_file)
    except FileNotFoundError as e:
      try:
        self.__reader_obj = PdfReader(self.__abs_in_file)
      except FileNotFoundError as e:
        print("File doesn't exist!")

  def get_outline(self):
    f_page_defined = False
    l_page_defined = False
    for section in self.__reader_obj.getOutlines():
      if isinstance(section, dict):
        title = section['/Title']
        page_num = self.__reader_obj.getDestinationPageNumber(section)+1
        if(title.split(" ")[0] == "1" and not f_page_defined):
          self.first_page = page_num
          f_page_defined = True
        if(title == self.__pdf_stop_keyword and not l_page_defined):
          self.last_page = page_num-1
          l_page_defined = True
        if(f_page_defined and not l_page_defined):
          self.__outline_arr.append([title, page_num, True])
      elif isinstance(section, list):
        for sub_section in section:
          title = sub_section['/Title']
          page_num = self.__reader_obj.getDestinationPageNumber(sub_section)+1
          if(f_page_defined and not l_page_defined):
            self.__outline_arr.append([title, page_num, False])

  def get_page_num(self):
   return len(self.__reader_obj.pages)

  def get_outline_arr(self):
    return self.__outline_arr

  def extract_exercises(self):
    index = self.get_topic_index(self.topic_name)
    start_page = self.__outline_arr[index][1]
    end_page = self.__outline_arr[index+1][1] 
    self.__ex_stop_keyword = self.__outline_arr[index+1][0]
    for page_num in range(start_page, end_page):
      page = self.__reader_obj.pages[page_num]
      page.extract_text(visitor_text=self.__reader_windows)
      self.text_body = "".join(self.__text_parts)
    self.__process_text()

  def __filter_ligature(sefl, text):
    filtered_text = ''
    ligatures = {'ﬁ':'fi'}
    for char in text:
      to_add = char
      for lig in ligatures.keys():
        if(char == lig):
          to_add = ligatures[lig]
      filtered_text += to_add
    return filtered_text   


  def __reader_windows(self, text, cm, tm, fontDict, fontSize):
      x = math.floor(tm[4])
      y = math.floor(tm[5])
      filtered_text = self.__filter_ligature(text)
      if(self.__ex_stop_keyword == filtered_text):
        self.__is_stop = True
        return
      if(y > 100 and y < 1000 and self.__is_start and not self.__is_stop):
        self.__text_parts.append(filtered_text)
        return
      if(filtered_text == self.__ex_start_keyword and fontDict['/BaseFont'] in self.__font_types['Exercises']):
        self.__is_start = True
        return


  def get_topic_index(self, topic):
    for index, item in enumerate(self.__outline_arr):
      if(item[0].lower() == topic.lower()):
        return index
    return -1

  def to_file(self, file_name):
    if(file_name == '' and self.topic_name != ''):
      file_name = self.topic_name.replace(' ', '_')
    try:
      with open(self.__out_file_dir+file_name+'.txt', 'w') as f:
        for questions in self.exercises_obj.questions:
          f.write(str(questions))
    except FileNotFoundError as e:
      try:
        with open(self.__abs_out_file_dir+file_name+'.txt', 'w') as f:
          for questions in self.exercises_obj.questions:
            f.write(str(questions))
      except FileNotFoundError as e:
        print("Error occured while writing a file!")

  def topic2table(self, topic):
    return re.sub('\d', '', topic).strip().replace(' ', '_').replace('.', '').lower()

  def exercises_to_db(self):
    if(self.topic_name == ''):
      raise('Topic name is not defined!')
    exercise_table = 'q_'+self.__table_name.lower()
    options_table = 'o_'+self.__table_name.lower()
    self.__sql_obj.setup_tables()
    self.__sql_obj.create_exercises_table(exercise_table, options_table)
    self.__sql_obj.add_exercises(exercise_table, options_table, self.exercises_obj)

  def __process_text(self):
    self.exercises_obj = Exercise(self.text_body)

  def reset_vars(self):
    self.__text_parts = []
    self.__ex_stop_keyword = ''
    self.text_body = ''
    self.__is_start = False
    self.__is_stop = False
