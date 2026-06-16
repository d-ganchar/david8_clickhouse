import dataclasses

from david8.protocols.dialect import DialectProtocol

from ..protocols.sql import TableFunctionProtocol


@dataclasses.dataclass(slots=True)
class BaseTableFunction(TableFunctionProtocol):
    @property
    def name(self) -> str:
        raise NotImplementedError()

    def _get_fn_args(self) -> tuple:
        return ()

    def get_sql(self, dialect: DialectProtocol) -> str:
        return f'{self.name}({", ".join(a for a in self._get_fn_args() if a)})'


@dataclasses.dataclass(slots=True)
class UrlTableFunction(BaseTableFunction):
    url_: str
    data_format: str = ''
    structure: list[tuple[str, str]] = dataclasses.field(default_factory=list)
    headers: dict[str, str] = dataclasses.field(default_factory=dict)

    @property
    def name(self) -> str:
        return 'url'

    def _get_fn_args(self) -> tuple:
        structure = ', '.join(' '.join(s) for s in self.structure)
        structure = f"'{structure}'" if structure else ''

        if self.headers:
            parts = (f"'{k}'='{v}'" for k, v in self.headers.items())
            headers = f"headers=({', '.join(parts)})"
        else:
            headers = ''

        return (
            f"'{self.url_}'",
            f"'{self.data_format}'" if self.data_format else "",
            structure,
            headers,
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

    def _get_fn_args(self) -> tuple:
        structure = ', '.join(' '.join(s) for s in self.structure)
        structure = f"'{structure}'" if structure else ''

        if self.creds:
            return (
                self.creds,
                f"url='{self.url_}'",
                f"access_key_id='{self.access_key_id}'" if self.access_key_id else '',
                f"secret_access_key='{self.secret_access_key}'" if self.secret_access_key else '',
                f"session_token='{self.session_token}'" if self.session_token else '',
                f"format='{self.data_format}'" if self.data_format else '',
                f"structure={structure}" if structure else '',
                f"compression_method='{self.compression_method}'" if self.compression_method else '',
            )

        return (
            f"'{self.url_}'",
            'NOSIGN' if self.no_sign else '',
            f"'{self.access_key_id}'" if self.access_key_id else "",
            f"'{self.secret_access_key}'" if self.secret_access_key else "",
            f"'{self.session_token}'" if self.session_token else "",
            f"'{self.data_format}'" if self.data_format else "",
            structure,
            f"'{self.compression_method}'" if self.compression_method else "",
        )
