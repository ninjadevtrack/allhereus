from core.models import *

import logging


def yo(text):
    print("***YO: {}".format(text))


logging.getLogger().setLevel(logging.DEBUG)

# TODO: specify the district ID
from core import roster
EDNUDGE_HOST="3.93.153.40"

r=roster.Roster(EDNUDGE_HOST)

district_id='nudge:district:cjsqe220m0000u7i5a1itgtjb'

en_learners = r.ednudge_get_learners(district_id)
en_instructors = r.ednudge_get_instructors(district_id)

eenrollments = r.ednudge_get_enrollments(district_id).data

esections = r.ednudge_get_sections(district_id).data

for en in eenrollments:
    yo("school_id:{}, enrollment_id:{}".format(en.school_id, en.id))
    roster_action="N"

    if en.person_type == "learner":
        # Ensure Student Exists

        # Get the EdNudge student
        yo("en:{}".format(en))
        en_learner = [x for x in en_learners.data 
            if x.id == en.person_id]
        if len(en_learner) == 0:
            yo("en.person_id={}, en.person_type={} not found.".format(
                en.person_id, en.person_type
            ))
            continue
        if len(en_learner) > 1:
            yo("We found more than one learner with person_id={}. SKIPPING....".format(en.person_id))
            continue
        
        # Get the en_learner so that we're not working with a list
        en_learner = en_learner[0]
        yo("Found en_learner:{}".format(en_learner))

        student_roster_action = "N"
        try:
            ah_student = Student.objects.get(
                ednudge_is_enabled = True,
                ednudge_learner_id = en.person_id
            )

            if ah_student.ednudge_merkleroot == en_learner.merkleroot:
                student_roster_action = "N"
            else:
                student_roster_action = "U"

        except Student.DoesNotExist:
            ah_student = None
            student_roster_action = "C"

        if student_roster_action == "C":
            school = School.objects.get(
                ednudge_is_enabled = True,
                ednudge_school_id = en.school_id
            )
            district = District.objects.get(
                ednudge_is_enabled = True,
                ednudge_district_id = district_id
            )
            ah_student = Student.objects.create(
                ednudge_is_enabled = True,
                ednudge_learner_id = en_learner.id,
                ednudge_learner_local_id = en_learner.local_id,
                student_id = en_learner.local_id,
                first_name = en_learner.first_name,
                last_name = en_learner.last_name,
                language = en_learner.home_language,
                email = en_learner.email,
                grade = en_learner.grade,
                school = school,
                district = district,
                ednudge_merkleroot = en_learner.merkleroot
            )
            yo("Created Student: {}".format(ah_student))

        if student_roster_action == "U":
            logging.debug("Updating AllHere Student for EdNudge learner_id=%s", en_learner.id)
            ah_student.first_name = en_learner.first_name
            ah_student.last_name = en_learner.last_name
            ah_student.language = en_learner.home_language
            ah_student.email = en_learner.email
            ah_student.grade = en_learner.grade
            ah_student.ednudge_merkleroot = en_learner.merkleroot
            ah_student.save(update_fields=[
                'first_name', 'last_name', 'language',
                'email','grade'])

        # Sync the SectionStudent
        sectionstudent_roster_action = "N"
        try:
            ah_sectionstudent = SectionStudent.objects.get(
                ednudge_is_enabled = True,
                ednudge_enrollment_id=en.id
            )
            if ah_sectionstudent.ednudge_merkleroot == en.merkleroot:
                sectionstudent_roster_action = "N"
            else:
                sectionstudent_roster_action = "U"
                
        except SectionStudent.DoesNotExist:
            ah_sectionstudent = None
            sectionstudent_roster_action = "C"

        if sectionstudent_roster_action == "C":
            logging.debug("Creating AllHere SectionStudent for EdNudge enrollment_id=%s,person_id=%s", en.id, en.person_id)
            ah_section = Section.objects.get(
                ednudge_is_enabled = True,
                ednudge_section_id = en.section_id)
            yo("ah_section:{}".format(ah_section))

            ah_sectionstudent = SectionStudent.objects.create(
                section = ah_section,
                student = ah_student,
                ednudge_is_enabled = True,
                ednudge_enrollment_id = en.id,
                ednudge_section_id = en.section_id,
                ednudge_person_id = en.person_id,
                ednudge_merkleroot = en.merkleroot
            )
        
        if sectionstudent_roster_action == "U":
            logging.debug("Updating AllHere SectionStudent for EdNudge enrollment_id=%s,person_id=%s", en.id, en.person_id)
            ah_section = Section.objects.get(
                ednudge_is_enabled = True,
                ednudge_section_id = en.section_id)
            #TODO: consider adding these to our model
            #ah_sectionstudent.ednudge_start_date = en.start_date
            #ah_sectionstudent.ednudge_end_date = en.end_date
            ah_sectionstudent.ednudge_merkleroot = en.merkleroot
            ah_sectionstudent.save(update_fields=['ednudge_merkleroot'])

    if en.person_type == "instructor":
        # Ensure Teacher Exists
        # Get the EdNudge teacher
        en_instructor = [x for x in en_instructors.data 
            if x.id == en.person_id]
        if len(en_instructor) == 0:
            yo("en.person_id={}, en.person_type={} not found.".format(
                en.person_id, en.person_type
            ))
            continue
        if len(en_instructor) > 1:
            yo("We found more than one instructor with person_id={}. SKIPPING....".format(en.person_id))
            continue        
        # Get the en_instructor so that we're not working with a list
        en_instructor = en_instructor[0]

        # Sync the teacher with AllHere
        teacher_roster_action = "N"
        try:
            ah_teacher = MyUser.objects.get(
                ednudge_is_enabled = True,
                ednudge_person_id = en.person_id
            )

            if ah_teacher.ednudge_merkleroot == en_instructor.merkleroot:
                teacher_roster_action = "N"
            else:
                teacher_roster_action = "U"

        except MyUser.DoesNotExist:
            ah_teacher = None
            teacher_roster_action = "C"

        if teacher_roster_action == "C":
            logging.debug("Creating AllHere MyUser for EdNudge Instructor Id=%s", en_instructor.id)
            # Ensure instructor's email is unique
            instructor_email = en_instructor.email
            try:
                test = MyUser.objects.get(email=instructor_email)
            except MyUser.DoesNotExist:
                # yo("Found a user with the same email address.  Skipping..... {}".format(test))
                # TODO: uncomment ```continue```
                #continue
                yo("Creating a fake email address and continuing....")
                instructor_email = "noemail-{}@allhere.com".format(en_instructor.id)

            school = School.objects.get(
                ednudge_is_enabled = True,
                ednudge_school_id = en.school_id
            )
            district = District.objects.get(
                ednudge_is_enabled = True,
                ednudge_district_id = district_id
            )
            ah_teacher = MyUser.objects.create(
                ednudge_is_enabled = True,
                ednudge_person_id = en_instructor.id,
                ednudge_person_local_id = en_instructor.local_id,
                ednudge_person_type = en.person_type,
                ednudge_merkleroot = en.merkleroot,

                school = school,
                district = district,

                role = 'T',

                first_name = en_instructor.first_name,
                last_name = en_instructor.last_name,

                email = instructor_email
            )

        if teacher_roster_action == "U":
            logging.debug("Creating AllHere MyUser for EdNudge Instructor Id=%s", en_instructor.id)
            ah_teacher.first_name = en_instructor.first_name
            ah_teacher.last_name = en_instructor.last_name
            ah_teacher.save(update_fields=['first_name','last_name'])

        # Sync the SectionTeacher
        sectionteacher_roster_action = "N"
        try:
            ah_sectionteacher = SectionTeacher.objects.get(
                ednudge_is_enabled = True,
                ednudge_enrollment_id=en.id
            )
            if ah_sectionteacher.ednudge_merkleroot == en.merkleroot:
                sectionteacher_roster_action = "N"
            else:
                sectionteacher_roster_action = "U"

        except SectionTeacher.DoesNotExist:
            ah_sectionteacher = None
            sectionteacher_roster_action = "C"

        if sectionteacher_roster_action == "C":
            logging.debug("Creating AllHere SectionTeacher for EdNudge enrollment_id=%s,person_id=%s", en.id, en.person_id)
            ah_section = Section.objects.get(
                ednudge_is_enabled = True,
                ednudge_section_id = en.section_id)
            yo("ah_section:{}".format(ah_section))

            ah_sectionteacher = SectionTeacher.objects.create(
                section = ah_section,
                teacher = ah_teacher,
                ednudge_is_enabled = True,
                ednudge_enrollment_id = en.id,
                ednudge_section_id = en.section_id,
                ednudge_person_id = en.person_id,
                ednudge_merkleroot = en.merkleroot
            )
        
        if sectionteacher_roster_action == "U":
            logging.debug("Updating AllHere SectionTeacher for EdNudge enrollment_id=%s,person_id=%s", en.id, en.person_id)
            ah_section = Section.objects.get(
                ednudge_is_enabled = True,
                ednudge_section_id = en.section_id)
            yo("ah_section:{}".format(ah_section))

            #TODO: consider adding these to our model
            #ah_sectionteacher.ednudge_start_date = en.start_date
            #ah_sectionteacher.ednudge_end_date = en.end_date
            ah_sectionteacher.ednudge_merkleroot = en.merkleroot
            ah_sectionteacher.save(update_fields=['ednudge_merkleroot'])

        yo("ah_sectionteacher: {}".format(ah_sectionteacher))