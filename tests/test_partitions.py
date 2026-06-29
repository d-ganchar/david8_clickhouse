from parameterized import parameterized

from david8_clickhouse.protocols.sql import SelectProtocol
from tests.base_test import BaseTest


class TestPartitions(BaseTest):
    @parameterized.expand([
        (
            BaseTest.qb.drop_partitions('events', [20260101]),
            'ALTER TABLE events DROP PARTITION 20260101',
        ),
        (
            BaseTest.qb_w.drop_partitions('events', ["2026-01-01"]),
            'ALTER TABLE "events" DROP PARTITION \'2026-01-01\'',
        ),
        (
            BaseTest.qb.drop_partitions('events', [20260101], on_cluster='games'),
            'ALTER TABLE events ON CLUSTER games DROP PARTITION 20260101',
        ),
        (
            BaseTest.qb_w.drop_partitions('events', ['2026-01-01', '2026-01-02'], 'raw', on_cluster='{cluster}'),
            "ALTER TABLE \"raw\".\"events\" ON CLUSTER {cluster} DROP PARTITION '2026-01-01', "
            "DROP PARTITION '2026-01-02'",
        ),
        (
            BaseTest.qb.drop_partitions('events', [(202601, 'PL'), (202601, 'BY')], 'raw', on_cluster='{cluster}'),
            "ALTER TABLE raw.events ON CLUSTER {cluster} DROP PARTITION (202601, 'PL'), "
            "DROP PARTITION (202601, 'BY')",
        ),
    ])
    def test_drop_partitions(self, query: SelectProtocol, exp_sql):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.attach_partition('events', '2020-11-21'),
            "ALTER TABLE events ATTACH PARTITION '2020-11-21'",
        ),
        (
            BaseTest.qb.attach_partition('events', '2020-11-21', 'maintenance'),
            "ALTER TABLE maintenance.events ATTACH PARTITION '2020-11-21'",
        ),
        (
            BaseTest.qb.attach_partition('events', '2020-11-21', 'maintenance', on_cluster='{cluster}'),
            "ALTER TABLE maintenance.events ON CLUSTER {cluster} ATTACH PARTITION '2020-11-21'",
        ),
        (
            BaseTest.qb.attach_partition('events', '2020-11-21', 'maintenance', 'dev_events', 'prod', '{cluster}',),
            "ALTER TABLE maintenance.events ON CLUSTER {cluster} ATTACH PARTITION '2020-11-21' FROM prod.dev_events",
        ),
        (
            BaseTest.qb.attach_partition('events', '2020-11-21', 'maintenance', from_tbl='dev_events'),
            "ALTER TABLE maintenance.events ATTACH PARTITION '2020-11-21' FROM dev_events",
        ),
    ])
    def test_attach_partition(self, query: SelectProtocol, exp_sql):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.replace_partition('events', '2020-11-21', 'maintenance', 'dev_events', 'prod', '{cluster}',),
            "ALTER TABLE maintenance.events ON CLUSTER {cluster} REPLACE PARTITION '2020-11-21' FROM prod.dev_events",
        ),
        (
            BaseTest.qb.replace_partition('events', '2020-11-21', 'maintenance', 'dev_events'),
            "ALTER TABLE maintenance.events REPLACE PARTITION '2020-11-21' FROM dev_events",
        ),
    ])
    def test_replace_partition(self, query: SelectProtocol, exp_sql):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.detach_partition('events', '2020-11-21'),
            "ALTER TABLE events DETACH PARTITION '2020-11-21'",
        ),
        (
            BaseTest.qb.detach_partition('events', '2020-11-21', 'maintenance'),
            "ALTER TABLE maintenance.events DETACH PARTITION '2020-11-21'",
        ),
        (
            BaseTest.qb.detach_partition('events', '2020-11-21', 'maintenance', '{cluster}'),
            "ALTER TABLE maintenance.events ON CLUSTER {cluster} DETACH PARTITION '2020-11-21'",
        ),
    ])
    def test_detach_partition(self, query: SelectProtocol, exp_sql):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.move_partition_to_table('events', '2020-11-21', 'events_v2'),
            "ALTER TABLE events MOVE PARTITION '2020-11-21' TO TABLE events_v2",
        ),
        (
            BaseTest.qb.move_partition_to_table('events', '2020-11-21', 'events_v2', on_cluster='{cluster}'),
            "ALTER TABLE events ON CLUSTER {cluster} MOVE PARTITION '2020-11-21' TO TABLE events_v2",
        ),
        (
            BaseTest.qb.move_partition_to_table('events', '2020-11-21', 'events_v2', 'maintenance'),
            "ALTER TABLE maintenance.events MOVE PARTITION '2020-11-21' TO TABLE events_v2",
        ),
        (
            BaseTest.qb.move_partition_to_table('events', '2020-11-21', 'events_v2', 'maintenance', ),
            "ALTER TABLE maintenance.events MOVE PARTITION '2020-11-21' TO TABLE events_v2",
        ),
        (
            BaseTest.qb.move_partition_to_table('events', '2020-11-21', 'events_v2', 'maintenance', 'prod'),
            "ALTER TABLE maintenance.events MOVE PARTITION '2020-11-21' TO TABLE prod.events_v2",
        ),
        (
            BaseTest.qb.move_partition_to_table(
                'events', '2020-11-21', 'events_v2', 'maintenance', 'prod', '{cluster}'
            ),
            "ALTER TABLE maintenance.events ON CLUSTER {cluster} MOVE PARTITION '2020-11-21' TO TABLE prod.events_v2",
        ),
    ])
    def test_move_to_table(self, query: SelectProtocol, exp_sql):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.move_partition_to_disk('events', '2020-11-21', 'fast_ssd'),
            "ALTER TABLE events MOVE PARTITION '2020-11-21' TO DISK 'fast_ssd'",
        ),
        (
            BaseTest.qb.move_partition_to_disk('events', '2020-11-21', 'fast_ssd', on_cluster='{cluster}'),
            "ALTER TABLE events ON CLUSTER {cluster} MOVE PARTITION '2020-11-21' TO DISK 'fast_ssd'",
        ),
        (
            BaseTest.qb.move_partition_to_disk('events', '2020-11-21', 'fast_ssd', 'prod'),
            "ALTER TABLE prod.events MOVE PARTITION '2020-11-21' TO DISK 'fast_ssd'",
        ),
        (
            BaseTest.qb.move_partition_to_disk('events', '2020-11-21', 'fast_ssd', 'prod', '{cluster}'),
            "ALTER TABLE prod.events ON CLUSTER {cluster} MOVE PARTITION '2020-11-21' TO DISK 'fast_ssd'",
        ),
    ])
    def test_move_to_disk(self, query: SelectProtocol, exp_sql):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.move_partition_to_volume('events', '2020-11-21', 'fast_ssd'),
            "ALTER TABLE events MOVE PARTITION '2020-11-21' TO VOLUME 'fast_ssd'",
        ),
        (
            BaseTest.qb.move_partition_to_volume('events', '2020-11-21', 'fast_ssd', on_cluster='{cluster}'),
            "ALTER TABLE events ON CLUSTER {cluster} MOVE PARTITION '2020-11-21' TO VOLUME 'fast_ssd'",
        ),
        (
            BaseTest.qb.move_partition_to_volume('events', '2020-11-21', 'fast_ssd', 'prod'),
            "ALTER TABLE prod.events MOVE PARTITION '2020-11-21' TO VOLUME 'fast_ssd'",
        ),
        (
            BaseTest.qb.move_partition_to_volume('events', '2020-11-21', 'fast_ssd', 'prod', '{cluster}'),
            "ALTER TABLE prod.events ON CLUSTER {cluster} MOVE PARTITION '2020-11-21' TO VOLUME 'fast_ssd'",
        ),
    ])
    def move_partition_to_volume(self, query: SelectProtocol, exp_sql):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.freeze_partition('events', '2020-11-21'),
            "ALTER TABLE events FREEZE PARTITION '2020-11-21'",
        ),
        (
            BaseTest.qb.freeze_partition('events', '2020-11-21', 'backup_name'),
            "ALTER TABLE events FREEZE PARTITION '2020-11-21' WITH NAME 'backup_name'",
        ),
        (
            BaseTest.qb.freeze_partition('events', '2020-11-21', 'backup_name', 'prod'),
            "ALTER TABLE prod.events FREEZE PARTITION '2020-11-21' WITH NAME 'backup_name'",
        ),
        (
            BaseTest.qb.freeze_partition('events', '2020-11-21', 'backup_name', 'prod', '{cluster}'),
            "ALTER TABLE prod.events ON CLUSTER {cluster} FREEZE PARTITION '2020-11-21' WITH NAME 'backup_name'",
        ),
    ])
    def test_freeze_partition(self, query: SelectProtocol, exp_sql):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.unfreeze_partition('events', '2020-11-21'),
            "ALTER TABLE events UNFREEZE PARTITION '2020-11-21'",
        ),
        (
            BaseTest.qb.unfreeze_partition('events', '2020-11-21', 'backup_name'),
            "ALTER TABLE events UNFREEZE PARTITION '2020-11-21' WITH NAME 'backup_name'",
        ),
        (
            BaseTest.qb.unfreeze_partition('events', '2020-11-21', 'backup_name', 'prod'),
            "ALTER TABLE prod.events UNFREEZE PARTITION '2020-11-21' WITH NAME 'backup_name'",
        ),
        (
            BaseTest.qb.unfreeze_partition('events', '2020-11-21', 'backup_name', 'prod', '{cluster}'),
            "ALTER TABLE prod.events ON CLUSTER {cluster} UNFREEZE PARTITION '2020-11-21' WITH NAME 'backup_name'",
        ),
    ])
    def test_unfreeze_partition(self, query: SelectProtocol, exp_sql):
        self.assertEqual(query.get_sql(), exp_sql)

    @parameterized.expand([
        (
            BaseTest.qb.fetch_partition('events', '2020-11-21', 'path-in-zookeeper'),
            "ALTER TABLE events FETCH PARTITION '2020-11-21' FROM 'path-in-zookeeper'",
        ),
        (
            BaseTest.qb.fetch_partition('events', '2020-11-21', 'path-in-zookeeper', 'prod'),
            "ALTER TABLE prod.events FETCH PARTITION '2020-11-21' FROM 'path-in-zookeeper'",
        ),
        (
            BaseTest.qb.fetch_partition('events', '2020-11-21', 'path-in-zookeeper', 'prod', '{cluster}'),
            "ALTER TABLE prod.events ON CLUSTER {cluster} FETCH PARTITION '2020-11-21' FROM 'path-in-zookeeper'",
        ),
    ])
    def test_fetch_partition(self, query: SelectProtocol, exp_sql):
        self.assertEqual(query.get_sql(), exp_sql)
