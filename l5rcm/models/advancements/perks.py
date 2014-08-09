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

from base import Base

class Perk(Base):
    def __init__(self, perk, rank, cost, extra_tag = None):
        super(Perk, self).__init__('perk', cost)
        self.perk       = perk
        self.rank       = rank
        self.extra_tag  = extra_tag
        self.extra_info = ''

    def to_dict(self):
        out = super(Perk, self).to_dict()
        out['perk'      ] = self.perk
        out['rank'      ] = self.rank
        out['extra_tag' ] = self.extra_tag
        out['extra_info'] = self.extra_info

        return out

class Merit(Perk):
    pass

class Flaw(Perk):
    pass
