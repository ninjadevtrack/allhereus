import os, sys

proj_path = "/var/app/"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from core.models import *

import logging

import os

def yo(text):
    print("***YO: {}".format(text))

logging.getLogger().setLevel(logging.DEBUG)

# TODO: specify the district ID
from core import roster
EDNUDGE_HOST=os.getenv('EDNUDGE_API_URL')
EDNUDGE_USERNAME=os.getenv('EDNUDGE_USERNAME')
EDNUDGE_PASSWORD=os.getenv('EDNUDGE_PASSWORD')
r=roster.Roster(EDNUDGE_HOST,EDNUDGE_USERNAME,EDNUDGE_PASSWORD)

def get_grade(val):
    val = val.lower()
    map = {
        'pre-kindergarten':'PK',
        'kindergarten':'K',
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        '6': '6',
        '7': '7',
        '8': '8',
        '9': '9',
        '10': '10',
        '11': '11',
        '12': '12',
        'other': 'O'
    }
    try:
        return map[val]
    except KeyError:
        return 'O'
    

if len(sys.argv) == 3:
    district_local_id = sys.argv[1]
    school_local_id = sys.argv[2]
elif len(sys.argv) == 2:
    district_local_id = sys.argv[1]
    school_local_id=None
else:
    print(f"Usage: {sys.argv[0]} $district_local_id $school_local_id")
    sys.exit()


district_id = District.objects.get(ednudge_district_local_id=district_local_id).ednudge_district_id
if school_local_id:
    en_schools = r.ednudge_get_schools(district_id).data
    en_school = [x for x in en_schools if x.local_id == school_local_id]
    school_id = en_school[0].id
    logging.debug(f"ENROLLMENTS for district={district_local_id} for school_id:{school_id}")
else:
    school_id=None
    logging.debug(f"ENROLLMENTS for distrcit={district_local_id} for ALL schools")

limit = 2000

en_learners = r.ednudge_get_learners_all(district_id, limit)
logging.debug(f"en_learners has {len(en_learners)} elements.")
en_instructors = r.ednudge_get_instructors_all(district_id, limit)
logging.debug(f"en_instructors has {len(en_instructors)} elements.")

eenrollments=[]
skip=0
limit = 2000
chunk = r.ednudge_get_enrollments(district_id, skip, limit, school_id)
while len(chunk.data) > 0:
    eenrollments = eenrollments + chunk.data
    skip += limit
    chunk = r.ednudge_get_enrollments(district_id, skip, limit, school_id)
    logging.debug(f"chunk:{chunk}")

logging.debug(f"eenrollments has {len(eenrollments)} elements")

