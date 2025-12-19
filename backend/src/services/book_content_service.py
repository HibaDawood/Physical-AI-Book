from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.models.book_content import BookContentCreate, BookContentUpdate, BookContent
from src.database.models import BookContentDB


class BookContentService:
    @staticmethod
    async def create_book_content(
        db: AsyncSession, 
        book_content: BookContentCreate
    ) -> BookContent:
        db_book_content = BookContentDB(
            **book_content.model_dump(exclude_unset=True)
        )
        db.add(db_book_content)
        await db.commit()
        await db.refresh(db_book_content)
        return BookContent.model_validate(db_book_content)

    @staticmethod
    async def get_book_content(
        db: AsyncSession, 
        content_id: UUID
    ) -> Optional[BookContent]:
        result = await db.execute(
            select(BookContentDB).where(BookContentDB.id == content_id)
        )
        db_book_content = result.scalar_one_or_none()
        if db_book_content:
            return BookContent.model_validate(db_book_content)
        return None

    @staticmethod
    async def get_book_contents(
        db: AsyncSession,
        language: Optional[str] = None,
        chapter_number: Optional[int] = None,
        parent_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[BookContent]:
        query = select(BookContentDB)
        
        if language:
            query = query.where(BookContentDB.language == language)
        if chapter_number is not None:
            query = query.where(BookContentDB.chapter_number == chapter_number)
        if parent_id:
            query = query.where(BookContentDB.parent_id == parent_id)
            
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        db_book_contents = result.scalars().all()
        return [BookContent.model_validate(db_book_content) for db_book_content in db_book_contents]

    @staticmethod
    async def get_chapters(
        db: AsyncSession,
        parent_id: Optional[UUID] = None
    ) -> List[BookContent]:
        query = select(BookContentDB).where(BookContentDB.chapter_number.is_not(None))
        
        if parent_id:
            query = query.where(BookContentDB.parent_id == parent_id)
        else:
            query = query.where(BookContentDB.parent_id.is_(None))
            
        query = query.order_by(BookContentDB.chapter_number)
        
        result = await db.execute(query)
        db_book_contents = result.scalars().all()
        return [BookContent.model_validate(db_book_content) for db_book_content in db_book_contents]

    @staticmethod
    async def update_book_content(
        db: AsyncSession,
        content_id: UUID,
        book_content_update: BookContentUpdate
    ) -> Optional[BookContent]:
        result = await db.execute(
            select(BookContentDB).where(BookContentDB.id == content_id)
        )
        db_book_content = result.scalar_one_or_none()
        
        if not db_book_content:
            return None

        update_data = book_content_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book_content, field, value)
            
        await db.commit()
        await db.refresh(db_book_content)
        return BookContent.model_validate(db_book_content)

    @staticmethod
    async def delete_book_content(
        db: AsyncSession,
        content_id: UUID
    ) -> bool:
        result = await db.execute(
            select(BookContentDB).where(BookContentDB.id == content_id)
        )
        db_book_content = result.scalar_one_or_none()
        
        if not db_book_content:
            return False

        await db.delete(db_book_content)
        await db.commit()
        return True