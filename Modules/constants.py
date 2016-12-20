from datetime import datetime
import datetime as dt

iZettle_countries = ['NO', 'FR', 'DE', 'FI', 'SE', 'ES', 'DK', 'IT', 'NL', 'GB', 'MX', 'BR']

first_part_link_admin_affected_id = 'https://admin.izettle.com/risk/details?organizationUUID='

cb_1st_party_fraud_list = ['FIRST PARTY FRAUD, FALSE ID', 'FIRST PARTY FRAUD, TRUE ID']
cb_3rd_party_fraud_list = ['THIRD PARTY MISUNDERSTANDING', 'THIRD PARTY FRAUDULENT BUYER']
cb_counterparty_list = ['COUNTERPARTY RISK, BANKRUPTCY', 'COUNTERPARTY RISK, OTHER']

complete_banned_statuses = ['BANNED', 'BANNED_FRAUD', 'BANNED_MATCH', 'BANNED_PROHIBITED_USE']

customer_status_mapping = {
    0: 'ACCEPTED',
    1: 'BANNED',
    2: 'UNCONFIRMED_IDENTITY',
    3: 'FROZEN',
    4: 'STOPPED_TRANSACTIONS',
    5: 'DELETED',
    6: 'STOPPED_DEPOSITS'
}

legal_entity_type_mapping = {1: 'Person', 2: 'Company', 3: 'Association'}

banned_status_mapping = {0: 'FRAUD', 1: 'PROHIBITED_USE', 2: 'MATCH'}

link_admin = 'https://admin.izettle.com/risk/details?organizationUUID='

entry_level_companies_groups = ['BR COMPANY Entry Level', 'Entry Level', 'Entry level',  'MX COMPANY Entry Level']

Peach_versions = {'before_peach': dt.datetime(2014,1,1), 'v.1': dt.datetime(2016,4,28), 'v.2': dt.datetime(2016,5,27),
                  'v.3': dt.datetime(2016,6,2), 'v.4': dt.datetime(2016,7,1), 'v.5': dt.datetime(2016,7,14), 
                  'v.6': dt.datetime(2016,7,22), 'v.7': dt.datetime(2016,8,10)}

currency_exchange_to_euro = {'BRL': 0.29, 'MXN': 0.048, 'DKK': 0.13447, 'EUR': 1, 'GBP': 1.2114, 'NOK': 0.10733, 'SEK':0.10594}

CandP_reader_type = ['com.izettle.reader.miura.a.a', 'com.izettle.reader.miura.a.b', 'com.izettle.reader.xac.50.1', 
                     'com.izettle.reader.datecs.1']
CandS_reader_type = ['com.izettle.reader.audio.2', 'com.izettle.reader.iOS.a.a.a', 'com.izettle.reader.android.a']

considered_entrymodes = ['EMV', 'CONTACTLESS_EMV', 'MAGSTRIPE', 'CONTACTLESS_MAGSTRIPE']

tag_id_ambassador_MX = 102 # from get_tag_entity(sun_conn)

business_type_mapping = {'Barber and Beauty Shops': 'Beauty/Barber/Spa',
                        'Miscellaneous and Specialty Retail Stores': 'Other Retail',
                        'Miscellaneous Repair Shops': 'Other Retail',
                        'Cleaning and maintenance': 'Cleaning Services',
                        'Lodging/Bed & Breakfast': 'Accommodation',
                        'Veterinary Services': 'Veterinary/Animal Care',
                        'Health Practitioners': 'Medical Practitioners/Services',
                        'Professional Services': 'Accounting/Legal/Business Services',
                        'General Contractors': 'Accounting/Legal/Business Services',
                        'Computer- & IT-services': 'IT Consulting/Services',
                        'Membership Organizations': 'Membership/Political Organizations',
                        'Schools and Educational Services': 'Education',
                        'Bands, Orchestras and Miscellaneous Entertainers': 'Music/Cinema',
                        'Art, Graphics, Photography': 'Art/Craft/Design',
                         'Eating places, Restaurants': 'Café/Restaurant/Bakery',
                        'Miscellaneous Food Stores': 'Food/Grocery/Beverage',
                        'Accessory and Apparel Stores': 'Apparel/Accessories',
                         'Charitable Organizations': 'Charitable organizations',
                        'Landscaping Services': 'Landscaping/Decoration Services',
                        'Recreation Services': 'Recreation/Entertainment'}
#df['active_business_type_description'] = df['business_type_description'].map(
#    lambda x: business_type_mapping[x] if x in business_type_mapping.keys() else x )

task_groups_mapping = {
    'CREDIT_RISK': 'Credit risk',
    'FRAUD': 'Fraud',
    'ML_TF': 'Money laundering',
    'PROHIBITED_USE': 'Prohibited use',
    'STRIPPERS_AND_PROSTITUTION': 'Prohibited use',
    'BENEFICIAL_OWNER': 'Beneficial owner',
    'PERSON_TO_BUSINESS_MIGRATION': 'p2b migration',
    'PURPOSE_AND_NATURE_OF_BUSINESS': 'Purpose and nature'
}