for en in eenrollments:
    logging.debug("school_id:{}, enrollment_id:{}".format(en.school_id, en.id))
    roster_action="N"

    if en.person_type == "learner":
        # Ensure Student Exists

        # Get the EdNudge student
        logging.debug("en:{}".format(en))
        en_learner = [x for x in en_learners 
            if x.id == en.person_id]
        if len(en_learner) == 0:
            logging.debug("en.person_id={}, en.person_type={} not found.".format(
                en.person_id, en.person_type
            ))
            continue
        if len(en_learner) > 1:
            logging.debug("We found more than one learner with person_id={}. SKIPPING....".format(en.person_id))
            continue
        
        # Get the en_learner so that we're not working with a list
        en_learner = en_learner[0]
        logging.debug("Found en_learner:{}".format(en_learner))

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
                grade = get_grade(en_learner.grade_level),
                school = school,
                district = district,
                total_absences = en_learner.year_to_date_absences,
                ednudge_merkleroot = en_learner.merkleroot
            )
            logging.debug("Created Student: {}".format(ah_student))

        if student_roster_action == "U":
            logging.debug("Updating AllHere Student for EdNudge learner_id=%s", en_learner.id)
            ah_student.first_name = en_learner.first_name
            ah_student.last_name = en_learner.last_name
            ah_student.language = en_learner.home_language
            ah_student.email = en_learner.email
            ah_student.grade = get_grade(en_learner.grade_level)
            ah_student.total_absences = en_learner.year_to_date_absences
            ah_student.ednudge_merkleroot = en_learner.merkleroot
            ah_student.save(update_fields=[
                'first_name', 'last_name', 'language',
                'email','grade', 'total_absences', 'ednudge_merkleroot'])

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
            logging.debug("ah_section:{}".format(ah_section))

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
        en_instructor = [x for x in en_instructors 
            if x.id == en.person_id]
        if len(en_instructor) == 0:
            logging.debug("en.person_id={}, en.person_type={} not found.".format(
                en.person_id, en.person_type
            ))
            continue
        elif len(en_instructor) > 1:
            logging.debug("We found more than one instructor with person_id={}. SKIPPING....".format(en.person_id))
            continue        
        else:
            # Get the en_instructor so that we're not working with a list
            en_instructor = en_instructor[0]
            logging.debug(f"Found instructor with person_id={en_instructor.id}.")

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
                # if the test succeeded, we need a fake email address
                logging.debug(f"Found a user with the same email address.  Creating a fake email address and continuing.... {test}")
                instructor_email = f"noemail-{en_instructor.id}@allhere.com".replace(":",".")
            except MyUser.DoesNotExist:
                logging.debug(f"The email address for this user is unique: {instructor_email}")

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
            logging.debug("Updating AllHere MyUser for EdNudge Instructor Id=%s", en_instructor.id)

            # Ensure instructor's email is unique
            instructor_email = en_instructor.email
            if instructor_email != ah_teacher.email:
                try:
                    test = MyUser.objects.get(email=instructor_email)
                    # if the test succeeded, someone already has the email address, so skip it
                    logging.debug(f"Found a user with the same email address.  We're going to skip this one.  Here's the other user: {test}")
                    instructor_email = ah_teacher.email
                except MyUser.DoesNotExist:
                    logging.debug(f"The email address for this user is unique: {instructor_email}")

            ah_teacher.first_name = en_instructor.first_name
            ah_teacher.last_name = en_instructor.last_name
            ah_teacher.email = instructor_email
            ah_teacher.ednudge_merkleroot = en_instructor.merkleroot
            ah_teacher.save(update_fields=['ednudge_merkleroot',
                'first_name','last_name', 'email'])

        # Sync the SectionTeacher
        sectionteacher_roster_action = "N"
        try:
            ah_sectionteacher = SectionTeacher.objects.get(
                ednudge_is_enabled = True,
                ednudge_enrollment_id=en.id
            )
            if (
                ah_sectionteacher.ednudge_merkleroot == en.merkleroot and
                en.deleted_at != "" and
                ah_sectionteacher.is_deleted == False
            ):
                sectionteacher_roster_action = "D"
            elif (
                ah_sectionteacher.ednudge_merkleroot == en.merkleroot and
                en.deleted_at == "" and
                ah_sectionteacher.is_deleted == True
            ):
                sectionteacher_roster_action = "UD"
            elif (
                ah_sectionteacher.ednudge_merkleroot == en.merkleroot and
                en.deleted_at == ""
            ):
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
            logging.debug("ah_section:{}".format(ah_section))

            #TODO: consider adding these to our model
            #ah_sectionteacher.ednudge_start_date = en.start_date
            #ah_sectionteacher.ednudge_end_date = en.end_date
            ah_sectionteacher.ednudge_merkleroot = en.merkleroot
            ah_sectionteacher.save(update_fields=['ednudge_merkleroot'])

        if sectionteacher_roster_action == "D":
            logging.debug("Soft Deleting AllHere SectionTeacher for EdNudge enrollment_id=%s,person_id=%s", en.id, en.person_id)
            ah_section = Section.objects.get(
                ednudge_is_enabled = True,
                ednudge_section_id = en.section_id)
            logging.debug("ah_section:{}".format(ah_section))

            ah_sectionteacher.is_deleted = True
            ah_sectionteacher.save(update_fields=['is_deleted'])

        if sectionteacher_roster_action == "UD":
            logging.debug("Soft UnDeleting AllHere SectionTeacher for EdNudge enrollment_id=%s,person_id=%s", en.id, en.person_id)
            ah_section = Section.objects.get(
                ednudge_is_enabled = True,
                ednudge_section_id = en.section_id)
            logging.debug("ah_section:{}".format(ah_section))

            ah_sectionteacher.is_deleted = False
            ah_sectionteacher.save(update_fields=['is_deleted'])

        logging.debug("ah_sectionteacher: {}".format(ah_sectionteacher))