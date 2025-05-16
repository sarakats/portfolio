-- Split original table into new tables to start normalizing data
create table PROVINCE as
select distinct PROVINCE_UID, PROVINCE_NAME
from FIELD_CROPS_HAY;

create table CCS as
select distinct CCS_UID, CCS_NAME, PROVINCE_UID
from FIELD_CROPS_HAY;

create table CROPS as
select distinct CROP_UID, CROP_NAME, CCS_UID
from FIELD_CROPS_HAY;

create table FARMS as
select FARMS_REPORTING, CROP_AREA_HA, CROP_UID, CCS_UID
from FIELD_CROPS_HAY;

-- Set primary key constraints
alter table PROVINCE
add constraint PROVINCE_PK
primary key (PROVINCE_UID);

alter table CCS
add constraint CCS_PK
primary key (CCS_UID);

alter table CROPS
add constraint CROPS_PK
primary key (CCS_UID, CROP_UID);

alter table FARMS
add constraint CROP_FARMS_PK
primary key (CCS_UID, CROP_UID, FARMS_REPORTING);

-- Set foreign key constraints
alter table CCS
add constraint CCS_PROVINCE_FK
foreign key(PROVINCE_UID)
references PROVINCE(PROVINCE_UID);

alter table CROPS 
add constraint CROP_CCS_FK
foreign key(CCS_UID)
references CCS(CCS_UID);

alter table FARMS
add constraint CROPS_FARMS_FK
foreign key(CCS_UID, CROP_UID)
references CROPS(CCS_UID, CROP_UID);

-- Drop original raw data table
drop table FIELD_CROPS_HAY;

-- Select query (total area of Potatoes grown in PEI)
select province.province_name as "Province Name", crops.crop_name as "Crop Name", sum(farms.crop_area_ha) as "Total Area"
from province
join ccs on province.province_uid = ccs.province_uid
join crops on ccs.ccs_uid = crops.ccs_uid
join farms on crops.crop_uid = farms.crop_uid and ccs.ccs_uid = farms.ccs_uid
where province.province_name like 'Prince Edward Island'
  and crops.crop_name like 'Potatoes'
group by province.province_name, crops.crop_name;

