import random
from app import db
from models import Course, Faculty, Room, TimeSlot, Schedule

class TimetableScheduler:
    """
    Basic constraint satisfaction scheduler for generating university timetables.
    Uses a simple backtracking approach with conflict checking.
    """
    
    def __init__(self):
        self.max_attempts = 1000
    
    def generate_timetable(self, department, semester, batch):
        """
        Generate a timetable for a specific department and semester.
        Returns True if successful, False otherwise.
        """
        try:
            # Get all courses for this department and semester
            courses = Course.query.filter_by(department=department, semester=semester).all()
            
            if not courses:
                print(f"No courses found for {department} - {semester}")
                return False
            
            # Get available faculty who can teach these courses
            available_faculty = {}
            for course in courses:
                faculty_list = Faculty.query.filter(
                    Faculty.department == department,
                    Faculty.subjects.contains(course.code)
                ).all()
                
                if not faculty_list:
                    print(f"No faculty found for course {course.code}")
                    return False
                
                available_faculty[course.code] = faculty_list
            
            # Get available rooms
            rooms = Room.query.all()
            if not rooms:
                print("No rooms available")
                return False
            
            # Get time slots
            time_slots = TimeSlot.query.all()
            if not time_slots:
                print("No time slots available")
                return False
            
            # Generate schedule assignments
            schedule_assignments = []
            
            for course in courses:
                # Each course needs to be scheduled for its required hours per week
                hours_needed = course.hours_per_week
                
                for hour in range(hours_needed):
                    assignment = self._find_valid_assignment(
                        course, available_faculty[course.code], rooms, time_slots, 
                        schedule_assignments, batch
                    )
                    
                    if assignment:
                        schedule_assignments.append(assignment)
                    else:
                        print(f"Could not schedule {course.code} for hour {hour + 1}")
                        return False
            
            # Save all assignments to database
            for assignment in schedule_assignments:
                schedule = Schedule(
                    course_id=assignment['course'].id,
                    faculty_id=assignment['faculty'].id,
                    room_id=assignment['room'].id,
                    timeslot_id=assignment['timeslot'].id,
                    batch=batch
                )
                db.session.add(schedule)
            
            db.session.commit()
            return True
            
        except Exception as e:
            print(f"Error in timetable generation: {str(e)}")
            db.session.rollback()
            return False
    
    def _find_valid_assignment(self, course, faculty_list, rooms, time_slots, existing_assignments, batch):
        """
        Find a valid assignment for a course that doesn't conflict with existing assignments.
        """
        attempts = 0
        
        while attempts < self.max_attempts:
            # Randomly select faculty, room, and time slot
            faculty = random.choice(faculty_list)
            
            # Filter rooms based on course type
            suitable_rooms = []
            for room in rooms:
                if course.is_lab and room.room_type == 'lab':
                    suitable_rooms.append(room)
                elif not course.is_lab and room.room_type == 'classroom':
                    suitable_rooms.append(room)
                # Labs can also use classrooms if needed
                elif course.is_lab and room.room_type == 'classroom':
                    suitable_rooms.append(room)
            
            if not suitable_rooms:
                return None
            
            room = random.choice(suitable_rooms)
            timeslot = random.choice(time_slots)
            
            # Check for conflicts
            if self._check_conflicts(faculty, room, timeslot, existing_assignments):
                continue
            
            # Check if this assignment already exists in database for this batch
            existing_schedule = Schedule.query.filter_by(
                faculty_id=faculty.id,
                room_id=room.id,
                timeslot_id=timeslot.id,
                batch=batch
            ).first()
            
            if existing_schedule:
                attempts += 1
                continue
            
            # Valid assignment found
            return {
                'course': course,
                'faculty': faculty,
                'room': room,
                'timeslot': timeslot
            }
            
            attempts += 1
        
        return None
    
    def _check_conflicts(self, faculty, room, timeslot, existing_assignments):
        """
        Check if the proposed assignment conflicts with existing assignments.
        Returns True if there's a conflict, False otherwise.
        """
        for assignment in existing_assignments:
            # Same time slot conflicts
            if assignment['timeslot'].id == timeslot.id:
                # Faculty conflict - same faculty can't be in two places
                if assignment['faculty'].id == faculty.id:
                    return True
                
                # Room conflict - same room can't host two classes
                if assignment['room'].id == room.id:
                    return True
        
        return False
    
    def validate_timetable(self, batch):
        """
        Validate a generated timetable for conflicts.
        Returns a list of conflicts found.
        """
        conflicts = []
        schedules = Schedule.query.filter_by(batch=batch).all()
        
        for i, schedule1 in enumerate(schedules):
            for j, schedule2 in enumerate(schedules[i+1:], i+1):
                if schedule1.timeslot_id == schedule2.timeslot_id:
                    # Faculty conflict
                    if schedule1.faculty_id == schedule2.faculty_id:
                        conflicts.append({
                            'type': 'faculty_conflict',
                            'faculty': schedule1.faculty.name,
                            'courses': [schedule1.course.code, schedule2.course.code],
                            'timeslot': f"{schedule1.timeslot.day} {schedule1.timeslot.start_time}"
                        })
                    
                    # Room conflict
                    if schedule1.room_id == schedule2.room_id:
                        conflicts.append({
                            'type': 'room_conflict',
                            'room': schedule1.room.number,
                            'courses': [schedule1.course.code, schedule2.course.code],
                            'timeslot': f"{schedule1.timeslot.day} {schedule1.timeslot.start_time}"
                        })
        
        return conflicts
