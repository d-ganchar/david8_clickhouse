import dataclasses

from david8.core.arg_convertors import to_col_or_expr
from david8.core.fn_generator import FnCallableFactory as _Factory
from david8.core.fn_generator import FnCallableFactory as _FnCallableFactory
from david8.core.fn_generator import Function as _Fn
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import ExprProtocol, FunctionProtocol, PredicateProtocol


@dataclasses.dataclass(slots=True)
class _MultiIfFn(_Fn):
    args: tuple[tuple[PredicateProtocol, str | ExprProtocol], ...]
    else_: str | ExprProtocol

    def _get_sql(self, dialect: DialectProtocol) -> str:
        items = ()
        for predicate, value in self.args:
            items += (predicate.get_sql(dialect), to_col_or_expr(value, dialect), )

        items += (to_col_or_expr(self.else_, dialect), )
        return f'{self.name}({", ".join(items)})'


@dataclasses.dataclass(slots=True)
class MultiIfFactory(_Factory):
    def __call__(
        self,
        *args: tuple[PredicateProtocol, str | ExprProtocol],
        else_: str | ExprProtocol,
    ) -> FunctionProtocol:
        return _MultiIfFn('multiIf', args, else_)


@dataclasses.dataclass(slots=True)
class _AttrNamesFn(_Fn):
    dict_name: str
    attr_names: tuple[str, ...] | str
    id_expr: str | ExprProtocol
    default_value_expr: int | str | float | ExprProtocol = None

    def _get_sql(self, dialect: DialectProtocol) -> str:
        if isinstance(self.attr_names, str):
            attr_names = f"'{self.attr_names}'"
        else:
            attr_names = ','.join(f"'{v}'" for v in self.attr_names)
            attr_names = f'({attr_names})'

        args = (f"'{self.dict_name}'", attr_names, to_col_or_expr(self.id_expr, dialect))
        if self.default_value_expr is not None:
            if isinstance(self.default_value_expr, (int, float)):
                args += (f'{self.default_value_expr}',)
            elif isinstance(self.default_value_expr, ExprProtocol):
                args += (self.default_value_expr.get_sql(dialect),)
            else:
                args += (f"'{self.default_value_expr}'",)

        return f"{self.name}({', '.join(args)})"


@dataclasses.dataclass(slots=True)
class AttrNamesFactory(_FnCallableFactory):
    def __call__(
        self,
        dict_name: str,
        attr_names: str | tuple[str, ...],
        id_expr: str | ExprProtocol
    ) -> FunctionProtocol:
        return _AttrNamesFn(self.name, dict_name=dict_name, attr_names=attr_names, id_expr=id_expr)


@dataclasses.dataclass(slots=True)
class AttrNamesDefaultFactory(_FnCallableFactory):
    def __call__(
        self,
        dict_name: str,
        attr_names: str | tuple[str, ...],
        id_expr: str | ExprProtocol,
        default_value_expr: int | str | float | ExprProtocol
    ) -> FunctionProtocol:
        return _AttrNamesFn(self.name, dict_name=dict_name, attr_names=attr_names, id_expr=id_expr,
                            default_value_expr=default_value_expr)
