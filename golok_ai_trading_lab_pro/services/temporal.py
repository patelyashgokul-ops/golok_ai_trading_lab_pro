"""Immutable chronological date windows with skipped embargo observations."""

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class Partitions:
    training: tuple
    validation: tuple
    holdout: tuple
    embargo: int


def freeze(training, validation, holdout, *, embargo=1):
    groups = tuple(tuple(group) for group in (training, validation, holdout))
    if (type(embargo) is not int or not 0 <= embargo <= 30 or any(not group for group in groups)
            or sum(map(len, groups)) > 2000 or any(type(day) is not date for group in groups for day in group)
            or any(tuple(sorted(set(group))) != group for group in groups)
            or any((right[0] - left[-1]).days <= embargo for left, right in zip(groups, groups[1:]))):
        raise ValueError("Use ordered non-overlapping date windows separated by the requested embargo.")
    return Partitions(*groups, embargo)


def walk_forward(frozen, *, train_size, validation_size):
    if (not isinstance(frozen, Partitions) or type(train_size) is not int or type(validation_size) is not int
            or not 1 <= train_size <= len(frozen.training) or not 1 <= validation_size <= len(frozen.validation)):
        raise ValueError("Use positive bounded train and validation fold sizes.")
    windows = []
    for offset in range(0, len(frozen.validation) - validation_size + 1, validation_size):
        test = frozen.validation[offset:offset + validation_size]
        cutoff = test[0] - timedelta(days=frozen.embargo)
        available = frozen.training + frozen.validation[:offset]
        train = tuple(day for day in available if day < cutoff)[-train_size:]
        if len(train) != train_size:
            raise ValueError("Embargo left an undersized training fold.")
        windows.append((train, test))
    return tuple(windows)
