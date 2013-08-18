from sqlalchemy import (Column, Integer, String, Numeric, Boolean,
                        ForeignKey, Table, create_engine)
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

dbBase = declarative_base()

### Association table for many-many relationships
langual_factor = Table('langual', dbBase.metadata,
                       Column('nDB_No', String(5),
                              ForeignKey('food_des.nDB_No')), 
                       Column('factor_Code', String(5),
                              ForeignKey('langdesc.factor_Code')))

class FoodDescription(dbBase):
    __tablename__ = 'food_des'
    
    nDB_No = Column(String(5), primary_key = True)
    fdGrp_Cd = Column(String(4), ForeignKey('fd_group.fdGrp_Cd'))
    long_Desc = Column(String(200), nullable = False)
    shrt_Desc = Column(String(60), nullable = False)
    comName = Column(String(100), nullable = True)
    manufacName = Column(String(65), nullable = True)
    survey = Column(Boolean, nullable = True)
    ref_desc = Column(String(135), nullable = True)
    refuse = Column(Integer(2), nullable = True)
    sciName = Column(String(65), nullable = True)
    n_Factor = Column(Numeric(4,2), nullable = True)
    pro_Factor = Column(Numeric(4,2), nullable = True)
    fat_Factor = Column(Numeric(4,2), nullable = True)
    cHO_Factor = Column(Numeric(4,2), nullable = True)

    fdGrp = relationship("FoodGroupDescription", backref = "fdDescs")
    nutrients = relationship("NutrientData", backref="food_des")
    footnotes = relationship("Footnote", backref="food_des")

class FoodGroupDescription(dbBase):
    __tablename__ = 'fd_group'

    fdGrp_Cd = Column(String(4), primary_key = True)
    fdGrp_Desc = Column(String(60), nullable = False)

class LanguaLFactorsDescription(dbBase):
    __tablename__ = 'langdesc'
    
    factor_Code = Column(String(5), primary_key = True)
    description = Column(String(140), nullable = False)
    food_des = relationship("FoodDescription", secondary =
                            langual_factor, backref = "langdesc")

class NutrientData(dbBase):
    __tablename__ = 'nut_data'

    nutr_ID = Column(Integer, primary_key = True)

    nDB_No = Column(String(5), ForeignKey('food_des.nDB_No'))
    nutr_No = Column(String(3), ForeignKey('nutr_def.nutr_No'))
    nutr_Val = Column(Numeric(10,3), nullable = False)
    num_Data_Pts = Column(Numeric(5,0), nullable = False)
    std_Error = Column(Numeric(8,3), nullable = True)
    src_Cd = Column(String(2), ForeignKey('src_cd.src_Cd'))
    deriv_Cd = Column(String(4), ForeignKey('deriv_cd.deriv_Cd'))
    ref_NDB_No = Column(String(5), nullable = True)
    add_Nutr_Mark = Column(Boolean, nullable = True)
    num_Studies = Column(Integer, nullable = True)
    minVal = Column(Numeric(10,3), nullable = True)
    maxVal = Column(Numeric(10,3), nullable = True)
    dF = Column(Integer, nullable = True)
    low_EB = Column(Numeric(10,3), nullable = True)
    up_EB = Column(Numeric(10,3), nullable = True)
    stat_cmt = Column(String(10), nullable = True)
    addMod_Date = Column(String(10), nullable = True)
    cC = Column(String(1), nullable = True)

    dataSrc_ID = Column(String(6), ForeignKey('data_src.dataSrc_ID'))
class NutrientDefinition(dbBase):
    __tablename__ = 'nutr_def'

    nutr_No = Column(String(3), primary_key = True)
    units = Column(String(7), nullable = False)
    tagname = Column(String(20), nullable = True)
    nutrDesc = Column(String(60), nullable = False)
    num_Dec = Column(String(1), nullable = False)
    sR_Order = Column(Integer(6), nullable = False)

    nut_data = relationship("NutrientData", backref="nutr_def")

class SourceCode(dbBase):
    __tablename__ = 'src_cd'

    src_Cd = Column(String(2), primary_key = True)
    srcCd_Desc = Column(String(60), nullable = False)
    nut_data = relationship("NutrientData", backref="source")

class DataDerivationCodeDescription(dbBase):
    __tablename__ = 'deriv_cd'

    deriv_Cd = Column(String(4), primary_key = True)
    deriv_Desc = Column(String(120), nullable = False)

    nut_data = relationship("NutrientData", backref="dataDeriv")

class Weight(dbBase):
    __tablename__ = 'weight'

    weight_ID = Column(Integer, primary_key = True)
    nDB_No = Column(String(5), ForeignKey('food_des.nDB_No'))
    seq = Column(String(2))
    amount = Column(Numeric(5,3), nullable = False)
    msre_Desc = Column(String(84), nullable = False)
    gm_Wgt = Column(Numeric(7,1), nullable = False)
    num_Data_Pts = Column(Integer, nullable = True)
    std_Dev = Column(Numeric(7,3), nullable = True)

    food_des = relationship("FoodDescription", backref = "weights")

class Footnote(dbBase):
    __tablename__ = 'footnote'

    footnote_id = Column(Integer, primary_key = True)
    nDB_No = Column(String(5), ForeignKey('food_des.nDB_No'))

    footnt_No = Column(String(4), nullable = False)
    footnt_Typ = Column(String(1), nullable = False)
    nutr_No = Column(String(3), nullable = True)
    footnt_Txt = Column(String(200), nullable = False)

class SourcesOfData(dbBase):
    __tablename__ = 'data_src'

    dataSrc_ID = Column(String(6), primary_key = True)
    authors = Column(String(255), nullable = True)
    title = Column(String(255), nullable = True)
    year = Column(String(4), nullable = True)
    journal = Column(String(135), nullable = True)
    vol_City = Column(String(16), nullable = True)
    issue_State = Column(String(5), nullable = True)
    start_Page = Column(String(5), nullable = True)
    end_Page = Column(String(5), nullable = True)

    nutrients = relationship("NutrientData", backref = "dataSource")
    
