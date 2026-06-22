"""
Deprecated since 0.7.0b1. Will be removed in 0.1.0
Use `functions` module instead, example:
from david8.functions import concat_with_separator
"""
from david8.core.fn_generator import SeparatedArgsFnFactory as _SeparatedArgsFnFactory

# https://clickhouse.com/docs/sql-reference/functions/string-functions#concatWithSeparator
concat_with_separator = _SeparatedArgsFnFactory(name='concatWithSeparator', separator=', ')
