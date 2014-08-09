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

class KihoNotFound(Exception):
    def __init__(self, kiho_id):
        self.kiho_id = kiho_id
        msg          = "Kiho not found: {}".format(kiho_id)
        Exception.__init__(self, msg)

class Kiho(object):

    # STATUS
    ST_ERROR          = 0
    ST_OK_BROTHERHOOD = 1
    ST_OK_MONK        = 2
    ST_OK_NINJA       = 3
    ST_OK_SHUGENJA    = 4

    # ELIGIBILITY
    ELIGIBILITY_RING_SCHOOL     = 5
    ELIGIBILITY_RING            = 6
    ELIGIBILITY_SCHOOL          = 7
    ELIGIBILITY_KO              = 8

    def __init__(self, pc, data):
        self.pc   = pc
        self.data = data

    def check_status(self):
        '''returns the pc status and if its ok to learn a kiho'''

        is_monk                 = self.pc.is_monk        ()
        is_brotherhood          = self.pc.is_brotherhood ()
        is_ninja                = self.pc.is_ninja       ()
        is_shugenja             = self.pc.is_shugenja    ()

        if is_brotherhood: return Kiho.ST_OK_BROTHERHOOD
        if is_monk       : return Kiho.ST_OK_MONK
        if is_ninja      : return Kiho.ST_OK_NINJA
        if is_shugenja   : return Kiho.ST_OK_SHUGENJA
        return Kiho.ST_ERROR


    def check_eligibility(self, kiho_id):
        '''returns True if the PC is eligible to learn this kiho and an hint on what's missing'''

        kiho = self.data.query.get_kiho(kiho_id)
        if kiho is None:
            raise KihoNotFound(kiho_id)

        potential_mastery       = 0

        is_monk                 = self.pc.is_monk        ()
        is_brotherhood          = self.pc.is_brotherhood ()
        is_ninja                = self.pc.is_ninja       ()
        is_shugenja             = self.pc.is_shugenja    ()

        ninja_rank              = self.pc.get_school_rank_sum('ninja')
        monk_rank               = self.pc.get_school_rank_sum('monk' )
        relevant_ring           = kiho.element
        ring_rank               = self.pc.get_ring_rank(relevant_ring)

        if is_monk:
            potential_mastery = monk_rank + ring_rank
        else:
            potential_mastery = ring_rank

        if is_brotherhood:
            return (potential_mastery >= kiho.mastery, Kiho.ELIGIBILITY_RING_SCHOOL)
        elif is_monk:
            return (potential_mastery >= kiho.mastery, Kiho.ELIGIBILITY_RING_SCHOOL)
        elif is_shugenja:
            return (ring_rank >= kiho.mastery, Kiho.ELIGIBILITY_RING)
        elif is_ninja:
            return (ninja_rank >= kiho.mastery, Kiho.ELIGIBILITY_SCHOOL)

        return (False, Kiho.ELIGIBILITY_KO)

    def calculate_cost(self, kiho_id):
        '''calculate the kiho cost, based on the pc'''

        kiho = self.data.query.get_kiho(kiho_id)
        if kiho is None:
            raise KihoNotFound(kiho_id)

        # tattoos are free as long as you're eligible
        if 'tattoo' in kiho.tags: return 0

        cost_mult               = 1

        is_monk                 = self.pc.is_monk        ()
        is_brotherhood          = self.pc.is_brotherhood ()
        is_ninja                = self.pc.is_ninja       ()
        is_shugenja             = self.pc.is_shugenja    ()

        if is_brotherhood:
            cost_mult = 1 # 1px / mastery
        elif is_monk:
            cost_mult = 1.5
        elif is_shugenja:
            cost_mult = 2
        elif is_ninja:
            cost_mult = 2

        return int(ceil(kiho.mastery*cost_mult))