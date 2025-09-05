from app import db
from datetime import datetime

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    hours_per_week = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    is_lab = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Course {self.code}: {self.name}>'

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    subjects = db.Column(db.Text)  # Comma-separated course codes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Faculty {self.name}>'

    def get_subjects_list(self):
        if self.subjects:
            return [s.strip() for s in self.subjects.split(',')]
        return []

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    room_type = db.Column(db.String(20), nullable=False)  # 'classroom' or 'lab'
    building = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Room {self.number} ({self.room_type})>'

class TimeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)  # Monday, Tuesday, etc.
    start_time = db.Column(db.String(10), nullable=False)  # HH:MM format
    end_time = db.Column(db.String(10), nullable=False)  # HH:MM format
    period_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TimeSlot {self.day} {self.start_time}-{self.end_time}>'

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    timeslot_id = db.Column(db.Integer, db.ForeignKey('time_slot.id'), nullable=False)
    batch = db.Column(db.String(50), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    course = db.relationship('Course', backref='schedules')
    faculty = db.relationship('Faculty', backref='schedules')
    room = db.relationship('Room', backref='schedules')
    timeslot = db.relationship('TimeSlot', backref='schedules')

    def __repr__(self):
        return f'<Schedule {self.course.code} - {self.faculty.name} - {self.room.number}>'

class TimetableGeneration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='generated')  # generated, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TimetableGeneration {self.name}>'
