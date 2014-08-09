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

from .base import Base

class NewPower(Base):
    def __init__(self, aid, tag, pid):
        super(NewPower, self).__init__(aid, tag)
        self.power_id = pid

    def to_dict(self):
        out = super(NewPower, self).to_dict()
        out['power_id'] = self.power_id
        return out

class Kiho(NewPower):
    def __init__(self, aid, kiho_id):
        super(Kiho, self).__init__(aid, 'kiho', kiho_id)

class Kata(NewPower):
    def __init__(self, aid, kata_id):
        super(Kata, self).__init__(aid, 'kata', kata_id)

class Spell(NewPower):
    def __init__(self, aid, spell_id):
        super(Spell, self).__init__(aid, 'spell', spell_id)

class MemorizedSpell(NewPower):
    def __init__(self, aid, spell_id):
        super(MemorizedSpell, self).__init__(aid, 'spellmemo', spell_id)
