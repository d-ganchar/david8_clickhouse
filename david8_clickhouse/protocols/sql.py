from typing import Union

from david8.protocols.sql import ExprProtocol, FunctionProtocol, QueryProtocol
from david8.protocols.sql import InsertProtocol as _InsertProtocol
from david8.protocols.sql import SelectProtocol as _SelectProtocol


class TableFunctionProtocol(ExprProtocol): ...

class SelectProtocol(_SelectProtocol):
    def from_table(
        self,
        table_name: str,
        alias: str = '',
        db_name: str = '',
        final: bool = False
    ) -> 'SelectProtocol': ...

    def sample(self, value: int | float, offset: int | float = None) -> 'SelectProtocol': ...

    def from_expr(
        self,
        expr:
        Union['SelectProtocol', FunctionProtocol, TableFunctionProtocol],
        alias: str = '',
    ) -> 'SelectProtocol': ...

    def limit_by(self, *args: str, limit: int = None, offset: int = None) -> 'SelectProtocol': ...


class CreateTableProtocol(QueryProtocol):
    def engine(self, value: str) -> 'CreateTableProtocol': ...

    def partition_by(self, *args: str | FunctionProtocol) -> 'CreateTableProtocol': ...

    def order_by(self, *args: str | FunctionProtocol) -> 'CreateTableProtocol': ...

    def if_not_exists(self) -> 'CreateTableProtocol': ...

    def on_cluster(self, name: str) -> 'CreateTableProtocol': ...


class InsertProtocol(_InsertProtocol):
    def into_table_fn(self, fn: TableFunctionProtocol) -> 'InsertProtocol': ...
