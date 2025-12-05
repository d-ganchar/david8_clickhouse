from david8.core.base_query_builder import BaseQueryBuilder as _BaseQueryBuilder
from david8.protocols.dml import AliasedProtocol, ExprProtocol, FunctionProtocol

from .select_query import ClickHouseSelect
from ..protocols.query_builder import QueryBuilderProtocol
from ..protocols.select import SelectProtocol


class ClickHouseQueryBuilder(QueryBuilderProtocol, _BaseQueryBuilder):
    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol:
        return ClickHouseSelect(select_columns=args, dialect=self._dialect)
