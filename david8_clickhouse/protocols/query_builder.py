from collections.abc import Iterable

from david8.protocols.query_builder import QueryBuilderProtocol as _QueryBuilderProtocol
from david8.protocols.sql import AliasedProtocol, ExprProtocol, FunctionProtocol, QueryProtocol

from ..protocols.sql import CreateTableProtocol, InsertProtocol, SelectProtocol


class QueryBuilderProtocol(_QueryBuilderProtocol):
    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol:
        pass

    def drop_partitions(
        self,
        table: str,
        partitions: Iterable[str | int | tuple[int | str, ...]],
        db: str = None,
        on_cluster: str = None,
    ) -> QueryProtocol:
        pass

    def attach_partition(
        self,
        table: str,
        partition: str | int,
        db: str = None,
        from_tbl: str = None,
        from_db: str = None,
        on_cluster: str = None,
    ) -> QueryProtocol:
        pass

    def detach_partition(
        self,
        table: str,
        partition: str | int,
        db: str = None,
        on_cluster: str = None
    ) -> QueryProtocol:
        pass

    def freeze_partition(
        self,
        table: str,
        partition: str | int,
        with_name: str = None,
        db: str = None,
        on_cluster: str = None
    ) -> QueryProtocol:
        pass

    def unfreeze_partition(
        self,
        table: str,
        partition: str | int,
        with_name: str = None,
        db: str = None,
        on_cluster: str = None
    ) -> QueryProtocol:
        pass

    def replace_partition(
        self,
        table: str,
        partition: str | int,
        db: str = None,
        from_tbl: str = None,
        from_db: str = None,
        on_cluster: str = None,
    ) -> QueryProtocol:
        pass

    def fetch_partition(
        self,
        table: str,
        partition: str | int,
        from_: str,
        db: str = None,
        on_cluster: str = None,
    ) -> QueryProtocol:
        pass

    def move_partition_to_table(
        self,
        table: str,
        partition: str | int,
        to_tbl: str,
        db: str = None,
        to_db: str = None,
        on_cluster: str = None,
    ) -> QueryProtocol:
        pass

    def move_partition_to_disk(
        self,
        table: str,
        partition: str | int,
        disk: str,
        db: str = None,
        on_cluster: str = None,
    ) -> QueryProtocol:
        pass

    def move_partition_to_volume(
        self,
        table: str,
        partition: str | int,
        volume: str,
        db: str = None,
        on_cluster: str = None,
    ) -> QueryProtocol:
        pass

    def create_table_as(self, query: SelectProtocol, table: str, db: str = '') -> CreateTableProtocol:
        pass

    def insert(self) -> InsertProtocol:
        pass
