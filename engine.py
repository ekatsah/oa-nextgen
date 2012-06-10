# -*- coding: UTF-8 -*-
# ENGINE.PY

# Copyright 2011, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from pickle import dump, load
from random import seed
from sys import stdin,exc_info
from traceback import print_tb
from os import system
from math import floor

from util import zone, in_zone, I, D, F, S
from matrix import matrix, player
from army import scheme, fleet
from galaxy import build


def create_world():
    global world
    world = matrix()
    
def write_rapports():
    for p in world.players.itervalues():
        fd = open('runz_' + str(world.tour) + '_' + str(p.id) + '.xml', 'w')
        p.write(fd, world.tour)
        fd.close()

def load_world(tour):
    global world
    data = open('runz_world_' + str(tour) + '.pkl', 'r')
    world = load(data)
    data.close()
    world.tour += 1

def store_world():
    data = open('runz_world_' + str(world.tour) + '.pkl', 'wb')
    dump(world, data, -1)
    data.close()

def inscription(name, domain, race):
    p = player(name, domain, race, world.tour)
    print "inscript id = " + str(p.id)
    z = zone(race)
    for a in world.neutral.assets.itervalues():
        if in_zone(a.referer.position, z):
            p.add_asset(a)
            world.neutral.del_asset(a.id)
            break
    else:
        raise Exception('Init system not found')
    
    # ajout des technos publiques
    for t in world.technos.itervalues():
        if I('public') in t.caracs:
            p.add_techno(t)
    p.compute_ftech(world)

    # ajout des plans publiques
    for v in world.schemes.itervalues():
        if v.domain == I('public'):
            p.add_scheme(v)

    #creation des flottes
    fl = fleet(p, 'Flotte de départ', a.referer.position)
    fl.add_ships(world.def_ships['Chasseur Standart'], race, 10, 0)
    fl.add_ships(world.def_ships['Chasseur Lourd'], race, 5, 0)
    fl.add_ships(world.def_ships['Colonisateur Standart'], race, 15, 0)
    fl.add_ships(world.def_ships['Sonde Standart'], race, 2, 0)
    fl.add_ships(world.def_ships['Croiseur'], race, 1, 0)
    fl.add_ships(world.def_ships['Vaisseau Usine'], race, 5, 0)
    fl.add_ships(world.def_ships['mdcIV'], race, 5, 0)
    p.add_fleet(fl)
    
    world.players[p.id]= p

def destroy_p(player, asset, pla, building, num):
    if building not in pla.constructions:
        player.add_msg('Impossible de détruire %d %s sur la planète %d de %s%s' % 
                       (num, building.name, pla.position + 1, asset.name, 
                        ': pas de construction de ce type'))
        return False

    num = pla.destroy(building, num)
    asset.add_ore(building.caracs[I('cost_ore')] * num / 2)
    player.set_budget(I('budget_destr'), building.caracs[I('cost_prod')]*num/3)
    player.add_msg('Destruction de %d %s sur la planète %d de %s' %
                   (num, building.name, pla.position + 1, asset.name))
    return True

def destroy(player, asset, building, num):
    already = 0
    for p in asset.planets:
        if building in p.constructions:
            already += p.destroy(building, num - already)
        assert(already > num)
        if already == num:
            break

    if already == 0:
        player.add_msg('Impossible de détruire %d %s sur %s: pas de const%s' % 
                       (num, building.name, asset.name, 'ruction de ce type'))
        return False
    else:
        asset.add_ore(building.caracs[I('cost_ore')] * already / 2)
        player.set_budget(I('budget_destr'), 
                          building.caracs[I('cost_prod')] * already / 3)
        player.add_msg('Destruction de %d %s sur %s' % (num, building.name, 
                                                        asset.name))
        return True

def construction_B(player, asset, building, count):
    assert(I('building') in building.caracs)
    asset.add_construction(build(building, count, None))
    player.add_msg('Lancement de %d %s sur %s.' % (count, buidling.name, 
                                                   asset.name))
    return True

def construction_S(player, asset, scheme, count):
    asset.add_construction(build(scheme, count, None))
    player.add_msg('Lancement de %d %s sur %s.' % (count, scheme.name, 
                                                   asset.name))
    return True

