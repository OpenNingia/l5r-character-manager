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
import dal.characterwriter

APP_NAME    = "l5rcm4"
APP_VERSION = "4.0.0"
APP_ORG     = "openningia"

class L5RCMCoreTestCase(unittest.TestCase):

    def setUp(self):

        self.api = api.L5R()

        # create empty character model
        self.api.new_pc()

        # Joining Akodo Bushi School of the Lion clan
        adv = self.api.create_rank_advancement()

        adv.clan    = 'lion'
        adv.family  = 'lion_akodo'
        adv.school  = 'lion_akodo_bushi_school'
        adv.rank    = 1

        school = self.api.data.query.get_school(adv.school)

        self.api.commit_rank_advancement(adv)

        # increase reflexes and awareness
        self.api.increase_trait('reflexes')
        self.api.increase_trait('reflexes')

        self.api.increase_trait('awareness')
        self.api.increase_trait('awareness')

        self.cw  = dal.characterwriter.CharacterWriter( self.api.pc )


    def test_write_object(self):
        self.assertTrue( self.cw.to_dict() is not None )

    def test_check_name(self):
        d   = self.cw.to_dict()
        self.assertEquals( self.api.query.get_name(), d['info']['name'] )


if __name__ == '__main__':
    unittest.main()
