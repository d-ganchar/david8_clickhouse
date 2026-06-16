from david8.protocols.sql import QueryProtocol
from parameterized import parameterized

from david8_clickhouse.cast_types import string, uint8
from david8_clickhouse.functions_table import s3, url_
from david8_clickhouse.input_output_formats import CSV, CSV_WITH_NAMES
from david8_clickhouse.protocols.sql import SelectProtocol
from tests.base_test import BaseTest


class TestTableFunction(BaseTest):
    @parameterized.expand([
        (
            BaseTest.qb
            .insert()
            .into_table_fn(
                url_(
                    'http://data/path/',
                    CSV,
                    [
                        ('name', string),
                        ('year', uint8),
                    ],
                    {
                        'Accept': 'text/csv; charset=utf-8',
                        'Accept-Language': 'en-US,en;',
                    }
                )
            )
            .columns('name', 'year')
            .from_select(BaseTest.qb.select('name', 'year').from_table('old_movie')),
            "INSERT INTO FUNCTION url('http://data/path/', 'CSV', 'name String, year UInt8', "
            "headers=('Accept'='text/csv; charset=utf-8', 'Accept-Language'='en-US,en;')) "
            "SELECT name, year FROM old_movie",
        ),
    ])
    def test_insert_into_table_fn(self, query: QueryProtocol, sql_exp: str):
        self.assertEqual(query.get_sql(), sql_exp)

    @parameterized.expand([
        (
            BaseTest.qb.select('*').from_expr(url_('http://data/path/date=*/country=*/code=*/*.parquet')),
            "SELECT * FROM url('http://data/path/date=*/country=*/code=*/*.parquet')",
        ),
        (
            BaseTest.qb
            .select('*')
            .from_expr(
                url_(
                    'http://data/path/date=*/country=*/code=*/*.parquet',
                    CSV,
                    [
                        ('name', string),
                        ('price', uint8),
                    ],
                    {
                        'Accept': 'text/csv; charset=utf-8',
                        'Accept-Language': 'en-US,en;',
                    }
                )
            ),
            "SELECT * FROM url('http://data/path/date=*/country=*/code=*/*.parquet', 'CSV', 'name String, "
            "price UInt8', headers=('Accept'='text/csv; charset=utf-8', 'Accept-Language'='en-US,en;'))",
        ),
    ])
    def test_select_from_table_fn(self, query: SelectProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        # no named creds
        (
            BaseTest.qb.select('*').from_expr(s3('https://public-datasets.com/test.csv')),
            "SELECT * FROM s3('https://public-datasets.com/test.csv')",
        ),
        (
            BaseTest.qb.select('*').from_expr(s3(
                'https://public-datasets.com/test.csv',
                no_sign=True,
                data_format=CSV_WITH_NAMES,
            )),
            "SELECT * FROM s3('https://public-datasets.com/test.csv', NOSIGN, 'CSVWithNames')",
        ),
        (
            BaseTest.qb.select('*').from_expr(s3(
                'https://public-datasets.com/test.csv',
                access_key_id='AWS_ACCESS_KEY_ID',
                secret_access_key='AWS_SECRET_ACCESS_KEY',
                session_token='1234',
            )),
            "SELECT * FROM s3('https://public-datasets.com/test.csv', 'AWS_ACCESS_KEY_ID', "
            "'AWS_SECRET_ACCESS_KEY', '1234')",
        ),
        (
            BaseTest.qb.select('*').from_expr(s3(
                'https://public-datasets.com/test.csv',
                data_format=CSV,
                structure=[
                    ('name', string),
                    ('price', uint8),
                ],
            )),
            "SELECT * FROM s3('https://public-datasets.com/test.csv', 'CSV', 'name String, price UInt8')",
        ),
        (
            BaseTest.qb.select('*').from_expr(s3(
                'https://public-datasets.com/test.csv',
                data_format=CSV,
                structure=[
                    ('name', string),
                    ('price', uint8),
                ],
                compression_method='gzip',
            )),
            "SELECT * FROM s3('https://public-datasets.com/test.csv', 'CSV', 'name String, price UInt8', 'gzip')",
        ),
        # named creds
        (
            BaseTest.qb.select('*').from_expr(s3('https://public-datasets.com/test.csv', 'creds')),
            "SELECT * FROM s3(creds, url='https://public-datasets.com/test.csv')",
        ),
        (
            BaseTest.qb.select('*').from_expr(s3(
                'https://public-datasets.com/test.csv',
                'creds',
                access_key_id='AWS_ACCESS_KEY_ID',
                secret_access_key='AWS_SECRET_ACCESS_KEY',
                session_token='1234',
            )),
            "SELECT * FROM s3(creds, url='https://public-datasets.com/test.csv', access_key_id='AWS_ACCESS_KEY_ID', "
            "secret_access_key='AWS_SECRET_ACCESS_KEY', session_token='1234')",
        ),
        (
            BaseTest.qb.select('*').from_expr(s3(
                'https://public-datasets.com/test.csv',
                'creds',
                data_format=CSV,
                structure=[
                    ('name', string),
                    ('price', uint8),
                ],
            )),
            "SELECT * FROM s3(creds, url='https://public-datasets.com/test.csv', "
            "format='CSV', structure='name String, price UInt8')",
        ),
        (
            BaseTest.qb.select('*').from_expr(s3(
                'https://public-datasets.com/test.csv',
                'creds',
                data_format=CSV,
                structure=[
                    ('name', string),
                    ('price', uint8),
                ],
                compression_method='gzip',
            )),
            "SELECT * FROM s3(creds, "
            "url='https://public-datasets.com/test.csv', format='CSV', structure='name String, price UInt8', "
            "compression_method='gzip')",
        ),
    ])
    def test_select_from_s3_fn(self, query: SelectProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)
