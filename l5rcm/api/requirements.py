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
from models.character import Snapshot

class RequirementSet(object):
    def __init__(self, pc, data, requirements):
        self.pc             = pc
        self.data           = data
        self.requirements   = requirements
        self.manual_matches = []

    def add_manual_match(self, field_name):
        self.manual_matches.append(field_name)

    def __match(self):
        matched   = []
        unmatched = []

        # create a character snapshot
        snapshot = Snapshot(self.pc)

        for r in self.requirements:

            if r.field in self.manual_matches:
                matched.append(r)
                continue

            if r.type == 'more':
                unmatched.append(r)
            else:
                if r.match(snapshot, self.data):
                    matched.append(r)
                else:
                    unmatched.append(r)
        return matched, unmatched

    def match_all(self):
        matched, unmatched = self.__match()
        return ( len(unmatched) == 0, unmatched )

    def match_at_least_one(self):
        matched, unmatched = self.__match()
        if len(matched) > 0:
            return (True, matched)
        return (False, [])