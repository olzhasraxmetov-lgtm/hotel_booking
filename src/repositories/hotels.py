from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM
from sqlalchemy import insert, select, func

class HotelsRepository(BaseRepository):
    model = HotelsORM

    async def get_all(self,location,title,limit,offset):

        query = select(HotelsORM)
        if location:
            query = query.filter(func.lower(HotelsORM.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsORM.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        res = await self.session.execute(query)
        return res.scalars().all()