import sqlite3
# import pypyodbc as pyodbc # you could alias it to existing pyodbc code (not every code is compatible)

import pyodbc
import uuid

import configparser

import datetime

import ctypes
import logging
import smtplib, ssl

from email.mime.text import MIMEText


class DbConnector:
    __db_name_inside = "inside.db3"

    __listOfRowsInsideDb = []
    # __listOfRowFromArmDBase = []

    __arm_connection = None
    __eam_connection = None

    def __init__(self):
        self.__connectToInsideDb()

    def connectToBases(self):

        config = configparser.ConfigParser()
        config.read('dbConnections.ini')

        # connStr = 'Driver={{SQL Server}};Server={0};Database={1};UID={2};PWD={3};'.format(
        #     config['Arm']['Server'],
        #     config['Arm']['Database'],
        #     config['Arm']['UID'],
        #     config['Arm']['PWD']
        # )
        # self.__arm_connection = pyodbc.connect(connStr)

        serverLine = str(config['Eam']['ServerE'])
        if (':' in serverLine):
            serverLine = serverLine.replace(':', ',')
        else:
            serverLine = '(local)\\' + serverLine

        connStr = 'Driver={{SQL Server}};Server={0};Database={1};UID={2};PWD={3};'.format(
            serverLine,
            config['Eam']['DatabaseE'],
            config['Eam']['UIDE'],
            config['Eam']['PWDE']
        )
        print(connStr)
        self.__eam_connection = pyodbc.connect(connStr)

        config.clear()

    def deleteEamAllData(self):

        eam_cursor = self.__eam_connection.cursor()

        conn = sqlite3.connect(self.__db_name_inside)
        cursor = conn.cursor()

        sql = "SELECT [Name], [TP_Id] " \
              "FROM Main "

        cursor.execute(sql)

        for _name, tp_id in cursor.fetchall():

            sql = "DELETE FROM [EAM_SMH].[tp].[Технологические параметры] " \
                  "WHERE [Название]=\'{}\'".format(_name)
            eam_cursor.execute(sql)
            eam_cursor.commit()

            sql = "DELETE FROM [EAM_SMH].[ref].[АСУ ТП]" \
                  "WHERE [Название]=\'{}\'".format(_name)
            eam_cursor.execute(sql)
            eam_cursor.commit()

            sql = "DELETE FROM [EAM_SMH].[ref].[Справочник типов измерений]" \
                  "WHERE [Название]=\'Type_{}\'".format(_name)
            eam_cursor.execute(sql)
            eam_cursor.commit()

            sql = "DELETE FROM [EAM_SMH].[ref].[Справочник единиц измерения]" \
                  "WHERE [Название]=\'ED_{}\'".format(_name)
            eam_cursor.execute(sql)
            eam_cursor.commit()

            sql = "DELETE FROM [EAM_SMH].[tp].[Диапазоны значений]" \
                  "WHERE [ID_Технологического параметра]=\'{}\'".format(tp_id)

            eam_cursor.execute(sql)
            eam_cursor.commit()

            # sql = "DELETE FROM [EAM_SMH].[tp].[Значения технологических параметров]" \
            #       "WHERE [ID_Технологического параметра]=\'{}\'".format(tp_id)
            # eam_cursor.execute(sql)
            # eam_cursor.commit()

        cursor.close()

    def __connectToInsideDb(self):

        conn = sqlite3.connect(self.__db_name_inside)
        cursor = conn.cursor()

        sql = "SELECT [Id_EamBase] " \
              "FROM Main " \
              "WHERE ([ref_Id] IS NULL) OR ([TP_Id] IS NULL)"

        cursor.execute(sql)

        for id_eam in cursor.fetchall():
            ref_Id = str(uuid.uuid4()).upper()
            TP_Id = str(uuid.uuid4()).upper()

            sql = 'UPDATE Main ' \
                  'SET [ref_Id]=?, [TP_Id]=? ' \
                  'WHERE [Id_EamBase]=? '

            req = (ref_Id, TP_Id, id_eam[0])
            cursor.execute(sql, req)
            conn.commit()

        sql = "SELECT [Id_EamBase] " \
              "FROM Main " \
              "WHERE ([Ed_Ism_Id] IS NULL) OR ([Type_Id] IS NULL) OR ([TEG_ASU] IS NULL)"

        cursor.execute(sql)

        for id_eam in cursor.fetchall():
            ed_ism_Id = str(uuid.uuid4()).upper()
            type_Id = str(uuid.uuid4()).upper()

            sql = 'UPDATE Main ' \
                  'SET [Ed_Ism_Id]=?, [Type_Id]=?, [TEG_ASU]=\'S-9999/AI1/OUT\' ' \
                  'WHERE [Id_EamBase]=? '

            req = (ed_ism_Id, type_Id, id_eam[0])
            cursor.execute(sql, req)
            conn.commit()

        #
        #         t_sql = "CREATE TRIGGER IF NOT EXISTS \'TR_{}\' " \
        #               "AFTER UPDATE OF [Param] " \
        #               "ON MAIN " \
        #               "BEGIN " \
        #               "UPDATE Main SET [isWorking]= " \
        #                   "CASE " \
        #                   "WHEN ".format(_name)+sql+"=1.0 THEN 1.0 " \
        #                   "WHEN "+sql+"<1.0 THEN 0.0 " \
        #                   "END " \
        #               "WHERE [Id_EamBase]=\'{}\'; " \
        #               "END;".format(eam_id)
        #         # print(t_sql)
        #         cursor.execute(t_sql)
        #         conn.commit()

        conn.close()

    def closeConnectionS(self):
        self.__eam_connection.close()

    def getListOfRows(self):
        return self.__listOfRowsInsideDb

    def getDataFromArmDBase(self):

        conn = sqlite3.connect(self.__db_name_inside)
        cursor = conn.cursor()

        sql = "SELECT [Id_armBase] " \
              "FROM Main " \
              "WHERE [Id_armBase] IS NOT NULL"

        cursor.execute(sql)

        arm_cursor = self.__arm_connection.cursor()
        for arm_id in cursor.fetchall():
            sql = "SELECT * " \
                  "FROM [_Техпараметры] " \
                  "WHERE [ID_Техпараметра] = '{}'".format(arm_id[0])
            arm_cursor.execute(sql)

            tempTup = arm_cursor.fetchone()

            sql = 'UPDATE Main ' \
                  'SET [Param]={}, [TEG_ASU]=\'{}\' ' \
                  'WHERE [Id_armBase]=\'{}\''.format(tempTup[12], tempTup[5], arm_id[0])

            cursor.execute(sql)
            conn.commit()

        sql = "SELECT [Id_EamBase] " \
              "FROM Main " \
              "WHERE [TEG_ASU] IS NULL"

        cursor.execute(sql)
        for eam_id in cursor.fetchall():
            sql = 'UPDATE Main ' \
                  'SET [TEG_ASU]=\'S-9999/AI1/OUT\' ' \
                  'WHERE [Id_EamBase]=\'{}\''.format(eam_id[0])

            cursor.execute(sql)
            conn.commit()

        conn.close()

    def setValuesToTP(self):
        # print(rowToEamBase)

        conn = sqlite3.connect(self.__db_name_inside)
        cursor = conn.cursor()

        sql = "SELECT [TP_Id], [Name], [Id_EamBase], [Type_Id], [Ed_Ism_Id], [ref_Id], [TEG_ASU] " \
              "FROM Main "

        cursor.execute(sql)

        eam_cursor = self.__eam_connection.cursor()

        for tp_id, _name, eam_id, type_id, ed_ism_id, ref_id, teg_asu in cursor.fetchall():
            sql = 'IF NOT EXISTS (SELECT * FROM [EAM_SMH].[tp].[Технологические параметры] WHERE [Название]=\'{}\') ' \
                    'INSERT INTO [EAM_SMH].[tp].[Технологические параметры] (' \
                  '[ID]' \
                  ',[Название]' \
                  ',[ID_Производственного фонда]' \
                  ',[ID_Типа]' \
                  ',[ID_Единицы измерения]' \
                  ',[ID_Группы диапазонов]' \
                  ',[ID АСУ ТП]' \
                  ',[ТЭГ АСУ ТП]' \
                  ') VALUES (?,?,?,?,?,?,?,?);'.format(_name)

            ID = tp_id
            name = _name
            pf_id = eam_id
            _type_id = '41111111-D387-46EC-9A0C-6F4365CE0381'
            _ed_ism = ed_ism_id
            group_diap = '6405CD6B-7DF6-44CE-BDBA-5C546AD0D3BF'
            _ref = ref_id
            teg = teg_asu

            tup_tp_for_eam = (ID, name, pf_id, _type_id, _ed_ism, group_diap, _ref, teg)
            # print(tup_tp_for_eam)

            eam_cursor.execute(sql, tup_tp_for_eam)
            eam_cursor.commit()

        conn.close()

        # sql = 'INSERT INTO [EAM_SMH].[tp].[Технологические параметры] (' \
        #       '[ID]' \
        #       ',[Название]' \
        #       ',[ID_Производственного фонда]' \
        #       ',[ID_Типа]' \
        #       ',[ID_Единицы измерения]' \
        #       ',[ID_Группы диапазонов]' \
        #       ',[ID АСУ ТП]' \
        #       ',[ТЭГ АСУ ТП]' \
        #       ') VALUES (?,?,?,?,?,?,?,?);'
        #
        # cursor.execute(sql, rowToEamBase)
        # cursor.commit()

    def set_refAsuTP_Table(self):
        conn = sqlite3.connect(self.__db_name_inside)
        cursor = conn.cursor()

        sql = "SELECT [ref_Id], [Name] " \
              "FROM Main "

        cursor.execute(sql)

        dateForDB = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        # print(dateForDB)

        eam_cursor = self.__eam_connection.cursor()

        for ref_id, name in cursor.fetchall():
            sql = 'IF EXISTS (SELECT * FROM [EAM_SMH].[ref].[АСУ ТП] WHERE [Название]=\'{}\') ' \
                  'UPDATE [EAM_SMH].[ref].[АСУ ТП] SET [Дата создания]=\'{}\' ' \
                  'ELSE ' \
                  'INSERT INTO [EAM_SMH].[ref].[АСУ ТП] (' \
                  '[ID]' \
                  ',[Название]' \
                  ',[Дата создания]' \
                  ',[ID_ГПО]' \
                  ') VALUES (?,?,?,?);'.format(name, dateForDB)

            ID = ref_id
            _name = name
            date = dateForDB
            id_gpo = None

            tup_asu_for_eam = (ID, _name, date, id_gpo)

            eam_cursor.execute(sql, tup_asu_for_eam)
            eam_cursor.commit()

        conn.close()

    def set_refEd_Ism_Table(self):

        conn = sqlite3.connect(self.__db_name_inside)
        cursor = conn.cursor()

        sql = "SELECT [Ed_Ism_Id], [Name] " \
              "FROM Main "

        cursor.execute(sql)

        dateForDB = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        # print(dateForDB)

        eam_cursor = self.__eam_connection.cursor()

        for ed_id, name in cursor.fetchall():
            sql = 'IF EXISTS (SELECT * FROM [EAM_SMH].[ref].[Справочник единиц измерения] WHERE [Название]=\'ED_{}\') ' \
                  'UPDATE [EAM_SMH].[ref].[Справочник единиц измерения] SET [Дата создания]=\'{}\' ' \
                  'ELSE ' \
                  'INSERT INTO [EAM_SMH].[ref].[Справочник единиц измерения] (' \
                  '[ID]' \
                  ',[Название]' \
                  ',[Полное название]' \
                  ',[Кодовое буквенное обозначение]' \
                  ',[Группа единиц]' \
                  ',[Код ОКЕИ]' \
                  ',[Дата создания]' \
                  ') VALUES (?,?,?,?,?,?,?);'.format(name, dateForDB)

            ID = ed_id
            _name = 'ED_' + str(name)
            _fname = None
            kodName = None
            groupEd = None
            kodOk = None
            date = dateForDB

            t_edIsm_for_eam = (ID, _name, _fname, kodName, groupEd, kodOk, date)

            eam_cursor.execute(sql, t_edIsm_for_eam)
            eam_cursor.commit()

        conn.close()

    def set_refType_Table(self):

        conn = sqlite3.connect(self.__db_name_inside)
        cursor = conn.cursor()

        sql = "SELECT [Type_Id], [Name], [Ed_Ism_Id] " \
              "FROM Main "

        cursor.execute(sql)

        dateForDB = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        # print(dateForDB)

        eam_cursor = self.__eam_connection.cursor()

        for type_id, name, Ed_Ism_Id in cursor.fetchall():
            sql = 'IF EXISTS (SELECT * FROM [EAM_SMH].[ref].[Справочник типов измерений] WHERE [Название]=\'Type_{}\') ' \
                  'UPDATE [EAM_SMH].[ref].[Справочник типов измерений] SET [Дата создания]=\'{}\' ' \
                  'ELSE ' \
                  'INSERT INTO [EAM_SMH].[ref].[Справочник типов измерений] (' \
                  '[ID]' \
                  ',[Название]' \
                  ',[Дата создания]' \
                  ',[ID_Единицы измерения]' \
                  ') VALUES (?,?,?,?);'.format(name, dateForDB)

            ID = type_id
            _name = 'Type_' + str(name)
            date = dateForDB
            ed_ism_Id = Ed_Ism_Id

            t_type_for_eam = (ID, _name, date, ed_ism_Id)

            eam_cursor.execute(sql, t_type_for_eam)
            eam_cursor.commit()

        conn.close()

    def set_MainValuesOfZnachToTP_Table(self):

        conn = sqlite3.connect(self.__db_name_inside)
        cursor = conn.cursor()

        sql = "SELECT [TP_Id], [isWorking] " \
              "FROM Main "

        cursor.execute(sql)

        eam_cursor = self.__eam_connection.cursor()

        dateForDB = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        # print(dateForDB)

        for tp_id, isWorking in cursor.fetchall():
            sql = 'INSERT INTO [EAM_SMH].[tp].[Значения технологических параметров] (' \
                  '[ID]' \
                  ',[ID_Технологического параметра]' \
                  ',[Дата и время измерения]' \
                  ',[Значение]' \
                  ',[IsLast]' \
                  ') VALUES (?,?,?,?,?);'

            ID = str(uuid.uuid4()).upper()
            _tp_id = tp_id
            date = dateForDB
            value = isWorking
            isLast = 1

            t_vales_for_eam = (ID, _tp_id, date, value, isLast)

            eam_cursor.execute(sql, t_vales_for_eam)
            eam_cursor.commit()

        conn.close()

    def set_DiapValue_Table(self):

        conn = sqlite3.connect(self.__db_name_inside)
        cursor = conn.cursor()

        sql = "SELECT [TP_Id] " \
              "FROM Main "

        cursor.execute(sql)

        eam_cursor = self.__eam_connection.cursor()

        for tp_Id in cursor.fetchall():
            sql = 'IF NOT EXISTS (SELECT * FROM [EAM_SMH].[tp].[Диапазоны значений] WHERE [ID_Технологического параметра]=\'{}\') ' \
                  'INSERT INTO [EAM_SMH].[tp].[Диапазоны значений] (' \
                  '[ID]' \
                  ',[ID_Технологического параметра]' \
                  ',[ID_Названия диапазонов]' \
                  ',[Значение от включая]' \
                  ',[Значение до не включая]' \
                  ') VALUES (NEWID(),?,?,?,?),(NEWID(),?,?,?,?),(NEWID(),?,?,?,?);'.format(tp_Id[0])

            # sql = 'INSERT INTO [EAM_SMH].[tp].[Диапазоны значений] (' \
            #       '[ID]' \
            #       ',[ID_Технологического параметра]' \
            #       ',[ID_Названия диапазонов]' \
            #       ',[Значение от включая]' \
            #       ',[Значение до не включая]' \
            #       ') VALUES (?,?,?,?,?);'

            # ID1 = str(uuid.uuid4()).upper()
            _id_tp1 = tp_Id[0]
            _id_name1 = 'FC5B63B4-D387-46EC-9A0C-6F4365CE0381'
            zn_ot1 = 0.5
            zn_do1 = 1.5

            # ID2 = str(uuid.uuid4()).upper()
            _id_tp2 = tp_Id[0]
            _id_name2 = 'B3EF80A6-660A-4698-963B-B9C4E3268E81'
            zn_ot2 = 1.5
            zn_do2 = 2.5

            # ID3 = str(uuid.uuid4()).upper()
            _id_tp3 = tp_Id[0]
            _id_name3 = '7358B284-6706-459B-A31A-C3B4C82FBA83'
            zn_ot3 = 2.5
            zn_do3 = 3.5

            tup_asu_for_eam = (_id_tp1, _id_name1, zn_ot1, zn_do1,
                               _id_tp2, _id_name2, zn_ot2, zn_do2,
                                _id_tp3, _id_name3, zn_ot3, zn_do3
                               )

            eam_cursor.execute(sql, tup_asu_for_eam)
            eam_cursor.commit()

            # sql = 'INSERT INTO [EAM_SMH].[tp].[Диапазоны значений] (' \
            #       '[ID]' \
            #       ',[ID_Технологического параметра]' \
            #       ',[ID_Названия диапазонов]' \
            #       ',[Значение от включая]' \
            #       ',[Значение до не включая]' \
            #       ') VALUES (?,?,?,?,?);'


            # sql = 'INSERT INTO [EAM_SMH].[tp].[Диапазоны значений] (' \
            #       '[ID]' \
            #       ',[ID_Технологического параметра]' \
            #       ',[ID_Названия диапазонов]' \
            #       ',[Значение от включая]' \
            #       ',[Значение до не включая]' \
            #       ') VALUES (?,?,?,?,?);'



        conn.close()

    def getArmConnection(self):
        return self.__arm_connection

    def getEamConnection(self):
        return self.__eam_connection

    def updateValesInInsideBase(self):

        conn = sqlite3.connect(self.__db_name_inside)
        cursor = conn.cursor()

        sql = "SELECT [Interprit], [Name], [Id_EamBase] " \
              "FROM Main "

        cursor.execute(sql)

        for inter, _name, eam_id in cursor.fetchall():

            if inter == 1:

                sql = "SELECT [Param] " \
                      "FROM Main " \
                      "WHERE [Id_EamBase]=\'{}\'; ".format(eam_id)
                cursor.execute(sql)

                _sql = ''
                if cursor.fetchone()[0] > 0.0:
                    _sql = "UPDATE Main SET [isWorking]=1.0 " \
                           "WHERE [Id_EamBase]=\'{}\'; ".format(eam_id)
                else:
                    _sql = "UPDATE Main SET [isWorking]=2.0 " \
                           "WHERE [Id_EamBase]=\'{}\'; ".format(eam_id)

                cursor.execute(_sql)
                conn.commit()

                # sql = "CREATE TRIGGER IF NOT EXISTS \'TR_{}\' " \
                #       "AFTER UPDATE OF [Param] " \
                #       "ON MAIN " \
                #       "BEGIN " \
                #       "UPDATE Main SET [isWorking]= " \
                #       "CASE " \
                #       "WHEN [Param]>0 THEN 1.0 " \
                #       "WHEN [Param]<=0 THEN 2.0 " \
                #       "END " \
                #       "WHERE [Id_EamBase]=\'{}\'; " \
                #       "END;".format(_name, eam_id)
                #
                # cursor.execute(sql)
                # conn.commit()

            if inter == 2:

                sql = "SELECT [Param] " \
                      "FROM Main " \
                      "WHERE [Id_EamBase]=\'{}\'; ".format(eam_id)
                cursor.execute(sql)

                _sql = ''
                if cursor.fetchone()[0] == 0.0:
                    _sql = "UPDATE Main SET [isWorking]=1.0 " \
                           "WHERE [Id_EamBase]=\'{}\'; ".format(eam_id)
                else:
                    _sql = "UPDATE Main SET [isWorking]=2.0 " \
                           "WHERE [Id_EamBase]=\'{}\'; ".format(eam_id)
                cursor.execute(_sql)
                conn.commit()

            if inter == 3:

                sql = "SELECT [Param] FROM Main  WHERE [Id_EamBase]=\'{}\'".format(eam_id)
                cursor.execute(sql)
                temp = str(cursor.fetchall()[0][0]).split(',')
                formattedList = ''.join([",\'%s\'" % x for x in temp])[1:]

                sql = "SELECT AVG([isWorking]) " \
                      "FROM Main " \
                      "WHERE [Id_armBase] IN " \
                      "(" \
                      "{}" \
                      ")".format(formattedList)
                cursor.execute(sql)

                _sql = ''
                if cursor.fetchone()[0] == 1.0:
                    _sql = "UPDATE Main SET [isWorking]=1.0 " \
                           "WHERE [Id_EamBase]=\'{}\'; ".format(eam_id)
                else:
                    _sql = "UPDATE Main SET [isWorking]=2.0 " \
                           "WHERE [Id_EamBase]=\'{}\'; ".format(eam_id)
                cursor.execute(_sql)
                conn.commit()
                # print(cursor.fetchall())

            if inter == 4:

                sql = "SELECT [Param] FROM Main  WHERE [Id_EamBase]=\'{}\'".format(eam_id)
                cursor.execute(sql)
                temp = str(cursor.fetchall()[0][0]).split(',')
                formattedList = ''.join([",\'%s\'" % x for x in temp])[1:]

                sql = "SELECT AVG([isWorking]) " \
                      "FROM Main " \
                      "WHERE [Id_armBase] IN " \
                      "(" \
                      "{}" \
                      ")".format(formattedList)
                cursor.execute(sql)

                _sql = ''
                val = cursor.fetchone()[0]
                if (val > 1.0 and val < 2.0):
                    _sql = "UPDATE Main SET [isWorking]=1.0 " \
                           "WHERE [Id_EamBase]=\'{}\'; ".format(eam_id)
                else:
                    _sql = "UPDATE Main SET [isWorking]=2.0 " \
                           "WHERE [Id_EamBase]=\'{}\'; ".format(eam_id)
                cursor.execute(_sql)
                conn.commit()
                # print(cursor.fetchall())

            if inter == 7:
                _sql = "UPDATE Main SET [isWorking]=3.0 " \
                       "WHERE [Id_EamBase]=\'{}\'; ".format(eam_id)
                cursor.execute(_sql)
                conn.commit()

    def eamSynchronization(self):
        conn = sqlite3.connect(self.__db_name_inside)
        cursor = conn.cursor()

        sql = "SELECT [Name] " \
              "FROM Main "

        cursor.execute(sql)

        eam_cursor = self.__eam_connection.cursor()

        for _name in cursor.fetchall():

            sql = 'IF EXISTS (SELECT * FROM [EAM_SMH].[ref].[Справочник единиц измерения] WHERE [Название]=\'ED_{}\') ' \
                  'SELECT ' \
                  '[ID]' \
                  ' FROM [EAM_SMH].[ref].[Справочник единиц измерения]' \
                  ' WHERE [Название]=\'ED_{}\';' \
                  'ELSE ' \
                  'SELECT 0'.format(_name[0], _name[0])

            rows = eam_cursor.execute(sql).fetchall()
            if rows[0][0] != 0:
                for ed_id in rows:
                    _sql = 'UPDATE [Main] ' \
                           'SET [Ed_Ism_Id]=\'{}\' ' \
                           'WHERE [Name]=\'{}\''.format(ed_id[0], _name[0])

                    cursor.execute(_sql)
                    conn.commit()

            sql = 'IF EXISTS (SELECT * FROM [EAM_SMH].[ref].[АСУ ТП] WHERE [Название]=\'{}\') ' \
                  'SELECT ' \
                  '[ID]' \
                  ' FROM [EAM_SMH].[ref].[АСУ ТП]' \
                  ' WHERE [Название]=\'{}\';' \
                  'ELSE ' \
                  'SELECT 0'.format(_name[0], _name[0])

            rows = eam_cursor.execute(sql).fetchall()
            if rows[0][0] != 0:
                for ref_id in rows:
                    _sql = 'UPDATE [Main] ' \
                           'SET [ref_Id]=\'{}\'' \
                           'WHERE [Name]=\'{}\''.format(ref_id[0], _name[0])

                    cursor.execute(_sql)
                    conn.commit()

            sql = 'IF EXISTS (SELECT * FROM [EAM_SMH].[tp].[Технологические параметры] WHERE [Название]=\'{}\') ' \
                  'SELECT ' \
                  '[ID]' \
                  ',[ID_Единицы измерения]' \
                  ',[ID АСУ ТП]' \
                  ' FROM [EAM_SMH].[tp].[Технологические параметры]' \
                  ' WHERE [Название]=\'{}\';' \
                  'ELSE ' \
                  'SELECT 0'.format(_name[0],_name[0])

            rows = eam_cursor.execute(sql).fetchall()
            if rows[0][0] != 0:
                for tp_id, ed_id, ref_asu in rows:

                    _sql = 'UPDATE [Main] ' \
                           'SET [TP_Id]=\'{}\'' \
                           ',[Ed_Ism_Id]=\'{}\'' \
                           ',[ref_Id]=\'{}\' ' \
                           'WHERE [Name]=\'{}\''.format(tp_id,ed_id,ref_asu,_name[0])

                    cursor.execute(_sql)
                    conn.commit()

        conn.close()


