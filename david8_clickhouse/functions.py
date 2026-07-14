from david8.core.fn_generator import ColStrIntArgFactory as _ColStrIntArgFactory
from david8.core.fn_generator import OneArgWindowFactory as _OneArgWindowFactory
from david8.core.fn_generator import SeparatedArgsFnFactory as _SeparatedArgsFnFactory
from david8.core.fn_generator import StrArgFactory as _StrArgFactory
from david8.protocols.sql import ExprProtocol, QueryProtocol

from .core.fn_generator import AttrNamesDefaultFactory as _AttrNamesDefaultFactory
from .core.fn_generator import AttrNamesFactory as _AttrNamesFactory
from .core.fn_generator import MultiIfFactory as _MultiIfFactory
from .core.table_functions import IcebergS3Fn as _IcebergS3Fn
from .core.table_functions import MongoDbFn as _MongoDbFn
from .core.table_functions import PostgresFn as _PostgresFn
from .core.table_functions import PrometheusQueryFn as _PrometheusQueryFn
from .core.table_functions import PrometheusQueryRangeFn as _PrometheusQueryRangeFn
from .core.table_functions import RedisFn as _RedisFn
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

def prometheus_query(
    time_series_table: str,
    promql_query: str,
    db_name: str = '',
    evaluation_time: ExprProtocol | None = None
) -> TableFunctionProtocol:
    return _PrometheusQueryFn(
        time_series_table=time_series_table,
        promql_query=promql_query,
        db_name=db_name,
        evaluation_time=evaluation_time,
    )

def prometheus_query_range(
    time_series_table: str,
    promql_query: str,
    start_time: ExprProtocol,
    end_time: ExprProtocol,
    step: ExprProtocol,
    db_name: str = '',
) -> TableFunctionProtocol:
    return _PrometheusQueryRangeFn(
        time_series_table=time_series_table,
        promql_query=promql_query,
        db_name=db_name,
        start_time=start_time,
        end_time=end_time,
        step=step,
    )

def iceberg_s3(
    s3_url: str = '',
    creds: str = '',
    filename: str = '',
    no_sign: bool = False,
    data_format: str = '',
    access_key_id: str = '',
    secret_access_key: str = '',
    session_token: str = '',
    compression_method: str = '',
) -> _IcebergS3Fn:
    return _IcebergS3Fn(
        url_=s3_url,
        creds=creds,
        filename=filename,
        no_sign=no_sign,
        data_format=data_format,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        session_token=session_token,
        compression_method=compression_method,
    )

def postgresql(
    creds: str = '',
    table: str | QueryProtocol = '',
    host: str = '',
    db: str = '',
    user: str = '',
    password: str = '',
) -> _PostgresFn:
    return _PostgresFn(
        creds=creds,
        source=table,
        host=host,
        db=db,
        user=user,
        password=password,
    )

def redis_(
    host: str,
    key: str,
    structure: list[tuple[str, str]] = None,
    db_index: int = 0,
    password: str = '',
    pool_size: int = 0,
    primary: str = '',
) -> _RedisFn:
    return _RedisFn(
        host=host,
        key=key,
        structure=structure or [],
        db_index=db_index,
        password=password,
        pool_size=pool_size,
        primary=primary,
    )


def mongodb(
    collection: str,
    creds: str = '',
    host: str = '',
    database: str = '',
    user: str = '',
    password: str = '',
    structure: list[tuple[str, str]] = None,
) -> _MongoDbFn:
    return _MongoDbFn(
        collection=collection,
        creds=creds,
        host=host,
        database=database,
        user=user,
        password=password,
        structure=structure or [],
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
stddev_pop = _OneArgWindowFactory(name='stddevPop')
stddev_samp = _OneArgWindowFactory(name='stddevSamp')
uniq_exact = _OneArgWindowFactory(name='uniqExact')
uniq = _OneArgWindowFactory(name='uniq')

multi_if = _MultiIfFactory()

















