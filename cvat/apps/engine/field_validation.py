# Copyright (C) 2024 CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

from typing import Any, Optional, Sequence

from rest_framework import serializers


def drop_null_keys(d: dict[str, Any], *, keys: Optional[Sequence[str]] = None) -> dict[str, Any]:
    if keys is None:
        keys = d.keys()
    return {k: v for k, v in d.items() if k in keys and v is not None}


def require_one_of_fields(data: dict[str, Any], keys: Sequence[str]) -> None:
    active_count = sum(key in data for key in keys)
    if active_count == 1:
        return

    options = ", ".join(f'"{k}"' for k in keys)

    if not active_count:
        raise serializers.ValidationError(f"One of the fields {options} required")
    else:
        raise serializers.ValidationError(f"Only 1 of the fields {options} can be used")


def require_field(data: dict[str, Any], key: Sequence[str]) -> None:
    if key not in data:
        raise serializers.ValidationError(f'The "{key}" field is required')


def require_one_of_values(data: dict[str, Any], key: str, values: Sequence[Any]) -> None:
    if data[key] not in values:
        raise serializers.ValidationError(
            '"{}" must be one of {}'.format(key, ", ".join(f"{k}" for k in values))
        )


def validate_percent(value: float) -> float:
    if not 0 <= value <= 1:
        raise serializers.ValidationError("Value must be in the range [0; 1]")

    return value