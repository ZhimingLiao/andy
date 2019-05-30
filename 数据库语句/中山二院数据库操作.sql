-- 就诊卡信息查询服务
select *
from EMPI_CARD a
         left join EMPI_ZS.EMPI_INFO b on a.PK_EMPI_ID = b.PK_EMPI_ID
-- left join EMPI_LI
where ROWNUM < 10

-- 人员信息查询
SELECT *
FROM MDM.MDM_DICT_USER
WHERE CODE = 'pyj12345'
  AND DEL_FLAG = '0'

select *
from code_name_type_tab

SELECT PI.PK_DC_PI,
       PI.PI_CODE,
       PI.PI_NAME,
       PI.MPI,
       pv.pk_pv,
       pv.pvcode,
       pv.code_pvtype,
       pv.name_pvtype,
       pv.date_begin,
       outp.pk_pv,
       outp.pvcode,
       outp.TIMES_OP,
       outp.interid,
       outp.code_srvdept,
       outp.name_srvdept,
       outp.code_psn_reg,
       outp.name_psn_reg,
       outp.date_interid
FROM DC_PI pi
         LEFT JOIN DC_PV pv ON pi.PK_DC_PI = pv.pk_dc_pi
         LEFT JOIN EMPI_INFO info ON pv.MPI = info.PK_EMPI_ID
         LEFT JOIN DC_PV_OUTP outp ON pi.mpi = outp.mpi
where rownum = 1

select a.*
from EMPI_INFO a
where IDCARD = '440103196310015720'

SELECT PI.PK_DC_PI
     , PI.PI_CODE
     , PI.PI_NAME
     , PI.MPI
     , pv.pk_pv
     , pv.pvcode
     , pv.code_pvtype
     , pv.name_pvtype
     , to_char(pv.date_begin, 'yyyyMMdd')
     , outp.pk_pv
     , outp.pvcode
     , outp.TIMES_OP
     , outp.interid
     , outp.code_srvdept
     , outp.name_srvdept
     , outp.code_psn_reg
     , outp.name_psn_reg
     , outp.date_interid
     , info.*
     , '' PK_DC_PI
     , '' CARD_NO
FROM DC_PI pi
         LEFT JOIN DC_PV pv ON pi.PK_DC_PI = pv.pk_dc_pi
         LEFT JOIN EMPI_INFO info ON pv.MPI = info.PK_EMPI_ID
         LEFT JOIN DC_PV_OUTP outp ON pi.mpi = outp.mpi
WHERE 1 = 1
  --and info.IDCARD is not null
  and trim(info.IDCARD) = '440103196310015720'
  and pi.pi_code = '10002'
  and pv.code_pvtype = '3'
  and pv.name_pvtype = '住院'
  and to_char(pv.date_begin, 'yyyyMMdd') = '20111111'
  and to_char(pv.date_end, 'yyyyMMdd') = '20170202'
  and pv.pvcode = 'pyj4444'
  and pv.TIMES_HOSP = '3'
  and outp.interid = '门急诊号'
  and outp.code_srvdept = '科室ID' "


SELECT PI.PK_DC_PI,
       PI.PI_CODE,
       PI.PI_NAME,
       PI.MPI,
       '' PK_DC_PI,
       '' CARD_NO,
       pv.pk_pv,
       pv.pvcode,
       pv.code_pvtype,
       pv.name_pvtype,
       pv.date_begin,
       outp.pk_pv,
       outp.pvcode,
       outp.TIMES_OP,
       outp.interid,
       outp.code_srvdept,
       outp.name_srvdept,
       outp.code_psn_reg,
       outp.name_psn_reg,
       outp.date_interid
FROM DC_PI pi
         LEFT JOIN DC_PV pv ON pi.PK_DC_PI = pv.pk_dc_pi
         LEFT JOIN EMPI_INFO info ON pv.MPI = info.PK_EMPI_ID
         LEFT JOIN DC_PV_OUTP outp ON pi.mpi = outp.mpi
WHERE 1 = 1
  and info.IDCARD = '440103196310015720'
  and pi.pi_code = '10002'
  and pv.code_pvtype = '3'
  and pv.pvcode = 'pyj4444'


