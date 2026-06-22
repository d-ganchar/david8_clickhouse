"""
Deprecated since 0.7.0b1. Will be removed in 0.1.0
Use `functions` module instead, example:
from david8.functions import yyyymmdd_to_date
"""
from david8.core.fn_generator import ColStrIntArgFactory as _ColStrIntArgFactory
from david8.core.fn_generator import StrArgFactory as _StrArgFactory

yyyymmdd_to_date = _ColStrIntArgFactory(name='YYYYMMDDToDate')
yyyymmdd_to_date32 = _ColStrIntArgFactory(name='YYYYMMDDToDate32')
to_date = _ColStrIntArgFactory(name='toDate')
parse_datetime_best_effort = _StrArgFactory(name='parseDateTimeBestEffort')
to_date_or_null = _StrArgFactory(name='toDateOrNull')
to_datetime_or_zero = _StrArgFactory(name='toDateTimeOrZero')
to_datetime_or_null = _StrArgFactory(name='toDateTimeOrNull')
