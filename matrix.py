# -*- coding: UTF-8 -*-
# MATRIX.PY

# Copyright 2011, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from random import randint, choice

from util import next_id, I, S, F, conf
from knowledge import techno, weapon
from galaxy import system
from army import scheme


class player:
    def __init__(self, name, domain, race, tour):
        self.id = next_id()
        self.name = name
        self.domain = domain
        self.assets = dict()
        self.race = race
        self.capital = None
        self.technos = dict()
        self.cache_ftech = dict() # cache future techno
        self.research = dict() # recherche techno en cours | tech -> points
        self.started = tour
        self.alife = True
        self.schemes, self.tmpschemes = dict(), dict()
        self.limits = conf.limits.copy()     # limites personnelles
        self.state = dict()                 # etat courant des limits
        for l in self.limits:
            self.state[l] = 0
        self.fleets, self.tmpfleets = dict(), dict()
        self.percent = [0, 0, 0] # budget tech, special, contre esp
        self.bank = [20000, 0, 0] # centaure, points tech, points spe
        self.budgets = dict()
        self.msg = list()
        self.alliances = dict()

    def __setstate__(self, state):
        self.__dict__ = state
        self.budgets = dict()
        self.budgets[I('reserv')] = self.bank[0]
        self.msg = list()
        self.tmpfleets = dict()
        self.tmpschemes = dict()

    def add_asset(self, asset):
        self.assets[asset.id] = asset
        asset.owner = self
        if not self.capital:
            self.capital = asset

    def get_budget(self, budget):
        return self.budgets[budget]

    def set_budget(self, budget, cost):
        if budget in self.budgets:
            self.budgets[budget] -= cost
        else:
            self.budgets[budget] = -cost
        self.bank[0] -= cost
        
    def add_msg(self, msg):
        self.msg.append(msg)
        
    def del_asset(self, id):
        if id in self.assets:
            del self.assets[id]
        if self.capital.id == id:
            if len(self.assets) > 0:
                self.capital = choice(self.assets)
            else:
                self.capital = None

    def compute_ftech(self, world):
        self.cache_ftech = dict()
        for tech in world.technos.itervalues():
            if tech.id in self.technos:
                continue

            axx = True
            for p in tech.parents:
                if p.id not in self.technos:
                    axx = False
            if axx:
                self.cache_ftech[tech.id] = tech

    def add_techno(self, techno, world=None):
        self.technos[techno.id] = techno
        if techno.id in self.research:
            del self.research[techno.id]

        if world:
            self.compute_ftech(world)
    
    def add_scheme(self, scheme):
        self.schemes[scheme.id] = scheme
    
    def add_fleet(self, fleet):
        lim = I('lim_flmil' if I('military') in fleet.caracs else 'lim_flciv')
        if self.state[lim] > self.limits[lim]:
            raise Exception('limit fleet')
        self.state[lim] += 1
        self.fleets[fleet.id] = fleet

    def add_tmpfleet(self, fid, fleet):
        self.tmpfleets[fid] = fleet

    def check_fleets(self):
        def check(fldict, fc, fm):
            fleets = list()
            for k, fl in fldict.iteritems():
                if fl.get_carac(I('size')) == 0:
                    fleets.append((k, fl))
                    continue

                if I('military') in fl.caracs:
                    if fm > self.limits[I('lim_flmil')]:
                        fleets.append((k, fl))
                    else:
                        fm += 1
                else:
                    if fc > self.limits[I('lim_flciv')]:
                        fleets.append((k, fl))
                    else:
                        fc += 1
            for k, _ in fleets:
                del fldict[k]

            return fleets, fc, fm

        fleets, fc, fm = check(self.fleets, 0, 0)
        tmpfleets, tfc, tfm = check(self.tmpfleets, fc, fm)

        self.state[I('lim_flmil')] = fm
        self.state[I('lim_flciv')] = fc
        assert (self.state[I('lim_flmil')] <= self.limits[I('lim_flmil')])
        assert (self.state[I('lim_flciv')] <= self.limits[I('lim_flciv')])

        for fl in self.tmpfleets.itervalues():
            self.fleets[fl.id] = fl

        return fleets + tmpfleets

    def remove_fleet(self, fleet):
        if fleet.id in self.fleets:
            lim = I('lim_flmil' if I('military') in fleet.caracs else 'lim_flciv')
            self.state[lim] -= 1
            assert(self.state[lim] >= 0)

        else:
            for k, fl in self.tmpfleets.iteritems():
                if fl == fleet:
                    del self.tmpfleets[k]
                    return
        raise Exception('fleet not found')
    
    def set_priority(self, tech, spe, cesp):
        if (tech < 0 or spe < 0 or cesp < 0 or 
            tech + spe + cesp > self.limits[I('lim_budget')]):
            return False
        else:
            self.percent = [tech, spe, cesp]
            return True

    def write(self, file, tour, pov = 0):    # pov : 0 - mj, 1 himself
        out = file.writelines
        out('<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n')
        out('<?xml-stylesheet type=\"text/xsl\" href=\"rapport.xsl\"?>\n')
        out('<player id="%d">\n' % self.id)
        out('  <name>%s</name>\n' % self.name)
        out('  <race>%s</race>\n' % S(self.race))
        out('  <domain>%s</domain>\n' % self.domain)
        out('  <tour>%d</tour>\n' % tour)
        if self.capital != None:
            out('  <capital>%d</capital>\n' % self.capital.id)
        for i in [0, 1, 2]:
            out('  <percent type="%s">%d%%</percent>\n' % 
                (S(F('percent')[i]), self.percent[i]))
            out('  <bank type="%s">%d</bank>\n' % 
                (S(F('points')[i]), self.bank[i]))
        for b, v in self.budgets.iteritems():
            out('  <budget type="%s">%d</budget>' % (S(b), v))
        out('  <assets>\n')
        for a in self.assets.itervalues():
            a.write(file, pov)
        out('  </assets>\n')
        out('  <fleets>\n')
        for f in self.fleets.itervalues():
            f.write(file, pov)
        out('  </fleets>\n')
        out('  <technos>\n')
        for t in self.technos.itervalues():
            t.write(file)
        out('  </technos>\n')
        out('  <ftechnos>\n')
        for t in self.cache_ftech.itervalues():
            t.write(file)
        out('  </ftechnos>\n')
        out('  <schemes>\n')
        for s in self.schemes.itervalues():
            s.write(file)
        out('  </schemes>\n')
        out('  <msgs>\n')
        for m in self.msg:
            out('  <msg>%s</msg>\n' % m)
        out('  </msgs>\n')
        out('</player>\n')


