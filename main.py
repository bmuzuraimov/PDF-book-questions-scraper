import argparse
from pdfscraper import pdfscraper

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
  else:
    print("Please enter the topic name: ")
    scraper.print_outline()
    topic_name = input()

  if(scraper.get_topic_index(topic_name) > -1):
    scraper.extract_exercises(topic_name)
    scraper.to_db()
    scraper.db_get_tables()
    # scraper.to_file()
  else:
    print("Topic doesn't exist!")