def construction_Bp(player, asset, building, count, planet):
    assert(I('building') in building.caracs)
    asset.add_construction(build(building, count, planet))
    player.add_msg('Lancement de %d %s sur %s %d.' % 
                   (count, building.name, asset.name, planet.position))
    return True

def construction_Sf(player, asset, scheme, count, fleet):
    asset.add_construction(build(scheme, count, fleet.id))
    player.add_msg('Lancement de %d %s pour la flotte %s sur %s.' % 
                   (count, scheme.name, fleet.name, asset.name))
    return True

def change_policy(player, asset, policy):
    asset.policy = policy
    player.add_msg('Changement de politique sur %s: %s.' %
                   (asset.name, S(policy)))
    return True

def change_taxe_p(player, asset, planet, taxe):
    planet.taxe = taxe
    player.add_msg('Changement de taxation sur la planète %d de %s: %s.' %
                   (planet.position + 1, asset.name, S(taxe)))
    return True

def change_taxe(player, asset, taxe):
    for p in asset.planets.itervalues():
        p.taxe = taxe
    player.add_msg('Changement de taxation sur %s: %s.' % (asset.name, S(taxe)))
    return True

def terraformer_p(player, asset, planet):
    try:
        planet.terraform()
    except Exception as e:
        player.add_msg('Impossible de terraformer la planète %d sur %s: %s.' %
                       (planet.position + 1, asset.name, str(e)))
        return False
    player.add_msg('Terraformation de la planète %d sur %s.' %
                   (planet.position + 1, asset.name))
    return True

def terraformer(player, asset):
    error, success = False, False
    for p in asset.planets:
        try:
            p.terraform()
            success = True
        except Exception as e:
            player.add_msg('Impossible de terraformer la planète %d sur %s: %s.'%
                           (p.position + 1, asset.name, str(e)))
            error = False
    if success and error:
        player.add_msg('Terraformation partielle de %s.' % asset.name)
    elif success and not error:
        player.add_msg('Terraformation de %s.' % asset.name)
    return not error

def set_priority(player, tech, spe, cesp):
    if player.set_priority(tech, spe, cesp):
        player.add_msg('Priorité de budget réglée')
        return True
    else:
        player.add_msg('Impossible de regler votre budget, il dépasse la limite')
        return False

def affect_tech(player, tech, point):
    if point < 0:
        player.add_msg("Impossible d'allouer moins de 0 points sur %s" % tech.name)
        return False
    if tech in player.research:
        player.research[tech] += point
    else:
        player.research[tech] = point

    # FIXME tech should be 1.
    player.bank[2] -= point
    player.add_msg("Vous avez alloué %d point sur %s" % (point, tech.name))

    return True

def colonize(player, fleet, race, asset, pla):
    if race in pla.pops:
        player.add_msg('La colonisation de la planete a échoué : pop dja la')
        return false
    if not pla.colonizable(race):
        player.add_msg('La colonisation de la planete a échoué : incolonizable')
        return false
    found = False
    for v, r in fleet.compos:
        if r != race or I('colo') not in v.caracs:
            continue
        fleet.remove_ships((v, r), 1)
        found = True
        break
    if found:
        pla.colonize(race)
        player.add_msg('La colonisation de la planete a réussie')
        return True
    else:
        player.add_msg('La colonisation de la planete a échoué: Pas de colo présent')
        return False

def decolonize(player, race, asset, pla):
    if race not in pla.pops:
        player.add_msg('La décolonisation de la planete a échoué : race absente')
        return false
    pla.decolonize(race)
    player.add_msg('La décolonisation de la planete a réussie')
    return True

def cargo_load(player, fleet, asset, res, count):
    code = resolv_ressource(res)
    
    pass

def cargo_load(player, fleet, asset, planet, res, count):
    pass

def move(player, fleet, x, y, guideline, target_hum, target_pla):
    fleet.move = (x, y)
    fleet.caracs[I('behaviour')] = guideline
    if guideline == I('pla_conquest'):
        fleet.caracs[I('target')] = target_pla
    elif guideline == I('player_attack'):
        fleet.caracs[I('target')] = target_hum
    else:
        fleet.caracs[I('target')] = None

    player.add_msg('Votre flotte %s a pour nouvelle destination (%d, %d) en %s' %
                   (fleet.name, x, y, S(guideline)))
    return True

