import os
from module.dbinteract import DBQuery

os.system('pip3 install -r requirements.txt')

if __name__ == "__main__":
	sql_obj = DBQuery('aihk.db')
	sql_obj.setup_tables()
	sql_obj.fill_basic_data()