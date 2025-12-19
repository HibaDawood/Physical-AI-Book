from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.bookmark import ChapterBookmarkCreate, ChapterBookmarkUpdate, ChapterBookmark
from src.database.models import ChapterBookmarkDB


class ChapterBookmarkService:
    @staticmethod
    async def create_bookmark(
        db: AsyncSession, 
        bookmark: ChapterBookmarkCreate
    ) -> ChapterBookmark:
        db_bookmark = ChapterBookmarkDB(
            **bookmark.model_dump(exclude_unset=True)
        )
        db.add(db_bookmark)
        await db.commit()
        await db.refresh(db_bookmark)
        return ChapterBookmark.model_validate(db_bookmark)

    @staticmethod
    async def get_bookmark(
        db: AsyncSession, 
        bookmark_id: UUID
    ) -> Optional[ChapterBookmark]:
        result = await db.execute(
            select(ChapterBookmarkDB).where(ChapterBookmarkDB.id == bookmark_id)
        )
        db_bookmark = result.scalar_one_or_none()
        if db_bookmark:
            return ChapterBookmark.model_validate(db_bookmark)
        return None

    @staticmethod
    async def get_user_bookmarks(
        db: AsyncSession,
        user_id: UUID
    ) -> List[ChapterBookmark]:
        result = await db.execute(
            select(ChapterBookmarkDB).where(ChapterBookmarkDB.user_id == user_id)
        )
        db_bookmarks = result.scalars().all()
        return [ChapterBookmark.model_validate(db_bookmark) for db_bookmark in db_bookmarks]

    @staticmethod
    async def update_bookmark(
        db: AsyncSession,
        bookmark_id: UUID,
        bookmark_update: ChapterBookmarkUpdate
    ) -> Optional[ChapterBookmark]:
        result = await db.execute(
            select(ChapterBookmarkDB).where(ChapterBookmarkDB.id == bookmark_id)
        )
        db_bookmark = result.scalar_one_or_none()
        
        if not db_bookmark:
            return None

        update_data = bookmark_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_bookmark, field, value)
            
        await db.commit()
        await db.refresh(db_bookmark)
        return ChapterBookmark.model_validate(db_bookmark)

    @staticmethod
    async def delete_bookmark(
        db: AsyncSession,
        bookmark_id: UUID
    ) -> bool:
        result = await db.execute(
            select(ChapterBookmarkDB).where(ChapterBookmarkDB.id == bookmark_id)
        )
        db_bookmark = result.scalar_one_or_none()
        
        if not db_bookmark:
            return False

        await db.delete(db_bookmark)
        await db.commit()
        return True