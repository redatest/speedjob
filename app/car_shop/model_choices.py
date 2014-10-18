# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

SALARY_CHOICES = [
	('all', ('Tous')),
	('0', ('')),
	('1', 'SMIC'),
	('2', '18k'),
	('3', '20k'),
	('4', '22k'),
	('5', '24k'),
	('6', '26k'),
	('7', '28k'),
	('8', '30k'),
	('9', '32k'),
	('10', '34k'),
	('11', '36k'),
	('12', '38k'),
	('13', '40k'),
	('14', '42k'),
	('15', '44k'),
	('16', '46k'),
	('17', '48k'),
 	('18', '50k et plus')
]

OFFER_CHOICES = [
	('all', _('Tous')),
	('0', ('')),
	('1', _('Freelance')),
	('2', _('CDD')),
	('3', _('CDI')),
	('4', _('Stage')),
	('5', _('Interim'))
]

CATEGORY_CHOICES = [
	('all', 'Tous'),
	('0', ('')),
	('1', 'Assurance'),
	('2', 'Banque'),
	('3', 'Comptabilite'), 
	('4', 'Finance'), 
	('5', 'Informatique'), 
	('6', 'Telecom'), 
	('7', 'Juridique'), 
	('8', 'Ressources Humaines'), 
	('9', 'Communication'),
	('10', 'Distribution'),
	('11', 'Marketing'),
	('12', 'Batiment et Travaux publics'), 
	('13', 'Immobilier'), 
	('14', 'Logistique'), 
	('15', 'Securite'), 
	('16', 'Transport'),
	('17', 'Energie et nucleaire'), 
	('18', 'Industrie'), 
	('19', 'Agriculture'),
	('20', 'Agroalimentaire'), 
	('21', 'Artisanat'),
	('22', 'Energies renouvelables'),
	('23', 'Environnement'),
	('24', 'Recherche et Developpement'),
	('25', 'Luxe'), 
	('26', 'Mode'), 
	('27', 'Production'),
	('28', 'Audiovisuel'),
	('29', 'Culture'), 
	('30', 'Tourisme'), 
	('31', 'Biotechnologies'), 
	('32', 'Sante'),
	('33', 'Social'), 
	('34', 'Animation'), 
	('35', 'Education'),
	('36', 'Humanitaire'), 
	('37', 'Hotellerie'),
	('38', 'Nettoyage'), 
	('39', 'Restauration'), 
	('40', 'International'),
	('41', 'Travailleur Handicape'),
	('42', 'Stage (- de 2 mois)'), 
	('43', 'Stage (2 mois et +)')
]


REGION_CHOICES = [ 
	('all', _('Tous')),
	('0', ('')),	
	('1', _('Nord Pas de Calais')), 
	('2', _('Picardie')), 
	('3', _('Haute Normandie')), 
	('4', _('Basse Normandie')), 
	('5', _('Ile de France')), 
	('6', _('Bretagne')), 
	('7', _('Champagne Ardenne')), 
	('8', _('Alsace')), 
	('9', _('Pays de la Loire')), 
	('10', _('Centre')), 
	('11', _('Bourgogne')), 
	('12', _('Rhone Alpes')), 
	('13', _('Aquitaine')), 
	('14', _('PACA')), 
	('15', _('Corse')), 
	('16', _('Midi Pyrenees')), 
	('17', _('Languedoc Roussillon')), 
	('18', _('Lorraine')),
	('19', _('Poitou Charentes')),
	('20', _('Limousin')),
	('21', _('Auvergne')),
	('22', _('Franche Comte'))
]


YESNO = [
	
	('all', _('Tous')),
    ('Used', _('Yes')),
    ('New',  _('No'))
]


