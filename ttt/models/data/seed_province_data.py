# seed_province_data.py

import asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from province_data import province_tax_list
from ttt.models.model_location import Province, TaxReduction

DATABASE_URL = "sqlite+aiosqlite:///database.db"


async def seed_data():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with async_session() as session:
        for name, code, percent in province_tax_list:
            province = Province(name=name, code=code)
            session.add(province)
            await session.flush()  # Get province.id
            tax = TaxReduction(province_id=province.id, tax_discount_percent=percent)
            session.add(tax)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_data())