LOG_FILENAME = 'ERROR_CONFIG.txt'
logging.basicConfig(filename=LOG_FILENAME, level=logging.WARNING)
# logging.debug('This message should go to the log file')

config = configparser.ConfigParser()
config.read('dbConnections.ini')

# sending
port = 25
host = '192.168.1.211'
sender_email = 'eam_converter@smd-chem.ru'
receiver_email = config['Email']['Receiver']

message = MIMEText('Внимание!!!\nПрограмма EamConverter завершила работу с ошибкой.\n', 'plain', 'utf-8')
context = ssl.create_default_context()

try:
    db = DbConnector()

    db.connectToBases()

    db.eamSynchronization()

    # init all components
    # db.deleteEamAllData()

    # return!!!!!
    db.set_refAsuTP_Table()
    db.set_refEd_Ism_Table()
    # db.set_refType_Table()
    db.setValuesToTP()
    db.set_DiapValue_Table()
    #
    db.closeConnectionS()

except Exception as e:
    # Logging!!!!
    with open(LOG_FILENAME, 'w'):
        logging.exception('Last exception')
    # Window!!!
    ctypes.windll.user32.MessageBoxW(0, "Возникла непредвиденная ошибка.\nФайл Error", "Ошибка", 1)

    #     send email
    with smtplib.SMTP(host, port) as server:
        server.sendmail(sender_email, receiver_email, message.as_string())

    server.close()


# db = DbConnector()
# db.connectToBases()
# # init all components
# db.deleteEamAllData()
#
# db.set_refAsuTP_Table()
# db.set_refEd_Ism_Table()
# db.set_refType_Table()
# db.setValuesToTP()
# db.set_DiapValue_Table()
# #
# # # Update
# # db.getDataFromArmDBase()
# # db.updateValesInInsideBase()
# # db.set_MainValuesOfZnachToTP_Table()
#
# db.closeConnectionS()