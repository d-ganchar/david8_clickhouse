import dataclasses

from david8.functions import now_
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import ExprProtocol

from ..protocols.sql import SelectProtocol, TableFunctionProtocol


def wrap_value(value: str, key: str = '') -> str:
    if key and value:
        return f"{key}='{value}'"
    return f"'{value}'" if value else ''


def structure_to_str(items: list[tuple[str, str]], key: str = 'structure') -> str:
    structure = ', '.join(' '.join(s) for s in items)
    return wrap_value(structure, key)


@dataclasses.dataclass(slots=True)
class BaseTableFunction(TableFunctionProtocol):
    @property
    def name(self) -> str:
        raise NotImplementedError()

    def _get_fn_args(self, dialect: DialectProtocol) -> tuple:
        return ()

    def get_sql(self, dialect: DialectProtocol) -> str:
        args = ", ".join(
            str(a)
            for a in self._get_fn_args(dialect)
            if a
        )
        return f"{self.name}({args})"


@dataclasses.dataclass(slots=True)
class UrlTableFunction(BaseTableFunction):
    url_: str
    data_format: str = ''
    structure: list[tuple[str, str]] = dataclasses.field(default_factory=list)
    headers: dict[str, str] = dataclasses.field(default_factory=dict)

    @property
    def name(self) -> str:
        return 'url'

    def _get_fn_args(self, dialect: DialectProtocol) -> tuple:
        if self.headers:
            parts = (f"'{k}'='{v}'" for k, v in self.headers.items())
            headers = f"headers=({', '.join(parts)})"
        else:
            headers = ''

        return (
            wrap_value(self.url_),
            wrap_value(self.data_format),
            structure_to_str(self.structure, ''),
            headers,
        )


@dataclasses.dataclass(slots=True)
class RedisFn(BaseTableFunction):
    host: str
    key: str
    structure: list[tuple[str, str]] = dataclasses.field(default_factory=list)
    db_index: int = 0
    password: str = ''
    pool_size: int = 0
    primary: str = ''

    @property
    def name(self) -> str:
        return 'redis'

    def _get_fn_args(self, dialect: DialectProtocol) -> tuple:
        return (
            wrap_value(self.host),
            wrap_value(self.key),
            structure_to_str(self.structure, ''),
            self.db_index,
            wrap_value(self.password),
            wrap_value(self.primary),
        )


@dataclasses.dataclass(slots=True)
class S3TableFunction(BaseTableFunction):
    url_: str
    data_format: str = ''
    creds: str = ''
    access_key_id: str = ''
    secret_access_key: str = ''
    session_token: str = ''
    compression_method: str = ''
    no_sign: bool = False
    structure: list[tuple[str, str]] = dataclasses.field(default_factory=list)

    @property
    def name(self) -> str:
        return 's3'

    def _get_fn_args(self, dialect: DialectProtocol) -> tuple:
        if self.creds:
            return (
                self.creds,
                wrap_value(self.url_, 'url'),
                wrap_value(self.access_key_id, 'access_key_id'),
                wrap_value(self.secret_access_key, 'secret_access_key'),
                wrap_value(self.session_token, 'session_token'),
                wrap_value(self.data_format, 'format'),
                structure_to_str(self.structure),
                wrap_value(self.compression_method, 'compression_method'),
            )

        return (
            wrap_value(self.url_),
            'NOSIGN' if self.no_sign else '',
            wrap_value(self.access_key_id),
            wrap_value(self.secret_access_key),
            wrap_value(self.session_token),
            wrap_value(self.data_format),
            structure_to_str(self.structure, ''),
            wrap_value(self.compression_method),
        )

@dataclasses.dataclass(slots=True)
class PostgresFn(BaseTableFunction):
    host: str = ''
    db: str = ''
    source: str | SelectProtocol = ''
    user: str = ''
    password: str = ''
    creds: str = ''

    @property
    def name(self) -> str:
        return 'postgresql'

    def _get_fn_args(self, dialect: DialectProtocol) -> tuple:
        if self.creds:
            table = wrap_value(self.source) if isinstance(self.source, str) else f'({self.source.get_sql(dialect)})'
            return self.creds, f"table={table}"

        return (
            wrap_value(self.host),
            wrap_value(self.db),
            wrap_value(self.source) if isinstance(self.source, str) else f'({self.source.get_sql(dialect)})',
            wrap_value(self.user),
            wrap_value(self.password),
        )


