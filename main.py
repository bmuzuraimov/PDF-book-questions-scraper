import argparse
from module import pdfscraper
from module.gui import App
from module.dbinteract import DBQuery
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
  scraper = pdfscraper.ContentExtractor('/docs/math1205.pdf')
  scraper.add_keyword_offset('Exercises', {'y':1001, 'x':140})
  scraper.add_content_type('Exercises', 'Review Questions', start_keyword = 'Exercises')
  scraper.add_font_types('Exercises', ['/DNKNIJ+Palatino-Bold'])
  parser = argparse.ArgumentParser()
  # Add an argument
  # extract exercises and store in db, main mode(gui), make personalized exercises
  parser.add_argument('--mode', type=str, required=False) # main, extract, personalize
  parser.add_argument('--topic', type=str, required=False, nargs='+')
  parser.add_argument('--time', type=int, required=False)
  # Parse the argument
  args = parser.parse_args()
  if(args.mode == 'main'):
    dbname = os.getenv('DBNAME')
    topic = '6.3 Permutations and Combinations'
    question_table = 'q_' + scraper.topic2table(topic)
    options_table = 'o_' + scraper.topic2table(topic)
    sql_obj = DBQuery(dbname)
    courses = sql_obj.fetch_data('courses')
    topics = sql_obj.fetch_data('topics')
    questions = sql_obj.fetch_data(question_table)
    options = sql_obj.fetch_data(options_table)

    gui_vars = {}
    gui_vars['app_title'] = os.getenv('PROJECT_NAME')
    gui_vars['topic'] = '1.8_Proof_methods_and_Strategy'
    gui_vars['course'] = courses[0][2]
    gui_vars['topics'] = topics
    gui_vars['questions'] = questions
    gui_vars['options'] = options
    app = App(gui_vars)
    app.mainloop()
  elif(args.mode == 'extract'):
    if(args.topic != None):
      topic_name = ' '.join(args.topic)
      if(scraper.get_topic_index(topic_name) > -1):
        scraper.set_topic(topic_name)
        scraper.extract_exercises()
        scraper.exercises_to_db()
        scraper.to_file('')
      else:
        print("Topic doesn't exist!")
  elif(args.mode == 'personalize'):
    pass
  elif(args.mode == 'help'):
    print("'python3 main.py --mode main' - launch gui and do exercises\n" +
          "'python3 main.py --mode extract' - extract exercises from pdf and stores in database\n" + 
          "'python3 main.py --mode personalize' - analyze pdf result of last quiz and create new personalized exercises\n")
  else:
    print('Please enter correct mode or see more options \'python3 main.py --mode help\'')