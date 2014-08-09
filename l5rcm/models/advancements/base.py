# -*- coding: utf-8 -*-
# Copyright (C) 2014 Daniele Simonetti
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import time

class Base(object):
    BUY_FOR_FREE = False

    @staticmethod
    def set_buy_for_free(flag):
        Advancement.BUY_FOR_FREE = flag

    @staticmethod
    def get_buy_for_free():
        return Advancement.BUY_FOR_FREE

    def __init__(self, aid, tag):
        self.id        = aid
        self.tag       = tag
        self.brief     = ''
        self.rule      = None
        self.cost      = 0
        self.ts        = time.time()

    def to_dict(self):
        out = {}
        out['id'   ] = self.id
        out['tag'  ] = self.tag
        out['brief'] = self.brief
        out['ruke' ] = self.rule
        out['cost' ] = self.cost
        out['ts'   ] = self.ts

        return out

    def __str__(self):
        return "{0}, {1}, {2}".format(self.id, self.tag, self.brief)

class NewValue(Base):
    def __init__(self, aid, tag, new_value):
        super(NewValue, self).__init__(aid, tag)
        self.new_value = new_value

    def to_dict(self):
        out = super(NewValue, self).to_dict()
        out['new_value'] = self.new_value
        
        return out
