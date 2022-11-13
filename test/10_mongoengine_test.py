from mo_school_models import Student, StudentGrade, SexChoices, CourseGrade
from bson.objectid import ObjectId
from mongoengine.queryset.visitor import Q


class TestMongoEngine(object):
    def get_one_student(self):
        stu_obj = Student.objects.first()
        print(stu_obj[f"stu_no"])
        return stu_obj

    def get_student_by_pk(self, pk):
        object_id = ObjectId(pk)
        # stu_obj = Student.objects.get(id=pk)
        stu_obj = Student.objects.get(id=object_id)
        print(stu_obj[f"stu_no"])
        return stu_obj

    def get_grades_1(self):
        query_set = StudentGrade.objects.filter(grade__score__gte=60)
        for item in query_set:
            print(item)

    def get_students_1(self):
        # query_set = Student.objects()
        # query_set = Student.objects.all()
        # query_set = Student.objects(age__gt=12)
        query_set = Student.objects.filter(age__gt=12)
        for item in query_set:
            print(item)

    def get_students_2(self):
        query_set = Student.objects.filter(stu_name__startswith="roy")
        for item in query_set:
            print(item)

    def get_students_3(self):
        # query_set = Student.objects.filter(age__gte=9, age__lte=12)
        query_set = Student.objects.filter(Q(age__gte=9) & Q(age__lte=12))
        for item in query_set:
            print(item)

    def get_students_4(self):
        # $and / $or
        query_set = Student.objects.filter(
            Q(
                age__gt=12,
                sex=SexChoices.MALE,
            )
            | Q(
                age__lt=9,
                sex=SexChoices.FEMALE,
            )
        )
        for item in query_set:
            print(item)
        print("total: ", query_set.count())

    def get_students_5(self):
        # aggregate
        query_set = StudentGrade.objects.filter(grade__course_name="cs")
        avg_score = query_set.average("grade.score")
        print("avg_score: ", avg_score)

        query_set = StudentGrade.objects.filter(stu_name="roytest")
        sum_score = query_set.sum("grade.score")
        print("total_score: ", sum_score)

    def get_students_6(self):
        query_set = Student.objects.filter(
            Q(
                age__gt=12,
                sex=SexChoices.MALE,
            )
            | Q(
                age__lt=9,
                sex=SexChoices.FEMALE,
            )
        )
        query_set = query_set.order_by("age")
        for item in query_set:
            print(item)

    def paginate(self, page=1, page_size=10):
        start = (page - 1) * page_size
        end = page * page_size
        # query_set = Student.objects.all()[start:end]
        query_set = Student.objects().skip(start).limit(page_size)
        for item in query_set:
            print(item)

    def add_one(self):
        stu_obj = Student(
            stu_no=10086,
            stu_name="roytest2",
            phone_no="1231231234",
        )
        stu_obj.validate()
        stu_obj.save()
        print("added")

    def add_one_2(self):
        stu_obj = Student.objects.create(
            stu_no=10086,
            stu_name="roytest2",
            phone_no="1231231234",
        )
        stu_obj.validate()
        stu_obj.save()
        print("added")

    def add_one_3(self):
        stu_obj = Student.objects.create(
            stu_no=10088,
            stu_name="roytest3",
            phone_no="1231231234",
        )
        grade1 = CourseGrade(
            course_name="cs",
            score=100,
        )
        grade2 = CourseGrade(
            course_name="ml",
            score=98,
        )
        stu_obj.grades = [
            grade1,
            grade2,
        ]
        stu_obj.validate()
        stu_obj.save()
        print("added")

    def update_one(self):
        """
        set
        unset
        inc
        dec
        push
        pull
        """
        query_set = Student.objects.filter(
            stu_no=10086,
        )
        # result = query_set.update_one(
        #     stu_name="updated_name",
        #     phone_no="3213213214",
        # )
        result = query_set.update_one(
            unset__phone_no=True,
        )
        print(result)

    def update_one_2(self):
        stu_obj = Student.objects.filter(
            stu_no=10086,
        ).first()
        if stu_obj:
            stu_obj.stu_name = "test name"
            result = stu_obj.save()
            print(result)

    def update_many(self):
        query_set = Student.objects.filter(
            age=9,
        )
        query_set.update(inc__age=1)
        for item in query_set:
            print(item)

    def delete_data(self):
        query_set = Student.objects(
            stu_no__gt=2000,
        )
        for item in query_set:
            print(item)
        result = query_set.delete()
        print(result)


def main():
    obj = TestMongoEngine()
    # obj.get_one_student()
    # obj.get_student_by_pk("636c70dc31091d1d224f9ca5")
    # obj.get_grades_1()
    # obj.get_students_1()
    # obj.get_students_2()
    # obj.get_students_3()
    # obj.get_students_4()
    # obj.get_students_5()
    # obj.paginate()
    # obj.add_one()
    # obj.add_one_2()
    # obj.add_one_3()
    # obj.update_one()
    # obj.update_one_2()
    # obj.update_many()
    obj.delete_data()


if __name__ == "__main__":
    main()
