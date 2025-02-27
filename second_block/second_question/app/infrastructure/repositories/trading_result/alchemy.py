import builtins
from collections.abc import Sequence
from datetime import date
from typing import (
    Any,
    override, Optional
)

from sqlalchemy import (
    Result,
    Row,
    RowMapping,
    and_,
    delete,
    insert,
    select,
    update,
    distinct,
    text,
    func
)

from app.domain.entities.trading_result import TradingResultEntity
from app.infrastructure.repositories.base import SQLAlchemyAbstractRepository
from app.infrastructure.repositories.trading_result.base import TradingResultRepository


class SQLAlchemyTradingResultRepository(SQLAlchemyAbstractRepository, TradingResultRepository):
    @override
    async def get_by_exchange_product_id(
            self,
            exchange_product_id: str,
            start: int = 0,
            limit: int = 10
    ) -> list[TradingResultEntity]:
        result: Result = await self._session.execute(
            select(TradingResultEntity)
            .filter_by(exchange_product_id=exchange_product_id)
            .offset(start)
            .limit(limit)
        )

        trading_result_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(trading_result_entities, list)
        for vote in trading_result_entities:
            assert isinstance(vote, TradingResultEntity)

        return trading_result_entities

    @override
    async def get_by_exchange_product_name(
            self,
            exchange_product_name: str,
            start: int = 0,
            limit: int = 10
    ) -> list[TradingResultEntity]:
        result: Result = await self._session.execute(
            select(TradingResultEntity)
            .filter_by(exchange_product_name=exchange_product_name)
            .offset(start)
            .limit(limit)
        )

        trading_result_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(trading_result_entities, list)
        for vote in trading_result_entities:
            assert isinstance(vote, TradingResultEntity)

        return trading_result_entities

    @override
    async def get_by_delivery_basis_name(
            self,
            delivery_basis_name: str,
            start: int = 0,
            limit: int = 10
    ) -> list[TradingResultEntity]:
        result: Result = await self._session.execute(
            select(TradingResultEntity)
            .filter_by(delivery_basis_name=delivery_basis_name)
            .offset(start)
            .limit(limit)
        )

        trading_result_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(trading_result_entities, list)
        for vote in trading_result_entities:
            assert isinstance(vote, TradingResultEntity)

        return trading_result_entities

    @override
    async def add(self, model: TradingResultEntity) -> TradingResultEntity:
        result: Result = await self._session.execute(
            insert(TradingResultEntity).values(**await model.to_dict()).returning(TradingResultEntity)
        )
        return result.scalar_one()

    @override
    async def get(self, oid: str) -> TradingResultEntity | None:
        result: Result = await self._session.execute(select(TradingResultEntity).filter_by(oid=oid))

        return result.scalar_one()

    @override
    async def update(self, oid: str, model: TradingResultEntity) -> TradingResultEntity:
        result: Result = await self._session.execute(
            update(TradingResultEntity)
            .filter_by(oid=oid)
            .values(**await model.to_dict(exclude={"id"}))
            .returning(TradingResultEntity)
        )

        return result.scalar_one()

    @override
    async def list(self, start: int = 0, limit: int = 10) -> list[TradingResultEntity]:
        result: Result = await self._session.execute(select(TradingResultEntity).offset(start).limit(limit))

        trading_result_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(trading_result_entities, list)

        for entity in trading_result_entities:
            assert isinstance(entity, TradingResultEntity)

        return trading_result_entities

    @override
    async def list_by_date(
            self,
            start_date: date,
            end_date: date,
            start: int = 0,
            limit: int = 10
    ) -> builtins.list[TradingResultEntity]:

        result: Result = await self._session.execute(
            select(TradingResultEntity).where(
                and_(
                    TradingResultEntity.date >= start_date,
                    TradingResultEntity.date <= end_date
                )
            )
            .offset(start)
            .limit(limit)
        )

        trading_result_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(trading_result_entities, list)

        for entity in trading_result_entities:
            assert isinstance(entity, TradingResultEntity)

        return trading_result_entities

    @override
    async def get_unique_trading_dates(
            self,
            start_date: date,
            end_date: date,
            start: int = 0,
            limit: int = 10
    ) -> builtins.list[date]:
        """
        Возвращает список уникальных дат торгов за указанный период.
        """
        result: Result = await self._session.execute(
            select(distinct(TradingResultEntity.date)).where(  # noqa
                and_(
                    TradingResultEntity.date >= start_date,
                    TradingResultEntity.date <= end_date
                )
            )
            .order_by(text("date desc"))
            .offset(start)
            .limit(limit)
        )

        unique_dates: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(unique_dates, list)

        for entity in unique_dates:
            assert isinstance(entity, date)

        return unique_dates

    @override
    async def delete(self, oid: str) -> None:
        await self._session.execute(delete(TradingResultEntity).filter_by(oid=oid))

    @override
    async def list_filtered(
            self,
            oil_id: Optional[str],
            delivery_type_id: Optional[str],
            delivery_basis_id: Optional[str],
            start: int = 0,
            limit: int = 10
    ) -> builtins.list[TradingResultEntity]:

        # Создаем базовый запрос
        query = select(TradingResultEntity)

        # Добавляем фильтры только если параметры не None
        if oil_id is not None:
            query = query.filter(func.substr(TradingResultEntity.exchange_product_id, 1, 4) == oil_id) # noqa
        if delivery_type_id is not None:
            query = query.filter(func.substr(TradingResultEntity.exchange_product_id, func.length(TradingResultEntity.exchange_product_id), 1) == delivery_type_id) # noqa
        if delivery_basis_id is not None:
            query = query.filter(func.substr(TradingResultEntity.exchange_product_id, 5, 3) == delivery_basis_id) # noqa

        # Применяем пагинацию
        query = query.offset(start).limit(limit)

        # Выполняем запрос
        result: Result = await self._session.execute(query)

        # Получаем результаты
        trading_result_entities: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(trading_result_entities, list)

        for entity in trading_result_entities:
            assert isinstance(entity, TradingResultEntity)

        return trading_result_entities