class matrix:
    def __init__(self):
        self.id = next_id()
        self.tour = 0
        self.neutral = player('Neutral', 'Galaxy', I('mutant'), 0)
        self.players = dict()
        self.players[self.neutral.id] = self.neutral
        self.technos, self.def_ships = static_create(self.neutral)
        self.tmpscheme = dict()

        self.schemes = dict() # hold all schemes, def_ships contain standart ships
        for sc in self.def_ships.itervalues():
            self.schemes[sc.id] = sc

        self.systems_p = dict()        # mapping by position
        self.systems_i = dict()        # mapping by id
        count = 0
        while count < conf.nsyst:
            position = (randint(-conf.bound, conf.bound), 
                        randint(-conf.bound, conf.bound))
            if position in self.systems_p:
                continue
            
            syst = system(position, self.neutral)
            self.systems_p[position] = syst
            self.systems_i[syst.id] = syst
            count += 1

    def __setstate__(self, state):
        self.__dict__ = state
        self.tmpscheme = dict()

def static_create(neutral):
    laser = weapon('laser', 1, 1, 0, 10, 5)
    laser.set_accuracy((27, 31, 20, 10, 1, 0, 0, 0, 0, 0))
    
    plasma = weapon('plasma', 2, 1, 1, 5, 8)
    laser.set_accuracy((1, 5, 13, 20, 30, 20, 10, 0, 0, 0))
    
    uo1 = techno('Usine d\'optimisation I')
    uo1.base_caracs(I('building'), 10, 0, 5, 3, 5)
    uo1.add_caracs(I('YOT'), 2)

    radar1 = techno('Radar I')
    radar1.base_caracs(I('building'), 100, 500, 10, 50, 10)
    radar1.add_caracs(I('syst_rad'), 1)
    radar1.add_caracs(I('fleet_rad'), 1)
    radar1.add_parents(uo1)
    
    sili = techno('Unité de production PCB')
    sili.base_caracs(I('building'), 10, 0, 10, 10, 5)
    sili.add_caracs(I('prod_merch'), (I('phys3'), 10))

    min1 = techno('Mine I')
    min1.base_caracs(I('building'), 10, 0, 1, 5, 1)
    min1.add_caracs(I('extract'), 1)
    min1.add_caracs(I('cost_merch'), (I('chim1'), 1))
    
    min2 = techno('Mine II')
    min2.base_caracs(I('building'), 15, 250, 1, 5, 2)
    min2.add_caracs(I('extract'), 2)
    min2.add_parents(min1)
    
    min3 = techno('Mine III')
    min3.base_caracs(I('building'), 20, 1000, 1, 5, 3)
    min3.add_caracs(I('extract'), 3)
    min3.add_parents(min2)
    
    rea1 = techno('Réacteur I')
    rea1.base_caracs(I('component'), 1, 0, 1, 0, 1)
    rea1.add_caracs(I('propeller'), 1)
    
    rea2 = techno('Réacteur II')
    rea2.base_caracs(I('component'), 2, 450, 2, 0, 2)
    rea2.add_caracs(I('propeller'), 3)
    rea2.add_caracs(I('cost_merch'), (I('chim1'), 1))
    rea2.add_parents(rea1)

    las1 = techno('Laser I')
    las1.base_caracs(I('component'), 3, 200, 1, 0, 3)
    las1.add_caracs(I('military'), 1)
    las1.add_caracs(I('weapon'), (laser, 1, 1)) # weapon, number, coef
    las1.add_parents(rea1)

    pla1 = techno('Plasma I')
    pla1.base_caracs(I('component'), 5, 200, 1, 0, 4)
    pla1.add_caracs(I('military'), 1)
    pla1.add_caracs(I('weapon'), (plasma, 1, 1)) # weapon, number, coef
    pla1.add_parents(las1)
    pla1.add_parents(rea2)

    colo = techno('Module de Colonisation')
    colo.base_caracs(I('component'), 5, 1000, 1, 0, 10)
    colo.add_caracs(I('colo'), 1)
    colo.add_parents(rea2)
    
    cargo1 = techno('Cargo I')
    cargo1.base_caracs(I('component'), 2, 250, 1, 0, 2)
    cargo1.add_caracs(I('cargo'), 10)
    cargo1.add_parents(rea1)
    
    scan1 = techno('Scanner I')
    scan1.base_caracs(I('component'), 15, 300, 1, 0, 5)
    scan1.add_caracs(I('syst_rad'), 1)
    scan1.add_parents(rea1)
    
    hscan1 = techno('Hyper-Scanner I')
    hscan1.base_caracs(I('component'), 15, 400, 1, 0, 7)
    hscan1.add_caracs(I('fleet_rad'), 1)
    hscan1.add_parents(scan1)
    hscan1.add_parents(rea2)

    mdc1 = techno('Module de Construction I')
    mdc1.base_caracs(I('component'), 50, 2000, 1, 0, 25)
    mdc1.add_caracs(I('SCM'), 1)
    mdc1.add_parents(colo)

    mdc4 = techno('Module de Construction IV')
    mdc4.base_caracs(I('component'), 150, 10000, 15, 0, 75)
    mdc4.add_caracs(I('SCM'), 16)
    mdc4.add_parents(mdc1)

    cha1 = scheme(neutral, 'Chasseur Standart', 'Galaxia', I('public'), 0)
    cha1.add_compo(rea1, 1)
    cha1.add_compo(las1, 1)
    cha1.finalize()

    chal = scheme(neutral, 'Chasseur Lourd', 'Galaxia', I('public'), 0)
    chal.add_compo(rea2, 1)
    chal.add_compo(las1, 2)
    chal.add_compo(pla1, 2)
    chal.finalize()
    
    sco = scheme(neutral, 'Colonisateur Standart', 'Galaxia', I('public'), 0)
    sco.add_compo(rea1, 1)
    sco.add_compo(colo, 1)
    sco.finalize()
    
    sonde = scheme(neutral, 'Sonde Standart', 'Galaxia', I('public'), 0)
    sonde.add_compo(rea1, 1)
    sonde.add_compo(scan1, 1)
    sonde.add_compo(hscan1, 1)
    sonde.finalize()

    vsous = scheme(neutral, 'Vaisseau Usine', 'Galaxia', I('public'), 0)
    vsous.add_compo(rea1, 1)
    vsous.add_compo(mdc1, 1)
    vsous.finalize()

    smdc = scheme(neutral, 'mdcIV', 'Galaxia', I('public'), 0)
    smdc.add_compo(rea1, 1)
    smdc.add_compo(mdc4, 1)
    smdc.finalize()

    croiz = scheme(neutral, 'Croiseur', 'Galaxia', I('public'), 0)
    croiz.add_compo(rea2, 1)
    croiz.add_compo(las1, 7)
    croiz.add_compo(pla1, 8)
    croiz.finalize()

    technos = dict()
    def_ships = dict()
    for x in locals().itervalues():
        if isinstance(x, techno):
            technos[x.id] = x
        if isinstance(x, scheme):
            def_ships[x.name] = x
    return technos, def_ships