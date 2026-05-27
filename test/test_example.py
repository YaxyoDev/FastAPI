# import pytest

# def test_equal_or_not_equal():
#     assert 3 == 3
#     assert 3 != 5
    
# def test_is_instance():
#     assert isinstance('hello world', str)
#     assert not isinstance('433', int)

# def test_boolean():
#     is_vip = True
#     assert is_vip is True
#     assert ('hello' == 'world') is False
    
# def test_type():
#     assert type('hello' is str)
#     assert type('world' is not int)
    
# def test_kottami_kichikmi():
#     assert 7 > 3
#     assert 4 < 10
    
# def test_list():
#     num_list = [1, 2, 3, 4, 5]
#     any_list = [False, False]
#     assert 1 in num_list
#     assert 7 not in any_list
    
#     assert all(num_list)
#     assert not any(any_list)
    
# # ===============================================

# class Student:
#     def __init__(self, first_name: str, last_name: str, major: str, years: int):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.major = major
#         self.years = years

# @pytest.fixture
# def default_employee():
#     return Student("Alex", "Smith", "Math", 4) 

# def test_person_init(default_employee):
#     assert default_employee.first_name == "Alex"
#     assert default_employee.last_name == "Smith"
#     assert default_employee.major == "Math"
#     assert default_employee.years == 4
    
        
