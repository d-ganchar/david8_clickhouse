from david8.expressions import param, val
from david8.predicates import eq, ne_c
from david8.protocols.sql import FunctionProtocol
from parameterized import parameterized

from david8_clickhouse.functions import (
    concat_with_separator,
    dict_get,
    dict_get_date,
    dict_get_datetime,
    dict_get_float32,
    dict_get_float32_or_default,
    dict_get_float64,
    dict_get_float64_or_default,
    dict_get_int8,
    dict_get_int8_or_default,
    dict_get_int16,
    dict_get_int16_or_default,
    dict_get_int32,
    dict_get_int32_or_default,
    dict_get_int64,
    dict_get_int64_or_default,
    dict_get_ipv4,
    dict_get_ipv6,
    dict_get_or_default,
    dict_get_string,
    dict_get_string_or_default,
    dict_get_uint8,
    dict_get_uint8_or_default,
    dict_get_uint16,
    dict_get_uint16_or_default,
    dict_get_uint32,
    dict_get_uint32_or_default,
    dict_get_uint64,
    dict_get_uint64_or_default,
    dict_get_uuid,
    multi_if,
    parse_datetime_best_effort,
    to_date,
    to_date_or_null,
    to_datetime_or_null,
    to_datetime_or_zero,
    yyyymmdd_to_date,
    yyyymmdd_to_date32,
)
from tests.base_test import BaseTest


