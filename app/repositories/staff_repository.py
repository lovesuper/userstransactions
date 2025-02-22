from typing import Optional

from sqlalchemy.future import select

from app.domain.staff import Staff


async def get_staff_by_id(db, staff_id: str) -> Optional[Staff]:
    result = await db.execute(select(Staff).filter(Staff.id == staff_id))

    return result.scalar_one_or_none()


async def get_staff_by_login(db, login: str) -> Optional[Staff]:
    result = await db.execute(select(Staff).filter(Staff.login == login))

    return result.scalar_one_or_none()


async def create_staff(db, staff: Staff) -> Staff:
    db.add(staff)
    await db.commit()
    await db.refresh(staff)

    return staff
