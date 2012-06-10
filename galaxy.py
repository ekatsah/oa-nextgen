# -*- coding: UTF-8 -*-
# GALAXY.PY

# Copyright 2011, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from random import randint, choice
from math import log, log1p, exp, floor
from heapq import heappush, heappop

from sys import stdin,exc_info
from traceback import print_tb

from knowledge import techno
from army import scheme, fleet
from util import next_id, random_string, conf, S, I, F, dict_sum, dict_max, dist
from util import t2int

class system:
    def __init__(self, pos, neutral):
        self.id = next_id()
        self.position = pos
        self.assets = dict()
        a = asset(neutral, self)
        a.populate()
        self.assets[a.id] = a


class build:
    def __init__(self, what, count, target):
        self.id = next_id()
        self.what = what
        self.poc = count * what.get_carac(I('poc'))
        assert(self.poc > 0)
        self.count = count
        assert(self.count > 0)
        self.target = target


class asset:
    def __init__(self, owner, syst):
        self.id = next_id()
        self.owner = owner
        self.referer = syst
        self.name = random_string()
        self.planets = dict()    #rule : pla1.id < pla2.id <=> pla1.position < pla2.position
        self.culture = 0
        self.merchs = dict()
        self.policy = I('tax')
        self.constructions = dict() 
        self.poc = 0
        self.ore = 0
        owner.add_asset(self)
        for m in F('goods'):
            self.merchs[m] = 0
    
    def get_pops(self):
        pops = dict()
        
        for p in self.planets.itervalues():
            for race, num in p.pops.iteritems():
                pops[race] = pops.get(race, 0) + num
        return pops
                
    def get_race(self):
        pops = self.get_pops()
        del pops[I('mutant')]
        try:
            return max(pops, key=pops.get)
        except:
            return self.owner.race

    def populate(self):
        for i in xrange(randint(conf.npla[0], conf.npla[1])):
            p = planet(i, self)
            self.planets[p.id] = p
            
        self.ore = 0
        for p in self.planets.itervalues():
            self.ore += p.ore[1]
            
    def add_construction(self, const):
        self.constructions[const.id] = const
    
    def remove_ore(self, quant):
        assert(quant <= self.ore)
        assert(quant > 0)
        quant2 = min(quant, self.ore)
        quant = quant2
        
        for p in self.planets.itervalues():
            if quant <= 0:
                break
            sub = min(quant, p.ore[1])
            quant -= sub
            p.ore[1] -= sub
            
        self.ore -= quant2

    def add_ore(self, quant):
        self.ore += quant
        each = quant / len(self.planets) + 1
        for p in self.planets.itervalues():
            if quant > 0:
                p.ore[1] += min(each, quant)
                quant -= min(each, quant)
            else:
                break

    def add_constructions(self, tech, count):
        tmp = []
        for p in self.planets.itervalues():
            if tech in p.constructions:
                heappush(tmp, [p.constructions[tech], p])
            else:
                heappush(tmp, [0, p])
        for _ in xrange(count):
            tup = heappop(tmp)                      # fixme broke rule 
            if tech in tup[1].constructions:
                tup[1].constructions[tech] += 1
            else:
                tup[1].constructions[tech] = 1
            tup[0] += 1
            heappush(tmp, tup)

    def build_construction(self, c):
        ore = c.what.get_carac(I('cost_ore')) * c.count
        if ore > self.ore:
            raise Exception('pas assez de minerai')
        cent = c.what.get_carac(I('cost_prod')) * c.count
        if cent > self.owner.bank[0]:
            raise Exception('pas assez de centaure')
        if isinstance(c.what, scheme) and not c.what.valid:
            raise Exception('plan invalide')

        self.remove_ore(ore)
        self.owner.set_budget(I('budget_const'), cent)
        if isinstance(c.what, techno):
            if c.target:
                if c.what in c.target.constructions:
                    c.target.constructions[c.what] += c.count
                else:
                    c.target.constructions[c.what] = c.count
                self.owner.add_msg(('Construction de %d %s sur la planete %d '
                                    'de %s.') % (c.count, c.what.name, 
                                                 c.target.position +1, 
                                                 self.name))
            else:
                self.add_constructions(c.what, c.count)
                self.owner.add_msg('Construction de %d %s sur %s.' %
                                   (c.count, c.what.name, self.name))
        else:
            ok = True

            if c.target in self.owner.fleets:
                f = self.owner.fleets[c.target]
                if (I('civilian') in f.caracs and 
                    I('military') in c.what.caracs and
                    self.owner.state[I('lim_flmil')] >= 
                                        self.owner.limits[I('lim_flmil')]):
                    ok = False

                if dist(f.position, self.referer.position) > 20:
                    ok = False
            else:
                ok = False

            if not ok:
                for fl in self.owner.fleets.itervalues():
                    if (I('civilian') in fl.caracs and 
                        I('military') in c.what.caracs):
                        continue
                    
                    if fl.position == self.referer.position:
                        f = fl
                        ok = True

            if not ok:
                if I('military') in c.what.caracs:
                    lim = I('lim_flmil')
                else:
                    lim = I('lim_flciv')

                if self.owner.state[lim] < self.owner.limits[lim]:
                    f = fleet(self.owner, "Fleet " + self.name, 
                                  self.referer.position)
                    self.owner.add_fleet(f)
                    ok = True

            if not ok:
                d = 999 # FIXME MAX_INT
                for fl in self.owner.fleets.itervalues():
                    if I('civilian') in fl.caracs and I('military') in c.what.caracs:
                        continue
                    if dist(fl.position, self.referer.position) < d:
                        d = dist(fl.position, self.referer.position)
                        f = fl
                        ok = True
            
            assert(ok)
            f.add_ships(c.what, self.get_race(), c.count, 0)
            self.owner.add_msg('Construction de %d %s sur %s %s %s' %
                               (c.count, c.what.name, self.name, 
                               'intégré dans', f.name))
    
    def resolv_constructions(self):
        self.poc = 0
        for p in self.planets.itervalues():
            self.poc += 1 + dict_sum(p.constructions, I('YOT'))
        if self.policy == I('construct'):
            self.poc = floor(self.poc * 1.5)

        poc = self.poc
        quit = 0
        while poc > 0 and not quit:
            quit = 1
            for c in self.constructions.itervalues():
                if poc <= 0:
                    break
                if c.poc > 0:
                    c.poc -= 1
                    poc -= 1
                    quit = 0
        
        const_ok = []
        for c in self.constructions.itervalues():
            if c.poc == 0:
                try:
                    self.build_construction(c)
                    const_ok.append(c.id)
                except Exception as e:
                    tb = exc_info()[2]
                    print str(e)
                    print str(print_tb(tb))
                    self.owner.add_msg('Impossible de construire %d %s sur %s: %s'%
                                       (c.count, c.what.name, self.name, str(e)))
        for id in const_ok:
            del self.constructions[id]

    def resolv_croissance(self):
        # merch, ore
        for p in self.planets.itervalues():
            if p.revolt:
                continue
            self.ore += p.prod_min()
            m, q = p.prod_merch()
            if m:
                self.merchs[m] += q
        # pop
        excess = dict()
        for p in self.planets.itervalues():
            if p.revolt:
                continue

            pops = p.increase_pop()
            for r, q in pops.iteritems():
                if r in excess:
                    excess[r] += q
                else:
                    excess[r] = q
        for r, p in excess.iteritems():
            plas = sorted(self.planets.itervalues(),  
                          key=lambda pla: pla.get_growth(r), reverse=True)
            for pla in plas:
                p -= pla.add_pop(r, p)

    def resolv_stabmoney(self):
        # evol stab
        genstab = 0
        if self.policy == I('entertain'):
            genstab += 1
        elif self.policy == I('integrism') or self.policy == I('slavery'):
            genstab -= 2

        if self.owner.capital:
            d = dist(self.referer.position, self.owner.capital.referer.position)
            if d < len(conf.stab_dist):
                genstab += conf.stab_dist[d]
            else:
                genstab += conf.stab_dist[-1]
        else:
            genstab += conf.stab_nocap

        # todo : bonus gouv and cmd
        for p in self.planets.itervalues():
            p.evol_stab(genstab)
            p.test_revolt()
        
        # money money
        money = 0
        for p in self.planets.itervalues():
            if p.revolt:
                continue
            money += p.collect()
        if self.policy == I('tax'):
            money = floor(money * 1.15)
        # todo : bonus gouv and cmd
        self.owner.set_budget(I('budget_tax'), -money)

    def write(self, file, pov = 0):
        out = file.writelines
        out('<asset id="%d">\n' % self.id)
        out('  <name>%s</name>\n' % self.name)
        out('  <position x="%d" y="%d"/>\n' % (self.referer.position[0], 
                                               self.referer.position[1]))
        out('  <policy>%s</policy>\n' % S(self.policy))
        out('  <culture>%d</culture>\n' % self.culture)
        out('  <poc>%d</poc>\n' % self.poc)
        out('  <ore>%d</ore>\n' % self.ore)
        out('  <planets>\n')
        for p in sorted(self.planets):
            self.planets[p].write(file, pov)
        out('  </planets>\n')
        for m in F('goods'):
            out('  <stock_merch type="%s">%d</stock_merch>\n"' % 
                (S(m), self.merchs[m]))
        out('</asset>\n')


