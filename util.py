# -*- coding: UTF-8 -*-
# UTIL.PY

# Copyright 2011, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from random import choice, randint
from string import capitalize
from sys import maxint

next_id_ = 0

def next_id():
    global next_id_
    next_id_ += 1
    return next_id_

def random_string():
    vowels = 'aaeeiioouuy'
    cons = 'bbbccdddfffghjjkklllmmnnppqrrssttvvwxz'
    rstring = ''
    for _ in xrange(randint(conf.rname[0]/2, conf.rname[1]/2)):
        rstring += choice(cons) + choice(vowels)
    return capitalize(rstring)

def get_carac(obj, carac):
    c = 0
    if carac in obj.caracs:
        c = obj.caracs[carac]
    if carac == I('behaviour') and c == 0:
        c = I('neutral')
    return c

def dist(pos1, pos2):
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))

def zone(race):
    if race == I('chrysoid'):
        return (-100, 100, -30, 0)
    elif race == I('largyn'):
        return (-30, 100, 30, 0)
    elif race == I('human'):
        return (30, 100, 100, 0)
    elif race == I('sparow'):
        return (-100, 0, -30, -100)
    elif race == I('fungus'):
        return (-30, 0, 30, -100)
    else:
        return (30, 0, 100, -100)

def in_zone(p, z): # p = (x, y), z (x1, y1, x2, y2)
    return (p[0] >= z[0] and p[0] <= z[2] and p[1] <= z[1] and p[1] >= z[3])

def dict_max(dict, carac):
    max = 0
    for t in dict:
        if carac in t.caracs and max < t.caracs[carac]:
                max = t.caracs[carac]
    return max

def dict_maxt(dict, carac):
    max = 0
    for t in dict:
        if carac in t[0].caracs and max < t[0].caracs[carac]:
                max = t[0].caracs[carac]
    return max

def dict_mint(dict, carac):
    min = maxint
    for t in dict:
        if carac in t[0].caracs and min > t[0].caracs[carac]:
                min = t[0].caracs[carac]
    return min

def dict_sum(dict, carac):
    sum = 0
    for t in dict:
        if carac in t.caracs:
            sum += t.caracs[carac] * dict[t]
    return sum

def dict_sumt(dict, carac):
    sum = 0
    for t in dict:
        if carac in t[0].caracs:
            sum += t[0].caracs[carac] * dict[t][0]
    return sum

