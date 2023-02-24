# -*- coding: utf-8 -*-

import os
from os.path import isdir, join
from typing import Generator, Iterator, Optional, Tuple

from pyglossary.compression import stdCompressions
from pyglossary.core import log
from pyglossary.glossary_type import EntryType, GlossaryType
from pyglossary.option import (
	BoolOption,
	EncodingOption,
	FileSizeOption,
)
from pyglossary.text_reader import TextGlossaryReader
from pyglossary.text_utils import (
	splitByBarUnescapeNTB,
	unescapeNTB,
)

enable = True
lname = "tabfile"
format = "Tabfile"
description = "Tabfile (.txt, .dic)"
extensions = (".txt", ".tab", ".tsv")
extensionCreate = ".txt"
singleFile = True
kind = "text"
wiki = "https://en.wikipedia.org/wiki/Tab-separated_values"
website = None
optionsProp = {
	"encoding": EncodingOption(),
	"enable_info": BoolOption(
		comment="Enable glossary info / metedata",
	),
	"resources": BoolOption(
		comment="Enable resources / data files",
	),
	"file_size_approx": FileSizeOption(
		comment="Split up by given approximate file size\nexamples: 100m, 1g",
	),
	"word_title": BoolOption(
		comment="Add headwords title to beginning of definition",
	),
}


class Reader(TextGlossaryReader):
	def __init__(self, glos: GlossaryType, hasInfo: bool = True) -> None:
		TextGlossaryReader.__init__(self, glos, hasInfo=hasInfo)
		self._resDir = ""
		self._resFileNames = []

	def open(self, filename: str) -> "Iterator[Tuple[int, int]]":
		yield from TextGlossaryReader.openGen(self, filename)
		resDir = f"{filename}_res"
		if isdir(resDir):
			self._resDir = resDir
			self._resFileNames = os.listdir(self._resDir)

	def __iter__(self) -> "Iterator[EntryType]":
		yield from TextGlossaryReader.__iter__(self)
		resDir = self._resDir
		for fname in self._resFileNames:
			with open(join(resDir, fname), "rb") as _file:
				yield self._glos.newDataEntry(
					fname,
					_file.read(),
				)

	def isInfoWord(self, word: str) -> bool:
		return word.startswith("#")

	def fixInfoWord(self, word: str) -> str:
		return word.lstrip("#")

	def nextBlock(self) -> "Optional[Tuple[str, str, None]]":
		if not self._file:
			raise StopIteration
		line = self.readline()
		if not line:
			raise StopIteration
		line = line.rstrip("\n")
		if not line:
			return None
		###
		word, tab, defi = line.partition("\t")
		if not tab:
			log.error(
				f"Warning: line starting with {line[:10]!r} has no tab!",
			)
			return None
		###
		if self._glos.alts:
			word = splitByBarUnescapeNTB(word)
			if len(word) == 1:
				word = word[0]
		else:
			word = unescapeNTB(word, bar=False)
		###
		defi = unescapeNTB(defi)
		###
		return word, defi, None


class Writer(object):
	_encoding: str = "utf-8"
	_enable_info: bool = True
	_resources: bool = True
	_file_size_approx: int = 0
	_word_title: bool = False

	compressions = stdCompressions

	def __init__(self, glos: GlossaryType) -> None:
		self._glos = glos
		self._filename = None

	def open(
		self,
		filename: str,
	) -> None:
		self._filename = filename

	def finish(self) -> None:
		pass

	def write(self) -> "Generator[None, EntryType, None]":
		from pyglossary.text_utils import escapeNTB, joinByBar
		from pyglossary.text_writer import TextGlossaryWriter
		writer = TextGlossaryWriter(
			self._glos,
			entryFmt="{word}\t{defi}\n",
			writeInfo=self._enable_info,
			outInfoKeysAliasDict=None,
		)
		writer.setAttrs(
			encoding=self._encoding,
			wordListEncodeFunc=joinByBar,
			wordEscapeFunc=escapeNTB,
			defiEscapeFunc=escapeNTB,
			ext=".txt",
			resources=self._resources,
			word_title=self._word_title,
			file_size_approx=self._file_size_approx,
		)
		writer.open(self._filename)
		yield from writer.write()
		writer.finish()
