import csv
import math
import itertools
from datetime import datetime, timedelta


class Series(list):
    """Minimal list-based Series supporting a few pandas-like operations."""

    @property
    def iloc(self):
        class _ILoc:
            def __init__(self, data):
                self.data = data

            def __getitem__(self, idx):
                return self.data[idx]

        return _ILoc(self)

    def __eq__(self, other):
        return [x == other for x in self]

    @property
    def values(self):
        return list(self)

    def pct_change(self):
        out = [math.nan]
        for i in range(1, len(self)):
            prev = self[i - 1]
            curr = self[i]
            if prev in (0, math.nan) or prev is None:
                out.append(math.nan)
            else:
                out.append((curr - prev) / prev)
        return Series(out)

    def fillna(self, value):
        return Series([value if x is None or (isinstance(x, float) and math.isnan(x)) else x for x in self])

    def sum(self):
        total = 0
        for x in self:
            if x is None or (isinstance(x, float) and math.isnan(x)):
                continue
            total += x
        return total

    def __pow__(self, power):
        return Series([x ** power if x is not None else None for x in self])

    def __mul__(self, other):
        if isinstance(other, Series):
            return Series([a * b for a, b in zip(self, other)])
        return Series([a * other for a in self])


class MultiIndex(list):
    @classmethod
    def from_product(cls, iterables):
        return cls(list(itertools.product(*iterables)))

    def get_level_values(self, level):
        return [t[level] for t in self]


class DataFrame:
    def __init__(self, data=None, index=None, columns=None):
        if isinstance(data, dict):
            self.data = {k: list(v) for k, v in data.items()}
            columns = list(data.keys()) if columns is None else columns
            n = len(next(iter(self.data.values()))) if self.data else 0
            self.index = list(range(n)) if index is None else list(index)
        elif isinstance(data, list):
            if columns is None:
                raise ValueError("columns must be provided when data is list")
            self.data = {c: [row[i] for row in data] for i, c in enumerate(columns)}
            self.index = list(range(len(data))) if index is None else list(index)
        else:
            self.data = {}
            self.index = []
        self._columns = columns if columns is not None else []

    @property
    def empty(self):
        return len(self.index) == 0

    def __getitem__(self, key):
        return Series(self.data[key])

    def __setitem__(self, key, value):
        self.data[key] = list(value)
        if key not in self._columns:
            self._columns.append(key)

    @property
    def loc(self):
        class _Loc:
            def __init__(self, outer):
                self.outer = outer

            def __getitem__(self, item):
                rows, col = item
                indices = [i for i, flag in enumerate(rows) if flag]
                vals = [self.outer.data[col][i] for i in indices]
                return Series(vals)


        return _Loc(self)

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, new_cols):
        new_cols = list(new_cols)
        if not hasattr(self, "_columns"):
            self._columns = new_cols
            return
        if len(new_cols) != len(self._columns):
            self._columns = new_cols
            return
        new_data = {}
        for old, new in zip(self._columns, new_cols):
            new_data[new] = self.data.pop(old)
        self.data = new_data
        self._columns = new_cols


def to_numeric(values, errors="raise"):
    if not isinstance(values, (list, Series)):
        try:
            return float(values)
        except Exception:
            if errors == "coerce":
                return math.nan
            raise
    out = []
    for v in values:
        try:
            out.append(float(v))
        except Exception:
            if errors == "coerce":
                out.append(math.nan)
            else:
                raise
    return Series(out)


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        data = {field: [] for field in rdr.fieldnames}
        for row in rdr:
            for field in rdr.fieldnames:
                data[field].append(row[field])
    return DataFrame(data)


def date_range(start, periods):
    dt = datetime.strptime(start, "%Y-%m-%d")
    return [dt + timedelta(days=i) for i in range(periods)]