prefix_link_cb = 'https://admin.izettle.com/risk/chargeback/edit?chargebackUUID='
#cb['link'] = prefix_link_cb + cb['uuid']

entity_type_mapping = {0: 'Transaction', 1: 'OrginasationClient'}

not_reviewer_ids = ['Ok2MEC7kEeW_E2fMXEykqw', '1DbnUC7jEeWn_HJzsba9aw', '3dDUoC7kEeWjThz3LH0ZOw', '3qkMMC7kEeWM7kCDRDI8Wg',
         'gv_psETkEeWi8ezF6zODMg', 'g_KHEETkEeW50rg0F78-9w', '4-kcoC7iEeWOAhjRWaGPMA', 'zvwfUETkEeWCnfCbmgNwyg',
         'zjFVQETkEeWHrWQS1TC9JA', '3qkMMC7kEeWS1yOFhErAIQ', '4-kcoC7iEeWS7nhAu8k0kQ', 'VAmDUETkEeW-AbwFdLFzug',
         'Ok2MEC7kEeW1yk6BVjGviA', 'zvwfUETkEeW_UiSGIzrT0g', '1R_AsC7jEeWZCUV5BbNinA', 'OZ-Y0C7kEeW6GLeB4fDqvQ',
         'UwjcMETkEeWXYR5Lje2Rzg', 'g_KHEETkEeW9TClqdZbGUg', '4t6xgC7iEeWcy3lkJydx4g', 'VAmDUETkEeWjhPULAjbG9g',
         '1R_AsC7jEeWYOol3MidkAw']

reviewer_id_mapping = {'4': 'Adamvonn Corswannnnt', '27709': 'KlasJohansson', '45621': 'MalinJohansson', '62248': 'YaninCover',
                   '68768': 'FayeFlensburg', '115962': 'AndreasMeisingseth', '371092': 'TomBaylis', '376403': 'ViktorKarlsson',
                   '516337': 'MelinaDos Santos Waller', '782671': 'TatianaAlves', '1290298': 'GuadalupeHidalgo Pérez',
                   '1325593': 'JaninKoch', '1399889': 'CassiaPinheiro', '1510102': 'AlineMartins', '1607891': 'IremarBrayner',
                   '1921663': 'FredrikWachtmeister', '2174798': 'KaiSnellink', '2630786': 'PabloBárdossy', '2877886': 
                       'MariaIzzo', 'Integration Tester': 'Integration Tester'}

# map red days and increase the open time of the tasks created one day before the red days (it's incremenatal and sorted ascending)
RED_DAYS_SE = [datetime(2015,1,1), datetime(2015,1,6), datetime(2015,4,3), datetime(2015,4,4), datetime(2015,4,5),
               datetime(2015,4,6), datetime(2015,5,1), datetime(2015,5,14), datetime(2015,5,24), datetime(2015,6,6),
               datetime(2015,6,19), datetime(2015,6,20), datetime(2015,10,31), datetime(2015,12,24), datetime(2015,12,25),
               datetime(2015,12,26), datetime(2015,12,31),
               datetime(2016,1,1), datetime(2016,1,6), datetime(2016,3,25), datetime(2016,3,26), datetime(2016,3,27),
               datetime(2016,3,28), datetime(2016,5,1), datetime(2016,5,5), datetime(2016,5,15), datetime(2016,6,6),
               datetime(2016,6,24), datetime(2016,6,25), datetime(2016,11,5), datetime(2016,12,24), datetime(2016,12,25),
               datetime(2016,12,26), datetime(2016,12,31),
               datetime(2017,1,1), datetime(2017,1,6), datetime(2017,4,14), datetime(2017,4,15), datetime(2017,4,16),
               datetime(2017,4,17), datetime(2017,5,1), datetime(2017,5,25), datetime(2017,6,4), datetime(2017,6,6),
               datetime(2017,6,23), datetime(2017,6,24), datetime(2017,11,4), datetime(2017,12,24), datetime(2017,12,25),
               datetime(2017,12,26), datetime(2017,12,31),
               datetime(2018,1,1), datetime(2018,1,6), datetime(2018,3,30), datetime(2018,3,31), datetime(2018,4,1),
               datetime(2018,4,2), datetime(2018,5,1), datetime(2018,5,10), datetime(2018,5,20), datetime(2018,6,6),
               datetime(2018,6,22), datetime(2018,6,23), datetime(2018,11,3), datetime(2018,12,24), datetime(2018,12,25),
               datetime(2018,12,26), datetime(2018,12,31)]