def trail(player, fleet, target_hum, target_fleet):
    pass

def moving():
    for player in world.players.itervalues():
        for fl in player.fleets.itervalues():
            if fl.move:
                dx, dy = fl.move[0] - fl.position[0], fl.move[1] - fl.position[1]
                if dx == 0 and dy == 0:
                    fl.move = None
                    continue
                dx = min(dx, fl.caracs[I('velocity')])
                dy = min(dy, fl.caracs[I('velocity')])
                fl.position = (fl.position[0] + dx, fl.position[1] + dy)
    return True

def divide(player, fl, name, guideline, target_hum, target_pla, fid):
    if guideline == I('pla_conquest'):
        nfleet = fleet(player, name, fl.position, guideline, target_pla)
    elif guideline == I('player_attack'):
        nfleet = fleet(player, name, fl.position, guideline, target_hum)
    else:
        nfleet = fleet(player, name, fl.position, guideline)

    if fid in player.tmpfleets:
        raise Exception("duplicate FID")
    nfleet.mother = fl
    player.add_tmpfleet(fid, nfleet)
    player.add_msg("Division de la flotte %s, formation de %s" %
                   (fl.name, nfleet.name))
    return True

def add_ships(player, fl, ship, num, race):
    try:
        _, dom = fl.mother.remove_ships((ship, race), num)
        fl.add_ships(ship, race, num, dom)
    except:
        player.add_msg("Impossible de transferer %d %s de la flotte %s vers %s" %
                       num, ship.name, fl.mother.name, fl.name)
        return False
    return True

def absorb(player, fld_exist, fld_tmp, fls_exist, fls_tmp):
    def fusion(fl1, fl2):
        for sh_ra, nu_do in fl2.compos.iteritems():
            fl1.add_ships(sh_ra[0], sh_ra[1], nu_do[0], nu_do[1])

    fldst, flsrc = fld_exist, fls_exist
    if flsrc is None:
        flsrc = fls_tmp
    if fldst is None:
        fldst = fld_tmp
    if flsrc is None or fldst is None:
        raise Exception("Impossible de réalisation l'absorbtion relative à %s " %
                        ("[%s %s %s %s]" % (str(fld_exist), str(fld_tmp),
                                            str(fls_exist), str(fls_tmp))))

    fusion(fldst, flsrc)
    player.remove_fleet(flsrc)
    player.add_msg("Fusion entre %s et %s réussie" %(fldst.name, flsrc.name))
    return True

def check_fleets():
    for player in world.players.itervalues():
        fleets = player.check_fleets()
        for _, fl in fleets:
            player.add_msg("Impossible de garder le controle de la flotte %s" %
                           fl.name)
    return True

def construct_fleet(player, fleet, ship):
    if ship.get_carac(I('colo')) > 0 or ship.get_carac(I('SCM')) > 0:
        player.add_msg("Impossible de construire des %s depuis %s: %s" % 
                       (ship.name, fleet.name, "vaisseau interdit"))
        return False

    fleet.caracs[I('build_order')] = ship
    player.add_msg("La flotte %s a maintenant un ordre de construction de %s" %
                   (fleet.name, ship.name))
    return True

def scheme_create(player, name, brand, domain, alliance, cut, sid):
    if sid in player.tmpschemes:
        raise Exception("Duplicate SID")

    if cut < 0 or cut > 100:
        player.add_msg("Impossible de creer le plan %s, les royaltises %s" %
                       (name, "sont hors limites"))
        return False

    sch = scheme(player, name, brand, domain, cut)
    player.tmpschemes[sid] = sch
    world.tmpscheme[(player.id, sid)] = sch

def scheme_add(player, scheme, compo, num):
    try:
        scheme.add_compo(compo, num)
        return True
    except:
        player.add_msg("Impossible d'ajouter %d %s sur le plan %s" % 
                       (num, compo.name, scheme.name))
        return False
    
