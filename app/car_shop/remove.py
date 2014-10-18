# -*- coding: utf-8 -*-

ss = "Ain02 -  Aisne03 -  Allier04 -  Alpes de Hautes-Provence05 -  Hautes-Alpes06 -  Alpes-Maritimes07 -  Ardeche08 -  Ardennes09 -  Ariege2A -  Corse-du-Sud2B -  Haute-Corse10 -  Aube11 -  Aude12 -  Aveyron13 -  Bouches-du-Rhone14 -  Calvados15 -  Cantal16 -  Charente17 -  Charente-Maritime18 -  Cher19 -  Correze21 -  Cote-d'Or22 -  Cotes d'Armor23 -  Creuse24 -  Dordogne25 -  Doubs26 -  Drome27 -  Eure28 -  Eure-et-Loir29 -  Finistere30 -  Gard31 -  Haute-Garonne32 -  Gers33 -  Gironde34 -  Herault35 -  Ille-et-Vilaine36 -  Indre37 -  Indre-et-Loire38 -  Isere39 -  Jura40 -  Landes41 -  Loir-et-Cher42 -  Loire43 -  Haute-Loire44 -  Loire-Atlantique45 -  Loiret46 -  Lot47 -  Lot-et-Garonne48 -  Lozere49 -  Maine-et-Loire50 -  Manche51 -  Marne52 -  Haute-Marne53 -  Mayenne54 -  Meurthe-et-Moselle55 -  Meuse56 -  Morbihan57 -  Moselle58 -  Nievre59 -  Nord60 -  Oise61 -  Orne62 -  Pas-de-Calais63 -  Puy-de-Dome64 -  Pyrenees-Atlantiques65 -  Hautes-Pyrenees66 -  Pyrenees-Orientales67 -  Bas-Rhin68 -  Haut-Rhin69 -  Rhone70 -  Haute-Saone71 -  Saone-et-Loire72 -  Sarthe73 -  Savoie74 -  Haute-Savoie75 -  Paris76 -  Seine-Maritime77 -  Seine et Marne78 -  Yvelines79 -  Deux-Sevres80 -  Somme81 -  Tarn82 -  Tarn-et-Garonne83 -  Var84 -  Vaucluse85 -  Vendee86 -  Vienne87 -  Haute-Vienne88 -  Vosges89 -  Yonne90 -  Territoire-de-Belfort91 -  Essonne92 -  Hauts de Seine93 -  Seine Saint Denis94 -  Val de Marne95"

dd = '<select><option value="">Secteur ?</option> - <option value="2.2">Assurance</option> - <option value="2.3">Banque</option> - <option value="3.5">Comptabilite</option> - <option value="3.4">Finance</option> - <option value="4.6">Informatique</option> - <option value="4.7">Telecom</option> - <option value="5.8">Juridique</option> - <option value="5.9">Ressources Humaines</option> - <option value="6.11">Communication</option> - <option value="6.13">Distribution</option> - <option value="6.12">Marketing</option> - <option value="7.15">Batiment &amp; Travaux publics</option> - <option value="7.14">Immobilier</option> - <option value="8.16">Logistique</option> - <option value="8.18">Securite</option> - <option value="8.17">Transport</option> - <option value="9.19">Energie &amp; nucleaire</option> - <option value="9.21">Industrie</option> - <option value="11.22">Agriculture</option> - <option value="11.24">Agroalimentaire</option> - <option value="11.23">Artisanat</option> - <option value="12.26">Energies renouvelables</option> - <option value="12.25">Environnement</option> - <option value="12.27">Recherche et Developpement</option> - <option value="13.28">Luxe</option> - <option value="13.30">Mode</option> - <option value="13.29">Production</option> - <option value="14.31">Audiovisuel</option> - <option value="14.32">Culture</option> - <option value="14.33">Tourisme</option> - <option value="15.36">Biotechnologies</option> - <option value="15.34">Sante</option> - <option value="15.35">Social</option> - <option value="16.39">Animation</option> - <option value="16.38">Education</option> - <option value="16.37">Humanitaire</option> - <option value="17.42">Hotellerie</option> - <option value="17.40">Nettoyage</option> - <option value="17.41">Restauration</option> - <option value="18.43">International</option> - <option value="12357">Travailleur Handicape</option> - <option value="19.44">Stage (- de 2 mois)</option> - <option value="19.45">Stage (2 mois et +)</option></select>'

import bleach

ddd = bleach.clean(dd, tags=[], strip=True)
print ddd.split(' - ')
ddd = ddd.split(' - ')

def cleanDepartement(sss):
	s = ss.split(' - ')
	li = []
	for i in s:

		if i[-2:].isdigit():
			x = ( str(int( i[-2:] ) -1) , i[:-2])
		else: 
			x = x = ("A", i[:-2])
		print x
		li.append(x)
	return li	

print(cleanDepartement(ss))

def clean_sectors(ar):
	# s = ar.split(' - ')
	li = []
	for i,j in enumerate(ar):
		x = ( str(i), j )
		li.append(x)
	return li	

print clean_sectors(ddd)
