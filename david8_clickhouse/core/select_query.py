import dataclasses

from david8.core.arg_convertors import to_col_or_expr
from david8.core.base_dql import BaseSelect as _BaseSelect
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import FunctionProtocol

from ..protocols.sql import SelectProtocol, TableFunctionProtocol


@dataclasses.dataclass
class ClickHouseSelect(_BaseSelect, SelectProtocol):
    final: bool = False
    _sample: int | float | None = None
    _sample_offset: int | float | None = None
    _limit_by: tuple[tuple[str, ...], int | None, int | None] = dataclasses.field(default_factory=tuple)

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

    def limit_by(self, *args: str, limit: int = None, offset: int = None) -> 'SelectProtocol':
        self._limit_by = (args, limit, offset, )
        return self

    def _limit_by_to_sql(self, dialect: DialectProtocol) -> str:
        if not self._limit_by:
            return ''

        names, limit, offset = self._limit_by

        if self._limit_by[0]:
            fields = ', '.join(to_col_or_expr(f, dialect) for f in names)
        else:
            fields = 'ALL'

        limit_str = ''
        if limit and offset:
            limit_str = f' {limit}, {offset}'
        elif limit:
            limit_str = f' {limit}'

        return f' LIMIT{limit_str} BY {fields}'


    def _get_sql(self, dialect: DialectProtocol):
        with_query = self._with_queries_to_sql(dialect)
        select = self._columns_to_sql(dialect)
        from_ref = self._from_to_sql(dialect)
        joins = self._joins_to_sql(dialect)
        where = self.where_construction.get_sql(dialect)
        group_by = self._group_by_to_sql(dialect)
        having = self._having_to_sql(dialect)
        window = self._windows_to_sql(dialect)
        union = self._union_to_sql(dialect)
        order_by = self._order_by_to_sql()
        select_str = ''.join([
            select,
            from_ref,
            joins,
            where,
            group_by,
            order_by,
            having,
            window,
            self._limit_by_to_sql(dialect),
            f' LIMIT {self.limit_value}' if self.limit_value else '',
            f' OFFSET {self.offset_value}' if self.offset_value else '',
            union,
        ])

        return f'{with_query}SELECT {select_str}'