class TestFunctionsDict(BaseTest):
    @parameterized.expand([
        (
            dict_get('dicts.currencies', 'full_name', 'currency_char').as_('currency'),
            "SELECT dictGet('dicts.currencies', 'full_name', currency_char) AS currency",
            "SELECT dictGet('dicts.currencies', 'full_name', \"currency_char\") AS \"currency\"",
        ),
        (
            dict_get_string('dicts.currencies', 'price', 'currency_char').as_('price'),
            "SELECT dictGetString('dicts.currencies', 'price', currency_char) AS price",
            "SELECT dictGetString('dicts.currencies', 'price', \"currency_char\") AS \"price\"",
        ),
        (
            dict_get_uuid('dicts.currencies', 'id', 'currency_char').as_('currency_id'),
            "SELECT dictGetUUID('dicts.currencies', 'id', currency_char) AS currency_id",
            "SELECT dictGetUUID('dicts.currencies', 'id', \"currency_char\") AS \"currency_id\"",
        ),
        (
            dict_get_date('dicts.currencies', 'created_dt', 'currency_char').as_('currency'),
            "SELECT dictGetDate('dicts.currencies', 'created_dt', currency_char) AS currency",
            "SELECT dictGetDate('dicts.currencies', 'created_dt', \"currency_char\") AS \"currency\"",
        ),
        (
            dict_get_datetime('dicts.currencies', 'created_dt', 'currency_char').as_('currency'),
            "SELECT dictGetDateTime('dicts.currencies', 'created_dt', currency_char) AS currency",
            "SELECT dictGetDateTime('dicts.currencies', 'created_dt', \"currency_char\") AS \"currency\"",
        ),
        (
            dict_get_float32('dicts.currencies', 'price', 'currency_char').as_('price'),
            "SELECT dictGetFloat32('dicts.currencies', 'price', currency_char) AS price",
            "SELECT dictGetFloat32('dicts.currencies', 'price', \"currency_char\") AS \"price\"",
        ),
        (
            dict_get_float64('dicts.currencies', 'price', 'currency_char').as_('price'),
            "SELECT dictGetFloat64('dicts.currencies', 'price', currency_char) AS price",
            "SELECT dictGetFloat64('dicts.currencies', 'price', \"currency_char\") AS \"price\"",
        ),
        (
            dict_get_uint8('dicts.currencies', 'price', 'currency_char').as_('price'),
            "SELECT dictGetUInt8('dicts.currencies', 'price', currency_char) AS price",
            "SELECT dictGetUInt8('dicts.currencies', 'price', \"currency_char\") AS \"price\"",
        ),
        (
            dict_get_uint16('dicts.currencies', 'price', 'currency_char').as_('price'),
            "SELECT dictGetUInt16('dicts.currencies', 'price', currency_char) AS price",
            "SELECT dictGetUInt16('dicts.currencies', 'price', \"currency_char\") AS \"price\"",
        ),
        (
            dict_get_uint32('dicts.currencies', 'price', 'currency_char').as_('price'),
            "SELECT dictGetUInt32('dicts.currencies', 'price', currency_char) AS price",
            "SELECT dictGetUInt32('dicts.currencies', 'price', \"currency_char\") AS \"price\"",
        ),
        (
            dict_get_uint64('dicts.currencies', 'price', 'currency_char').as_('price'),
            "SELECT dictGetUInt64('dicts.currencies', 'price', currency_char) AS price",
            "SELECT dictGetUInt64('dicts.currencies', 'price', \"currency_char\") AS \"price\"",
        ),
        (
            dict_get_int8('dicts.currencies', 'price', 'currency_char').as_('price'),
            "SELECT dictGetInt8('dicts.currencies', 'price', currency_char) AS price",
            "SELECT dictGetInt8('dicts.currencies', 'price', \"currency_char\") AS \"price\"",
        ),
        (
            dict_get_int16('dicts.currencies', 'price', 'currency_char').as_('price'),
            "SELECT dictGetInt16('dicts.currencies', 'price', currency_char) AS price",
            "SELECT dictGetInt16('dicts.currencies', 'price', \"currency_char\") AS \"price\"",
        ),
        (
            dict_get_int32('dicts.currencies', 'price', 'currency_char').as_('price'),
            "SELECT dictGetInt32('dicts.currencies', 'price', currency_char) AS price",
            "SELECT dictGetInt32('dicts.currencies', 'price', \"currency_char\") AS \"price\"",
        ),
        (
            dict_get_int64('dicts.currencies', 'price', 'currency_char').as_('price'),
            "SELECT dictGetInt64('dicts.currencies', 'price', currency_char) AS price",
            "SELECT dictGetInt64('dicts.currencies', 'price', \"currency_char\") AS \"price\"",
        ),
        (
            dict_get_ipv4('dicts.currencies', 'created_ip', 'currency_char').as_('ip'),
            "SELECT dictGetIPv4('dicts.currencies', 'created_ip', currency_char) AS ip",
            "SELECT dictGetIPv4('dicts.currencies', 'created_ip', \"currency_char\") AS \"ip\"",
        ),
        (
            dict_get_ipv6('dicts.currencies', 'created_ip', 'currency_char').as_('ip'),
            "SELECT dictGetIPv6('dicts.currencies', 'created_ip', currency_char) AS ip",
            "SELECT dictGetIPv6('dicts.currencies', 'created_ip', \"currency_char\") AS \"ip\"",
        ),
    ])
    def test_dict_get(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)

    @parameterized.expand([
        (
            dict_get_or_default('dicts.currencies', 'full_name', 'currency_char', 'EURO').as_('currency'),
            "SELECT dictGetOrDefault('dicts.currencies', 'full_name', currency_char, 'EURO') AS currency",
            "SELECT dictGetOrDefault('dicts.currencies', 'full_name', \"currency_char\", 'EURO') AS \"currency\"",
        ),
        (
            dict_get_string_or_default('dicts.currencies', 'price', 'currency_char', 'EURO').as_('price'),
            "SELECT dictGetStringOrDefault('dicts.currencies', 'price', currency_char, 'EURO') AS price",
            "SELECT dictGetStringOrDefault('dicts.currencies', 'price', \"currency_char\", 'EURO') AS \"price\"",
        ),
        (
            dict_get_float32_or_default('dicts.currencies', 'price', 'currency_char', 1.9).as_('price'),
            "SELECT dictGetFloat32OrDefault('dicts.currencies', 'price', currency_char, 1.9) AS price",
            "SELECT dictGetFloat32OrDefault('dicts.currencies', 'price', \"currency_char\", 1.9) AS \"price\"",
        ),
        (
            dict_get_float64_or_default('dicts.currencies', 'price', 'currency_char', 7.65).as_('price'),
            "SELECT dictGetFloat64OrDefault('dicts.currencies', 'price', currency_char, 7.65) AS price",
            "SELECT dictGetFloat64OrDefault('dicts.currencies', 'price', \"currency_char\", 7.65) AS \"price\"",
        ),
        (
            dict_get_uint8_or_default('dicts.currencies', 'price', 'currency_char', 8).as_('price'),
            "SELECT dictGetUInt8OrDefault('dicts.currencies', 'price', currency_char, 8) AS price",
            "SELECT dictGetUInt8OrDefault('dicts.currencies', 'price', \"currency_char\", 8) AS \"price\"",
        ),
        (
            dict_get_uint16_or_default('dicts.currencies', 'price', 'currency_char', 10).as_('price'),
            "SELECT dictGetUInt16OrDefault('dicts.currencies', 'price', currency_char, 10) AS price",
            "SELECT dictGetUInt16OrDefault('dicts.currencies', 'price', \"currency_char\", 10) AS \"price\"",
        ),
        (
            dict_get_uint32_or_default('dicts.currencies', 'price', 'currency_char', 16).as_('price'),
            "SELECT dictGetUInt32OrDefault('dicts.currencies', 'price', currency_char, 16) AS price",
            "SELECT dictGetUInt32OrDefault('dicts.currencies', 'price', \"currency_char\", 16) AS \"price\"",
        ),
        (
            dict_get_uint64_or_default('dicts.currencies', 'price', 'currency_char', 27).as_('price'),
            "SELECT dictGetUInt64OrDefault('dicts.currencies', 'price', currency_char, 27) AS price",
            "SELECT dictGetUInt64OrDefault('dicts.currencies', 'price', \"currency_char\", 27) AS \"price\"",
        ),
        (
            dict_get_int8_or_default('dicts.currencies', 'price', 'currency_char', 3).as_('price'),
            "SELECT dictGetInt8OrDefault('dicts.currencies', 'price', currency_char, 3) AS price",
            "SELECT dictGetInt8OrDefault('dicts.currencies', 'price', \"currency_char\", 3) AS \"price\"",
        ),
        (
            dict_get_int16_or_default('dicts.currencies', 'price', 'currency_char', 36).as_('price'),
            "SELECT dictGetInt16OrDefault('dicts.currencies', 'price', currency_char, 36) AS price",
            "SELECT dictGetInt16OrDefault('dicts.currencies', 'price', \"currency_char\", 36) AS \"price\"",
        ),
        (
            dict_get_int32_or_default('dicts.currencies', 'price', 'currency_char', 33).as_('price'),
            "SELECT dictGetInt32OrDefault('dicts.currencies', 'price', currency_char, 33) AS price",
            "SELECT dictGetInt32OrDefault('dicts.currencies', 'price', \"currency_char\", 33) AS \"price\"",
        ),
        (
            dict_get_int64_or_default('dicts.currencies', 'price', 'currency_char', 101).as_('price'),
            "SELECT dictGetInt64OrDefault('dicts.currencies', 'price', currency_char, 101) AS price",
            "SELECT dictGetInt64OrDefault('dicts.currencies', 'price', \"currency_char\", 101) AS \"price\"",
        ),
    ])
    def test_dict_get_or_default(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)


