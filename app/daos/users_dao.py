import datetime

from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool

from app.utils import password_util
from app.models import User, SignUpRequest, Status


async def create_user(db_conn: AsyncConnectionPool, user: SignUpRequest) -> User:
    hashed_password = password_util.hash_password(user.password)
    async with db_conn.cursor() as cur:
        stmt = '''
        INSERT INTO users(username, email, first_name, last_name)
        VALUES (%s, %s, %s, %s)
        RETURNING id, time_created, time_modified;
        '''
        args = (user.username, user.email, user.first_name, user.last_name)
        await cur.execute(stmt, args)
        tmp = await cur.fetchone()
        user_id = tmp[0]
        time_created = tmp[1]
        time_modified = tmp[2]
        stmt = '''
        INSERT INTO user_passwords(id, password, expiry)
        VALUES (%s, %s, %s);
        '''
        expiry = time_created + datetime.timedelta(days=90)
        args = (user_id, hashed_password, expiry)
        await cur.execute(stmt, args)

        await db_conn.commit()

    user = user.to_user(user_id=user_id, status=Status.active, time_created=time_created, time_modified=time_modified)

    return user


async def get_user_by_email(db_conn: AsyncConnectionPool, email: str) -> User:
    async with db_conn.cursor(row_factory=class_row(User)) as cur:
        await cur.execute(
            '''
            SELECT id, email, username, first_name, last_name, status, time_created, time_modified
            FROM users
            WHERE users.email = %s
            LIMIT 1;
            ''',
            (email,)
        )
        user = await cur.fetchone()
    return user
    pass
