import csv
from nutritionModel import *
from run import session, createTables

def fixString(str):
    str = str.strip('~').decode('latin-1').encode('utf-8')
    if not str:
        return None
    return str

def stripTilde(table):
    for row in table:
        yield [fixString(str) for str in row]

createTables()

print "Importing Food Group Descriptions"
with open('data/FD_GROUP.txt', 'rb') as fd_group_file:
    utility_csv  = csv.reader(fd_group_file, delimiter='^')
    for row in stripTilde(utility_csv):
        new_fd_group = FoodGroupDescription()
        new_fd_group.fdGrp_Cd = row[0]
        new_fd_group.fdGrp_Desc = row[1]
        session.add(new_fd_group)

session.commit()

print "Importing LanguaL Factors Descriptions"
with open('data/LANGDESC.txt', 'rb') as langdesc_file:
    utility_csv  = csv.reader(langdesc_file, delimiter='^')
    for row in stripTilde(utility_csv):
        new_langdesc = LanguaLFactorsDescription()
        new_langdesc.factor_Code = row[0]
        new_langdesc.description = row[1]
        session.add(new_langdesc)
session.commit()


print "Importing Nutrient Definitions"
with open('data/NUTR_DEF.txt', 'rb') as nutr_def_file:
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

session.commit()

print "Importing Data Sources"
with open('data/DATA_SRC.txt', 'rb') as data_src_file:
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

session.commit()

print "Importing Data Derivation Code Descriptions"
with open('data/DERIV_CD.txt', 'rb') as deriv_cd_file:
    utility_csv  = csv.reader(deriv_cd_file, delimiter='^')
    for row in stripTilde(utility_csv):
        newDeriv_cd = DataDerivationCodeDescription()
        newDeriv_cd.deriv_Cd = row[0]
        newDeriv_cd.deriv_Desc = row[1]
        session.add(newDeriv_cd)

session.commit()


print "Importing Source Codes"
with open('data/SRC_CD.txt', 'rb') as src_cd_file:
    utility_csv  = csv.reader(src_cd_file, delimiter='^')
    for row in stripTilde(utility_csv):
        new_src_cd = SourceCode()
        new_src_cd.src_Cd = row[0]
        new_src_cd.srcCd_Desc = row[1]
        session.add(new_src_cd)

session.commit()

print "Importing Food Descriptions"
with open('data/FOOD_DES.txt', 'rb') as food_des_file:
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

session.commit()


print "Importing Weights"
with open('data/WEIGHT.txt', 'rb') as weight_file:
    foodDesQuery = session.query(FoodDescription)
    utility_csv  = csv.reader(weight_file, delimiter='^')
    for row in stripTilde(utility_csv):
        new_weight = Weight()
        new_weight.nDB_No = row[0]
        new_weight.seq = row[1]
        new_weight.amount = row[2]
        new_weight.msre_Desc = row[3]
        new_weight.gm_Wgt = row[4]
        new_weight.num_Data_Pts = row[5]
        new_weight.std_Dev = row[6]

        session.add(new_weight)

session.commit()


print "Importing Footnotes"
with open('data/FOOTNOTE.txt', 'rb') as footnote_file:
    utility_csv  = csv.reader(footnote_file, delimiter='^')
    for row in stripTilde(utility_csv):
        new_footnote = Footnote()
        new_footnote.nDB_No = row[0]
        new_footnote.footnt_No = row[1]
        new_footnote.footnt_Typ = row[2]
        new_footnote.nutr_No = row[3]
        new_footnote.footnt_Txt = row[4]
        
        session.add(new_footnote)

session.commit()

print "Joining Food Descriptions and Langual tables"
with open('data/LANGUAL.txt', 'rb') as langual_file:
    langualQuery = session.query(LanguaLFactorsDescription)
    utility_csv  = csv.reader(langual_file, delimiter='^')
    for row in stripTilde(utility_csv):
        food_des = foodDesQuery.filter_by(nDB_No = row[0]).first()
        langual = langualQuery.filter_by(factor_Code = row[1]).first()
        if food_des and langual:
            food_des.langdesc.append(langual)

session.commit()

with open('data/NUT_DATA.txt', 'rb') as nut_data_file:
    dataSrcQuery = session.query(SourcesOfData)
    print "Importing Nutrient Data"
    utility_csv  = csv.reader(nut_data_file, delimiter='^')
    i = 0
    for row in stripTilde(utility_csv):
        i = i+1
        print i
        new_nut = NutrientData()

        new_nut.nDB_No = row[0]
        new_nut.nutr_No = row[1]
        new_nut.nutr_Val = row[2]
        new_nut.num_Data_Pts = row[3]
        new_nut.std_Error = row[4]
        new_nut.src_Cd = row[5]
        new_nut.deriv_Cd = row[6]
        new_nut.ref_NDB_No = row[7]

        if row[8]:
            nutr_mark = True
        else:
            nutr_mark = False
            new_nut.add_Nutr_Mark = nutr_mark

        new_nut.num_Studies = row[9]
        new_nut.minVal = row[10]
        new_nut.maxVal = row[11]
        new_nut.dF = row[12]
        new_nut.low_EB = row[13]
        new_nut.up_EB = row[14]
        new_nut.stat_cmt = row[15]
        new_nut.addMod_Date = row[16]
        new_nut.cC = row[17]

        dataSource = dataSrcQuery.filter_by(dataSrc_ID = row[7]).first()
        if dataSource:
            new_nut.dataSource = dataSource

        session.add(new_nut)

session.commit()


