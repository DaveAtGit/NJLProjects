
#
template_filetype = 'Template'

#   dictionary for data -> Matrix
Matrix = {}

#   conventions for MasterList
#   tabs..
TAB_XLS = [  # 'NameKonvention',
          'ProjektEigenschaften',
          'DatenpunktEigenschaften',
          'ApparateEigenschaften',
          'AnlageEigenschaften',
          'SteuerungsEigenschaften',
          'KabelEigenschaften',
          'ApparateEigenschaften',
          'AdressierungsKonzept',
          'MasterListe']


#   Matrix['MasterListe']
MST_Site = 'MST_Anlage'
MST_Device = 'MST_Apparat'
MST_DeviceDivision = 'MST_AppDiv'
MST_DeviceFunction = 'MST_AppFunktion'
MST_DPName = 'MST_Datenpunkt'
MST_DPFunction = 'MST_DPFunktion'
MST_DPAddress = 'MST_Adresse'
MST_DPComment = 'MST_Kommentar'
MST_DPUnit = 'MST_Einheit'
MST_DPControlFunction = 'MST_Reglerart'
MST_DeviceName = 'MST_Name'
MST_DeviceManufacturer = 'MST_Hersteller'
MST_DeviceType = 'MST_Apparate-Typ'
MST_DevicePower = 'MST_Leistung (kW)'
MST_DeviceCurrent = 'MST_Strom (A)'
MST_DeviceVoltage = 'MST_Spannung (V)'
MST_DeviceSpeed = 'MST_Drehzahl (U/min)'
MST_MessureType = 'MST_Messtyp'


#   Matrix['ProjektEigenschaften']
PRJ_1 = 'PRJ_1'
PRJ_2 = 'PRJ_2'
prjName = 'prjName'
prjNumber = 'prjNumber'
prjField = 'prjField'

prjType = 'prjType'
prjAddress1 = 'prjAddress1'
prjAddress2 = 'prjAddress2'
prjObjectAddress1 = 'prjObjectAddress1'
prjObjectAddress2 = 'prjObjectAddress2'
prjCostumer = 'prjCostumer'
prjObjectCostumer = 'prjObjectCostumer'
prjPlaner = 'prjPlaner'
prjObjPlaner1 = 'prjObjPlaner1'
prjObjPlaner2 = 'prjObjPlaner2'

prjAE = 'prjAE-Bezeichner'
prjAA = 'prjAA-Bezeichner'
prjDE1 = 'prjDE-Bezeichner1'
prjDE2 = 'prjDE-Bezeichner2'
prjDE3 = 'prjDE-Bezeichner3'
prjDA = 'prjDA-Bezeichner'
prjESchemaStart = 'prjESchemaStart'
prjESchemaDiff = 'prjESchemaDiff'
prjSite1 = 'prjSite1'
prjSite2 = 'prjSite2'
prjSite3 = 'prjSite3'
prjSite4 = 'prjSite4'
prjSite5 = 'prjSite5'
prjSite6 = 'prjSite6'
prjSite7 = 'prjSite7'
prjSite8 = 'prjSite8'
prjSite9 = 'prjSite9'
prjSite10 = 'prjSite10'
prjSite11 = 'prjSite11'
prjSite12 = 'prjSite12'
prjSite13 = 'prjSite13'
prjSite14 = 'prjSite14'
prjSite15 = 'prjSite15'
prjSite16 = 'prjSite16'
prjSite17 = 'prjSite17'
prjSite18 = 'prjSite18'
prjSite19 = 'prjSite19'
prjSite20 = 'prjSite20'


#   Matrix['DatenpunktEigenschaften']
DPT_1 = 'DPT_1'
DPT_2 = 'DPT_2'
# dptAE0 = 'dptAE 0'
# dptAE1 = 'dptAE 1'
# dptAE2 = 'dptAE 2'
# dptAE3 = 'dptAE 3'
# dptAE4 = 'dptAE 4'
# dptAE5 = 'dptAE 5'
# dptAA0 = 'dptAA 0'
# dptAA1 = 'dptAA 1'
# dptAA2 = 'dptAA 2'
# dptAA3 = 'dptAA 3'
# dptDE0 = 'dptDE 0'
# dptDE1 = 'dptDE 1'
# dptDE2 = 'dptDE 2'
# dptDE3 = 'dptDE 3'
# dptDA0 = 'dptDA 0'
# dptDA1 = 'dptDA 1'
# dptDA2 = 'dptDA 2'
# dptDA3 = 'dptDA 3'


#   Matrix['SteuerungsEigenschaften']
STG_START_INDEX = 3
STG_1 = 'STG_1'
STG_2 = 'STG_2'
STG_3 = 'STG_3'
stgIP = 'stgIPAdresse'
stgName = 'stgSteuerfeld'
stgManufacturer = 'stgHersteller'
stgType1 = 'stgReihe'
stgType2 = 'stgTyp'
# stgAE1 = 'stgAnaloger Eingang 1'
# stgAE2 = 'stgAnaloger Eingang 2'
# stgAE3 = 'stgAnaloger Eingang 3'
# stgAE4 = 'stgAnaloger Eingang 4'
# stgAE5 = 'stgAnaloger Eingang 5'
# stgAA1 = 'stgAnaloger Ausgang 1'
# stgAA2 = 'stgAnaloger Ausgang 2'
# stgAA3 = 'stgAnaloger Ausgang 3'
# stgAA4 = 'stgAnaloger Ausgang 4'
# stgAA5 = 'stgAnaloger Ausgang 5'
# stgDE1 = 'Digitaler Eingang 1'
# stgDE2 = 'Digitaler Eingang 2'
# stgDE3 = 'Digitaler Eingang 3'
# stgDE4 = 'Digitaler Eingang 4'
# stgDE5 = 'Digitaler Eingang 5'
# stgDA1 = 'Digitaler Ausgang 1'
# stgDA2 = 'Digitaler Ausgang 2'
# stgDA3 = 'Digitaler Ausgang 3'
# stgDA4 = 'Digitaler Ausgang 4'
# stgDA5 = 'Digitaler Ausgang 5'


