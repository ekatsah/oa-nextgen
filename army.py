# -*- coding: UTF-8 -*-
# SHIPS.PY

# Copyright 2011, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from math import log, floor
from util import next_id, dict_max, dict_maxt, dict_sum, dict_sumt, dict_mint 
from util import I, S, F, conf, get_carac


def define(obj, carac, func):
        tmp = func(obj.compos, carac)
        if tmp > 0:
            obj.caracs[carac] = tmp


class scheme:
    define = define
    get_carac = get_carac

    def __init__(self, owner, name, brand, domain, cut): # domain public/private/alliance
        self.id = next_id()
        self.name = name
        self.brand = brand
        self.domain = domain
        self.cut = cut
        self.owner = owner
        self.compos = dict()
        self.caracs = dict()
        self.merchs = dict()
        self.valid = True

    def add_compo(self, tech, num):
        # FIXME restriction 1 mdc et 1 colo.
        if tech not in self.compos:
            self.compos[tech] = num
        else:
            self.compos[tech] = self.compos[tech] + num
            
    def finalize(self):
        # civ or mil?
        self.define(I('military'), dict_max)
        if I('military') not in self.caracs:
            self.caracs[I('civilian')] = 1
        
        tmp = max(1, dict_sum(self.compos, I('cases')))
        self.caracs[I('size')] = floor(log(tmp-1, 2))+1
        self.caracs[I('poc')] = floor(tmp/2)
        tmp = 17 - self.caracs[I('size')] + dict_max(self.compos, I('propeller'))
        if I('military') in self.caracs:
            tmp = floor(tmp*2/3)
        self.caracs[I('velocity')] = tmp
        self.caracs[I('cost_prod')] = dict_sum(self.compos, I('cost_prod')) # wait, wat?
        self.caracs[I('cost_ore')] = dict_sum(self.compos, I('cost_ore'))
        
        self.define(I('cargo'), dict_sum)
        self.define(I('syst_rad'), dict_max)
        self.define(I('fleet_rad'), dict_max)
        self.define(I('SCM'), dict_max)
        self.define(I('colo'), dict_max)

        sa, pa = 0, 0
        for t in self.compos:
            if I('weapon') in t.caracs:
                w = t.caracs[I('weapon')][0]
                n = t.caracs[I('weapon')][1]
                sa += (w.ha+w.sa) * n * self.compos[t]
                pa += (w.pa) * n * self.compos[t]
        if sa > 0:
            self.caracs[I('SA')] = sa
        if pa > 0:
            self.caracs[I('PA')] = pa
                
        for t in self.compos:
            if I('cost_merch') in t.caracs:
                merch = t.caracs[I('cost_merch')]
                if merch[0] not in self.merchs:
                    self.merchs[merch[0]] = 0
                self.merchs[merch[0]] += merch[1] * self.compos[t]

    def price(self):
        m = 0;
        for i in self.merchs.itervalues():
            m += 15 * i

        return self.get_carac(I('cost_prod')) * 3 + \
               self.get_carac(I('cost_ore')) * 8 + m

    def write(self, file):
        out = file.writelines
        out('<ship id="%d">\n' % self.id)
        out('  <name>%s</name>\n' % self.name)
        out('  <brand>%s</brand>\n' % self.brand)
        if self.domain == I('public') or self.domain == I('private'): #fixme implem alliances
            out('  <domain>%s</domain>\n' % S(self.domain))
        out('  <owner id="%d">%s</owner>\n' % (self.owner.id, self.owner.name))
        for t, n in self.compos.iteritems():
            out('  <compo id="%d" name="%s">%d</compo>\n' % (t.id, t.name, n))
        for c, n in self.caracs.iteritems():
            out('  <carac name="%s">%d</carac>\n' % (S(c), n))
        for m, n in self.merchs.iteritems():
            out('  <merch name="%s">%d</merch>\n' % (S(m), n))
        out('</ship>\n')

        
