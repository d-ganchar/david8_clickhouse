from david8.protocols.sql import FunctionProtocol
from parameterized import parameterized

from david8_clickhouse.functions import uniq_state, var_pop, var_samp, stddev_samp, stddev_pop
from tests.base_test import BaseTest


class TestAggFunctions(BaseTest):
    @parameterized.expand([
        (
            uniq_state('user_id').over(partition_by=['service'], order_by=['ts']),
            'SELECT uniqState(user_id) OVER (PARTITION BY service ORDER BY ts)',
        ),
    ])
    def test_unique_state(self, fn: FunctionProtocol, exp_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            var_pop('value').over(partition_by=['service'], order_by=['ts']),
            'SELECT varPop(value) OVER (PARTITION BY service ORDER BY ts)',
        ),
    ])
    def test_var_pop(self, fn: FunctionProtocol, exp_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            var_samp('value').over(partition_by=['service'], order_by=['ts']),
            'SELECT varSamp(value) OVER (PARTITION BY service ORDER BY ts)',
        ),
    ])
    def test_var_samp(self, fn: FunctionProtocol, exp_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            stddev_samp('latency').over(partition_by=['host'], order_by=['ts']),
            'SELECT stddevSamp(latency) OVER (PARTITION BY host ORDER BY ts)',
        ),
    ])
    def test_stddev_samp(self, fn: FunctionProtocol, exp_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            stddev_pop('latency').over(partition_by=['host'], order_by=['ts']),
            'SELECT stddevPop(latency) OVER (PARTITION BY host ORDER BY ts)',
        ),
    ])
    def test_stddev_pop(self, fn: FunctionProtocol, exp_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)