class TestFunctionsDatesTimes(BaseTest):

    @parameterized.expand([
        (
            yyyymmdd_to_date('year_month_dd').as_('date'),
            'SELECT YYYYMMDDToDate(year_month_dd) AS date',
            'SELECT YYYYMMDDToDate("year_month_dd") AS "date"',
        ),
        (
            yyyymmdd_to_date(20260101).as_('date'),
            'SELECT YYYYMMDDToDate(20260101) AS date',
            'SELECT YYYYMMDDToDate(20260101) AS "date"',
        ),
        (
            yyyymmdd_to_date32('year_month_dd').as_('date'),
            'SELECT YYYYMMDDToDate32(year_month_dd) AS date',
            'SELECT YYYYMMDDToDate32("year_month_dd") AS "date"',
        ),
        (
            to_date('created_dt').as_('date'),
            'SELECT toDate(created_dt) AS date',
            'SELECT toDate("created_dt") AS "date"',
        ),
        (
            to_date(val('2026-01-01')).as_('date'),
            "SELECT toDate('2026-01-01') AS date",
            'SELECT toDate(\'2026-01-01\') AS "date"',
        ),
        (
            to_date_or_null('created_dt').as_('date'),
            'SELECT toDateOrNull(created_dt) AS date',
            'SELECT toDateOrNull("created_dt") AS "date"',
        ),
        (
            to_date_or_null(val('2026-01-01')).as_('date'),
            "SELECT toDateOrNull('2026-01-01') AS date",
            'SELECT toDateOrNull(\'2026-01-01\') AS "date"',
        ),
        (
            to_datetime_or_zero('created_dt').as_('date'),
            'SELECT toDateTimeOrZero(created_dt) AS date',
            'SELECT toDateTimeOrZero("created_dt") AS "date"',
        ),
        (
            to_datetime_or_zero(val('2026-01-01')).as_('date'),
            "SELECT toDateTimeOrZero('2026-01-01') AS date",
            'SELECT toDateTimeOrZero(\'2026-01-01\') AS "date"',
        ),
        (
            to_datetime_or_null('created_dt').as_('date'),
            'SELECT toDateTimeOrNull(created_dt) AS date',
            'SELECT toDateTimeOrNull("created_dt") AS "date"',
        ),
        (
            to_datetime_or_null(val('2026-01-01')).as_('date'),
            "SELECT toDateTimeOrNull('2026-01-01') AS date",
            'SELECT toDateTimeOrNull(\'2026-01-01\') AS "date"',
        ),
        (
            parse_datetime_best_effort('created_dt').as_('date'),
            'SELECT parseDateTimeBestEffort(created_dt) AS date',
            'SELECT parseDateTimeBestEffort("created_dt") AS "date"',
        ),
        (
            parse_datetime_best_effort(val('2026-01-01')).as_('date'),
            "SELECT parseDateTimeBestEffort('2026-01-01') AS date",
            'SELECT parseDateTimeBestEffort(\'2026-01-01\') AS "date"',
        ),
    ])
    def test_1arg_functions(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)


