from app.db.connection import db, metadata, engine, connection

# load the table structure from the DB once, when the module is imported
schedule = db.Table('Schedule', metadata, autoload_with=engine)


def get_available_slots(position, start_date, limit=3):
    """The first `limit` free slots for the position, from start_date onward (earliest first)"""
    query = (
        db.select(schedule)
        .where(
            schedule.columns.position == position,      # exact match - PDF names = DB names
            schedule.columns.available == True,
            schedule.columns.date >= start_date,
        )
        .order_by(schedule.columns.date, schedule.columns.time)
        .limit(limit)
    )
    return connection.execute(query).fetchall()


def find_slot(position, slot_date, slot_time):
    """The ScheduleID of a specific slot (position + date + time), or None if it doesn't exist"""
    query = db.select(schedule.columns.ScheduleID).where(
        schedule.columns.position == position,
        schedule.columns.date == slot_date,
        schedule.columns.time == slot_time,
    )
    return connection.execute(query).scalar()


def reserve_slot(schedule_id):
    """Mark the slot as taken. Returns True if reserved, False if it was already taken / doesn't exist"""
    query = (
        db.update(schedule)
        .where(
            schedule.columns.ScheduleID == schedule_id,
            schedule.columns.available == True,    
        )
        .values(available=False)
    )
    result = connection.execute(query)
    connection.commit()                            
    return result.rowcount == 1                     