def scheme_finalize():
    for sch in world.tmpscheme.itervalues():
        if len(sch.compos) == 0:
            sch.owner.add_msg("Impossible de créer le plan %s: il est vide" % 
                              sch.name)
            continue

        if sch.owner.state[I('lim_scheme')] >= sch.owner.limits[I('lim_scheme')]:
            sch.owner.add_msg("Impossible de créer le plan %s: plus de place dispo" % 
                              sch.name)
            continue
        
        sch.finalize()

        if sch.caracs[I('cost_prod')] * 10 > sch.owner.bank[0]:
            sch.owner.add_msg("Impossible de créer le plan %s: %s" % 
                              (sch.name, "vous n'etes pas assez riche"))
            continue
        
        sch.owner.set_budget(I('budget_sch'), sch.caracs[I('cost_prod')] * 10)
        sch.owner.state[I('lim_scheme')] += 1
        sch.owner.add_scheme(sch)
        sch.owner.add_msg("Vous venez de creer le vaisseau %s" % sch.name)
        world.schemes[sch.id] = sch

        if sch.domain == I('public'):
            for p in world.players.itervalues():
                p.add_scheme(sch)

    return True

def scheme_mask(player, scheme):
    if scheme.owner != player:
        del player.schemes[scheme.id]
        player.add_msg("Vous venez de masquer le vaisseau %s" % scheme.name)
        return True
    else:
        player.add_msg("Vous ne pouvez pas masquer %s : vous êtes son créateur" %
                        scheme.name)
        return False

def scheme_invalid(player, scheme):
    if scheme.owner == player:
        scheme.valid = False
        player.state[I('lim_scheme')] -= 1
        assert(player.state[I('lim_scheme')] >= 0)
        player.add_msg("Vous venez d'invalider le vaisseau %s", scheme.name)
        return True
    else:
        player.add_msg("Vous ne pouvez pas invalider %s : vous n'êtes pas son" %
                       (scheme.name, "créateur"))
        return False

def end_of_tour():
    for p in world.players.itervalues():
        for a in p.assets.itervalues():
            a.resolv_constructions()
            a.resolv_croissance()
            a.resolv_stabmoney()

        m = p.get_budget(I('budget_tax'))
        ptech = floor(m * p.percent[0] / 100)
        p.set_budget(I('budget_research'), ptech)
        # FIXME probably ugly bug. (should be 1 not 2)
        p.bank[2] += ptech

        # resol techno
        for tech, pt in p.research.iteritems():
            if pt >= tech.get_carac(I('cost_research')):
                p.add_techno(tech, world)
                p.add_msg("Vous venez de découvrir %s" % tech.name)

        for f in p.fleets.itervalues():
            f.build()

    return True

#==( Core engine )==============================================================
            
functions = {"create_world": (),
             "write_rapports": (),
             "load_world": ('int',),
             "store_world": (),
             "inscription": ('copy', 'copy', 's2i races'),
             "destroy_p": ('dict world players', 'dict 1 assets', 
                           'dict 2 planets', 'dict 1 technos', 'int'),
             "destroy": ('dict world players', 'dict 1 assets', 
                         'dict 1 technos', 'int'),
             "construction_B": ('dict world players', 'dict 1 assets',
                              'dict 1 technos', 'int'),
             "construction_S": ('dict world players', 'dict 1 assets',
                              'dict 1 schemes', 'int'),
             "construction_Bp": ('dict world players', 'dict 1 assets',
                                 'dict 1 technos', 'int', 'dict 2 planets'),
             "construction_Sf": ('dict world players', 'dict 1 assets',
                                'dict 1 schemes', 'int', 'dict 1 fleets'),
             "change_policy": ('dict world players', 'dict 1 assets',
                               's2i policy'),
             "change_taxe_p": ('dict world players', 'dict 1 assets',
                               'dict 2 planets', 's2i taxe_level'),
             "change_taxe": ('dict world players', 'dict 1 assets', 
                             's2i taxe_level'),
             "terraformer_p": ('dict world players', 'dict 1 assets',
                               'dict 2 planets'),
             "set_priority": ('dict world players', 'int', 'int', 'int'),
             "affect_tech": ('dict world players', 'dict 1 cache_ftech', 'int'),
             "terraformer":('dict world players', 'dict 1 assets'),
             "colonize": ('dict world players', 'dict 1 fleets', 's2i races',
                          'dict 1 assets', 'dict 4 planets'),
             "decolonize": ('dict world players', 's2i races',
                            'dict 1 assets', 'dict 3 planets'),
             "construct_fleet": ('dict world players', 'dict 1 fleets',
                                 'dict 1 schemes'),
             "cargo_load": ('dict world players', 'dict 1 fleets', 
                            'dict 1 assets', 'copy', 'int'),
             "cargo_load_p": ('dict world players', 'dict 1 fleets', 
                              'dict 1 assets', 'dict 3 planets', 'copy', 'int'),
             "move": ('dict world players', 'dict 1 fleets', 'int', 'int',
                      's2i fleet_behaviour', 'dictn world players', 'int'),
             "moving": (),
             "divide": ('dict world players', 'dict 1 fleets', 'copy',
                        's2i fleet_behaviour', 'dictn world players', 'int', 
                        'int'),
             "add_ships": ('dict world players', 'dict 1 tmpfleets',
                           'dict world schemes', 'int', 's2i races'),
             "absorb": ('dict world players', 'dictn 1 fleets', 
                        'dictn 1 tmpfleets', 'dictn 1 fleet', 
                        'dictn 1 tmpfleets'),
             "check_fleets": (),
             "scheme_create": ('dict world players', 'copy', 'copy', 
                               's2i plan_domain', 'dictn 1 alliances', 'int', 
                               'int'),
             "scheme_add": ('dict world players', 'dict 1 tmpschemes',
                            'dict 1 technos', 'int'),
             "scheme_finalize": (),
             "scheme_mask": ('dict world players', 'dict 1 schemes'),
             "scheme_invalid": ('dict world players', 'dict 1 schemes'),
             "end_of_tour" : ()}

