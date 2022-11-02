import argparse
from module import pdfscraper
from module import gui

if __name__ == "__main__":
  scraper = pdfscraper.ContentExtractor('/docs/book.pdf')
  scraper.add_keyword_offset('Exercises', {'y':1001, 'x':140})
  scraper.add_content_type('Exercises', 'Review Questions', start_keyword = 'Exercises')
  scraper.add_font_types('Exercises', ['/DNKNIJ+Palatino-Bold'])
  parser = argparse.ArgumentParser()
  # Add an argument
  parser.add_argument('--topic', type=str, required=False, nargs='+')
  parser.add_argument('--time', type=int, required=False)
  # Parse the argument
  args = parser.parse_args()
  if(args.topic != None):
    topic_name = ' '.join(args.topic)
    if(scraper.get_topic_index(topic_name) > -1):
      scraper.set_topic(topic_name)
      scraper.extract_exercises()
      scraper.to_db()
      scraper.to_file('')
    else:
      print("Topic doesn't exist!")
  else:
    gui_vars = {}
    gui_vars['app_title'] = 'Nodea'
    gui_vars['topic'] = '1.8_Proof_methods_and_Strategy'
    app = gui.App(gui_vars)
    app.mainloop()
    # print("Please enter the topic name: ")
    # scraper.print_outline()
    # topic_name = input()