class fleet:
    define = define
    get_carac = get_carac
    
    def __init__(self, owner, name, pos, guideline=I('neutral'), target=None):
        self.id = next_id()
        self.name = name
        self.owner = owner
        self.compos = dict()     # (vso, race) -> (nombre, degats)
        self.caracs = dict()
        self.cargo = dict()
        self.position = pos
        self.move = None        # position destination
        self.caracs[I('behaviour')] = guideline
        self.caracs[I('target')] = target
        
    def finalize(self):
        inv = (self.get_carac(I('behaviour')), self.get_carac(I('target')),
               self.get_carac(I('build_order'))) 
        self.caracs = dict()
        
        self.caracs[I('behaviour')] = inv[0]
        self.caracs[I('target')] = inv[1]
        if isinstance(inv[2], scheme):
            self.caracs[I('build_order')] = inv[2]
        self.define(I('military'), dict_maxt)
        if I('military') not in self.caracs:
            self.caracs[I('civilian')] = 1
        
        self.define(I('cargo'), dict_sumt)
        self.define(I('SCM'), dict_sumt)
        self.define(I('syst_rad'), dict_maxt)
        self.define(I('fleet_rad'), dict_maxt)
        self.define(I('SA'), dict_sumt)
        self.define(I('PA'), dict_sumt)
        self.caracs[I('velocity')] = dict_mint(self.compos, I('velocity'))
        try:
            power = (dict_sumt(self.compos, I('poc')) * self.caracs[I('SA')] * 
                     self.caracs[I('PA')] * conf.coef['fleet'])
        except KeyError:
            power = 0
        self.caracs[I('size')] = F('fleet_size')[max(9, floor(log(power+1, 2)))]
        
    def add_ships(self, ship, race, num, dom, fin=True):
        assert(num > 0)
        assert(dom >= 0)
        assert(race in F('races'))
        assert(isinstance(ship, scheme))
        
        tnum, tdom = 0, 0
        if (ship, race) in self.compos:
            tnum, tdom = self.compos[(ship, race)]
        self.compos[(ship, race)] = (tnum + num, tdom + dom)
        if fin:
            self.finalize()
    
    def remove_ships(self, fl, num):
        assert(fl in self.compos)
        assert(num <= self.compos[fl][0] and num > 0)
        if num == self.compos[fl][0]:
            tnum, tdom = self.compos[fl]
            del self.compos[fl]
        else:
            tnum, odom = self.compos[fl]
            tdom = int(odom * float(num/tnum))
            self.compos[fl] = (tnum - num, odom - tdom)
        self.finalize()
        return tnum, tdom

    def build(self):
        ship, num, com = self.get_carac(I('build_order')), 0, [] 
        if not isinstance(ship, scheme):
            return
        
        price, poc = ship.price(), ship.get_carac(I('poc'))
        for (s, r), (n, _) in self.compos.iteritems():
            p = s.get_carac(I('SCM'))
            if poc > p:
                continue
            pn = floor(p / poc) * n
            if self.owner.bank[0] >= (price * pn):
                self.owner.set_budget(I('budget_const'), price * pn)
                com.append((pn, r))
                num += pn

        for n, r in com:
            self.add_ships(ship, r, n, 0, False)
        self.finalize()
        self.owner.add_msg("Votre flotte %s a produit %d %s" % 
                           (self.name, num, ship.name))

    def write(self, file, pov):
        out = file.writelines
        out('<fleet id="%d">\n' % self.id)
        out('  <name>%s</name>\n' % self.name)
        out('  <position>(%d,%d)</position>\n' % 
            (self.position[0], self.position[1]))
        if self.move:
            out('  <dest>(%d,%d)</dest>\n' % (self.move[0], self.move[1]))
        for c, v in self.caracs.iteritems():
            if c == I('build_order'):
                out('  <carac name="%s">%s</carac>\n' % (S(c), v.name))
            elif c == I('target'):
                continue
            elif c == I('behaviour'):
                if v == I('pla_conquest'):
                    out('  <carac name="%s">%s %d</carac>\n' % 
                        (S(c), S(v), self.get_carac(I('target'))))
                elif v == I('player_attack'):
                    out('  <carac name="%s">%s %s</carac>\n' % 
                        (S(c), S(v), self.get_carac(I('target')).name))
                else:
                    out('  <carac name="%s">%s</carac>\n' % (S(c), S(v)))
            else:
                out('  <carac name="%s">%d</carac>\n' % (S(c), v))
        for squad, v in self.compos.iteritems():
            out('<squad type="%s" sid="%d" race="%s" dammage="%d">%d</squad>\n'%
                (squad[0].name, squad[0].id, S(squad[1]), v[1], v[0]))
        out('</fleet>\n')
