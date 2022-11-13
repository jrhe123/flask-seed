from sqlalchemy.orm import Session
from sqlalchemy import (
    select,
    sql,
    Table,
    and_,
    or_,
    text,
    func,
    desc,
    update,
    delete,
    MetaData,
)

from school_models import Student, Course, StudentCourseGrade, SexEnum
from db_engine import engine_future as engine


class MySqlOrmTest(object):
    def delete_more(self):
        # init session
        session = Session(bind=engine, future=True)

        stmt = delete(Student).where(Student.id < 1)
        result = session.execute(stmt)
        session.commit()

        print("affected rows: ", result.rowcount)

        session.close()

    def delete_one(self):
        # init session
        session = Session(bind=engine, future=True)

        user_obj = session.get(Student, {"id": 1})
        session.delete(user_obj)
        session.commit()

        session.close()

    def update_one_data(self):
        # init session
        session = Session(bind=engine, future=True)

        stmt = (
            update(Student)
            .where(Student.id == 1)
            .values(
                age=21,
                stu_name="updated",
            )
            .execution_options(
                synchronize_session="fetch",  # False / fetch / evaluate
            )
        )
        result = session.execute(stmt)
        session.commit()

        print("affacted rows: ", result.rowcount)

        session.close()

    def update_one(self):
        # init session
        session = Session(bind=engine, future=True)

        student_obj = session.get(Student, {"id": 1})
        student_obj.phone_no = "9991231234"
        session.add(student_obj)
        session.commit()

        session.close()


def main():
    obj = MySqlOrmTest()

    # obj.update_one()
    # obj.update_one_data()
    # obj.delete_one()
    obj.delete_more()


if __name__ == "__main__":
    main()
