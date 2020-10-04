from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
today = datetime.today()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=today)

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def ui():
    while True:
        action = int(input("1) Today's tasks\n"
                           "2) Week's tasks\n"
                           "3) All tasks\n"
                           "4) Add task\n"
                           "0) Exit\n"))
        if action == 1:
            print()
            get_day_tasks(today)
        elif action == 2:
            get_week_tasks()
        elif action == 3:
            get_all_tasks()
        elif action == 4:
            add_task()
        elif action == 0:
            print('\nBye!')
            exit()


def get_day_tasks(current_day, current_day_name='Today'):
    print(f"{current_day_name} {current_day.day} {current_day.strftime('%b')}:")
    rows = session.query(Table).filter(Table.deadline == current_day.date()).all()

    if rows:
        for i, row in enumerate(rows):
            print(f'{i + 1}. {row.task}')
        print()
    else:
        print('Nothing to do!\n')


def get_week_tasks():
    print()
    current_day = today
    for i in range(today.weekday(), today.weekday() + 7):
        get_day_tasks(current_day, current_day.strftime('%A'))
        current_day += timedelta(days=1)


def get_all_tasks():
    print('\nAll tasks:')
    rows = session.query(Table).order_by(Table.deadline).all()

    if rows:
        for i, row in enumerate(rows):
            print(f"{i + 1}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        print()
    else:
        print('Nothing to do!\n')


def add_task():
    task = input('\nEnter task\n')
    deadline_string = input('Enter deadline:\n')
    deadline = datetime.strptime(deadline_string, '%Y-%m-%d').date()

    session.add(Table(task=task, deadline=deadline))
    session.commit()
    print('The task has been added!\n')


def delete_table():
    Base.metadata.drop_all(engine)


ui()
