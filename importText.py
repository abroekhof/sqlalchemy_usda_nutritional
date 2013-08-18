import csv
from nutritionModel import *
from run import session, createTables

def fixString(str):
    if not str:
        return None
    return str.strip('~').decode('latin-1').encode('utf-8')

def stripTilde(table):
    for row in table:
        yield [fixString(str) for str in row]



createTables()

data_src_file = open('DATA_SRC.txt', 'rb')
datsrcln_file = open('DATSRCLN.txt', 'rb')
deriv_cd_file = open('DERIV_CD.txt', 'rb')
fd_group_file = open('FD_GROUP.txt', 'rb')
food_des_file = open('FOOD_DES.txt', 'rb')
footnote_file = open('FOOTNOTE.txt', 'rb')
langdesc_file = open('LANGDESC.txt', 'rb')
langual_file = open('LANGUAL.txt', 'rb')
nut_data_file = open('NUT_DATA.txt', 'rb')
nutr_def_file = open('NUTR_DEF.txt', 'rb')
src_cd_file = open('SRC_CD.txt', 'rb')
weight_file = open('WEIGHT.txt', 'rb')

print "Importing Food Group Descriptions"
utility_csv  = csv.reader(fd_group_file, delimiter='^')
for row in stripTilde(utility_csv):
    new_fd_group = FoodGroupDescription()
    new_fd_group.fdGrp_Cd = row[0]
    new_fd_group.fdGrp_Desc = row[1]
    session.add(new_fd_group)

print "Importing LanguaL Factors Descriptions"
utility_csv  = csv.reader(langdesc_file, delimiter='^')
for row in stripTilde(utility_csv):
    new_langdesc = LanguaLFactorsDescription()
    new_langdesc.factor_Code = row[0]
    new_langdesc.description = row[1]
    session.add(new_langdesc)

print "Importing Nutrient Definitions"
utility_csv  = csv.reader(nutr_def_file, delimiter='^')
for row in stripTilde(utility_csv):
    new_nutr_def = NutrientDefinition()
    new_nutr_def.nutr_No = row[0]
    new_nutr_def.units = row[1]
    new_nutr_def.tagname = row[2]
    new_nutr_def.nutrDesc = row[3]
    new_nutr_def.num_Dec = row[4]
    new_nutr_def.sR_Order = row[5]
    session.add(new_nutr_def)

print "Importing Data Sources"
utility_csv  = csv.reader(data_src_file, delimiter='^')
for row in stripTilde(utility_csv):
    new_data_src = SourcesOfData()
    new_data_src.dataSrc_ID = row[0]
    new_data_src.authors = row[1]
    new_data_src.title = row[2]
    new_data_src.year = row[3]
    new_data_src.journal = row[4]
    new_data_src.vol_City = row[5]
    new_data_src.issue_State = row[6]
    new_data_src.start_Page = row[7]
    new_data_src.end_Page = row[8]
    session.add(new_data_src)

print "Importing Data Derivation Code Descriptions"
utility_csv  = csv.reader(deriv_cd_file, delimiter='^')
for row in stripTilde(utility_csv):
    newDeriv_cd = DataDerivationCodeDescription()
    newDeriv_cd.deriv_Cd = row[0]
    newDeriv_cd.deriv_Desc = row[1]
    session.add(newDeriv_cd)

print "Importing Source Codes"
utility_csv  = csv.reader(src_cd_file, delimiter='^')
for row in stripTilde(utility_csv):
    new_src_cd = SourceCode()
    new_src_cd.src_Cd = row[0]
    new_src_cd.srcCd_Desc = row[1]
    session.add(new_src_cd)

