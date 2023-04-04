from typing import List
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.category import Category
from models.subcategory import Subcategory
from models.ad import Ad


async def get_category_by_id(id: int, session: AsyncSession) -> Category | None:
    query = await session.execute(select(Category).where(Category.id == id))
    category = query.scalar_one_or_none()
    return category


async def get_category_by_name(name: str, session: AsyncSession) -> Category | None:
    query = await session.execute(select(Category).where(Category.category_name == name))
    category = query.scalar_one_or_none()
    return category


async def get_category_count(session: AsyncSession) -> int | None:
    query = await session.execute(select(func.count(Category.id)))
    category_count = query.scalar_one_or_none()
    return category_count


async def get_all_categories(session: AsyncSession) -> List[Category]:
    query = await session.execute(select(Category))
    all_categories = query.scalars().all()
    return all_categories


async def popular_categories(session: AsyncSession) -> List[Category]:
    query = await session.execute(select(
            Category, func.count(Ad.id))
            .join(Subcategory, Subcategory.id == Ad.subcategory_id)
            .join(Category, Subcategory.id == Category.id)
            .group_by(Category.id)
            .limit(10)
    )
    popular_categories = query.scalars().all()
    return popular_categories


async def create_category(category_name: str, session: AsyncSession) -> Category | None:
    category = Category(
        category_name = category_name
    )
    
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category



async def get_subcategory_by_id(id: int, session: AsyncSession) -> Subcategory | None:
    query = await session.execute(select(Subcategory).where(Subcategory.id == id))
    subcategory = query.scalar_one_or_none()
    return subcategory


async def get_subcategory_by_name(name: str, session: AsyncSession) -> Subcategory | None:
    query = await session.execute(select(Subcategory).where(Subcategory.subcategory_name == name))
    subcategory = query.scalar_one_or_none()
    return subcategory


async def get_subcategory_count(session: AsyncSession) -> int | None:
    query = await session.execute(select(func.count(Subcategory.id)))
    subcategory_count = query.scalar_one_or_none()
    return subcategory_count


async def get_all_subcategories(session: AsyncSession) -> List[Subcategory]:
    query = await session.execute(select(Subcategory))
    all_subcategories = query.scalars().all()
    return all_subcategories


async def create_subcategory(subcategory_name: str, category_id, session: AsyncSession) -> Subcategory | None:
    subcategory = Subcategory(
        subcategory_name = subcategory_name,
        category_id = category_id
    )
    
    session.add(subcategory)
    await session.commit()
    await session.refresh(subcategory)
    return subcategory