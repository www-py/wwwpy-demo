from __future__ import annotations

from typing import Tuple, List


class Datatable:
    def __init__(self, rows: Tuple):
        assert len(rows) >= 1  # at least the header
        self.header = rows[0]
        assert all(map(lambda field_name: isinstance(field_name, str), self.header))  # verify header are strings
        self.rows: List[Row] = list(map(lambda r: Row(self, r[0], r[1]), enumerate(rows[1:])))
        self._field_index_dict = {f.upper(): index for (index, f) in enumerate(self.header)}
        self._n = None
        self._update = {}
        super().__init__()

    def __str__(self):
        return str((self.header,) + tuple(self.rows))

    def _fieldByName(self, field_name: str, row: Row) -> Field:
        field_name = field_name.upper()
        value = self._valueByName(field_name, row)
        return Field(field_name, value, row, self)

    def _valueByName(self, field_name: str, row: Row):
        index = self._get_field_index(field_name)
        return row[index]

    def _get_field_index(self, field_name):
        index = self._field_index_dict.get(field_name.upper(), None)
        if index is None:
            raise Exception(f'Field name not found `{field_name}`')
        return index

    def __iter__(self):
        if self._n is not None:
            raise Exception('enumeration already started')
        self._n = 1
        return self

    def __next__(self):
        if self._n < len(self.rows):
            result = self.rows[self._n]
            self._n += 1
            return result
        else:
            self._n = None
            raise StopIteration

    def _get_old_value(self, field_name: str, row: Row):
        t = self._get_old_tuple(row)
        if t is None:
            return self._valueByName(field_name, row)
        index = self._get_field_index(field_name)
        return t[index]

    def _set_value(self, field_name: str, row: Row, value: any):
        old_tuple = self._get_old_tuple(row)
        if old_tuple is None:
            old_tuple = tuple(row)
            self._update[row._row_index] = old_tuple

        index = self._get_field_index(field_name)
        row[index] = value

    def _get_old_tuple(self, row):
        old_tuple = self._update.get(row._row_index, None)
        return old_tuple

    def delta(self) -> list:
        update = []
        for index, old_tuple in self._update.items():
            cur_row = self.rows[index]
            new_tuple = tuple(cur_row)
            if new_tuple != old_tuple:
                update.append((old_tuple, new_tuple))
        return [tuple(update)]


class Field:
    def __init__(self, name: str, value, row: Row, table: Datatable):
        self.name = name
        self._row = row
        self._value = value
        self._table = table

    @property
    def value(self):
        return self._value

    @property
    def as_string(self):
        value = self.value
        return '' if value is None else str(value)

    @property
    def as_float(self):
        value = self.value
        return 0.0 if value is None else float(value)

    @property
    def as_int(self):
        value = self.value
        return 0 if value is None else int(value)

    @value.setter
    def value(self, value):
        self._table._set_value(self.name, self._row, value)

    @property
    def oldValue(self):
        return self._table._get_old_value(self.name, self._row)


class Row(list):

    def __init__(self, table: Datatable, row_index: int, iterable=...):
        super().__init__(iterable)
        self._row_index = row_index
        self._table = table

    def valueByName(self, field_name: str):
        return self._table._valueByName(field_name, self)

    def fieldByName(self, field_name: str) -> Field:
        return self._table._fieldByName(field_name, self)
