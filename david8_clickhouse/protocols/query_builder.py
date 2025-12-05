from david8.protocols.dml import AliasedProtocol, ExprProtocol, FunctionProtocol
from david8.protocols.query_builder import QueryBuilderProtocol as _QueryBuilderProtocol

from ..protocols.select import SelectProtocol


class QueryBuilderProtocol(_QueryBuilderProtocol):
    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol:
        pass