#   Matrix['Kabeleigenschaften']
CAB_Text = 'CAB_Text'
CAB_0 = 'CAB_0'
CAB_1 = 'CAB_1'
CAB_2 = 'CAB_2'
CAB_3 = 'CAB_3'
CAB_4 = 'CAB_4'
CAB_5 = 'CAB_5'
CAB_6 = 'CAB_6'
# cabWireless = 'cabWireless'
# cabLNPE_1 = 'cabLNPE_1'
# cab3LPE_1 = 'cab3LPE_1'
# cab3LNPE_1 = 'cab3LNPE_1'
# cab3LPEs_1 = 'cab3LPEs_1'
# cab3LNPEs_1 = 'cab3LNPEs_1'
# cab2L_1 = 'cab2L_1'
# cab3L_1 = 'cab3L_1'
# cab4L_1 = 'cab4L_1'
# cab5L_1 = 'cab5L_1'
# cab6L_1 = 'cab6L_1'
# cab2Ls_1 = 'cab2Ls_1'
# cab3Ls_1 = 'cab3Ls_1'
# cab4Ls_1 = 'cab4Ls_1'
# cab5Ls_1 = 'cab5Ls_1'
# cab6Ls_1 = 'cab6Ls_1'


#   Matrix['Adressierungskonzept']
ADR_1 = 'ADR_1'
ADR_2 = 'ADR_2'
adrAuto = 'adrAutoAddress'
adrHardware = 'adrHardware'


#   Matrix['ApparateEigenschaften']
APP_Function = 'APP_Function'
APP_Function2 = 'APP_Function2'
APP_Text = 'APP_Text'
APP_Cable1 = 'APP_Cable1'
APP_Cable2 = 'APP_Cable2'
APP_Cable3 = 'APP_Cable3'
APP_Cable4 = 'APP_Cable4'
APP_Cable5 = 'APP_Cable5'
APP_Cable6 = 'APP_Cable6'

appCabType = 'app KabelTyp'
appPath = 'app KabelPfad'
# appSENS_0 = 'app SENS 0'
# appSENS_A1 = 'app SENS A1'
# appSENT_A1 = 'app SENT A1'
# appSENF_A1 = 'app SENF A1'
# appSENL_A1 = 'app SENL A1'
# appSEND_A1 = 'app SEND A1'
# appSENP_A1 = 'app SENP A1'
# appSENV_A1 = 'app SENV A1'
# appMOTS_C1 = 'app MOTS C1'
# appMOTS_C2 = 'app MOTS C2'
# appMOTS_C3 = 'app MOTS C3'
# appMOTS_C4 = 'app MOTS C4'
# appMOTS_C5 = 'app MOTS C5'
# appMOTS_C6 = 'app MOTS C6'
# appMOTS_D1 = 'app MOTS D1'
# appMOTS_D2 = 'app MOTS D2'
# appMOTS_D3 = 'app MOTS D3'
# appMOTS_D4 = 'app MOTS D4'
# appMOTS_D5 = 'app MOTS D5'
# appMOTS_D6 = 'app MOTS D6'
# appMOT1_C1 = 'app MOT1 C1'
# appMOT1_C2 = 'app MOT1 C2'
# appMOT1_C3 = 'app MOT1 C3'
# appMOT1_C4 = 'app MOT1 C4'
# appMOT1_C5 = 'app MOT1 C5'
# appMOT1_D1 = 'app MOT1 D1'
# appMOT1_D2 = 'app MOT1 D2'
# appMOT1_D3 = 'app MOT1 D3'
# appMOT1_D4 = 'app MOT1 D4'
# appMOT1_D5 = 'app MOT1 D5'
# appPMPx_C1 = 'app PMPx C1'
# appPMPx_C2 = 'app PMPx C2'
# appPMPx_C3 = 'app PMPx C3'
# appPMPx_C4 = 'app PMPx C4'
# appPMPx_C5 = 'app PMPx C5'
# appPMPx_D1 = 'app PMPx D1'
# appPMPx_D2 = 'app PMPx D2'
# appPMPx_D3 = 'app PMPx D3'
# appPMPx_D4 = 'app PMPx D4'
# appPMPx_D5 = 'app PMPx D5'
# appRVTx_A1 = 'app RVTx A1'
# appRVTx_A2 = 'app RVTx A2'
# appRVTx_B1 = 'app RVTx B1'
# appRVTx_B2 = 'app RVTx B2'
# appRVTx_C1 = 'app RVTx C1'
# appRVTx_C2 = 'app RVTx C2'
# app SM01 A1
# app SM02 A1
# app SM03 A1
# app RM01 A1
# app RM02 A1
# app RM03 A1
# app KLPx A1
# app KLPx A2
# app KLPx A3
# app KLPx B1
# app KLPx B2
# app KLPx B3
# app KLPx C1
# app KLPx C2
# app KLPx C3
# app PNT3 A1
# app PNT3_230
# app A_OUT A1
# app D_OUT A1
# app LOG1
