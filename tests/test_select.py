from david8.expressions import col as c
from david8.expressions import interval
from david8.expressions import val as v
from david8.functions import sub
from david8.predicates import between, eq, eq_c
from parameterized import parameterized

from david8_clickhouse import QueryBuilderProtocol
from david8_clickhouse.functions import to_date
from david8_clickhouse.protocols.sql import SelectProtocol
from tests.base_test import BaseTest


class TestSelect(BaseTest):
    @parameterized.expand([
        (
            BaseTest.qb.select('name').from_table('events', final=True),
            'SELECT name FROM events FINAL',
        ),
        (
            BaseTest.qb_w.select('name').from_table('events', final=True),
            'SELECT "name" FROM "events" FINAL',
        ),
        (
            BaseTest.qb.select('name').from_table('events', db_name='legacy', final=True),
            'SELECT name FROM legacy.events FINAL',
        ),
        (
            BaseTest.qb_w.select('name').from_table('events', db_name='legacy', final=True),
            'SELECT "name" FROM "legacy"."events" FINAL',
        ),
    ])
    def test_final(self, query: SelectProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.select('*').from_table('visits').sample(10000000),
            'SELECT * FROM visits SAMPLE 10000000',
        ),
        (
            BaseTest.qb.select('*').from_table('visits').sample(0.1, 0.5),
            'SELECT * FROM visits SAMPLE 0.1 OFFSET 0.5',
        ),
    ])
    def test_sample(self, query: SelectProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.select('*').from_table('tbl').limit_by(),
            'SELECT * FROM tbl LIMIT BY ALL',
        ),
        (
            BaseTest.qb.select('*').from_table('tbl').limit_by('col1', 'col2'),
            'SELECT * FROM tbl LIMIT BY col1, col2',
        ),
        (
            BaseTest.qb.select('*').from_table('tbl').limit_by('col1', limit=10, offset=50).limit(100),
            'SELECT * FROM tbl LIMIT 10, 50 BY col1 LIMIT 100',
        ),
    ])
    def test_limit_by(self, query: SelectProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)

    def test_with_expr(self):
        self.assertEqual(
            self.qb
            .with_expr(
                v('2026-06-01 15:23:00').as_('ts_upper_bound'),
                to_date('ts_upper_bound').as_('event_date'),
                sub('ts_upper_bound', interval().hour(1)).as_('ts_lower_bound'),
            )
            .select('*')
            .from_table('hits')
            .where(
                eq_c('EventDate', 'event_date'),
                between('EventTime', c('ts_lower_bound'), c('ts_upper_bound'))
            ).get_sql(),
            "WITH '2026-06-01 15:23:00' AS ts_upper_bound, "
            "toDate(ts_upper_bound) AS event_date, "
            "(ts_upper_bound - INTERVAL 1 HOUR) AS ts_lower_bound "
            "SELECT * FROM hits "
            "WHERE EventDate = event_date AND "
            "EventTime BETWEEN ts_lower_bound AND ts_upper_bound"
        )

    @parameterized.expand([
        (
            BaseTest.qb,
            'WITH alias1 AS (SELECT * FROM legacy_table WHERE bad_category = %(p1)s), alias2 AS '
            '(SELECT * FROM new_table WHERE category = %(p2)s) SELECT * FROM legacy_table',
            'SELECT * FROM legacy_table WHERE bad_category = %(p1)s',
            'SELECT * FROM new_table WHERE category = %(p1)s',
        ),
        (
            BaseTest.qb_w,
            'WITH "alias1" AS (SELECT "*" FROM "legacy_table" WHERE "bad_category" = %(p1)s), "alias2" AS '
            '(SELECT "*" FROM "new_table" WHERE "category" = %(p2)s) SELECT "*" FROM "legacy_table"',
            'SELECT "*" FROM "legacy_table" WHERE "bad_category" = %(p1)s',
            'SELECT "*" FROM "new_table" WHERE "category" = %(p1)s',
        )
    ])
    def test_with_query_args(self, qb: QueryBuilderProtocol, exp_sql: str, q1_sql: str, q2_sql) -> None:
        query1 = qb.select('*').from_table('legacy_table').where(eq('bad_category', 'val1'))
        query2 = qb.select('*').from_table('new_table').where(eq('category', 'val2'))
        query = (
            qb.with_(
                ('alias1', query1),
                ('alias2', query2),
            )
            .select('*')
            .from_table('legacy_table')
        )

        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual({'p1': 'val1', 'p2': 'val2'}, query.get_parameters())
        # check render and parameters after query.get_sql() for subqueries
        self.assertEqual(query1.get_sql(), q1_sql)
        self.assertEqual(query1.get_parameters(), {'p1': 'val1'})

        self.assertEqual(query2.get_sql(), q2_sql)
        self.assertEqual(query2.get_parameters(), {'p1': 'val2'})