-- 查询科室
SELECT a.PK_DICT_DEPT
     , a.PK_DICT_CONTENT
     , a.PK_ORG
     , a.CODE
     , a.NAME
     , a.PK_FATHER
     , a.EU_LEVEL
     , a.EU_DEPTTYPE
     , a.SHORTNAME
     , a.FLAG_ACTIVE
     , a.DT_DEPTTYPE
     , a.PHONE
     , a.NOTE
     , a.WBCODE
     , a.PY_CODE
     , a.D_CODE
     , a.CREATOR
     , a.CREATE_TIME
     , a.MODIFIER
     , a.MODITY_TIME
     , a.DEL_FLAG
     , a.TS
     , a.ENGLISHNAME
     , a.EU_CODE_DEPTTYPE
     , a.DEPT_ROLE_CODE
     , a.DEPT_ROLE_NAME
     , a.DEPT_ADDRESS
     , a.ROLE_STARTTIME
     , a.ROLE_ENDTIME
     , a.SUPER_DEPT_NAME
     , a.DEPT_LINKMAN
     , b.CODE AS KCODE
     , b.NAME AS KNAME
     , a.FLAG_ACTIVE
FROM MDM_DICT_DEPT a
         LEFT JOIN MDM_DICT_DEPT b ON a.PK_FATHER = b.PK_DICT_DEPT
WHERE a.CODE = '01020202'
  AND ROWNUM = 1
  AND a.DEL_FLAG = '0'

SELECT COUNT(0) Cid
FROM MDM_DICT_DEPT a
WHERE 1 = 1
  and a.CODE = '01020202'
  AND DEL_FLAG = '0'

-- 术语查询
SELECT cn.PK_DICT_COMMON,
       cn.PK_DICT_CONTENT,
       cn.CODE_DICT_CONTENT,
       cn.CODE,
       cn.NAME,
       cn.PY_CODE,
       cn.CREATOR,
       cn.CREATE_TIME,
       cn.MODIFIER,
       cn.MODIFY_TIME,
       cn.OPR_FLAG,
       cn.WBCODE,
       cn.NAME_DICT_CONTENT,
       cn.FLAG_ACTIVE,
       ct.CODE_DICT_CONTENT,
       ct.NAME_DICT_CONTENT,
       ct.DEL_FLAG,
       ct.CREATOR,
       ct.CREATE_TIME,
       ct.MODIFIER,
       ct.MODIFY_TIME,
       ct.EDITION_CODE,
       ct.EDITION_NAME,
       ct.FLAG_ACTIVE,
       ct.EDITION_CODE
FROM MDM_DICT_COMMON cn
         LEFT JOIN MDM_DICT_CONTENT ct ON cn.CODE_DICT_CONTENT = ct.CODE_DICT_CONTENT
WHERE cn.CODE_DICT_CONTENT = 'GB/T 8561-1988'
  AND cn.CODE = '44'
  AND ct.EDITION_CODE is null
  AND cn.OPR_FLAG = '0'

SELECT PK_DC_ORD_PACS,
       PK_DC_CN_ORDER,
       CODE_ORD,
       MPI,
       CODE_PATI,
       PVCODE,
       PATINAME,
       CODE_SEX,
       NAME_SEX,
       BIRTHDAY,
       ADDR_PRE,
       TELENO_PRE,
       CODE_REQ,
       CODE_ORG_REQ,
       NAME_ORG_REQ,
       CODE_DEPT_REQ,
       NAME_DEPT_REQ,
       CODE_PSN_REQ,
       NAME_PSN_REQ,
       TELE_PSN_REQ,
       DATE_LAB,
       DESC_ILLNESS,
       CODE_DIAG,
       NAME_DIAG,
       DESC_DIAG,
       DIAG_DATE,
       DISEASE_PRE,
       PURP_RIS,
       CODE_EU_TYPE,
       NAME_EU_TYPE,
       CODE_EU_BODY,
       NAME_EU_BODY,
       CODE_SRV,
       NAME_SRV,
       DATE_RIS,
       DATE_RESERVATION,
       EU_STATE,
       FLAG_URGENT,
       FLAG_BED,
       EU_DESC,
       NOTE,
       LEVEL_SECRECY,
       DATA_SOURCE,
       SOURCE_PK,
       CREATE_TIME,
       EDIT_TIME,
       FLAG_MAKE,
       CODE_HOSP,
       NLS,
       NLY,
       DATE_EXAM,
       CODE_AUDI,
       NAME_AUDI,
       APPLIFORM_VALIDITY_LOWER,
       APPLIFORM_VALIDITY_UPPER,
       CODE_PRIORITY,
       NAME_PRIORITY
