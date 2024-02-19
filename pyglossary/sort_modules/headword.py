from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from pyglossary.icu_types import T_Collator

	from .sort_keys_types import sortKeyType, sqliteSortKeyType


desc = "Headword"


def normal(sortEncoding: str = "utf-8", **_options) -> "sortKeyType":
	def sortKey(words: "list[str]") -> bytes:
		return words[0].encode(sortEncoding, errors="replace")

	return sortKey


def locale(
	collator: "T_Collator",  # noqa: F821
) -> "sortKeyType":
	cSortKey = collator.getSortKey

	def sortKey(words: "list[str]") -> bytes:
		return cSortKey(words[0])

	return lambda **_options: sortKey


def sqlite(sortEncoding: str = "utf-8", **_options) -> "sqliteSortKeyType":
	def sortKey(words: "list[str]") -> bytes:
		return words[0].encode(sortEncoding, errors="replace")

	return [
		(
			"headword",
			"TEXT" if sortEncoding == "utf-8" else "BLOB",
			sortKey,
		),
	]


def sqlite_locale(
	collator: "T_Collator",  # noqa: F821
) -> "Callable[..., sqliteSortKeyType]":
	cSortKey = collator.getSortKey

	def sortKey(words: "list[str]") -> bytes:
		return cSortKey(words[0])

	return lambda **_options: [("sortkey", "BLOB", sortKey)]
