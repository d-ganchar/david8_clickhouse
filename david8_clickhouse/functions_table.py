# https://clickhouse.com/docs/sql-reference/table-functions

from .core.table_functions import S3TableFunction as _S3TableFunction
from .core.table_functions import UrlTableFunction as _UrlTableFunction
from .protocols.sql import TableFunctionProtocol


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