class TestFunctionsStr(BaseTest):

    @parameterized.expand([
        (
            concat_with_separator('col1', 1, 'col2', 0.5, param(2)).as_('new_field'),
            "SELECT concatWithSeparator(col1, '1', col2, '0.5', %(p1)s) AS new_field",
            'SELECT concatWithSeparator("col1", \'1\', "col2", \'0.5\', %(p1)s) AS "new_field"',
            {'p1': 2}
        ),
    ])
    def test_concat_with_separator(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str, exp_params: dict):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)
        self.assertEqual(query.get_parameters(), exp_params)


class TestConditionalFunctions(BaseTest):
    @parameterized.expand([
        (
            multi_if(
                (eq('status', 'unknown'), 'new_status'),
                (eq('status', 'old_status'), val('legacy')),
                else_='status',
            ).as_('fixed_status'),
            "SELECT multiIf(status = %(p1)s, new_status, status = %(p2)s, 'legacy', status) AS fixed_status",
            'SELECT multiIf("status" = %(p1)s, "new_status", "status" = %(p2)s, \'legacy\', "status") AS '
            '"fixed_status"',
            {'p1': 'unknown', 'p2': 'old_status'}
        ),
        (
            multi_if(
                (eq('new_status', 'unknown'), 'old_status'),
                (ne_c('new_status', 'old_status'), 'new_status'),
                else_=param('active'),
            ).as_('fixed_status'),
            "SELECT multiIf(new_status = %(p1)s, old_status, new_status != old_status, new_status, %(p2)s) AS "
            "fixed_status",
            'SELECT multiIf("new_status" = %(p1)s, "old_status", "new_status" != "old_status", "new_status", %(p2)s)'
            ' AS "fixed_status"',
            {'p1': 'unknown', 'p2': 'active'},
        ),
    ])
    def test_multi_if(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str, exp_params: dict):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)
        self.assertEqual(query.get_parameters(), exp_params)
