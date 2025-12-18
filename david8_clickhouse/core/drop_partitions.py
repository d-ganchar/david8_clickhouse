import dataclasses
from collections.abc import Iterable

from david8.core.base_expressions import FullTableName
from david8.core.base_query import BaseQuery
from david8.protocols.dialect import DialectProtocol


@dataclasses.dataclass(slots=True)
class DropPartitions(BaseQuery):
    partitions: Iterable[str | int | tuple[int | str, ...]]
    table: FullTableName = dataclasses.field(default_factory=FullTableName)
    on_cluster: str = None

    def _render_sql_prefix(self, dialect: DialectProtocol) -> str:
        return f'ALTER TABLE {self.table.get_sql(dialect)} '

    def _render_sql(self, dialect: DialectProtocol) -> str:
        if isinstance(self.on_cluster, str):
            cluster = f"'{self.on_cluster}'" if self.on_cluster.startswith('{') else self.on_cluster
            return f"ON CLUSTER {cluster} "

        return ''

    def _render_sql_postfix(self, dialect: DialectProtocol) -> str:
        partitions = ()
        for partition in self.partitions:
            if isinstance(partition, (int, tuple)):
                partitions += (f'DROP PARTITION {partition}',)
                continue

            partitions += (f"DROP PARTITION '{partition}'",)

        return f'{", ".join(partitions)}'