def resolv_dict(input, args, elem, field):
    input = int(input)
    src = world if elem == 'world' else args[int(elem)-1]
    if input in getattr(src, field):
        return getattr(src, field)[input]
    else:
        raise Exception('function dict fail on args "' + str(input) + '"')

def resolv_dictn(input, args, elem, field):
    try:
        return resolv_dict(input, args, elem, field)
    except:
        return None

def resolv_s2i(input, family):
    val = D(input)
    if val in F(family):
        return val
    else:
        raise Exception('function s2i fail on args "' + input + '"')
    
def resolv_input(line):
    input = line.split(':')
    if input[0] not in functions:
        raise Exception('function name not found')

    args = []
    current = 1
    for params in functions[input[0]]:
        param = params.split(' ')
        if param[0] == 'copy':
            args.append(input[current])
        elif param[0] == 'int':
            args.append(int(input[current]))
        elif param[0] == 's2i':
            args.append(resolv_s2i(input[current], param[1]))
        elif param[0] == 'dict':
            args.append(resolv_dict(input[current], args, param[1], param[2]))
        elif param[0] == 'dictn':
            args.append(resolv_dictn(input[current], args, param[1], param[2]))
        else:
            raise Exception('function param not found on args#' + str(current))
        current += 1

    globals()[input[0]](*args) # callin function wouhooo hoohoo

def parse_input(src):
    seed(1337)
    for line in src:
        line = line.rstrip('\n')
        try:
            resolv_input(line)
        except Exception as e:
            tb = exc_info()[2]
            print 'shit happened on "' + line + '"'
            print str(e)
            print str(print_tb(tb))
            raise Exception("exit")

if __name__ == '__main__':
    system("echo -n 'Size: ';cat *py rapport.* | wc -l")
    system("rm runz_* &> /dev/null")

    ordres = [['create_world', 'inscription:Testor1:DN:Fungus:mouh',
               'end_of_tour', 'write_rapports', 'store_world'],
              ['load_world:0',
               'construction_S:1198:771:21:2',
               'construction_S:1198:771:21:2:1199',
               'check_fleets',
               'scheme_create:1198:VsoTest:X:Privé:0:0:1',
               'scheme_add:1198:1:11:2',
               'scheme_finalize',
               'scheme_mask:1198:24',
               'end_of_tour', 'write_rapports', 'store_world'],
              ['load_world:1', 'affect_tech:1198:13:250', 'affect_tech:1198:12:500',
               'check_fleets',
               'end_of_tour', 'write_rapports', 'store_world']]

    for tour in ordres:
        print "NEW TOUR"
        try:
            parse_input(tour)
        except:
            break
