#!/usr/bin/env python

"""
Rev-1ファイルのzaidを普通のzaidに変換（decode）、
またはその逆（encode）をするためのモジュール。

Rev-1ファイルに限らず、littleエンディアンでエンコードされたasciiコードを
デコードするのにも使える。

例："poly"をエンコードすることを考える。
まず各文字をasciiコードに変換する。
'p'のコード = 112 = 0x70 = 0b1110000
'o'のコード = 111 = 0x6f = 0b1101111
'l'のコード = 108 = 0x6c = 0b1101100
'y'のコード = 121 = 0x79 = 0b1111001

コードの2進表記を後ろから(つまり'y', 'l', 'o', 'p'の順で)結合する。
'1111001' + '1101100' + '1101111' + '1110000'
= 1111001110110011011111110000
これを10進数に変換すると、
255539184となりエンコードが完了する。

実際、Rev-1ファイルでは"poly"が"255539184"へと変換されている。

デコードはこの逆の操作となる。

※もっといい感じのライブラリや関数が既にあるかもしれない。
"""


def encode(d: str) -> int:
    e = ""
    for c in reversed(d):
        e += bin(ord(c))[2:].zfill(7)
    e = int(e, 2)
    return e


def decode(encoded: int) -> str:
    e = bin(encoded)[2:]
    remain = len(e) % 7
    if remain != 0:
        div = len(e) // 7
        e = e.zfill(7*(div+1))
    d = ""
    for i in range(len(e)//7+1):
        if n := e[i*7:i*7+7]:
            d += chr(int(n, 2))
    return d[::-1]


# ユニットテスト
if __name__ == "__main__":
    e = 13533748281
    d = "98252"
    assert encode(d) == e, f"左辺={encode(d)} 右辺={e}"
    assert decode(e) == d, f"左辺={decode(e)} 右辺={d}"

    e = 255539184
    d = "poly"
    assert encode(d) == e, f"左辺={encode(d)} 右辺={e}"
    assert decode(e) == d, f"左辺={decode(e)} 右辺={d}"

