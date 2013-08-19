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

    # 5-digit Nutrient Databank number that uniquely identifies a food item. If
    # this field is defined as numeric, the leading zero will be lost.
    nDB_No = Column(String(5), primary_key = True)
    # 4-digit code indicating food group to which a food item belongs.
    fdGrp_Cd = Column(String(4), ForeignKey('fd_group.fdGrp_Cd'))
    # 200-character description of food item.
    long_Desc = Column(String(200), nullable = False)
    # 60-character abbreviated description of food item. Generated from the
    # 200-character description using abbreviations in Appendix A. If short
    # description is longer than 60 characters, additional abbreviations are
    # made.
    shrt_Desc = Column(String(60), nullable = False)
    # Other names commonly used to describe a food, including local or regional
    # names for various foods, for example, soda or pop for carbonated
    # beverages.
    comName = Column(String(100), nullable = True)
    # Indicates the company that manufactured the product, when appropriate.
    manufacName = Column(String(65), nullable = True)
    # Indicates if the food item is used in the USDA Food and Nutrient Database
    # for Dietary Studies (FNDDS) and thus has a complete nutrient profile for
    # the 65 FNDDS nutrients.
    survey = Column(Boolean, nullable = True)
    # Description of inedible parts of a food item (refuse), such as seeds or
    # bone.
    ref_desc = Column(String(135), nullable = True)
    # Percentage of refuse.
    refuse = Column(Integer(2), nullable = True)
    # Scientific name of the food item. Given for the least processed form of
    # the food (usually raw), if applicable.
    sciName = Column(String(65), nullable = True)
    # Factor for converting nitrogen to protein (see p. 11).
    n_Factor = Column(Numeric(4,2), nullable = True)
    # Factor for calculating calories from protein (see p. 12).
    pro_Factor = Column(Numeric(4,2), nullable = True)
    # Factor for calculating calories from fat (see p. 12).
    fat_Factor = Column(Numeric(4,2), nullable = True)
    # Factor for calculating calories from carbohydrate (see p. 12).
    cHO_Factor = Column(Numeric(4,2), nullable = True)

    fdGrp = relationship("FoodGroupDescription", backref = "fdDescs")
    nutrients = relationship("NutrientData", backref="food_des")
    footnotes = relationship("Footnote", backref="food_des")

class FoodGroupDescription(dbBase):
    __tablename__ = 'fd_group'
    
    # 4-digit code identifying a food group. Only the first 2 digits are
    # currently assigned. In the future, the last 2 digits may be used. Codes
    # may not be consecutive.
    fdGrp_Cd = Column(String(4), primary_key = True)
    # Name of food group.
    fdGrp_Desc = Column(String(60), nullable = False)

class LanguaLFactorsDescription(dbBase):
    __tablename__ = 'langdesc'
    
    # The LanguaL factor from the Thesaurus. Only those codes used to factor the
    # foods contained in the LanguaL Factor file are included in this file
    factor_Code = Column(String(5), primary_key = True)
    # The description of the LanguaL Factor Code from the thesaurus
    description = Column(String(140), nullable = False)

    food_des = relationship("FoodDescription", secondary =
                            langual_factor, backref = "langdesc")

class NutrientData(dbBase):
    __tablename__ = 'nut_data'

    nutr_ID = Column(Integer, primary_key = True)
    
    # 5-digit Nutrient Databank number.
    nDB_No = Column(String(5), ForeignKey('food_des.nDB_No'))
    # Unique 3-digit identifier code for a nutrient 
    nutr_No = Column(String(3), ForeignKey('nutr_def.nutr_No'))
    # Amount in 100 grams, edible portion 
    nutr_Val = Column(Numeric(10,3), nullable = False)
    # Number of data points (previously called Sample_Ct) is the number of
    # analyses used to calculate the nutrient value. If the number of data
    # points is 0, the value was calculated or imputed.
    num_Data_Pts = Column(Numeric(5,0), nullable = False)
    # Standard error of the mean. Null if cannot be calculated. The standard
    # error is also not given if the number of data points is less than three.
    std_Error = Column(Numeric(8,3), nullable = True)
    # Code indicating type of data.
    src_Cd = Column(String(2), ForeignKey('src_cd.src_Cd'))
    # Data Derivation Code giving specific information on how the value is
    # determined
    deriv_Cd = Column(String(4), ForeignKey('deriv_cd.deriv_Cd'))
    # NDB number of the item used to impute a missing value. Populated only for
    # items added or updated starting with SR14.
    ref_NDB_No = Column(String(5), nullable = True)
    # Indicates a vitamin or mineral added for fortification or enrichment. This
    # field is populated for ready-to-eat breakfast cereals and many brand-name
    # hot cereals in food group 8.
    add_Nutr_Mark = Column(Boolean, nullable = True)
    # Number of studies
    num_Studies = Column(Integer, nullable = True)
    # Minimum values
    minVal = Column(Numeric(10,3), nullable = True)
    # Maximum value
    maxVal = Column(Numeric(10,3), nullable = True)
    # Degrees of freedom
    dF = Column(Integer, nullable = True)
    # Lower 95% error bound
    low_EB = Column(Numeric(10,3), nullable = True)
    # Upper 95% error bound
    up_EB = Column(Numeric(10,3), nullable = True)
    # Statistical comments
    stat_cmt = Column(String(10), nullable = True)
    # Indicates when a value was either added to the database or last modified.
    addMod_Date = Column(String(10), nullable = True)
    # Confidence Code indicating data quality, based on evaluation of sample
    # plan, sample handling, analytical method, analytical quality control, and
    # number of samples analyzed. Not included in this release, but is planned
    # for future releases.
    cC = Column(String(1), nullable = True)

    dataSrc_ID = Column(String(6), ForeignKey('data_src.dataSrc_ID'))

