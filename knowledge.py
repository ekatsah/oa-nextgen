# -*- coding: UTF-8 -*-
# KNOWLEDGE.PY

# Copyright 2011, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from util import next_id, S, I, get_carac


class weapon:
    def __init__(self, name, ha, sa, pa, velocity, scope):
        self.id = next_id()
        self.name = name
        self.sa = sa
        self.ha = ha
        self.pa = pa
        self.velocity = velocity
        self.scope = scope
        self.accuracy = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        
    def set_accuracy(self, a):
        if len(a) == 10:
            self.accuracy = a
        else:
            print 'error' # assert, raise exec??
    
    def write(self, file, n, coef):
        out = file.writelines
        out('<weapon id="%d">\n' % self.id)
        out('  <attack ha="%d" sa="%d" pa="%d"/>\n' % 
            (self.sa * n, self.sa * n, self.pa * n))
        out('  <velocity>%d</velocity>\n' % (self.velocity + coef))
        out('  <scope>%d</scope>' % (self.scope + coef))
        for i in xrange(0, len(self.accuracy)):
            if self.accuracy[i] > 0:
                out('  <rate hull="%d">%d</rate>\n' % 
                    (i, self.accuracy[i] * (1.07 ** coef)))
        out('</weapon>\n')


class techno:
    get_carac = get_carac
    
    def __init__(self, name):
        self.id = next_id()
        self.name = name
        self.caracs = dict()
        self.parents = list()
        self.antagonists = list()

    def add_caracs(self, carac, value):     # FIXME check if already set?
        self.caracs[carac] = value

    def base_caracs(self, type, cost, search, bulk, struct, ore):
        self.add_caracs(I('type'), type)
        self.add_caracs(I('cost_prod'), cost)
        if search > 0:
            self.add_caracs(I('cost_research'), search)
        else:
            self.add_caracs(I('public'), 1)
        if type == I('building'):
            self.add_caracs(I('poc'), bulk)
        elif type == I('component'):
            self.add_caracs(I('cases'), bulk)
        if struct > 0:
            self.add_caracs(I('structural'), struct)
        self.add_caracs(I('cost_ore'), ore)

    def add_parents(self, tech):
        self.parents.append(tech)
        
    def write(self, file):
        out = file.writelines
        out('<techno id="%d">\n' % self.id)
        out('  <name>%s</name>\n' % self.name)
        for k, v in self.caracs.iteritems():
            if k == I('type'):
                out('  <carac name="%s">%s</carac>\n' % (S(k), S(v)))
            elif k == I('prod_merch') or k == I('cost_merch'):
                out('  <carac name="%s" merch="%s">%d</carac>\n' % 
                    (S(k), S(v[0]), v[1]))
            elif k == I('weapon'):
                v[0].write(file, v[1], v[2])
            else:
                out('  <carac name="%s">%d</carac>\n' % (S(k), v))
        for t in self.parents:
            out('  <parent>%d</parent>\n' % t.id)
        out ('</techno>\n')
