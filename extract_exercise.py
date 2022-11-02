from PyPDF2 import PdfReader
import math
import argparse
import py_stringmatching as sm

class Book():
  def __init__(self):
      self.excercise_pos = (1001, 140)
      self.first_page = 0
      self.last_page = 0
      self.outline_arr = []
      self.is_exercise = False
      self.parts = []
      self.text_body = ""
      self.stop_topic = ""
      self.is_stop = False

  def read_pdf(self):
    try:
      return PdfReader('./resources/book.pdf')
    except FileNotFoundError as e:
      try:
        return PdfReader('./Documents/aihk/resources/book.pdf')
      except FileNotFoundError as e:
        print("File doesn't exist!")

  def get_outline(self):
    f_page_defined = False
    l_page_defined = False
    for section in reader_obj.getOutlines():
      if isinstance(section, dict):
        title = section['/Title']
        page_num = reader_obj.getDestinationPageNumber(section)+1
        if(title.split(" ")[0] == "1" and not f_page_defined):
          self.first_page = page_num
          f_page_defined = True
        if(title == "Appendixes" and not l_page_defined):
          self.last_page = page_num-1
          l_page_defined = True
        if(f_page_defined and not l_page_defined):
          self.outline_arr.append([title, page_num, True])
      elif isinstance(section, list):
        for sub_section in section:
          title = sub_section['/Title']
          page_num = reader_obj.getDestinationPageNumber(sub_section)+1
          if(f_page_defined and not l_page_defined):
            self.outline_arr.append([title, page_num, False])

  def get_page_num(self):
   return len(reader_obj.pages)

  def extract_exercises(topic):
    index = get_topic_index(topic)
    start_page = self.outline_arr[index][1]
    end_page = self.outline_arr[index+1][1] 
    stop_topic = self.outline_arr[index+1][0]
    for page_num in range(start_page, end_page):
      page = reader_obj.pages[page_num]
      page.extract_text(visitor_text=visitor_body)
      text_body = "".join(self.parts)

  def visitor_body(self, text, cm, tm, fontDict, fontSize):
      x = math.floor(tm[4])
      y = math.floor(tm[5])
      if(stop_topic == text):
        is_stop = True
      if(y > 100 and y < 1000 and self.is_exercise and not is_stop):
        self.parts.append(text)
      if(text == "Exercises" and x == self.excercise_pos[1]):
        self.is_exercise = True


  def get_topic_index(self, topic):
    for index, item in enumerate(self.outline_arr):
      if(item[0] == topic):
        return index
    return -1
    
  def process_text(self, text_body):
    delim_tok = sm.DelimiterTokenizer(['/', '=', '?'])
    tokens = delim_tok.tokenize(text_body)

  def write_file(self, content):
    try:
      with open('./exercises/'+topic_in+'.txt', 'w') as f:
        f.write(content)
    except FileNotFoundError as e:
      try:
        with open('./Documents/aihk/exercises/'+topic_in+'.txt', 'w') as f:
          f.write(content)
      except FileNotFoundError as e:
        print("Error occured while writing a file!")


if __name__ == "__main__":
  book = Book()
  reader_obj = book.read_pdf()
  book.get_outline()
  parser = argparse.ArgumentParser()
  # Add an argument
  parser.add_argument('--topic', type=str, required=False, nargs='+')
  parser.add_argument('--time', type=int, required=False)
  # Parse the argument
  args = parser.parse_args()
  topic_in = ' '.join(args.topic)
  if(get_topic_index(topic_in) > -1):
    book.extract_exercises(topic_in)
    book.write_file(text_body)
  else:
    print("Topic doesn't exist!")