from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def ui():
    while True:
        action = int(input("1) Today's tasks\n"
                           "2) Add task\n"
                           "0) Exit\n"))
        if action == 1:
            get_tasks()
        elif action == 2:
            add_task()
        elif action == 0:
            print('\nBye!')
            exit()


def get_tasks():
    print('\nToday:')
    rows = session.query(Table).all()

    if rows:
        for i, row in enumerate(rows):
            print(f'{i + 1}. {row.task}')
        print()
    else:
        print('Nothing to do!\n')


def add_task():
    task = input('\nEnter task\n')
    session.add(Table(task=task))
    session.commit()
    print('The task has been added!\n')


def delete_table():
    Base.metadata.drop_all(engine)


ui()
