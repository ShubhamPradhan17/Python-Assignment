import pytest
from ParkingLot import ParkingLot
from Vehicle import Car

@pytest.fixture
def parking_lot():
    pl = ParkingLot()
    pl.create_parking_lot(3)
    return pl

def test_create_parking_lot(parking_lot):
    assert parking_lot.capacity == 3

def test_park_success(parking_lot):
    slot = parking_lot.park("KA-01-HH-1234", "White")
    assert slot == 1
    assert parking_lot.occupied_slot == 1

def test_park_full_lot(parking_lot):
    parking_lot.park("KA-01-HH-1234", "White")
    parking_lot.park("KA-01-HH-9999", "Black")
    parking_lot.park("KA-01-HH-7777", "Red")
    slot = parking_lot.park("KA-01-HH-8888", "Blue")
    assert slot == -1 

def test_leave_slot_success(parking_lot):
    parking_lot.park("KA-01-HH-1234", "White")
    status = parking_lot.leave_slot(1)
    assert status is True
    assert parking_lot.occupied_slot == 0 

def test_leave_invalid_slot(parking_lot):
    parking_lot.park("KA-01-HH-1234", "White")
    status = parking_lot.leave_slot(2)  
    assert status is False

def test_get_regno_from_color(parking_lot):
    parking_lot.park("KA-01-HH-1234", "White")
    parking_lot.park("KA-01-HH-9999", "Black")
    regnos = parking_lot.get_regno_from_color("White")
    assert regnos == ["KA-01-HH-1234"]

def test_get_slotno_from_regno(parking_lot):
    parking_lot.park("KA-01-HH-1234", "White")
    slot_no = parking_lot.get_slotno_from_regno("KA-01-HH-1234")
    assert slot_no == 1

def test_get_slotno_from_color(parking_lot):
    parking_lot.park("KA-01-HH-1234", "White")
    parking_lot.park("KA-01-HH-9999", "White")
    slotnos = parking_lot.get_slotno_from_color("White")
    assert slotnos == ["1", "2"]

def test_status_check(parking_lot, capsys):
    parking_lot.park("KA-01-HH-1234", "White")
    parking_lot.check_status()
    captured = capsys.readouterr()
    assert "1\tKA-01-HH-1234\tWhite" in captured.out

