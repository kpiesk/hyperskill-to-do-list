from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


today = datetime.today()

engine = create_engine('sqlite:///todo.db?check_same_thread=False')  # creating the database file
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=today)

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)  # creating the table in the database

# accessing the database
Session = sessionmaker(bind=engine)
session = Session()


def ui():
    while True:
        action = input("1) Today's tasks\n"
                       "2) Week's tasks\n"
                       "3) All tasks\n"
                       "4) Missed tasks\n"
                       "5) Add task\n"
                       "6) Delete task\n"
                       "0) Exit\n")

        if action == '1':
            print()
            print_day_tasks()
        elif action == '2':
            print_week_tasks()
        elif action == '3':
            print_all_tasks()
        elif action == '4':
            print_missed_tasks()
        elif action == '5':
            add_task()
        elif action == '6':
            delete_task()
        elif action == '0':
            print('\nBye!')
            session.close()
            exit()
        else:
            print('Incorrect input.\n')


# Prints the given day's task
# (if not specified, the given day is today's day)
def print_day_tasks(current_day=today, current_day_name='Today'):
    print(f"{current_day_name} {current_day.day} {current_day.strftime('%b')}:")
    rows = session.query(Table).filter(Table.deadline == current_day.date()).all()
    if rows:
        for i, row in enumerate(rows):
            print(f'{i + 1}. {row.task}')
        print()
    else:
        print('Nothing to do!\n')


# Prints week's tasks
# (tasks whose deadline date is earlier than today's date)
def print_week_tasks():
    print()
    current_day = today
    for i in range(today.weekday(), today.weekday() + 7):
        print_day_tasks(current_day, current_day.strftime('%A'))
        current_day += timedelta(days=1)


# Prints all existing tasks in the database sorted by deadline
def print_all_tasks():
    print('\nAll tasks:')
    rows = session.query(Table).order_by(Table.deadline).all()
    if rows:
        print_given_tasks(rows)
    else:
        print('Nothing to do!')
    print()


# Allows user to add a new task to a database
def add_task():
    task = input('\nEnter task:\n')
    deadline = datetime.strptime(input('Enter deadline:\n'), '%Y-%m-%d').date()
    session.add(Table(task=task, deadline=deadline))
    session.commit()
    print('The task has been added!\n')


# Prints all missed tasks
# (tasks whose deadline date is earlier than today's date)
def print_missed_tasks():
    print('\nMissed tasks:')
    rows = session.query(Table)\
        .filter(Table.deadline < today.date())\
        .order_by(Table.deadline).all()
    if rows:
        print_given_tasks(rows)
    else:
        print('Nothing is missed!')
    print()


# Allows user to delete a chosen task
def delete_task():
    rows = session.query(Table).order_by(Table.deadline).all()
    if rows:
        print('\nChoose the number of the task you want to delete:')
        print_given_tasks(rows)
        delete_row = rows[int(input()) - 1]
        session.delete(delete_row)
        session.commit()
        print('The task has been deleted!\n')
    else:
        print('\nNothing to delete!\n')


# Prints the given tasks
def print_given_tasks(rows):
    for i, row in enumerate(rows):
        print(f"{i + 1}. {row.task}. "
              f"{row.deadline.day} {row.deadline.strftime('%b')}")


# Allows to delete the entire table (if needed)
def delete_table():
    Base.metadata.drop_all(engine)


ui()