class planet:
    def __init__(self, pos, asset):
        self.id = next_id()
        self.referer = asset
        self.position = pos    # position of pla inside planet system
        self.atmosphere = choice(F('atmosphere'))
        self.caracs = (randint(1, 99), randint(1, 99)) # temp, rad
        self.size = randint(1, 5)
        self.structure = self.size*50 + randint(0, 100)
        self.terra = [ 0, False ]     # terra level, true si deja terra ce tour
        self.taxe = I('tax_norm')
        self.stab = [ 100, 100 ] # current stab, old stab
        self.ore = [randint(1, 5), randint(5, 10)]
        self.revolt = False
        self.constructions = dict()
        if not randint(0, 10):    # ~environ 10% de chance de prod
            self.merch = choice(F('goods'))
        else:
            self.merch = None

        self.pops = dict()
        pmax = self.get_popmax(I('mutant'))
        self.pops[I('mutant')] = randint(pmax/2, 3*pmax/4)

    def __setstate__(self, state):
        self.__dict__ = state
        self.terra = [self.terra[0], False]
        self.stab[1] = self.stab[0]

    def evol_stab(self, general):
        self.stab[0] += (general + conf.stab_tax[t2int(self.taxe)])

    def test_revolt(self):
        if self.stab < randint(0, 100):
            self.revolt = True

    def prod_min(self):
        mine = dict_sum(self.constructions, I('extract'))
        extra = dict_max(self.constructions, I('advance_ex')) + self.ore[0]
        prod = (2 * extra - mine + 1) * (mine / 2.0)
        self.ore[1] += prod
        return prod
    
    def terraform(self):
        # FIXME : exception in engine better suited?
        if self.terra[1]:
            raise Exception('Déjà terraformé ce tour')
        owner = self.referer.owner
        if owner.limits['lim_terraform'] < self.terra[0]:
            raise Exception('Limites physiques atteintes')
        cost = (self.terra[0] + 1) * conf.coef['terraform']
        if owner.bank[0] < cost:
            raise Exception('Pas assez de centaures')
        owner.set_budget(I('budget_terra'), cost)
        self.terra = [ self.terra[0] + 1, True ]
        
    def prod_merch(self):
        if not self.merch:
            return (None, 0)
        prod = 0
        for c in self.constructions:
            if (I('prod_merch') in c.caracs and 
                c.caracs[I('prod_merch')][0] == self.merch):
                prod += self.constructions[c] * c.caracs[I('prod_merch')][1]
        return (self.merch, prod)
    
    def collect(self):
        p = sum(self.pops.itervalues())
        return floor(p * t2int(self.taxe) / 10)
            
    def write(self, file, pov = 0):
        out = file.writelines
        out('<planet id="%d">\n' % self.id)
        out('  <position>%d</position>\n' % self.position)
        out('  <atmosphere>%s</atmosphere>\n' % S(self.atmosphere))
        out('  <size>%d</size>\n' % self.size)
        out('  <caracs temp="%d" rad="%d"/>\n' % 
            (self.caracs[0], self.caracs[1]))
        out('  <ore prod="%d">%d</ore>\n' % (self.ore[0], self.ore[1]))
        out('  <terra>%d</terra>\n' % self.terra[0])
        out('  <struct max="%d">0</struct>\n' % self.structure)
        out('  <taxe>%s</taxe>\n' % S(self.taxe))
        out('  <revolt>%d</revolt>\n' % self.revolt)
        out('  <stab evol="%d">%d</stab>\n' % 
            (self.stab[1] - self.stab[0], self.stab[0]))
        out('  <merch>%s</merch>\n' % S(self.merch) if self.merch else '')
        for race in F('races'):
            if not self.colonizable(race):
                continue
            pmax = self.get_popmax(race)
            if race in self.pops:
                pass
                out('  <pop race="%s" max="%d" growth="%d">%d</pop>\n' % 
                    (S(race), pmax, self.get_growth(race), self.pops[race]))
            else:
                out('  <pop race="%s" max="%d">0</pop>\n' % (S(race), pmax))
        for k, v in self.constructions.iteritems():
            out('  <building type="%s" id="%d">%d</building>\n' % 
                (k.name, k.id, v))
        out('</planet>\n')
        
    race_limits = {I('mutant'): ((0, 100), (0, 100), (-10, -10, -10, -10, -10)),
                   I('human'): ((29, 92), (0, 48), (5, 3, 1, 4, 2)),
                   I('sparow'): ((0, 67), (0, 44), (5, 2, 1, 4, 3)),
                   I('fungus'): ((15, 75), (35, 88), (1, 5, 3, 3, 3)),
                   I('wougzy'): ((10, 68), (22, 75), (4, 2, 2, 5, 2)),
                   I('largyn'): ((19, 79), (9, 57), (5, 3, 1, 4, 2)),
                   I('chrysoid'): ((62, 100), (17, 100), (3, 5, 4, 1, 2)),
                   I('zorglub'): ((11, 58), (47, 100), (1, 4, 3, 2, 5))}
    
    def colonizable(self, race):
        assert(race in F('races'))
        rc = self.race_limits[race]     # race caracs
        pc = self.caracs                # planet caracs
        t = self.terra[0] * 2
        if ((pc[0] >= rc[0][0] - t) and (pc[0] <= rc[0][1] + t) and
            (pc[1] >= rc[1][0] - t) and (pc[1] <= rc[1][1] + t)):
            return True
        else:
            return False
    
    def colonize(self, race):
        assert(race in F('races'))
        assert(race not in self.pops)
        self.pops[race] = 10

    def decolonize(self, race):
        assert(race in F('races'))
        assert(race in self.pops)
        del self.pops[race]

    def increase_pop(self):
        decolo = list()
        excess = dict()
        for r, p in self.pops.iteritems():
            n = floor(p * (100 + self.get_growth(r)) / 100)
            if n < 0:
                decolo.append(r)
                continue
            if n < 10:
                n = 10
            pmax = self.get_popmax(r)
            e = max(0, n - pmax)
            self.pops[r] = min(pmax, n)
            if e:
                excess[r] = e
        for r in decolo:
            del self.pops[r]
        return excess
    
    def get_growth(self, race):
        if race == I('mutant'):
            return -10
        else:
            return 20 if self.referer.policy == I('expand') else 15

    def add_pop(self, race, pop):
        if race not in self.pops:
            return 0
        pmax = self.get_popmax(race)
        e = min(pmax - self.pops[race], pop)
        self.pops[race] = min(pmax, self.pops[race] + pop)
        return e

    def get_popmax(self, race):
        rc = self.race_limits[race]     # race caracs
        pc = self.caracs                # planet caracs
        te, tm = (rc[0][1] - rc[0][0])/2, (rc[0][1] + rc[0][0])/2
        re, rm = (rc[1][1] - rc[1][0])/2, (rc[1][1] + rc[1][0])/2
        ta = 10 * log(self.terra[0]+2) * tm / (te * (abs(tm - pc[0]) + 41))
        ra = 10 * log(self.terra[0]+2) * rm / (re * (abs(rm - pc[1]) + 41))
        pmax = 5000*log1p(self.size)*exp(10*ta*ra)*(1+self.terra[0])/log(re+te)
        return int(pmax * (11 - len(self.pops) / 10) / 10)

    def destroy(self, techno, num):
        assert(techno in self.constructions)
        if self.constructions[techno] > num:
            self.constructions[techno] -= num
        elif self.constructions[techno] == num:
            del self.constructions[techno]
        else:
            num = self.constructions[techno]
            del self.constructions[techno]
        return num 
