from collections.abc import Iterable

from david8.core.base_expressions import FullTableName
from david8.core.base_query_builder import BaseQueryBuilder as _BaseQueryBuilder
from david8.protocols.sql import AliasedProtocol, ExprProtocol, FunctionProtocol, QueryProtocol

from ..protocols.query_builder import QueryBuilderProtocol
from ..protocols.sql import CreateTableProtocol, InsertProtocol, SelectProtocol
from .ddl import CreateTable
from .dml import Insert
from .partitions import (
    BasePartitionFromOperation,
    BasePartitionOperation,
    BasePartitionToOperation,
    BasePartitionWithNameOperation,
)
from .select_query import ClickHouseSelect


class ClickHouseQueryBuilder(QueryBuilderProtocol, _BaseQueryBuilder):
    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol:
        return ClickHouseSelect(select_columns=args, dialect=self._dialect)

    def with_expr(self, *args: AliasedProtocol) -> SelectProtocol:
        return ClickHouseSelect(_with_expr=args, dialect=self._dialect)

    def drop_partitions(
        self,
        table: str,
        partitions: Iterable[str | int | tuple[int | str, ...]],
        db: str = None,
        on_cluster: str = None,
    ) -> QueryProtocol:
        return BasePartitionOperation(dialect=self._dialect, on_cluster=on_cluster,
                              table=FullTableName(table, db), partitions=partitions, operation_name='DROP')

    def attach_partition(self, table: str, partition: str | int, db: str = None,
                         from_tbl: str = None, from_db: str = None, on_cluster: str = None) -> QueryProtocol:
        return BasePartitionFromOperation(
            dialect=self._dialect,
            partitions=(partition,),
            table=FullTableName(table, db),
            on_cluster=on_cluster,
            from_=FullTableName(from_tbl, from_db),
            operation_name='ATTACH',
        )

    def detach_partition(
        self,
        table: str,
        partition: str | int,
        db: str = None,
        on_cluster: str = None
    ) -> QueryProtocol:
        return BasePartitionOperation(
            dialect=self._dialect,
            on_cluster=on_cluster,
            table=FullTableName(table, db),
            partitions=(partition,),
            operation_name='DETACH'
        )

    def fetch_partition(
        self,
        table: str,
        partition: str | int,
        from_: str,
        db: str = None,
        on_cluster: str = None,
    ) -> QueryProtocol:
        return BasePartitionFromOperation(
            dialect=self._dialect,
            on_cluster=on_cluster,
            table=FullTableName(table, db),
            partitions=(partition,),
            operation_name='FETCH',
            from_=from_,
        )

    def replace_partition(
        self,
        table: str,
        partition: str | int,
        db: str = None,
        from_tbl: str = None,
        from_db: str = None,
        on_cluster: str = None,
    ) -> QueryProtocol:
        return BasePartitionFromOperation(
            dialect=self._dialect,
            on_cluster=on_cluster,
            table=FullTableName(table, db),
            partitions=(partition,),
            operation_name='REPLACE',
            from_=FullTableName(from_tbl, from_db),
        )

    def move_partition_to_table(self, table: str, partition: str | int, to_tbl: str, db: str = None,
                                to_db: str = None, on_cluster: str = None) -> QueryProtocol:
        return BasePartitionToOperation(
            dialect=self._dialect,
            partitions=(partition,),
            operation_name='MOVE',
            table=FullTableName(table, db),
            on_cluster=on_cluster,
            to=FullTableName(to_tbl, to_db),
        )

    def move_partition_to_disk(self, table: str, partition: str | int, disk: str, db: str = None,
                               on_cluster: str = None) -> QueryProtocol:
        return BasePartitionToOperation(
            dialect=self._dialect,
            partitions=(partition,),
            operation_name='MOVE',
            to_mode='DISK',
            table=FullTableName(table, db),
            on_cluster=on_cluster,
            to=disk,
        )

    def move_partition_to_volume(self, table: str, partition: str | int, volume: str, db: str = None,
                                 on_cluster: str = None) -> QueryProtocol:
        return BasePartitionToOperation(
            dialect=self._dialect,
            partitions=(partition,),
            operation_name='MOVE',
            to_mode='VOLUME',
            table=FullTableName(table, db),
            on_cluster=on_cluster,
            to=volume,
        )

    def freeze_partition(self, table: str, partition: str | int, with_name: str = None, db: str = None,
                         on_cluster: str = None) -> QueryProtocol:
        return BasePartitionWithNameOperation(
            dialect=self._dialect,
            partitions=(partition,),
            operation_name='FREEZE',
            table=FullTableName(table, db),
            on_cluster=on_cluster,
            with_name=with_name,
        )

    def unfreeze_partition(self, table: str, partition: str | int, with_name: str = None, db: str = None,
                           on_cluster: str = None) -> QueryProtocol:
        return BasePartitionWithNameOperation(
            dialect=self._dialect,
            partitions=(partition,),
            operation_name='UNFREEZE',
            table=FullTableName(table, db),
            on_cluster=on_cluster,
            with_name=with_name,
        )

    def create_table_as(self, query: SelectProtocol, table: str, db: str = '') -> CreateTableProtocol:
        return CreateTable(dialect=self._dialect, query=query, table=FullTableName(table, db))

    def insert(self) -> InsertProtocol:
        return Insert(dialect=self._dialect)
