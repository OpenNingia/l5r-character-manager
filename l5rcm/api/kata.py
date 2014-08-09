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
from .requirements import RequirementSet

class KataNotFound(Exception):
    def __init__(self, kata_id):
        self.kata_id = kata_id
        msg          = "Kata not found: {}".format(kata_id)
        Exception.__init__(self, msg)

class Kata(object):

    def __init__(self, pc, data):
        self.pc   = pc
        self.data = data

    def check_mastery(self, kata_id):
        '''returns True if the PC can master the kata'''

        kata_dal = self.data.query.get_kata(kata_id)
        if not kata_dal:
            raise KataNotFound(kata_id)

        relevant_ring = kata_dal.element
        ring_val      = self.pc.get_ring_rank(relevant_ring)
        return ring_val >= kata_dal.mastery

    def check_eligibility(self, kata_id):
        '''returns True if the PC is eligible to learn this kata, and returns the matching requirement'''

        kata_dal = self.data.query.get_kata(kata_id)
        if not kata_dal:
            raise KataNotFound(kata_id)

        rs             = RequirementSet(self.pc, self.data, kata_dal.require)
        match, matched = rs.match_at_least_one()
        eligible       = self.check_mastery(kata_id) and match

        return (eligible, matched)


    def calculate_cost(self, kata_id):
        '''calculate the kata cost'''

        kata_dal = self.data.query.get_kata(kata_id)
        if not kata_dal:
            raise KataNotFound(kata_id)

        return kata_dal.mastery