print "Importing Food Descriptions"
foodGrpQuery = session.query(FoodGroupDescription)
utility_csv  = csv.reader(food_des_file, delimiter='^')
for row in stripTilde(utility_csv):
    new_food_des = FoodDescription()
    new_food_des.nDB_No = row[0]
    # Item one is a foreign key!
    new_food_des.long_Desc = row[2]
    new_food_des.shrt_Desc = row[3]
    new_food_des.comName = row[4]
    new_food_des.manufacName = row[5]
    if row[6]:
        survey = True
    else:
        survey = False
    new_food_des.survey = survey
    new_food_des.ref_desc = row[7]
    new_food_des.refuse = (row[8])
    new_food_des.sciName = row[9]
    new_food_des.n_Factor = (row[10])
    new_food_des.pro_Factor = (row[11])
    new_food_des.fat_Factor = (row[12])
    new_food_des.cHO_Factor = (row[13])
    
    foodGroup = foodGrpQuery.filter_by(fdGrp_Cd = row[1]).first()
    if foodGroup:
        new_food_des.fdGrp = foodGroup

    session.add(new_food_des)

print "Importing Weights"
foodDesQuery = session.query(FoodDescription)
utility_csv  = csv.reader(weight_file, delimiter='^')
for row in stripTilde(utility_csv):
    new_weight = Weight()
    # Item zero is a foreign key!
    new_weight.seq = row[1]
    new_weight.amount = row[2]
    new_weight.msre_Desc = row[3]
    new_weight.gm_Wgt = row[4]
    new_weight.num_Data_Pts = row[5]
    new_weight.std_Dev = row[6]

    food_des = foodDesQuery.filter_by(nDB_No = row[0]).first()
    if food_des:
        new_weight.food_des = food_des

    session.add(new_weight)

print "Importing Footnotes"
utility_csv  = csv.reader(footnote_file, delimiter='^')
for row in stripTilde(utility_csv):
    new_footnote = Footnote()
    # Item zero is a foreign key!
    new_footnote.footnt_No = row[1]
    new_footnote.footnt_Typ = row[2]
    new_footnote.nutr_No = row[3]
    new_footnote.footnt_Txt = row[4]
    food_des = foodDesQuery.filter_by(nDB_No = row[0]).first()
    if food_des:
        new_footnote.food_des = food_des
    
    session.add(new_footnote)

print "Joining Food Descriptions and Langual tables"
langualQuery = session.query(LanguaLFactorsDescription)
utility_csv  = csv.reader(langual_file, delimiter='^')
for row in stripTilde(utility_csv):
    food_des = foodDesQuery.filter_by(nDB_No = row[0]).first()
    langual = langualQuery.filter_by(factor_Code = row[1]).first()
    if food_des and langual:
        food_des.langdesc.append(langual)


nutrDefQuery = session.query(NutrientDefinition)
srcCdQuery = session.query(SourceCode)
derivQuery = session.query(DataDerivationCodeDescription)
dataSrcQuery = session.query(SourcesOfData)
print "Importing Nutrient Data"
utility_csv  = csv.reader(nut_data_file, delimiter='^')
for row in stripTilde(utility_csv):
    new_nut = NutrientData()

    # Item zero is a foreign key!
    # Item one is a foreign key!
    new_nut.nutr_Val = row[2]
    new_nut.num_Data_Pts = row[3]
    new_nut.std_Error = row[4]
    # Item five is a foreign key!
    # Item six is a foreign key!
    new_nut.ref_NDB_No = row[7]
    new_nut.add_Nutr_Mark = row[8]
    new_nut.num_Studies = row[9]
    new_nut.minVal = row[10]
    new_nut.maxVal = row[11]
    new_nut.dF = row[12]
    new_nut.low_EB = row[13]
    new_nut.up_EB = row[14]
    new_nut.stat_cmt = row[15]
    new_nut.addMod_Date = row[16]
    new_nut.cC = row[17]

    food_des = foodDesQuery.filter_by(nDB_No = row[0]).first()
    if food_des:
        new_nut.food_des = food_des

    nutr_def = nutrDefQuery.filter_by(nutr_No = row[1]).first()
    if nutr_def:
        new_nut.nutr_def = nutr_def

    source = srcCdQuery.filter_by(src_Cd = row[5]).first()
    if source:
        new_nut.source = source

    dataDeriv = derivQuery.filter_by(deriv_Cd = row[6]).first()
    if dataDeriv:
        new_nut.dataDeriv = dataDeriv

    dataSource = dataSrcQuery.filter_by(dataSrc_ID = row[7]).first()
    if dataSource:
        new_nut.dataSource = dataSource

    
session.commit()