tables = {'races' : (('mutant', 'Mutant'), # races, missing black wougzy?
                     ('chrysoid', 'Chrysoïde'), 
                     ('largyn', 'Largyn'), 
                     ('human', 'Humain'),
                     ('sparow', 'Sparow'),
                     ('fungus', 'Fungus'), 
                     ('wougzy', 'Wougzy'),
                     ('zorglub', 'Zorglub')),
          'techno_type' : (('building', 'Batiment'),
                           ('component', 'Composant'),
                           ('mastery', 'Maitrise')),
          'techno_carac' : (('prod_merch', 'Production marchandises'),
                            ('weapon', 'Arme'),
                            ('extract', 'Capacitée d\'extraction'),
                            ('advance_ex', 'Capacitée d\'extraction avancée'),
                            ('propeller', 'Propulsion'),
                            ('syst_rad', 'Détection Système'),
                            ('fleet_rad', 'Détection Flotte'),
                            ('cargo', 'Capacité Cargo'),
                            ('YOT', 'Optimisation des Chantiers'), # yard optimisation technic
                            ('SCM', 'Construction Spaciale'), # space construction module
                            ('colo', 'Colonisation Planétaire'),
                            ('shield', 'Bouclier'),
                            
                            ('type', 'Type'),       # caracs de base
                            ('cost_prod', 'Cout centaure'),
                            ('cost_research', 'Cout de recherche'),
                            ('cost_ore', 'Cout minerai'),
                            ('cost_merch', 'Cout marchandise'),
                            ('cases', 'Nombre de cases'), # pdc = cases/2
                            ('structural', 'Point de structure'),
                            ('public', 'Public'),
                            ('military', 'Militaire')),
                            
          'goods' : (('chim1', 'Silicarbonate'),
                     ('chim2', 'Techno-Fluides'),
                     ('chim3', 'Fibroplasts'),
                     ('phys1', 'ServoMoteurs'),
                     ('phys2', 'Régulateurs'),
                     ('phys3', 'Circuits'),
                     ('noble1', 'Oxole'),
                     ('noble2', 'Tixium'),
                     ('noble3', 'Lixiam')),
          'res_type' : (('population', 'Population'),
                        ('ore', 'Minerai'),
                        ('goods', 'Marchandise'),
                        ('building', None)),
          'policy' : (('tax', 'Impot'), # politiques
                      ('construct', 'Construction'),
                      ('expand', 'Expansion'),
                      ('peace', 'Pacification'),
                      ('defense', 'Défense'),
                      ('entertain', 'Loisir'),
                      ('integrism', 'Intégrisme'),
                      ('slavery', 'Esclavagisme')),
          'genders' : (('unknow', 'Inconnu'),
                       ('male', 'Male'),
                       ('female', 'Femelle')),
          'plan_carac' : (('civilian', 'Civile'),
                          ('size', 'Taille'),
                          ('poc', 'PdC'), # point of construction
                          ('velocity', 'Vitesse'),
                          ('cost_prod', None),
                          ('cost_ore', None),
                          ('cost_merch', None),
                          ('military', None),
                          ('cargo', None),
                          ('syst_rad', None),
                          ('fleet_rad', None),
                          ('SCM', None),
                          ('colo', None),
                          ('SA', 'AS'),
                          ('PA', 'AP')),
          'plan_domain' : (('public', None),
                           ('private', 'Privé'),
                           ('allies', 'Alliance')),
          'fleet_carac' : (('civilian', None),
                           ('military', None),
                           ('cargo', None),
                           ('behaviour', 'Comportement'),
                           ('target', 'Cible particulière'),
                           ('SA', None),
                           ('PA', None),
                           ('velocity', None),
                           ('syst_rad', None),
                           ('fleet_rad', None),
                           ('build_order', 'Directive de construction'),
                           ('size', None)),
          'fleet_behaviour' : (('neutral', 'Attitude Neutre'),
                              ('syst_conquest', 'Conquete système'),
                              ('pla_conquest', 'Conquete de la planète'),
                              ('prev_attack', 'Attaque préventive'),
                              ('player_attack', 'Attaque des flottes du commandant'),
                              ('attack', 'Attaque toute flotte'),
                              ('pillage', 'Pillage')),
          'lieutenant' : (('amiral', 'Amiral'), ('gouvernor', 'Gouverneur')),
          'military_carac' : (('pugnacity', 'Combativité'),
                              ('motivation', 'Motivation'),
                              ('mastery', None),
                              ('rigor', 'Rigueur'),
                              ('initiative', 'Initiative')),
          'manage_carac' : (('managing', 'Gestion'),
                            ('monopoly', 'Monopolisme'),
                            ('cupidity', 'Cupidité'),
                            ('velocity', None),
                            ('fraud', 'Fraude')),
          'atmosphere' : (('Aneutral', 'neutre'),
                          ('acid', 'acide'),
                          ('sulfur', 'sulfureuse'),
                          ('humid', 'humide'),
                          ('methan', 'methanique')),
          'limits' : (('lim_flciv', 'Limitation de flotte civile'),
                      ('lim_flmil', 'Limitation de flotte militaire'),
                      ('lim_scheme', 'Limitation du nombre de plan'),
                      ('lim_terraform', 'Limitation de terraformation'),
                      ('lim_budget', 'Limitation au budget max')),
          'fleet_size' : (('size1', 'Ridicule'),
                          ('size2', 'Anodine'),
                          ('size3', 'Petite'),
                          ('size4', 'Moyenne'),
                          ('size5', 'Grande'),
                          ('size6', 'Très grande'),
                          ('size7', 'Titanesque'),
                          ('size8', 'Cyclopéenne'),
                          ('size9', 'Inimaginable'),
                          ('size10', 'Divine')),
          'percent' : (('tech_percent', 'Priorité Technologique'),
                       ('spe_percent', 'Priorité Services Spéciaux'),
                       ('cesp_percent', 'Priorité Contre Espionnage')),
          'points' : (('centaure', 'centaures'),
                      ('tech_point', 'points technologiques'),
                      ('spe_point', 'points spéciaux')),
          'budgets' : (('reserv', 'Centaure du tour précédent'),
                      ('budget_const', 'Constructions'),
                      ('budget_terra', 'Terraformation'),
                      ('budget_destr', 'Destruction'),
                      ('budget_tax', 'Impot systeme'),
                      ('budget_research', 'Recherche Technologique'),
                      ('budget_cesp', 'Depense contre esp'),
                      ('budget_spe', 'Depense en opération spéciale'),
                      ('budget_sch', 'Depense de création de plan')),
          'taxe_level' : (('tax_null', 'Nulle'),
                          ('tax_light', 'Légère'),
                          ('tax_norm', 'Normale'),
                          ('tax_med', 'Medium'),
                          ('tax_heavy', 'Lourde'),
                          ('tax_total', 'Totale'))
          }

