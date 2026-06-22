from david8.protocols.sql import FunctionProtocol
from parameterized import parameterized

from david8_clickhouse.functions import uniq_state
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