class NutrientDefinition(dbBase):
    __tablename__ = 'nutr_def'

    # Unique 3-digit identifier code for a nutrient.
    nutr_No = Column(String(3), primary_key = True)
    # Units of measure (mg, g, g, and so on).
    units = Column(String(7), nullable = False)
    # International Network of Food Data Systems (INFOODS) Tagnames. A unique
    # abbreviation for a nutrient/food component developed by INFOODS to aid in
    # the interchange of data.
    tagname = Column(String(20), nullable = True)
    # Name of nutrient/food component.
    nutrDesc = Column(String(60), nullable = False)
    # Number of decimal places to which a nutrient value is rounded.
    num_Dec = Column(String(1), nullable = False)
    # Used to sort nutrient records in the same order as various reports
    # produced from SR.
    sR_Order = Column(Integer(6), nullable = False)

    nut_data = relationship("NutrientData", backref="nutr_def")

class SourceCode(dbBase):
    __tablename__ = 'src_cd'

    # 2-digit code
    src_Cd = Column(String(2), primary_key = True)
    # Description of source code that identifies the type of nutrient data.
    srcCd_Desc = Column(String(60), nullable = False)

    nut_data = relationship("NutrientData", backref="source")

class DataDerivationCodeDescription(dbBase):
    __tablename__ = 'deriv_cd'

    # Derivation Code.
    deriv_Cd = Column(String(4), primary_key = True)
    # Description of derivation code giving specific information on how the
    # value was determined.
    deriv_Desc = Column(String(120), nullable = False)

    nut_data = relationship("NutrientData", backref="dataDeriv")

class Weight(dbBase):
    __tablename__ = 'weight'

    weight_ID = Column(Integer, primary_key = True)
    # 5-digit Nutrient Databank number.
    nDB_No = Column(String(5), ForeignKey('food_des.nDB_No'))
    # Sequence number
    seq = Column(String(2))
    # Unit modifier (for example, 1 in "1 cup").
    amount = Column(Numeric(5,3), nullable = False)
    # Description (for example, cup, diced, and 1-inch pieces).
    msre_Desc = Column(String(84), nullable = False)
    # Gram weight
    gm_Wgt = Column(Numeric(7,1), nullable = False)
    # Number of data points
    num_Data_Pts = Column(Integer, nullable = True)
    # Standard deviation
    std_Dev = Column(Numeric(7,3), nullable = True)

    food_des = relationship("FoodDescription", backref = "weights")

class Footnote(dbBase):
    __tablename__ = 'footnote'

    footnote_id = Column(Integer, primary_key = True)
    # 5-digit Nutrient Databank number.
    nDB_No = Column(String(5), ForeignKey('food_des.nDB_No'))
    # Sequence number. If a given footnote applies to more than one nutrient
    # number, the same footnote number is used. As a result, this file cannot be
    # indexed.
    footnt_No = Column(String(4), nullable = False)
    # Type of footnote (see pdf, p.35)
    footnt_Typ = Column(String(1), nullable = False)
    # Unique 3-digit identifier code for a nutrient to which footnote applies.
    nutr_No = Column(String(3), nullable = True)
    # Footnote text
    footnt_Txt = Column(String(200), nullable = False)

class SourcesOfData(dbBase):
    __tablename__ = 'data_src'

    # Unique number identifying the reference/source.
    dataSrc_ID = Column(String(6), primary_key = True)
    # List of authors for a journal article or name of sponsoring organization
    # for other documents.
    authors = Column(String(255), nullable = True)
    # Title of article or name of document, such as a report from a company or
    # trade association. 
    title = Column(String(255), nullable = True)
    # Year article or document was published.
    year = Column(String(4), nullable = True)
    # Name of the journal in which the article was published.
    journal = Column(String(135), nullable = True)
    # Volume number for journal articles, books, or reports; city where
    # sponsoring organization is located.
    vol_City = Column(String(16), nullable = True)
    # Issue number for journal article; State where the sponsoring organization
    # is located.
    issue_State = Column(String(5), nullable = True)
    # Starting page number of article/document.
    start_Page = Column(String(5), nullable = True)
    # Ending page number of article/document.
    end_Page = Column(String(5), nullable = True)

    nutrients = relationship("NutrientData", backref = "dataSource")
    
