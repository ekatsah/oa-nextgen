# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models


class Feature(models.Model):
    code = models.CharField(max_length="40", unique=True)
    name = models.CharField(max_length="40")
    type = models.CharField(max_length="40")
    description = models.TextField(null=True)

    @staticmethod
    def generate():
        F = Feature.objects.create

        # -- res_type
        F(code='c_population', name='Population', type='res_type')
        F(code='c_ore', name='Minerai', type='res_type')
        F(code='c_goods', name='Marchandise', type='res_type')
        F(code='c_building', name='Building', type='res_type')

        # -- atmosphere
        F(code='aneutral', name='neutre', type='atmosphere')
        F(code='acid', name='acide', type='atmosphere')
        F(code='sulfur', name='sulfureuse', type='atmosphere')
        F(code='humid', name='humide', type='atmosphere')
        F(code='methan', name='methanique', type='atmosphere')

        # -- goods
        F(code='chim1', name='Silicarbonate', type='goods')
        F(code='chim2', name='Techno-Fluides', type='goods')
        F(code='chim3', name='Fibroplasts', type='goods')
        F(code='phys1', name='ServoMoteurs', type='goods')
        F(code='phys2', name='Régulateurs', type='goods')
        F(code='phys3', name='Circuits', type='goods')
        F(code='noble1', name='Oxole', type='goods')
        F(code='noble2', name='Tixium', type='goods')
        F(code='noble3', name='Lixiam', type='goods')

        # -- limits
        F(code='lim_flciv', name='Limitation de flotte civile', type='limits')
        F(code='lim_flmil', name='Limitation de flotte militaire', type='limits')
        F(code='lim_scheme', name='Limitation du nombre de plan', type='limits')
        F(code='lim_terraform', name='Limitation de terraformation', type='limits')
        F(code='lim_budget', name='Limitation au budget max', type='limits')

        # -- lieutenant
        F(code='amiral', name='Amiral', type='lieutenant')
        F(code='gouvernor', name='Gouverneur', type='lieutenant')

        # -- plan_carac
        F(code='s_civilian', name='Civile', type='plan_carac')
        F(code='s_size', name='Taille', type='plan_carac')
        F(code='s_poc', name='PdC', type='plan_carac')
        F(code='s_velocity', name='Vitesse', type='plan_carac')
        F(code='s_cost_prod', name='Prod Cost', type='plan_carac')
        F(code='s_cost_ore', name='Ore Cost', type='plan_carac')
        F(code='s_cost_merch', name='Merch Cost', type='plan_carac')
        F(code='s_military', name='Military', type='plan_carac')
        F(code='s_cargo', name='Cargo', type='plan_carac')
        F(code='s_syst_rad', name='System scanner', type='plan_carac')
        F(code='s_fleet_rad', name='Fleet scanner', type='plan_carac')
        F(code='s_SCM', name='SCM', type='plan_carac')
        F(code='s_colo', name='Colonizator', type='plan_carac')
        F(code='s_SA', name='AS', type='plan_carac')
        F(code='s_PA', name='AP', type='plan_carac')

        # -- percent
        F(code='tech_percent', name='Priorité Technologique', type='percent')
        F(code='spe_percent', name='Priorité Services Spéciaux', type='percent')
        F(code='cesp_percent', name='Priorité Contre Espionnage', type='percent')

        # -- manage_carac
        F(code='managing', name='Gestion', type='manage_carac')
        F(code='monopoly', name='Monopolisme', type='manage_carac')
        F(code='cupidity', name='Cupidité', type='manage_carac')
        F(code='fraud', name='Fraude', type='manage_carac')

        # -- military_carac
        F(code='pugnacity', name='Combativité', type='military_carac')
        F(code='motivation', name='Motivation', type='military_carac')
        F(code='m_mastery', name='Masterization', type='military_carac')
        F(code='rigor', name='Rigueur', type='military_carac')
        F(code='initiative', name='Initiative', type='military_carac')

        # -- policy
        F(code='tax', name='Impot', type='policy')
        F(code='construct', name='Construction', type='policy')
        F(code='expand', name='Expansion', type='policy')
        F(code='peace', name='Pacification', type='policy')
        F(code='defense', name='Défense', type='policy')
        F(code='entertain', name='Loisir', type='policy')
        F(code='integrism', name='Intégrisme', type='policy')
        F(code='slavery', name='Esclavagisme', type='policy')

        # -- techno_carac
        F(code='prod_merch', name='Production marchandises', type='techno_carac')
        F(code='weapon', name='Arme', type='techno_carac')
        F(code='extract', name='Capacitée d\'extraction', type='techno_carac')
        F(code='advance_ex', name='Capacitée d\'extraction avancée', type='techno_carac')
        F(code='propeller', name='Propulsion', type='techno_carac')
        F(code='syst_rad', name='Détection Système', type='techno_carac')
        F(code='fleet_rad', name='Détection Flotte', type='techno_carac')
        F(code='cargo', name='Capacité Cargo', type='techno_carac')
        F(code='YOT', name='Optimisation des Chantiers', type='techno_carac')
        F(code='SCM', name='Construction Spaciale', type='techno_carac')
        F(code='colo', name='Colonisation Planétaire', type='techno_carac')
        F(code='shield', name='Bouclier', type='techno_carac')
        F(code='type', name='Type', type='techno_carac')
        F(code='cost_prod', name='Cout centaure', type='techno_carac')
        F(code='cost_research', name='Cout de recherche', type='techno_carac')
        F(code='cost_ore', name='Cout minerai', type='techno_carac')
        F(code='cost_merch', name='Cout marchandise', type='techno_carac')
        F(code='cases', name='Nombre de cases', type='techno_carac')
        F(code='structural', name='Point de structure', type='techno_carac')
        F(code='public', name='Public', type='techno_carac')
        F(code='military', name='Militaire', type='techno_carac')

        # -- races
        F(code='mutant', name='Mutant', type='races')
        F(code='chrysoid', name='Chrysoïde', type='races')
        F(code='largyn', name='Largyn', type='races')
        F(code='human', name='Humain', type='races')
        F(code='sparow', name='Sparow', type='races')
        F(code='fungus', name='Fungus', type='races')
        F(code='wougzy', name='Wougzy', type='races')
        F(code='zorglub', name='Zorglub', type='races')

        # -- fleet_carac
        F(code='f_civilian', name='Civilian', type='fleet_carac')
        F(code='f_military', name='Military', type='fleet_carac')
        F(code='f_cargo', name='Cargo', type='fleet_carac')
        F(code='f_behaviour', name='Behaviour', type='fleet_carac')
        F(code='f_target', name='Target', type='fleet_carac')
        F(code='f_SA', name='Spacial Attack', type='fleet_carac')
        F(code='f_PA', name='Planetary Attack', type='fleet_carac')
        F(code='f_velocity', name='Velocity', type='fleet_carac')
        F(code='f_syst_rad', name='System Scanner', type='fleet_carac')
        F(code='f_fleet_rad', name='Fleet Scanner', type='fleet_carac')
        F(code='f_build_order', name='Directive de construction', type='fleet_carac')
        F(code='f_size', name='Size', type='fleet_carac')

        # -- budgets
        F(code='reserv', name='Centaure du tour précédent', type='budgets')
        F(code='budget_const', name='Constructions', type='budgets')
        F(code='budget_terra', name='Terraformation', type='budgets')
        F(code='budget_destr', name='Destruction', type='budgets')
        F(code='budget_tax', name='Impot systeme', type='budgets')
        F(code='budget_research', name='Recherche Technologique', type='budgets')
        F(code='budget_cesp', name='Depense contre esp', type='budgets')
        F(code='budget_spe', name='Depense en opération spéciale', type='budgets')
        F(code='budget_sch', name='Depense de création de plan', type='budgets')

        # -- fleet_behaviour
        F(code='neutral', name='Attitude Neutre', type='fleet_behaviour')
        F(code='syst_conquest', name='Conquete système', type='fleet_behaviour')
        F(code='pla_conquest', name='Conquete de la planète', type='fleet_behaviour')
        F(code='prev_attack', name='Attaque préventive', type='fleet_behaviour')
        F(code='player_attack', name='Attaque des flottes du commandant', type='fleet_behaviour')
        F(code='attack', name='Attaque toute flotte', type='fleet_behaviour')
        F(code='pillage', name='Pillage', type='fleet_behaviour')
 
        # -- techno_type
        F(code='building', name='Batiment', type='techno_type')
        F(code='component', name='Composant', type='techno_type')
        F(code='mastery', name='Maitrise', type='techno_type')
 
        # -- genders
        F(code='unknow', name='Inconnu', type='genders')
        F(code='male', name='Male', type='genders')
        F(code='female', name='Femelle', type='genders')
  
        # -- fleet_size
        F(code='size1', name='Ridicule', type='fleet_size')
        F(code='size2', name='Anodine', type='fleet_size')
        F(code='size3', name='Petite', type='fleet_size')
        F(code='size4', name='Moyenne', type='fleet_size')
        F(code='size5', name='Grande', type='fleet_size')
        F(code='size6', name='Très grande', type='fleet_size')
        F(code='size7', name='Titanesque', type='fleet_size')
        F(code='size8', name='Cyclopéenne', type='fleet_size')
        F(code='size9', name='Inimaginable', type='fleet_size')
        F(code='size10', name='Divine', type='fleet_size')
   
        # -- plan_domain
        F(code='d_public', name='Public', type='plan_domain')
        F(code='d_private', name='Privé', type='plan_domain')
        F(code='d_allies', name='Alliance', type='plan_domain')
   
        # -- taxe_level
        F(code='tax_null', name='Nulle', type='taxe_level')
        F(code='tax_light', name='Légère', type='taxe_level')
        F(code='tax_norm', name='Normale', type='taxe_level')
        F(code='tax_med', name='Medium', type='taxe_level')
        F(code='tax_heavy', name='Lourde', type='taxe_level')
        F(code='tax_total', name='Totale', type='taxe_level')
   
        # -- points
        F(code='centaure', name='centaures', type='points')
        F(code='tech_point', name='points technologiques', type='points')
        F(code='spe_point', name='points spéciaux', type='points')


class ManyFeature(models.Model):
    feature = models.ForeignKey(Feature)
    int_value = models.IntegerField(null=True)
    str_value = models.CharField(max_length=40)
    # 1 for int, 2 for code
    type = models.IntegerField(default=1)

    class Meta:
        abstract = True

    def value(self):
        if self.type == 1:
            return self.int_value
        else:
            return self.str_value

