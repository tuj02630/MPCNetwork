from unittest import TestCase

import mysql.connector

from Lambda.Database.Data.Criteria import Criteria
from Lambda.Database.Data.Hardware import Hardware
from Lambda.Database.Data.Recording import Recording
from Lambda.Database.MPCDatabase import MPCDatabase, MatchItem

from Lambda.Database.Data.Account import Account

database = MPCDatabase()

ac = Account("TestUser", "password", "email@email.com")
aw = Account("WrongUser", "WrongPassword", "wrong@email.com")
database.insert(ac, True)
iac = database.get_id_by_name(Account, ac.username)
hc = Hardware("TestDevice", "720p", account_id=iac)
hw = Hardware("WrongDevice", "1000090p", account_id=100000)
database.insert(hc, True)
ihc = database.get_id_by_name(Hardware, hc.name)
rc = Recording("TestFile", "CURDATE()", "NOW()", hardware_id=ihc, account_id=iac)
database.insert(rc, True)
cc = Criteria(5000, 500, 500)
cw = Criteria(50000000, 500000, 500000)
length = len([a.criteria_type for a in database.get_all(Criteria)])
if length > 1 or length == 0:
    database.delete(Criteria, MatchItem(Criteria.TYPE, cc.criteria_type))
    database.insert(cc, True)
else:
     pass

icc = database.get_id_by_type(Criteria, 5000)


class TestMPCDatabase(TestCase):

    def test_verify_field(self):
        i = database.verify_field(Account, Account.NAME, aw.username)
        if i:
            self.fail()
        self.assertTrue(database.verify_field(Account, Account.NAME, ac.username))

    def test_verify_fields(self):
        i = database.verify_fields(Account, [(Account.NAME, ac.username), [Account.PASSWORD, ac.password]])
        j = database.verify_fields(Account, [(Account.NAME, ac.username), [Account.PASSWORD, aw.password]])
        if j:
            self.fail()
        self.assertTrue(i)

    def test_verify_id(self):
        i = database.get_id_by_name(Account, ac.username)
        j = database.verify_id(Account, 100000000)
        if j:
            self.fail()
        self.assertTrue(database.verify_id(Account, i))

    def test_verify_name(self):
        i = database.verify_name(Account, aw.username)
        if i:
            self.fail()
        self.assertTrue(database.verify_name(Account, ac.username))

    def test_get_all(self):
        database.get_all(Account)
        self.assertTrue(True)

    def test_get_field_by_name(self):
        a = database.get_field_by_name(Account, Account.PASSWORD, ac.username)
        b = database.get_field_by_name(Account, Account.PASSWORD, aw.username)
        try:
            database.get_field_by_name(Account, "Wrong Field", ac.username)
            self.fail()
        except Exception as e:
            pass
        if b is not None:
            self.fail()
        self.assertTrue(a == ac.password)

    def test_get_by_name(self):
        a: Account = database.get_by_name(Account, ac.username)
        b = database.get_by_name(Account, aw.username)
        if b is not None:
            self.fail()
        self.assertTrue(a.username == ac.username and a.password == ac.password and a.email == ac.email)

    def test_get_by_id(self):
        i = database.get_id_by_name(Account, ac.username)
        a: Account = database.get_by_id(Account, i)
        self.assertTrue(a.username == ac.username and a.password == ac.password and a.email == ac.email)

    def test_get_id_by_name(self):
        database.get_id_by_name(Account, ac.username)

    def test_get_max_id(self):
        database.get_max_id(Account)

    def test_get_all_by_account_id(self):
        i = database.get_id_by_name(Account, ac.username)
        a: list[Recording] = database.get_all_by_account_id(Recording, i)
        b: list[Recording] = database.get_all_by_account_id(Recording, 10000000)
        self.assertTrue(a[0].file_name == rc.file_name and len(b) == 0)

    def test_get_all_by_account_name(self):
        a: list[Recording] = database.get_all_by_account_name(Recording, ac.username)
        b: list[Recording] = database.get_all_by_account_name(Recording, aw.username)
        self.assertTrue(a[0].file_name == rc.file_name and len(b) == 0)

    def test_get_ids_by_account_id(self):
        a: list[int] = database.get_ids_by_account_id(Recording, iac)
        b: list[int] = database.get_ids_by_account_id(Recording, 10000000)
        ri = database.get_id_by_name(Recording, rc.file_name)
        self.assertTrue(a[0] == ri and len(b) == 0)

    def test_get_ids_by_account_name(self):
        a: list[int] = database.get_ids_by_account_name(Recording, ac.username)
        b: list[int] = database.get_ids_by_account_name(Recording, aw.username)
        ri = database.get_id_by_name(Recording, rc.file_name)
        self.assertTrue(a[0] == ri and len(b) == 0)

    def test_get_all_by_hardware_id(self):
        a: list[Recording] = database.get_all_by_hardware_id(Recording, ihc)
        b: list[Recording] = database.get_all_by_hardware_id(Recording, 100000)
        self.assertTrue(a[0].file_name == rc.file_name and len(b) == 0)

    def test_get_all_by_account_id_hardware_id(self):
        a: list[Recording] = database.get_all_by_account_id_hardware_id(Recording, iac, ihc)
        b: list[Recording] = database.get_all_by_account_id_hardware_id(Recording, 100000, 10000)
        self.assertTrue(a[0].file_name == rc.file_name and len(b) == 0)

    def test_get_by_type(self):
        c: Criteria = database.get_by_type(Criteria, cc.criteria_type)
        c2: Criteria = database.get_by_type(Criteria, cw.criteria_type)
        self.assertTrue(c.criteria_type == cc.criteria_type and c2 is None)

    def test_get_id_by_type(self):
        database.get_id_by_type(Criteria, cc.criteria_type)

    def test_get_saving_policy_ids_by_hardware_id(self):
        self.fail()

    def test_get_hardware_ids_by_saving_policy_id(self):
        self.fail()

    def test_get_notification_ids_by_hardware_id(self):
        self.fail()

    def test_get_hardware_ids_by_notification_id(self):
        self.fail()

    def test_get_all_by_join_id(self):
        self.fail()

    def test_update_fields(self):
        self.fail()

    def test_delete_by_field(self):
        self.fail()
