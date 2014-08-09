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

APP_NAME    = "l5rcm4"
APP_VERSION = "4.0.0"
APP_ORG     = "openningia"

class L5RCMCoreTestCase(unittest.TestCase):

    def setUp(self):

        self.api = api.L5R()

        # create empty character model
        self.api.new_pc()

    def test_initial(self):

        for trait, rank in self.api.query.iter_traits(): # generator
            self.assertTrue( rank == 2, '{} rank is {}'.format(trait, rank) )

        self.assertFalse ( self.api.query.is_monk       () )
        self.assertFalse ( self.api.query.is_brotherhood() )
        self.assertFalse ( self.api.query.is_bushi      () )
        self.assertFalse ( self.api.query.is_ninja      () )
        self.assertFalse ( self.api.query.is_shugenja   () )

        self.assertTrue  ( self.api.query.get_current_clan  () is None )
        self.assertTrue  ( self.api.query.get_current_family() is None )
        self.assertTrue  ( self.api.query.get_current_school() is None )

    def test_data_location(self):
        core_pack_path = dal.get_path('core.data')
        self.assertTrue( core_pack_path is not None )
        self.assertTrue( os.path.exists(core_pack_path), '{} not found'.format(core_pack_path) )

    def test_increase_trait(self):

        self.api.increase_trait('strength')
        self.assertTrue( self.api.query.get_trait_rank('strength') == 3 )

        self.api.increase_void()
        self.assertTrue( self.api.query.get_ring_rank('void') == 3 )

    def test_increase_skill(self):
        self.api.increase_skill('kenjutsu')
        self.assertTrue( self.api.query.get_skill_rank('kenjutsu') == 1 )
        self.api.undo_advancement()
        self.assertTrue( self.api.query.get_skill_rank('kenjutsu') == 0 )

    def test_xp(self):
        self.assertTrue( self.api.query.get_xp_spent () == 0 )

        self.assertTrue( self.api.buy_trait_rank('strength') )
        self.assertTrue( self.api.query.get_trait_rank('strength') == 3 )
        self.assertTrue( self.api.query.get_xp_spent  () == 12 ) # increasing a trait from 2 to 3 costs 12 xp

        self.assertTrue( self.api.buy_void_rank() )
        self.assertTrue( self.api.query.get_ring_rank('void') == 3 )
        self.assertTrue( self.api.query.get_xp_spent () == 30, 'xp spent are {}'.format(self.api.query.get_xp_spent ()) ) # increasing void from 2 to 3 costs 18 xp

        self.api.undo_advancement()
        self.assertTrue( self.api.query.get_ring_rank('void') == 2 )
        self.assertTrue( self.api.query.get_xp_spent () == 12, 'xp spent are {}'.format(self.api.query.get_xp_spent ()) ) # increasing void from 2 to 3 costs 18 xp

    def test_exp_limit(self):
        self.api.set_xp_limit(0)

        self.assertFalse( self.api.buy_skill_rank('kenjutsu') )
        self.assertTrue ( self.api.query.get_skill_rank('kenjutsu') == 0 )

    def test_rank_advancement(self):

        adv = self.api.create_rank_advancement()

        adv.clan    = 'crab'
        adv.family  = 'crab_hida'
        adv.school  = 'crab_hida_bushi_school'
        adv.rank    = 1

        school = self.api.data.query.get_school(adv.school)
        self.assertTrue( len(self.api.data.schools) > 0 )
        self.assertTrue( school is not None, '{} not found in dal'.format(adv.school) )

        self.api.commit_rank_advancement(adv)

        self.assertTrue( self.api.query.get_current_clan  () == 'crab'                   )
        self.assertTrue( self.api.query.get_current_family() == 'crab_hida'              )
        self.assertTrue( self.api.query.get_current_school() == 'crab_hida_bushi_school' )

        self.assertTrue( self.api.query.is_bushi() )

        self.api.undo_rank_advancement()

        self.assertFalse( self.api.query.is_bushi() )

    def test_unknown_school(self):

        unknown_school = 'crab_unknown_school'
        adv = self.api.create_rank_advancement()

        adv.clan    = 'crab'
        adv.family  = 'crab_hida'
        adv.school  = 'crab_unknown_school'
        adv.rank    = 1

        self.assertRaises(Exception, self.api.commit_rank_advancement, adv)

    def test_advanced_school(self):

        adv = self.api.create_rank_advancement()

        adv.clan    = 'crab'
        adv.family  = 'crab_hida'
        adv.school  = 'crab_hida_bushi_school'

        self.assertTrue( adv.rank        == 1 )

        advanced_school      = 'crab_defender_of_the_wall'
        missing_requirements = self.api.get_missing_requirements_to_join_school(advanced_school)
        self.assertFalse( len(missing_requirements) == 0,
            'missing requirements: {}'.format(' '.join([str(x) for x in missing_requirements])) )

        self.api.commit_rank_advancement(adv)

        self.assertTrue( adv.school_rank == 1 )
        self.assertTrue( self.api.query.get_first_rank_advancement() is not None )

        self.api.increase_trait('willpower')
        self.api.increase_trait('willpower')

        self.api.increase_trait('stamina')
        self.api.increase_trait('stamina')

        self.api.increase_trait('strength')
        self.api.increase_trait('strength')
        self.api.increase_trait('strength')

        self.api.increase_skill('defense')
        self.api.increase_skill('defense')
        self.api.increase_skill('defense')
        self.api.increase_skill('defense')

        self.api.increase_skill('heavy_weapons')
        self.api.increase_skill('heavy_weapons')
        self.api.increase_skill('heavy_weapons')
        self.api.increase_skill('heavy_weapons')
        self.api.increase_skill('heavy_weapons')

        self.api.increase_skill('lore_shadowlands')
        self.api.increase_skill('lore_shadowlands')
        self.api.increase_skill('lore_shadowlands')
        self.api.increase_skill('lore_shadowlands')
        self.api.increase_skill('lore_shadowlands')

        #self.api.add_skill_emphasis('heavy_weapons', 'Tetsubo')

        missing_requirements = self.api.get_missing_requirements_to_join_school(advanced_school)
        self.assertTrue( len(missing_requirements) == 0,
            'missing requirements: {}'.format(' '.join([str(x) for x in missing_requirements])) )

    def test_insight(self):

        self.assertTrue( self.api.query.get_insight_rank() == 1 )

        self.api.increase_trait('willpower')
        self.api.increase_trait('stamina')

        self.assertTrue( self.api.query.get_ring_rank('earth') == 3 )

        self.api.increase_trait('awareness')
        self.api.increase_trait('reflexes')

        self.assertTrue( self.api.query.get_ring_rank('air') == 3 )

        self.api.increase_trait('perception')
        self.api.increase_trait('strength')

        self.assertTrue( self.api.query.get_ring_rank('water') == 3 )

        self.api.increase_trait('intelligence')
        self.api.increase_trait('agility')

        self.assertTrue( self.api.query.get_ring_rank('fire') == 3 )

        self.api.increase_void()

        self.assertTrue( self.api.query.get_ring_rank('void') == 3 )

        self.assertTrue( self.api.query.get_insight_rank() == 2 )


if __name__ == '__main__':
    unittest.main()
