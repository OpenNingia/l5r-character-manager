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

from .base import NewValue

class Trait(NewValue):
    def __init__(self, aid, trait_id, new_value):
        super(Trait, self).__init__(aid, 'trait', new_value)
        self.trait_id  = trait_id

    def to_dict(self):
        out = super(Trait, self).to_dict()
        out['trait_id'] = self.trait_id
        return out
