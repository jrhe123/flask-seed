from sqlalchemy.orm import Session
from sqlalchemy import select, sql, Table, and_, or_, text, func, desc, MetaData

from school_models import Student, Course, StudentCourseGrade, SexEnum
from db_engine import engine_future as engine


class MySqlOrmTest(object):
    def test_raw_sql(self):
        # init session
        session = Session(bind=engine, future=True)
        raw_sql = text("SELECT * FROM users")
        result = session.execute(raw_sql).scalars().all()
        for item in result:
            print(item)
        session.close()

    def test_pagination(self):
        # init session
        session = Session(bind=engine, future=True)
        # v1 future
        # stmt = select(Student).order_by(Student.id.desc()).limit(10).offset(0)
        # query_set = session.execute(stmt).scalars().all()
        # v2
        # query_set = session.query(Student).slice(0, 10)
        for item in query_set:
            print(item)
        session.close()

    def test_asc_desc(self):
        # init session
        session = Session(bind=engine, future=True)
        # 1. cs score desc
        # stmt = (
        #     select(StudentCourseGrade)
        #     .where(StudentCourseGrade.student_id == Student.id)
        #     .where(StudentCourseGrade.course_id == Course.id)
        #     .where(Course.course_name == "cs")
        #     .order_by(StudentCourseGrade.score.desc())
        # )
        # query_set = session.execute(stmt).scalars().all()
        # for item in query_set:
        #     print(item)
        # 2. total score desc
        stmt = (
            select(
                Student,
                func.sum(StudentCourseGrade.score).label("total_score"),
            )
            .where(Student.id == StudentCourseGrade.student_id)
            .group_by(Student.id)
            .order_by(desc("total_score"))
        )
        query_set = session.execute(stmt).mappings().all()
        for item in query_set:
            print(item)
        session.close()
        pass

    def test_group_by_all_score_gt_90_having_2_grades(self):
        # init session
        session = Session(bind=engine, future=True)
        stmt = (
            select(
                StudentCourseGrade.student_id,
                func.count().label("course_count"),
            )
            .where(StudentCourseGrade.score >= 90)
            .group_by(StudentCourseGrade.student_id)
            .having(func.count() == 2)
        )
        query_set = session.execute(stmt).mappings().all()
        for item in query_set:
            print(item)
        session.close()

    def test_group_by_male_female(self):
        # init session
        session = Session(bind=engine, future=True)
        # group by "class_name"
        stmt = select(
            Student.class_name,
            Student.sex,
            func.count().label("stu_count"),
        ).group_by(
            Student.class_name,
            Student.sex,
        )
        query_set = session.execute(stmt).mappings().all()
        for item in query_set:
            print(item)
        session.close()

    def test_group_by(self):
        # init session
        session = Session(bind=engine, future=True)
        # group by "class_name"
        stmt = select(Student.class_name, func.count().label("stu_count")).group_by(
            Student.class_name
        )
        query_set = session.execute(stmt).mappings().all()
        for item in query_set:
            print(item)
        session.close()

    def test_distinct(self):
        # init session
        session = Session(bind=engine, future=True)

        stmt = select(Student.address).distinct()
        result = session.execute(stmt).scalars().all()
        for item in result:
            print(item)

        session.close()

    def join_tables(self):
        # init session
        session = Session(bind=engine, future=True)

        # 0
        stmt = (
            select(StudentCourseGrade)
            .where(Student.id == StudentCourseGrade.student_id)
            .where(Course.id == StudentCourseGrade.course_id)
        )
        querySet = session.execute(stmt).scalars().all()
        for item in querySet:
            print(item)
            print(item.student)
            print(item.course)

        # stmt = (
        #     select(Student, Course, StudentCourseGrade)
        #     .where(Student.id == StudentCourseGrade.student_id)
        #     .where(Course.id == StudentCourseGrade.course_id)
        # )
        # querySet = session.execute(stmt).mappings().all()
        # for item in querySet:
        #     print(item)

        # 1
        # student = session.get(Student, {"id": 1})
        # grade_list = student.grade_list
        # to use filter, needs to add "dynamic" in the model
        # formatted_grade_list = grade_list.filter(StudentCourseGrade.id < 2)

        # print("start+++++++++++")
        # print("student: ", student)
        # print("grade_list: ", grade_list)
        # print("formated: ", formatted_grade_list)
        # print("end+++++++++++")

        # 2
        # grade = session.get(StudentCourseGrade, {"id": 1})
        # student = grade.student
        # print(grade)
        # print(student)

        session.close()

    def search_total_score_in_all_course_stu_1(self):
        # init session
        session = Session(bind=engine, future=True)
        stmt = select(func.sum(StudentCourseGrade.score).label("total_score"),).where(
            StudentCourseGrade.student_id == 1,
        )
        result = session.execute(stmt).mappings().one()
        print(result)

        session.close()

    def search_avg_score_in_math(self):
        # init session
        session = Session(bind=engine, future=True)
        stmt = select(func.avg(StudentCourseGrade.score).label("avg_score"),).where(
            StudentCourseGrade.course_id == 1,
        )
        result = session.execute(stmt).mappings().one()
        print(result)

        session.close()

    def search_max_score_and_min_score_in_math(self):
        # init session
        session = Session(bind=engine, future=True)
        stmt = select(
            func.max(StudentCourseGrade.score).label("max_score"),
            func.min(StudentCourseGrade.score).label("min_score"),
        ).where(
            StudentCourseGrade.course_id == 1,
        )
        result = session.execute(stmt).mappings().one()
        print(result)

        session.close()

    def search_student_count(self):
        # init session
        session = Session(bind=engine, future=True)
        stmt = select(func.count().label("stu_count")).select_from(Student)
        # 1
        # count = session.execute(stmt).first()
        # print(count[0])
        # 2
        # count = session.execute(stmt).scalar_one()
        # print(count)
        # 3
        count = session.execute(stmt).mappings().one()
        print(count["stu_count"])
        session.close()

    def search_student_name_contains_roy_and_age_not_null_male(self):
        # init session
        session = Session(bind=engine, future=True)
        stmt = select([Student]).where(
            and_(
                Student.stu_name.ilike(r"%roy%"),
                Student.age.is_not(None),
                Student.sex == SexEnum.MALE,
            )
        )
        rows = session.execute(stmt).scalars().all()
        for item in rows:
            print(item)
        session.close()

    def search_student_age_gt_12_female_and_lt_18_male(self):
        # init session
        session = Session(bind=engine, future=True)
        stmt = select([Student]).where(
            or_(
                and_(
                    Student.age > 12,
                    Student.sex == SexEnum.FEMALE,
                ),
                and_(
                    Student.age < 18,
                    Student.sex == SexEnum.MALE,
                ),
            )
        )
        rows = session.execute(stmt).scalars().all()
        for item in rows:
            print(item)
        session.close()

    def search_student_age_between_12_18_and_female(self):
        # init session
        session = Session(bind=engine, future=True)
        # stmt = (
        #     select([Student])
        #     .where(
        #         Student.age.between(12, 18),
        #     )
        #     .where(
        #         Student.sex == SexEnum.FEMALE,
        #     )
        # )
        stmt = select([Student]).where(
            and_(
                Student.age.between(12, 18),
                Student.sex == SexEnum.FEMALE,
            )
        )
        rows = session.execute(stmt).scalars().all()
        for item in rows:
            print(item)
        session.close()

    def search_student_name_contains_roy(self):
        # init session
        session = Session(bind=engine, future=True)
        stmt = select([Student]).where(
            # Student.stu_name.like(r"%roy%"),
            # Student.stu_name.contains(r"roy"),
            Student.stu_name.ilike(r"%roy%"),  # case insensitive
        )
        rows = session.execute(stmt).scalars().all()
        for item in rows:
            print(item)
        session.close()

    def search_student_age_12_or_18(self):
        # init session
        session = Session(bind=engine, future=True)
        # age_list = (12, 18)
        # stmt = select([Student]).where(Student.age.in_(age_list))
        stmt = select([Student]).where(
            or_(
                Student.age == 12,
                Student.age == 18,
            )
        )
        rows = session.execute(stmt).scalars()
        for item in rows:
            print(item)
        session.close()

    def search_student_age_exists(self):
        # init session
        session = Session(bind=engine, future=True)
        # stmt = select([Student]).where(Student.age.is_(None))
        stmt = select([Student]).where(Student.age.is_not(None))
        rows = session.execute(stmt).scalars()
        for item in rows:
            print(item)
        session.close()

    def search_student_age_between_12_18(self):
        # init session
        session = Session(bind=engine, future=True)
        stmt = select([Student]).where(
            Student.age.between(12, 18),
        )
        rows = session.execute(stmt).scalars()
        for item in rows:
            print(item)
        session.close()

    def search_student_age_gt_12(self):
        # init session
        session = Session(bind=engine, future=True)
        stmt = select([Student]).where(
            Student.age > 12,
        )
        rows = session.execute(stmt).scalars()
        for item in rows:
            print(item)
        session.close()


def main():
    obj = MySqlOrmTest()
    # obj.search_student_age_gt_12()
    # obj.search_student_age_between_12_18()
    # obj.search_student_age_exists()
    # obj.search_student_age_12_or_18()
    # obj.search_student_name_contains_roy()
    # obj.search_student_age_between_12_18_and_female()
    # obj.search_student_age_gt_12_female_and_lt_18_male()
    # obj.search_student_name_contains_roy_and_age_not_null_male()
    # obj.search_student_count()
    # obj.search_max_score_and_min_score_in_math()
    # obj.search_avg_score_in_math()
    # obj.search_total_score_in_all_course_stu_1()
    # obj.join_tables()
    # obj.test_distinct()
    # obj.test_raw_sql()
    # obj.test_group_by()
    # obj.test_group_by_male_female()
    # obj.test_group_by_all_score_gt_90_having_2_grades()
    # obj.test_asc_desc()
    obj.test_pagination()


if __name__ == "__main__":
    main()
