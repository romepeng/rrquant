#!/usr/bin/python
# -*- coding: utf8 -*-


def list_getitem(data, i):
    """对C++引出的vector，实现python的切片，
       将引入的vector类的__getitem__函数覆盖即可。
    """
    if isinstance(i, int):
        length = len(data)
        index = length + i if i < 0 else i
        if index < 0 or index >= length:
            raise IndexError("index out of range: %d" % i)
        return data.get(index)

    elif isinstance(i, slice):
        return [data.get(x) for x in range(*i.indices(len(data)))]

    else:
        raise IndexError("Error index type")
