from david8.protocols.dml import SelectProtocol as _SelectProtocol

class SelectProtocol(_SelectProtocol):
    def from_table(self, table_name: str, alias: str = '', db_name: str = '', final: bool = False) -> 'SelectProtocol':
        """
        final flag: https://clickhouse.com/docs/sql-reference/statements/select/from#final-modifier
        """