from david8.core.fn_generator import ColStrIntArgFactory as _ColStrIntArgFactory
from david8.core.fn_generator import OneArgWindowFactory as _OneArgWindowFactory
from david8.core.fn_generator import SeparatedArgsFnFactory as _SeparatedArgsFnFactory
from david8.core.fn_generator import StrArgFactory as _StrArgFactory

from .core.fn_generator import AttrNamesDefaultFactory as _AttrNamesDefaultFactory
from .core.fn_generator import AttrNamesFactory as _AttrNamesFactory
from .core.fn_generator import MultiIfFactory as _MultiIfFactory
from .core.table_functions import S3TableFunction as _S3TableFunction
from .core.table_functions import UrlTableFunction as _UrlTableFunction
from .protocols.sql import TableFunctionProtocol


# table functions
def url_(
    url_value: str,
    data_format: str = '',
    structure: list[tuple[str, str]] = None,
    headers: dict[str, str] = None,
) -> TableFunctionProtocol:
    return _UrlTableFunction(url_=url_value, data_format=data_format, structure=structure or [], headers=headers or {})


def s3(
    url_value: str,
    creds: str = '',
    no_sign: bool = False,
    access_key_id: str = '',
    secret_access_key: str = '',
    session_token: str = '',
    data_format: str = '',
    structure: list[tuple[str, str]] = None,
    compression_method: str = '',
) -> TableFunctionProtocol:
    return _S3TableFunction(
        url_=url_value,
        data_format=data_format,
        structure=structure or [],
        creds=creds,
        no_sign=no_sign,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        session_token=session_token,
        compression_method=compression_method,
    )

# string functions
concat_with_separator = _SeparatedArgsFnFactory(name='concatWithSeparator', separator=', ')

# dict functions
dict_get = _AttrNamesFactory(name='dictGet')
dict_get_date = _AttrNamesFactory(name='dictGetDate')
dict_get_datetime = _AttrNamesFactory(name='dictGetDateTime')
dict_get_float32 = _AttrNamesFactory(name='dictGetFloat32')
dict_get_float64 = _AttrNamesFactory(name='dictGetFloat64')
dict_get_ipv4 = _AttrNamesFactory(name='dictGetIPv4')
dict_get_ipv6 = _AttrNamesFactory(name='dictGetIPv6')
dict_get_int16 = _AttrNamesFactory(name='dictGetInt16')
dict_get_int32 = _AttrNamesFactory(name='dictGetInt32')
dict_get_int64 = _AttrNamesFactory(name='dictGetInt64')
dict_get_int8 = _AttrNamesFactory(name='dictGetInt8')
dict_get_string = _AttrNamesFactory(name='dictGetString')
dict_get_uint16 = _AttrNamesFactory(name='dictGetUInt16')
dict_get_uint32 = _AttrNamesFactory(name='dictGetUInt32')
dict_get_uint64 = _AttrNamesFactory(name='dictGetUInt64')
dict_get_uint8 = _AttrNamesFactory(name='dictGetUInt8')
dict_get_uuid = _AttrNamesFactory(name='dictGetUUID')
dict_get_uuid_or_default = _AttrNamesDefaultFactory(name='dictGetUUID')
dict_get_uint8_or_default = _AttrNamesDefaultFactory(name='dictGetUInt8OrDefault')
dict_get_uint64_or_default = _AttrNamesDefaultFactory(name='dictGetUInt64OrDefault')
dict_get_uint16_or_default = _AttrNamesDefaultFactory(name='dictGetUInt16OrDefault')
dict_get_uint32_or_default = _AttrNamesDefaultFactory(name='dictGetUInt32OrDefault')
dict_get_string_or_default = _AttrNamesDefaultFactory(name='dictGetStringOrDefault')
dict_get_int16_or_default = _AttrNamesDefaultFactory(name='dictGetInt16OrDefault')
dict_get_int8_or_default = _AttrNamesDefaultFactory(name='dictGetInt8OrDefault')
dict_get_int32_or_default = _AttrNamesDefaultFactory(name='dictGetInt32OrDefault')
dict_get_int64_or_default = _AttrNamesDefaultFactory(name='dictGetInt64OrDefault')
dict_get_ipv4_or_default = _AttrNamesDefaultFactory(name='dictGetIPv4OrDefault')
dict_get_ipv6_or_default = _AttrNamesDefaultFactory(name='dictGetIPv6OrDefault')
dict_get_float32_or_default = _AttrNamesDefaultFactory(name='dictGetFloat32OrDefault')
dict_get_float64_or_default = _AttrNamesDefaultFactory(name='dictGetFloat64OrDefault')
dict_get_datetime_or_default = _AttrNamesDefaultFactory(name='dictGetDateTimeOrDefault')
dict_get_or_default = _AttrNamesDefaultFactory(name='dictGetOrDefault')
dict_get_date_or_default = _AttrNamesDefaultFactory(name='dictGetDateOrDefault')

# datetime functions
yyyymmdd_to_date = _ColStrIntArgFactory(name='YYYYMMDDToDate')
yyyymmdd_to_date32 = _ColStrIntArgFactory(name='YYYYMMDDToDate32')
to_date = _ColStrIntArgFactory(name='toDate')
parse_datetime_best_effort = _StrArgFactory(name='parseDateTimeBestEffort')
to_date_or_null = _StrArgFactory(name='toDateOrNull')
to_datetime_or_zero = _StrArgFactory(name='toDateTimeOrZero')
to_datetime_or_null = _StrArgFactory(name='toDateTimeOrNull')

# agg functions
uniq_state = _OneArgWindowFactory(name='uniqState')
var_pop = _OneArgWindowFactory(name='varPop')
var_samp = _OneArgWindowFactory(name='varSamp')

multi_if = _MultiIfFactory()

