RED_DAYS_BR = [datetime(2015,1,1), datetime(2015,1,25), datetime(2015,4,3), datetime(2015,4,4), datetime(2015,4,5),
               datetime(2015,4,21), datetime(2015,5,1), datetime(2015,7,9), datetime(2015,9,7), datetime(2015,10,12),
               datetime(2015,11,2), datetime(2015,11,15), datetime(2015,11,20), datetime(2015,12,24), datetime(2015,12,25),
               datetime(2015,12,26), datetime(2015,12,31),
               datetime(2016,1,1), datetime(2016,1,25), datetime(2016,3,25), datetime(2016,3,26), datetime(2016,3,27),
               datetime(2016,4,21), datetime(2016,5,1), datetime(2016,7,9), datetime(2016,9,7), datetime(2016,10,12),
               datetime(2016,11,2), datetime(2016,11,15), datetime(2016,11,20), datetime(2016,12,25),
               datetime(2016,12,26), datetime(2016,12,31),
               datetime(2017,1,1), datetime(2017,1,25), datetime(2017,4,14), datetime(2017,4,15), datetime(2017,4,16),
               datetime(2017,4,21), datetime(2017,5,1), datetime(2017,7,9), datetime(2017,9,7), datetime(2017,10,12),
               datetime(2017,11,2), datetime(2017,11,15), datetime(2017,11,20), datetime(2017,12,25),
               datetime(2017,12,26), datetime(2017,12,31),
               datetime(2018,1,1), datetime(2018,1,25), datetime(2018,3,30), datetime(2018,3,31), datetime(2018,4,1),
               datetime(2018,4,21), datetime(2018,5,1), datetime(2018,7,9), datetime(2018,9,7), datetime(2018,10,12),
               datetime(2018,11,2), datetime(2018,11,15), datetime(2018,11,20), datetime(2018,12,25),
               datetime(2018,12,26), datetime(2018,12,31)]

map_month = {'2015-12': 'December 2015', '2016-1': 'January 2016', '2016-2': 'February 2016', 
             '2016-3': 'March 2016', '2016-4': 'April 2016', '2016-5': 'May 2016', '2016-6': 'June 2016', 
             '2016-7': 'July 2016', '2016-8': 'August 2016', '2016-9': 'September 2016', '2016-10': 'October 2016', 
             '2016-11': 'November 2016', '2016-12': 'December 2016', '2017-1': 'January 2017', 
             '2017-2': 'February 2017', '2017-3': 'March 2017', '2017-4': 'April 2017', '2017-5': 'May 2017', 
             '2017-6': 'June 2017', '2017-7': 'July 2017', '2017-8': 'August 2017', '2017-9': 'September 2017', 
             '2017-10': 'October 2017', '2017-11': 'November 2017', '2017-12': 'December 2017'}

order_month = {'December 2015': 0, 'January 2016': 1, 'February 2016':2, 'March 2016':3, 'April 2016':4, 'May 2016':5, 
               'June 2016':6, 'July 2016':7, 'August 2016':8, 'September 2016':9, 'October 2016':10, 
               'November 2016':11, 'December 2016':12, 'January 2017':13, 'February 2017':14, 'March 2017':15, 
               'April 2017':16, 'May 2017':17, 'June 2017':18, 'July 2017':19, 'August 2017':20, 'September 2017':21, 
               'October 2017':22, 'November 2017':23, 'December 2017':24}

def map_vertical_segment():
    return map(
    lambda x: 'individual' if x == 'MERCHANT_CATEGORY_INDIVIDUAL' else 
    'retail' if x in ['MERCHANT_CATEGORY_ACCESSORY_STORES', 'MERCHANT_CATEGORY_ART_COMMERCIAL', 
                      'MERCHANT_CATEGORY_MISC_AND_SPECIALTY_RETAIL_STORES', 
                      'MERCHANT_CATEGORY_ART_DEALERS_AND_GALLERIES', 'MERCHANT_CATEGORY_DOOR_TO_DOOR'] else 
    'services' if x in ['MERCHANT_CATEGORY_BUSINESS_SERVICES', 'MERCHANT_CATEGORY_COMPUTER_REPAIR_AND_SERVICES', 
                       'MERCHANT_CATEGORY_LANDSCAPING_SERVICES', 'MERCHANT_CATEGORY_PROFESSIONAL_SERVICES', 
                       'MERCHANT_CATEGORY_GENERAL_CONTRACTORS', 'MERCHANT_CATEGORY_OTHER_SERVICES',
                       'MERCHANT_CATEGORY_MISC_REPAIR_SHOPS_AND_RELATED_SERVICES'] else 
    'health services' if x in ['MERCHANT_CATEGORY_HEALTH_PRACTITIONERS', 'MERCHANT_CATEGORY_VETERINARY_SERVICES'] else 
    'food & drink' if x in ['MERCHANT_CATEGORY_EATING_PLACES_RESTAURANTS', 
                            'MERCHANT_CATEGORY_LODGING_BED_AND_BREAKFAST', 'MERCHANT_CATEGORY_MISC_FOOD_STORES'] else 
    'hair & beauty' if x == 'MERCHANT_CATEGORY_BARBER_SHOPS' else 
    'other' if x in ['MERCHANT_CATEGORY_BANDS_ORCHESTRAS_AND_MISC_ENT', 'MERCHANT_CATEGORY_CHARITABLE_ORGANIZATIONS',
                     'MERCHANT_CATEGORY_MEMBERSHIP_ORGANIZATIONS', 'MERCHANT_CATEGORY_RECREATION_SERVICES',
                     'MERCHANT_CATEGORY_SCHOOLS_AND_EDUCATIONAL_SERVICES', 'MERCHANT_CATEGORY_TAXI_LIMO'] else
    'to_be_found' )
