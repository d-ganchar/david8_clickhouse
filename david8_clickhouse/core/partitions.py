import dataclasses
from collections.abc import Iterable

from david8.core.base_expressions import FullTableName
from david8.core.base_query import BaseQuery
from david8.protocols.dialect import DialectProtocol

from ..core.expressions import on_cluster


@dataclasses.dataclass(slots=True)
class BasePartitionOperation(BaseQuery):
    partitions: Iterable[str | int | tuple[int | str, ...]]
    operation_name: str = ''
    table: FullTableName = dataclasses.field(default_factory=FullTableName)
    on_cluster: str = None

    def _render_sql_prefix(self, dialect: DialectProtocol) -> str:
        return f'ALTER TABLE {self.table.get_sql(dialect)} '

    def _render_sql(self, dialect: DialectProtocol) -> str:
        cluster = on_cluster(self.on_cluster)
        if cluster:
            return f'{cluster} '
        return ''

    def _render_sql_postfix(self, dialect: DialectProtocol) -> str:
        partitions = ()
        for partition in self.partitions:
            if isinstance(partition, (int, tuple)):
                partitions += (f'{self.operation_name} PARTITION {partition}',)
                continue

            partitions += (f"{self.operation_name} PARTITION '{partition}'",)

        return f'{", ".join(partitions)}'


@dataclasses.dataclass
class BasePartitionWithNameOperation(BasePartitionOperation):
    with_name: str = ''

    def _render_sql_postfix(self, dialect: DialectProtocol) -> str:
        sql = super()._render_sql_postfix(dialect)
        if self.with_name:
            return f"{sql} WITH NAME '{self.with_name}'"
        return sql


@dataclasses.dataclass
class BasePartitionFromOperation(BasePartitionOperation):
    from_: FullTableName | str = dataclasses.field(default_factory=FullTableName)

    def _render_sql_postfix(self, dialect: DialectProtocol) -> str:
        sql = super()._render_sql_postfix(dialect)
        from_ = self.from_.get_sql(dialect) if isinstance(self.from_, FullTableName) else f"'{self.from_}'"
        if from_:
            return f"{sql} FROM {from_}"
        return sql


@dataclasses.dataclass
class BasePartitionToOperation(BasePartitionOperation):
    to_mode: str = 'TABLE'
    to: FullTableName | str = ''

    def _render_sql_postfix(self, dialect: DialectProtocol) -> str:
        sql = super()._render_sql_postfix(dialect)
        to = self.to.get_sql(dialect) if isinstance(self.to, FullTableName) else f"'{self.to}'"
        return f'{sql} TO {self.to_mode} {to}'