@dataclasses.dataclass(slots=True)
class IcebergS3Fn(BaseTableFunction):
    url_: str
    data_format: str = ''
    creds: str = ''
    access_key_id: str = ''
    secret_access_key: str = ''
    session_token: str = ''
    compression_method: str = ''
    filename: str = ''
    no_sign: bool = False

    @property
    def name(self) -> str:
        return 'icebergS3'

    def _get_fn_args(self, dialect: DialectProtocol) -> tuple:
        if self.creds:
            return (
                self.creds,
                wrap_value(self.access_key_id, 'access_key_id'),
                wrap_value(self.secret_access_key, 'secret_access_key'),
                wrap_value(self.session_token, 'session_token'),
                wrap_value(self.data_format, 'format'),
                wrap_value(self.filename, 'filename'),
                wrap_value(self.compression_method, 'compression_method'),
            )

        return (
            wrap_value(self.url_),
            'NOSIGN' if self.no_sign else '',
            wrap_value(self.access_key_id),
            wrap_value(self.secret_access_key),
            wrap_value(self.session_token),
            wrap_value(self.data_format),
            wrap_value(self.compression_method),
        )


@dataclasses.dataclass(slots=True)
class PrometheusQueryFn(BaseTableFunction):
    promql_query: str
    time_series_table: str
    db_name: str = ''
    evaluation_time: ExprProtocol | None = None

    @property
    def name(self) -> str:
        return 'prometheusQuery'

    def _get_fn_args(self, dialect: DialectProtocol) -> tuple:
        if self.db_name:
            items = (wrap_value(self.db_name), wrap_value(self.time_series_table), )
        else:
            items = (wrap_value(self.time_series_table), )

        evaluation_time = self.evaluation_time.get_sql(dialect) if self.evaluation_time else now_().get_sql(dialect)
        items += (wrap_value(self.promql_query), evaluation_time)

        return items


@dataclasses.dataclass(slots=True)
class PrometheusQueryRangeFn(BaseTableFunction):
    promql_query: str
    time_series_table: str
    start_time: ExprProtocol
    end_time: ExprProtocol
    step: ExprProtocol
    db_name: str = ''

    @property
    def name(self) -> str:
        return 'prometheusQueryRange'

    def _get_fn_args(self, dialect: DialectProtocol) -> tuple:
        if self.db_name:
            items = (wrap_value(self.db_name), wrap_value(self.time_series_table), )
        else:
            items = (wrap_value(self.time_series_table), )

        items += (
            wrap_value(self.promql_query),
            self.start_time.get_sql(dialect),
            self.end_time.get_sql(dialect),
            self.step.get_sql(dialect),
        )

        return items


@dataclasses.dataclass(slots=True)
class MongoDbFn(BaseTableFunction):
    collection: str
    creds: str = ''
    host: str = ''
    database: str = ''
    user: str = ''
    password: str = ''
    structure: list[tuple[str, str]] = dataclasses.field(default_factory=list)

    @property
    def name(self) -> str:
        return 'mongodb'

    def _get_fn_args(self, dialect: DialectProtocol) -> tuple:
        if self.creds:
            return (
                self.creds,
                wrap_value(self.host, 'host'),
                wrap_value(self.collection, 'collection'),
                structure_to_str(self.structure),
            )

        return (
            wrap_value(self.host),
            wrap_value(self.database),
            wrap_value(self.collection),
            wrap_value(self.user),
            wrap_value(self.password),
            structure_to_str(self.structure, ''),
        )


@dataclasses.dataclass(slots=True)
class RemoteFn(BaseTableFunction):
    creds: str = ''
    table: str = ''
    host: str = ''
    db: str = ''
    user: str = ''
    password: str = ''
    sharding_key: str = ''

    @property
    def name(self) -> str:
        return 'remote'

    def _get_fn_args(self, dialect: DialectProtocol) -> tuple:
        if self.creds:
            return (
                self.creds,
                wrap_value(self.db, 'db'),
                wrap_value(self.table, 'table'),
                wrap_value(self.sharding_key, 'sharding_key'),
            )

        return (
            wrap_value(self.host),
            wrap_value(self.db),
            wrap_value(self.table),
            wrap_value(self.user),
            wrap_value(self.password),
            wrap_value(self.sharding_key),
        )


@dataclasses.dataclass(slots=True)
class RemoteSecureFn(RemoteFn):
    @property
    def name(self) -> str:
        return 'remoteSecure'