# Need : symbol -> int, pour le stockage              func I
#        int -> string, pour l'output dans rapport    func S
#        string -> int, pour l'input                  func D (decode)

lookup_i2s = dict()
lookup_S2i = dict()
lookup_s2i = dict()
lookup_f2s = dict()
        
def init():
    global tables, lookup_i2s, lookup_S2i, lookup_f2s, lookup_S2s
    current = 1
    for family in sorted(tables):
        fl = list()
        for t in sorted(tables[family]):
            symbol = t[0]
            string = t[1]
            int = current
            
            if symbol in lookup_S2i:
                int = lookup_S2i[symbol]
            else:
                lookup_S2i[symbol] = int
                current += 1
            if string:
                assert(string not in lookup_s2i)
                assert(int not in lookup_i2s)
                lookup_s2i[string] = int
                lookup_i2s[int] = string
                
            fl.append(int)
        assert(family not in lookup_f2s)
        lookup_f2s[family] = fl

init()

def S(i): return lookup_i2s[i]
def I(symbol): return lookup_S2i[symbol]
def D(str): return lookup_s2i[str]
def F(symbol): return lookup_f2s[symbol]

class conf:
    bound = 100         # taille galaxie (-bound, bound)
    rname = (4, 10)     # taille min, max des random name
    nsyst = 100         # nombre de syst dans la galaxie
    npla = (5, 15)      # nombre de pla par syst, min max
    limits = {I('lim_flciv'): 15,
              I('lim_flmil'): 15,
              I('lim_scheme'): 10,
              I('lim_terraform') : 10,
              I('lim_budget') : 100}
    stab_dist = [ 3, 2, 1, -1, -1, -1, -1, -2, -2, -4, -6, -8, -12 ]
    stab_tax = [ 6, 3, 0, -3, -7, -11 ]
    stab_nocap = -10 # malus stab sans capitale

    coef = {'fleet' : 1/10, # coef du calcul de puissance des flottes
            'terraform' : 10 # cout d'un etage de terraform
            }

def t2int(tax):
    assert(tax in F('taxe_level'))
    taxl =  {I('tax_null'): 0, I('tax_light'): 1, I('tax_norm'): 2, 
                I('tax_med'): 3, I('tax_heavy'): 4, I('tax_total'): 5}
    return taxl[tax]

