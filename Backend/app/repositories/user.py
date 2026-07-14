from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserTable, BannedUserTable, BanCode


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _select_user(self, **filters) -> UserTable | None:
        query = select(UserTable).filter_by(**filters)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, id: int):
        await self._select_user(id=id)

    async def get_user_by_username(self, username: str):
        await self._select_user(username=username)

    async def get_user_by_tg_id(self, tg_id: int):
        await self._select_user(telegram_id=tg_id)

    async def add_user(self, username: str, password_hash: str, tg_id: int, need_commit: bool = False):
        new_user = UserTable(username=username, password_hash=password_hash, telegram_id=tg_id)
        self.session.add(new_user)
        if need_commit:
            await self.session.commit()
            await self.session.refresh(new_user)
        else: await self.session.flush()
        return new_user

    async def get_user_ban_data(self, user_id: int):
        query = select(BannedUserTable).filter_by(user_id=user_id, is_active=True)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def ban_user(self, user_id: int, ban_code: BanCode, duration: int | None, need_commit: bool = False):
        new_ban = BannedUserTable(user_id=user_id, ban_code=ban_code, duration=duration)
        self.session.add(new_ban)
        if need_commit:
            await self.session.commit()
            await self.session.refresh(new_ban)
        else: await self.session.flush()
        return new_ban