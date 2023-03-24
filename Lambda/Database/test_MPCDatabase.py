import mysql.connector

from Lambda.Database.MPCDatabase import MPCDatabase

database = MPCDatabase()


def test_connect():
    database = MPCDatabase()
    assert True


def test_query():
    try:
        database.query("Select * From Customer")
    except mysql.connector.Error as err:
        assert False
    assert True


def test_insert():
    assert False


def test_gen_select_script():
    assert False


def test_gen_insert_script():
    assert False





def test_insert_customer():
    database.insert_customer(Customer("Keita Nakashima", "12345"), True)
    assert True


def test_verify_customer_id():
    assert False


def test_get_customers():
    assert False


def test_get_customer_by_name():
    assert False


def test_get_customer_id_by_name():
    assert False


def test_insert_hardware():
    assert False


def test_verify_hardware_id():
    assert False


def test_get_hardwares():
    assert False


def test_get_hardwares_by_customer_name():
    assert False


def test_get_hardware_ids_by_customer_id():
    assert False


def test_insert_recording():
    assert False


def test_get_recordings():
    assert False


def test_get_recordings_by_customer_id():
    assert False


def test_get_recordings_by_customer_name():
    assert False



