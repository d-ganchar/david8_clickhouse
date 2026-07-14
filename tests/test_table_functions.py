from david8.expressions import interval
from david8.functions import now_, sub
from david8.predicates import eq_c
from david8.protocols.sql import QueryProtocol
from parameterized import parameterized

from david8_clickhouse.cast_types import string, uint8
from david8_clickhouse.functions import (
    iceberg_s3,
    mongodb,
    postgresql,
    prometheus_query,
    prometheus_query_range,
    redis_,
)
from david8_clickhouse.functions_table import s3, url_
from david8_clickhouse.input_output_formats import CSV, CSV_WITH_NAMES, PARQUET
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
            BaseTest.qb.insert().into_table_fn(url_('http://data/path/date=*/country=*/code=*/*.parquet'))
            .from_select(BaseTest.qb.select('*').from_table('t')),
            "INSERT INTO FUNCTION url('http://data/path/date=*/country=*/code=*/*.parquet') SELECT * FROM t",
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
            BaseTest.qb.insert().into_table_fn(s3('https://public-datasets.com/test.csv'))
            .from_select(BaseTest.qb.select('*').from_table('t')),
            "INSERT INTO FUNCTION s3('https://public-datasets.com/test.csv') SELECT * FROM t",
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
    def test_s3(self, query: SelectProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        # no named creds
        (
            BaseTest.qb.select('*').from_expr(iceberg_s3('https://bucket.s3.amazonaws.com/warehouse/table/')),
            "SELECT * FROM icebergS3('https://bucket.s3.amazonaws.com/warehouse/table/')",
        ),
        (
            BaseTest.qb.select('*').from_expr(iceberg_s3(
                'https://bucket.s3.amazonaws.com/warehouse/table/',
                no_sign=True,
            )),
            "SELECT * FROM icebergS3('https://bucket.s3.amazonaws.com/warehouse/table/', NOSIGN)",
        ),
        (
            BaseTest.qb.select('*').from_expr(iceberg_s3(
                'https://bucket.s3.amazonaws.com/warehouse/table/',
                no_sign=True,
                data_format=PARQUET,
            )),
            "SELECT * FROM icebergS3('https://bucket.s3.amazonaws.com/warehouse/table/', NOSIGN, 'Parquet')",
        ),
        (
            BaseTest.qb.select('*').from_expr(iceberg_s3(
                'https://bucket.s3.amazonaws.com/warehouse/table/',
                access_key_id='AWS_ACCESS_KEY_ID',
                secret_access_key='AWS_SECRET_ACCESS_KEY',
                data_format=PARQUET,
            )),
            "SELECT * FROM icebergS3('https://bucket.s3.amazonaws.com/warehouse/table/', "
            "'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'Parquet')",
        ),
        (
            BaseTest.qb.select('*').from_expr(iceberg_s3(
                'https://bucket.s3.amazonaws.com/warehouse/table/',
                access_key_id='AWS_ACCESS_KEY_ID',
                secret_access_key='AWS_SECRET_ACCESS_KEY',
                session_token='1234',
                data_format=PARQUET,
            )),
            "SELECT * FROM icebergS3('https://bucket.s3.amazonaws.com/warehouse/table/', "
            "'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', '1234', 'Parquet')",
        ),
        # named creds
        (
            BaseTest.qb.select('*').from_expr(iceberg_s3(
                creds='creds',
                compression_method='gzip',
                filename='test_table',
            )),
            "SELECT * FROM icebergS3(creds, filename='test_table', compression_method='gzip')",
        ),
    ])
    def test_iceberg_s3(self, query: SelectProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        # no named creds
        (
            BaseTest.qb.select('*').from_expr(postgresql(
                host='localhost:5432',
                db='david8_db',
                table='cats',
                user='Baksya',
                password='the best'
            )),
            "SELECT * FROM postgresql('localhost:5432', 'david8_db', 'cats', 'Baksya', 'the best')",
        ),
        (
            BaseTest.qb.select('*').from_expr(postgresql(
                host='localhost:5432',
                db='david8_db',
                table=BaseTest.qb.select('*').from_table('tbl1').where(eq_c('col1', 'col2')),
                user='Baksya',
                password='the best'
            )),
            "SELECT * FROM postgresql('localhost:5432', 'david8_db', (SELECT * FROM tbl1 WHERE col1 = col2), "
            "'Baksya', 'the best')",
        ),
        # named creds
        (
            BaseTest.qb.select('*').from_expr(postgresql(creds='mypg', table='cats')),
            "SELECT * FROM postgresql(mypg, table='cats')",
        ),
        (
            BaseTest.qb.select('*').from_expr(postgresql(
                creds='mypg',
                table=BaseTest.qb.select('*').from_table('tbl1').where(eq_c('col1', 'col2'))
            )),
            "SELECT * FROM postgresql(mypg, table=(SELECT * FROM tbl1 WHERE col1 = col2))",
        ),
    ])
    def test_postgres(self, query: SelectProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.select('*').from_expr(redis_(
                'redis1:6379',
                'metrics',
                [
                    ('name', string),
                    ('value', uint8),
                ]
            )),
            "SELECT * FROM redis('redis1:6379', 'metrics', 'name String, value UInt8')",
        ),
        (
            BaseTest.qb.select('*').from_expr(redis_(
                'redis1:6379',
                'metrics',
                [
                    ('name', string),
                    ('value', uint8),
                ],
                1,
                'user-pass',
                10,
                'col'
            )),
            "SELECT * FROM redis('redis1:6379', 'metrics', 'name String, value UInt8', 1, 'user-pass', 'col')",
        ),
        # insert
        (
            BaseTest.qb.insert().into_table_fn(redis_(
                'redis1:6379',
                'metrics',
                [
                    ('name', string),
                    ('value', uint8),
                ],
            ))
            .from_select(BaseTest.qb.select('name', 'value').from_table('t')),
            "INSERT INTO FUNCTION redis('redis1:6379', 'metrics', 'name String, value UInt8') "
            "SELECT name, value FROM t",
        ),
    ])
    def test_redis(self, query: SelectProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.select('*').from_expr(prometheus_query(
                'table', 'rate(http_requests{job="prometheus"}[10m])[1h:10m]')
            ),
            "SELECT * FROM prometheusQuery('table', 'rate(http_requests{job=\"prometheus\"}[10m])[1h:10m]', now())",
        ),
        (
            BaseTest.qb.select('*').from_expr(prometheus_query(
                'table', 'rate(http_requests{job="prometheus"}[10m])[1h:10m]', 'db')
            ),
            "SELECT * FROM "
            "prometheusQuery('db', 'table', 'rate(http_requests{job=\"prometheus\"}[10m])[1h:10m]', now())",
        ),
    ])
    def test_prometheus_query(self, query: SelectProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.select('*').from_expr(prometheus_query_range(
                'table',
                'rate(http_requests{job="prometheus"}[10m])[1h:10m]',
                sub(now_(), interval().minute(10)),
                now_(),
                interval().minute(1),
            )),
            "SELECT * FROM prometheusQueryRange('table', 'rate(http_requests{job=\"prometheus\"}[10m])[1h:10m]', "
            "(now() - INTERVAL 10 MINUTE), now(), INTERVAL 1 MINUTE)",
        ),
        (
            BaseTest.qb.select('*').from_expr(prometheus_query_range(
                'table',
                'rate(http_requests{job="prometheus"}[10m])[1h:10m]',
                sub(now_(), interval().minute(10)),
                now_(),
                interval().minute(1),
                'db'
            )),
            "SELECT * FROM prometheusQueryRange('db', 'table', 'rate(http_requests{job=\"prometheus\"}[10m])[1h:10m]',"
            " (now() - INTERVAL 10 MINUTE), now(), INTERVAL 1 MINUTE)",
        ),
    ])
    def test_prometheus_query_range(self, query: SelectProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.select('*').from_expr(mongodb(
                host='127.0.0.1:27017',
                database='test',
                collection='my_collection',
                user='test_user',
                password='mongo_pass',
                structure=[
                    ('name', string),
                    ('value', uint8),
                ]
            )),
            "SELECT * FROM mongodb('127.0.0.1:27017', 'test', 'my_collection', 'test_user', 'mongo_pass', "
            "'name String, value UInt8')",
        ),
        (
            BaseTest.qb.select('*').from_expr(mongodb(
                'my_collection',
                'mongo_creds',
                structure=[
                    ('name', string),
                    ('value', uint8),
                ]
            )),
            "SELECT * FROM mongodb(mongo_creds, collection='my_collection', structure='name String, value UInt8')",
        ),
        # insert
        (
            BaseTest.qb.insert().into_table_fn(mongodb(
                'my_collection',
                'mongo_creds',
            ))
            .from_select(BaseTest.qb.select('name', 'value').from_table('t')),
            "INSERT INTO FUNCTION mongodb(mongo_creds, collection='my_collection') SELECT name, value FROM t",
        ),
    ])
    def test_mongodb(self, query: SelectProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)
