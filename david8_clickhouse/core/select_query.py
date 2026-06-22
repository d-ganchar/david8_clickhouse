
from david8.core.base_dql import BaseSelect as _BaseSelect
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import FunctionProtocol

from ..protocols.sql import SelectProtocol, TableFunctionProtocol


class ClickHouseSelect(_BaseSelect, SelectProtocol):
    final: bool = False
    _sample: int | float | None = None
    _sample_offset: int | float | None = None

    def from_table(self, table_name: str, alias: str = '', db_name: str = '', final: bool = False) -> SelectProtocol:
        super().from_table(table_name, alias, db_name)
        self.final = final
        return self

    def from_expr(
        self,
        expr: SelectProtocol | FunctionProtocol | TableFunctionProtocol,
        alias: str = ''
    ) -> SelectProtocol:
        return super().from_expr(expr, alias)

    def _from_to_sql(self, dialect: DialectProtocol) -> str:
        sql = super()._from_to_sql(dialect)
        if self.final and self.from_table_cnstr.table:
            sql = f'{sql} FINAL'

        if self._sample:
            sql = f'{sql} SAMPLE {self._sample}'
            if self._sample_offset:
                sql = f'{sql} OFFSET {self._sample_offset}'

        return sql

    def sample(self, value: int | float, offset: int | float = None) -> 'SelectProtocol':
        self._sample = value
        self._sample_offset = offset
        return self
