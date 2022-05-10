#!/usr/bin/env python

"""
Rev-1ファイルを解析（パース）するためのモジュール。

各クラスの構造とメンバ変数は、
https://mcnp.lanl.gov/pdf_files/la-ur-17-20098.pdf
に準拠するので参照されたい。

使い方：
>>> import rev1
>>> f = open("REV1.01v")
>>> parsed = rev1.load(f)
"""


from __future__ import annotations
import dataclasses
from itertools import chain
from typing import Iterable


@dataclasses.dataclass
class Nxs:
    nxss: int
    za: int
    f: int
    ng: int
    nxsec: int
    ncov: int
    covtype: int

    @staticmethod
    def from_strs(strings: Iterable[str]) -> Nxs:
        elms = [int(e) for e in strings]
        return Nxs(*elms[0:7])


@dataclasses.dataclass
class Jxs:
    ix_erg: int
    ix_xs_zamt: int
    ix_xs_data: int
    ix_cov: int
    ix_cov_data: int

    @staticmethod
    def from_strs(strings: Iterable[str]) -> Jxs:
        elms = [int(e) for e in strings]
        return Jxs(*elms[0:5])


@dataclasses.dataclass
class CovInfo:
    za1: int
    mt1: int
    za2: int
    mt2: int
    fcv: int
    isparce: int  # maybe 1
    ix_dat: int

    @staticmethod
    def from_strs(strings: Iterable[str]) -> CovInfo:
        elms = [int(float(e)) for e in strings]
        return CovInfo(*elms)


@dataclasses.dataclass
class Xss:
    ix_erg: list[float]  # maybe len = 44+1
    ix_xs_zamt: list[str]
    ix_xs_data: list[str]
    ix_cov: list[CovInfo]
    ix_cov_data: list[float]

    @staticmethod
    def from_strs(elms: Iterable[str], jxs: Jxs) -> Xss:
        elms = [""] + list(elms)  # Rev-1ファイルが1-indexedのため
        ix_erg = [float(elm) for elm in elms[jxs.ix_erg:jxs.ix_xs_zamt]]
        ix_xs_zamt = elms[jxs.ix_xs_zamt: jxs.ix_xs_data]
        ix_xs_data = elms[jxs.ix_xs_data: jxs.ix_cov]

        strs_for_ixcov = [elm for elm in elms[jxs.ix_cov: jxs.ix_cov_data]]
        n = len(strs_for_ixcov) // 7
        ix_cov = [CovInfo.from_strs(strs_for_ixcov[i*7: i*7+7])
                  for i in range(n)]

        ix_cov_data = [float(elm) for elm in elms[jxs.ix_cov_data:]]
        return Xss(ix_erg, ix_xs_zamt, ix_xs_data,
                   ix_cov, ix_cov_data)


@dataclasses.dataclass
class Rev1:
    zaid: str
    awr: float
    temp: float
    date: str
    info: str
    aziz: list[tuple[int, float]]
    nxs: Nxs
    jxs: Jxs
    xss: Xss

    @staticmethod
    def from_str(s: str) -> Rev1:
        rows = s.split("\n")

        zaid, awr, temp, data = rows[0].split()
        zaid, awr, temp, data = zaid, float(awr), float(temp), data

        info = rows[1].strip()

        def strs_from_rows(start: int, end_ex: int | None) -> list[str]:
            return list(chain.from_iterable(
                row.split() for row in rows[start:end_ex]))

        strs_for_aziz = strs_from_rows(2, 6)
        aziz = [(int(az), float(iz)) for az, iz
                in zip(strs_for_aziz[::2], strs_for_aziz[1::2])]

        nxs = Nxs.from_strs(strs_from_rows(6, 8))
        jxs = Jxs.from_strs(strs_from_rows(8, 12))
        xss = Xss.from_strs(strs_from_rows(12, None), jxs)

        return Rev1(zaid, awr, temp, data, info, aziz, nxs, jxs, xss)

    def ix_cov_data_slice(self, start: int, end_ex: int) -> list[float]:
        """
        xss.cov_dataから指定された開始位置から終了位置までのデータを返す。

        Parameters
        ----------
        start:
            開始位置
        end_ex:
            終了位置（range等と同じくこの位置のデータは返り値に含まれない）
        """
        return self.xss.ix_cov_data[start-self.jxs.ix_cov_data:
                                    end_ex-self.jxs.ix_cov_data]


def loads(s: str) -> Rev1:
    """
    文字列をパースする。
    """
    return Rev1.from_str(s)


def load(path: str) -> Rev1:
    """
    指定されたpathを開きパースする。
    """
    with open(path, "rt") as f:
        rev1 = Rev1.from_str(f.read())
    return rev1
