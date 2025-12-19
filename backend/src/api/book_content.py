from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from uuid import UUID
from src.models.book_content import BookContent, BookContentCreate, BookContentUpdate
from src.models.bookmark import ChapterBookmark, ChapterBookmarkCreate
from src.services.book_content_service import BookContentService
from src.services.bookmark_service import ChapterBookmarkService
from src.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/book/contents", response_model=List[BookContent])
async def get_book_contents(
    language: Optional[str] = Query(None, regex=r"^[a-z]{2}$"),
    chapter_number: Optional[int] = Query(None, ge=0),
    parent_id: Optional[UUID] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """
    Fetch structured book content based on filters
    """
    contents = await BookContentService.get_book_contents(
        db, language, chapter_number, parent_id, skip, limit
    )
    return contents


@router.get("/book/contents/{content_id}", response_model=BookContent)
async def get_book_content(
    content_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Fetch specific content by ID
    """
    content = await BookContentService.get_book_content(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.get("/book/chapters", response_model=List[BookContent])
async def get_book_chapters(
    parent_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get chapter list with hierarchy
    """
    chapters = await BookContentService.get_chapters(db, parent_id)
    return chapters


@router.post("/book/contents", response_model=BookContent)
async def create_book_content(
    book_content: BookContentCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create new book content
    """
    content = await BookContentService.create_book_content(db, book_content)
    return content


@router.put("/book/contents/{content_id}", response_model=BookContent)
async def update_book_content(
    content_id: UUID,
    book_content_update: BookContentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update existing book content
    """
    content = await BookContentService.update_book_content(db, content_id, book_content_update)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.delete("/book/contents/{content_id}")
async def delete_book_content(
    content_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete book content
    """
    success = await BookContentService.delete_book_content(db, content_id)
    if not success:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"message": "Content deleted successfully"}


@router.post("/user/bookmarks", response_model=ChapterBookmark)
async def create_bookmark(
    bookmark: ChapterBookmarkCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a bookmark
    """
    new_bookmark = await ChapterBookmarkService.create_bookmark(db, bookmark)
    return new_bookmark


@router.get("/user/bookmarks", response_model=List[ChapterBookmark])
async def get_user_bookmarks(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user bookmarks
    """
    bookmarks = await ChapterBookmarkService.get_user_bookmarks(db, user_id)
    return bookmarks


@router.put("/user/bookmarks/{bookmark_id}", response_model=ChapterBookmark)
async def update_bookmark(
    bookmark_id: UUID,
    bookmark_update: ChapterBookmarkCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a bookmark
    """
    bookmark = await ChapterBookmarkService.update_bookmark(db, bookmark_id, bookmark_update)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@router.delete("/user/bookmarks/{bookmark_id}")
async def delete_bookmark(
    bookmark_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a bookmark
    """
    success = await ChapterBookmarkService.delete_bookmark(db, bookmark_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return {"message": "Bookmark deleted successfully"}