DEPARTEMENT_CHOICES = [
	('all', _('Tous')),
	('0', ('')),
	('1', 'Ain'),
	('2', ' Aisne'),
	('3', ' Allier'),
	('4', ' Alpes de Hautes-Provence'),
	('5', ' Hautes-Alpes'),
	('6', ' Alpes-Maritimes'),
	('7', ' Ardeche'),
	('8', ' Ardennes'),
	('9', ' Ariege'),
	 ('10', ' Aube'),
	('11', ' Aude'),
	('12', ' Aveyron'),
	('13', ' Bouches-du-Rhone'),
	('14', ' Calvados'),
	('15', ' Cantal'),
	('16', ' Charente'),
	('17', ' Charente-Maritime'),
	('18', ' Cher'),
	('20', ' Correze'),
	('21', " Cote-d'Or"),
	('22', " Cotes d'Armor"),
	('23', ' Creuse'),
	('24', ' Dordogne'),
	('25', ' Doubs'),
	('26', ' Drome'),
	('27', ' Eure'),
	('28', ' Eure-et-Loir'),
	('29', ' Finistere'),
	('30', ' Gard'),
	('31', ' Haute-Garonne'),
	('32', ' Gers'),
	('33', ' Gironde'),
	('34', ' Herault'),
	('35', ' Ille-et-Vilaine'),
	('36', ' Indre'),
	('37', ' Indre-et-Loire'),
	('38', ' Isere'),
	('39', ' Jura'),
	('40', ' Landes'),
	('41', ' Loir-et-Cher'),
	('42', ' Loire'),
	('43', ' Haute-Loire'),
	('44', ' Loire-Atlantique'),
	('45', ' Loiret'),
	('46', ' Lot'),
	('47', ' Lot-et-Garonne'),
	('48', ' Lozere'),
	('49', ' Maine-et-Loire'),
	('50', ' Manche'),
	('51', ' Marne'),
	('52', ' Haute-Marne'),
	('53', ' Mayenne'),
	('54', ' Meurthe-et-Moselle'),
	('55', ' Meuse'),
	('56', ' Morbihan'),
	('57', ' Moselle'),
	('58', ' Nievre'),
	('59', ' Nord'),
	('60', ' Oise'),
	('61', ' Orne'),
	('62', ' Pas-de-Calais'),
	('63', ' Puy-de-Dome'),
	('64', ' Pyrenees-Atlantiques'),
	('65', ' Hautes-Pyrenees'),
	('66', ' Pyrenees-Orientales'),
	('67', ' Bas-Rhin'),
	('68', ' Haut-Rhin'),
	('69', ' Rhone'),
	('70', ' Haute-Saone'),
	('71', ' Saone-et-Loire'),
	('72', ' Sarthe'),
	('73', ' Savoie'),
	('74', ' Haute-Savoie'),
	('75', ' Paris'),
	('76', ' Seine-Maritime'),
	('77', ' Seine et Marne'),
	('78', ' Yvelines'),
	('79', ' Deux-Sevres'),
	('80', ' Somme'),
	('81', ' Tarn'),
	('82', ' Tarn-et-Garonne'),
	('83', ' Var'),
	('84', ' Vaucluse'),
	('85', ' Vendee'),
	('86', ' Vienne'),
	('87', ' Haute-Vienne'),
	('88', ' Vosges'),
	('89', ' Yonne'),
	('90', ' Territoire-de-Belfort'),
	('91', ' Essonne'),
	('92', ' Hauts de Seine'),
	('93', ' Seine Saint Denis'),
	('94', ' Val de Marne'),
	('95',  "Val d'Oise"),
	('96', ' Corse-du-Sud'),
	('97', ' Haute-Corse')
]

DISPONIBILITY_CHOICES = [
	('all', _('Tous')),
	('0', ('')),
	('1', 'immediat'),
	('2', '1 mois'),
	('3', '2 mois'),
	('4', '3 mois'),
	('5', '3 mois et plus ')
]

STATUS_CHOICES = [
	('all', _('Tous')),
	('0', ('')),
	('1', 'en poste'),
	('2', 'preavis en cous ou termine')
]

STUDY_LEVEL_CHOICES = [
	('all', _('Tous')),
	('0', ('')),
	('1', '2nd'),
	('2', 'BAC'),
	('3', 'BAC+2'), 
	('4', 'BAC+3'), 
	('5', 'BAC+4'),
	('6', 'BAC+5 et plus'),
	('7', 'BEPC'),
	('8', 'CAP/BEF')
]

EXPERIENCE_CHOICES = [
	('all', _('Tous')),
	('0', ('')),
	('1', 'debutant'),
	('2', '6 mois'),
	('3', '1 ans '),
	('4', '2 ans '),
	('5', '3 ans '),
	('6', '4 ans '),
	('7', '5 a 10 ans '),
	('8', '10 ans et plus')
]

PERIOD_CHOICES = [
	('all', _('Tous')),
	('0', ('')),
	('1', 'temps plein'),
	('2', 'temps partiel')
]

