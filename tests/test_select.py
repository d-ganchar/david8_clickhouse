from parameterized import parameterized

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
