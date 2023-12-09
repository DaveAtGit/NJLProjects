from django.test import TestCase

# Create your tests here.
# ------- not for using: examples, tests..


#   called from: view.downloader
def test_func():
    """

    """
    pass


#   example..
def outer_func(list1_var):
    def inner_func(list2_var):
        for value in list2_var:
            print(value)
        return list2_var
    a_list = inner_func(list1_var)
    return a_list


#   example..
def get_all_values(nested_dictionary):
    """
    This recursive function gives back all key/values from a nested dictionary
    """
    for key, value in nested_dictionary.items():
        if type(value) is dict:
            get_all_values(value)
        else:
            print(key, ":", value)

