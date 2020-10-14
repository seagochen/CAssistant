#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Oct 14, 2020
# Modified: Oct 14, 2020


def discard_nil(tablet, adopt_func=None, discard_func=None):
    if tablet is None:
        if discard_func is not None:
            discard_func(tablet)
        else:
            pass
    else:
        if adopt_func is not None:
            adopt_func(tablet)

        elif discard_func is not None:
            discard_func(tablet)

        else:
            pass


def discard_empty(trunk, adopt_func=None, discard_func=None):
    if trunk is None or len(trunk) <= 0:
        if discard_func is not None:
            discard_func(trunk)

        else:
            pass

    else:
        if adopt_func is not None:
            adopt_func(trunk)

        elif discard_func is not None:
            discard_func(trunk)

        else:
            pass