from nutritionModel import dbBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://ab940@localhost/nutrition')
Session = sessionmaker(bind=engine)
session = Session()

def createTables():
    dbBase.metadata.create_all(engine)

if __name__ == '__main__':
    createTables()
