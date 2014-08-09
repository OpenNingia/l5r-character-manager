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

import unittest
import os

# character creation / progression api
import api
import api.constants

import dal
import dal.query

import api.kiho

from . import mixin

APP_NAME    = "l5rcm4"
APP_VERSION = "4.0.0"
APP_ORG     = "openningia"

class L5RCMPowersTestCase(mixin.WarningTestMixin, unittest.TestCase):

    def setUp(self):

        self.api = api.L5R()

        # create empty character model
        self.api.new_pc()

        # create a monk character
        # this is to facilitate powers ( kata/kiho ) testing
        adv = self.api.create_rank_advancement()

        adv.clan    = 'monks'
        adv.family  = 'monks_the_temple_of_kaimetsu_uo'
        adv.school  = 'monks_the_temples_of_the_thousand_fortunes_monk_school'

        self.api.commit_rank_advancement(adv)

    def test_monk(self):
        self.assertTrue( self.api.query.is_monk       () )
        self.assertTrue( self.api.query.is_brotherhood() )

    def test_can_learn_kiho(self):

        self.assertTrue( self.api.query.kiho.check_status() == api.kiho.Kiho.ST_OK_BROTHERHOOD )
        self.assertTrue( self.api.query.get_school_rank_sum('monk') == 1 )
        self.assertTrue( self.api.query.get_ring_rank('air') == 2 )
        self.assertTrue( self.api.query.kiho.check_eligibility('air_fist') ==
             (True, api.kiho.Kiho.ELIGIBILITY_RING_SCHOOL) )
        self.assertTrue( self.api.query.kiho.check_eligibility('flee_the_darkness') ==
             (False, api.kiho.Kiho.ELIGIBILITY_RING_SCHOOL) )

    def test_add_kiho(self):

        # this is a non existant kiho
        self.assertRaises( Exception, self.api.add_kiho, '_gold_carp_punch_' )

        # these should return True instead
        self.assertTrue( self.api.add_kiho('air_fist') )
        self.assertTrue( 'air_fist' in self.api.query.get_kiho() )

        # undoing the advancement should undo the kiho too
        self.api.undo_advancement()
        self.assertFalse( 'air_fist' in self.api.query.get_kiho() )


    def test_can_learn_kata(self):
        self.assertFalse( self.api.query.kata.check_mastery    ('disappearing_world_style') )
        self.assertFalse( self.api.query.kata.check_eligibility('disappearing_world_style')[0] )

        # this only needs void 3
        self.assertTrue ( self.api.query.kata.check_mastery    ('balance_the_elements_style') )

    def test_add_kata(self):

        # this is a kiho, not a kata, should raise and exception
        self.assertRaises( Exception, self.api.add_kata, 'air_fist' )

        self.assertTrue( self.api.add_kata('disappearing_world_style') )
        self.assertTrue( 'disappearing_world_style' in self.api.query.get_kata() )

    def test_buy_kata(self):

        self.assertWarns( UserWarning, self.api.buy_kata, 'disappearing_world_style' )

        self.api.set_xp_limit(200)

        # join akodo bushi school
        adv = self.api.create_rank_advancement()

        adv.clan    = 'lion'
        adv.family  = 'lion_akodo'
        adv.school  = 'lion_akodo_bushi_school'
        adv.rank    = 1

        self.api.commit_rank_advancement(adv)

        self.assertTrue( self.api.query.has_tag("lion_akodo_bushi_school") )

        # increase fire ring until 4
        self.assertTrue(self.api.buy_trait_rank('agility'     ))
        self.assertTrue(self.api.buy_trait_rank('intelligence'))
        self.assertTrue(self.api.buy_trait_rank('agility'     ))
        self.assertTrue(self.api.buy_trait_rank('intelligence'))

        self.assertTrue( self.api.query.get_trait_rank('agility') == 5 )
        self.assertTrue( self.api.query.get_trait_rank('intelligence') == 4 )
        self.assertTrue( self.api.query.get_ring_rank('fire') == 4 )
       
        self.assertTrue( self.api.buy_kata('disappearing_world_style') )   
        self.assertTrue( 'disappearing_world_style' in self.api.query.get_kata() )        

if __name__ == '__main__':
    unittest.main()
