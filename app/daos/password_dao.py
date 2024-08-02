from psycopg_pool import AsyncConnectionPool
from app.exceptions import UserNotFound


async def get_user_password(db_conn: AsyncConnectionPool, email: str) -> str:
    async with db_conn.cursor() as cur:
        stmt = '''
        SELECT password
        from user_passwords up
        INNER JOIN users u
            ON u.id = up.id
        WHERE u.email = %s;
        '''
        args = (email,)
        await cur.execute(stmt, args)
        ret = await cur.fetchone()
        if ret is None:
            raise UserNotFound(f"User: {email} does not exist")
        hashed_password = ret[0]

    return hashed_password