FROM DC_ORD_PACS
WHERE rownum < 3

select *
from DC_ORD_PACS
where rownum < 3

--2019-04-24
-- 数据交换索引信息 Table Code:data_exchange_index
select *
from CDR.DATA_EXCHANGE_INDEX
--where rownum < 200
order by MANAGE_BEGINTIME desc

select *
from cdr.DC_ORD_PACS
where CODE_REQ = '@BS004782278972'
order by CREATE_TIME desc


select *
from DC_ORD_PACS
where FLAG_MAKE <> '2'
  and DATA_SOURCE = 'HIS'
  and CODE_REQ = '0923848747'
  and PK_DC_ORD_PACS = '@BS00456'

select a.CODE_REQ, a.*
from DC_ORD_PACS a
         inner join DC_ORD_PACS_ITEM b on a.PK_DC_ORD_PACS = b.PK_DC_ORD_PACS
where a.DATA_SOURCE = 'HIS'
  and a.FLAG_MAKE <> '2'
  and a.PK_DC_ORD_PACS = '@BS004546'
  and a.CODE_REQ = '0923848747'

select a.CODE_REQ,
       a.APPLIFORM_VALIDITY_LOWER,
       a.APPLIFORM_VALIDITY_UPPER,
       a.CODE_PRIORITY,
       a.NAME_PRIORITY,
       a.DATE_LAB,
       a.CODE_PSN_REQ,
       a.NAME_PSN_REQ,
       a.CODE_DEPT_REQ,
       a.NAME_DEPT_REQ,
       a.DATE_EXAM,
       a.CODE_AUDI,
       a.NAME_AUDI,
       b.CODE_ORD,
       b.CODE_SRV,
       b.NAME_SRV,
       b.CODE_METHTEST,
       b.NAME_METHTEST,
       b.CODE_CHEC_TYPE,
       b.NAME_CHEC_TYPE,
       b.CODE_EU_BODY,
       b.NAME_EU_BODY,
       b.DATE_EX,
       b.CODE_DEPT_EXE,
       b.NAME_DEPT_EXE,
       e.TIMES_HOSP,
       e.NAME_PVTYPE,
       e.CODE_PVTYPE,
       a.EU_DESC,
       a.PVCODE,
       a.CODE_PATI,
       f.ID_APP,
       g.CODE_IP,
       d.IDCARD,
       d.MI_NO,
       d.PI_NAME,
       d.TELENO,
       d.CODE_SEX,
       d.BIRTHDAY,
       d.ADDR_WORKUNIT,
       g.BEDS_NO,
       g.BEDS_NAME,
       g.BFNO,
       g.BFMANE,
       g.DEPT_PHY_ADM,
       g.DEPT_PHY_ADM_NAME,
       g.DEPT_NURSE_ADM,
       g.DEPT_NURSE_ADM_NAME,
       c.CODE_DIAGPHASE,
       c.NAME_DIAGPHASE,
       c.NAME_DIAGSYS,
       c.CODE_DIAG,
       c.NAME_DIAG

from DC_ORD_PACS a
         inner join DC_ORD_PACS_ITEM b on a.PK_DC_ORD_PACS = b.PK_DC_ORD_PACS
         inner join DC_PV_DIAG_ITEM c on c.CODE_REQ = a.CODE_REQ
         left join EMPI_ZS.EMPI_INFO d on a.MPI = d.PK_EMPI_ID
         left join dc_pv e on a.PVCODE = e.PVCODE
         left join dc_pv_outp f on f.PK_PV = e.PK_PV
         left join DC_PV_INP g on g.PK_PV = e.PK_PV
where a.CODE_REQ = '0923848747yy'
