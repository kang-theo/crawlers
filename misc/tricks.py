# 1. key-value revert in a dictionary
my_dict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

reversed_dict = dict(map(reversed, my_dict.items()))
print(reversed_dict)
# output:
# {'Ford': 'brand', 'Mustang': 'model', 1964: 'year'}

# 2. sort a dictionary list
dicts_lists = [
    {
      "Name": "James",
      "Age": 20
    },{
      "Name": "May",
      "Age": 14
    },{
      "Name": "Katy",
      "Age": 23
    }
]

dicts_lists.sort(key=lambda item: item.get("Age"))
print(dicts_lists)

# 3. merge two lists into a dictionary
key_list = ['A', 'B', 'C']
value_list = ["blue", "red", "bold"]

dict_ = dict(zip(key_list, value_list))
print(dict_)

# 4. sort a list according another list
a = ["blue", "green", "orange", "purple", "yellow"]
b = [3,2,5,4,1]

zip_ab = zip(b, a) # return an iterator
# print(list(zip_ab)) #  converted to a list using the list() constructor
# print(list(zip_ab)[0][0]) # use list to show the results in zip_ab

# sort according to x[0]
sorted_zip_ab = sorted(zip(b, a), key=lambda x: x[0])
# print(sorted_zip_ab)

sorted_list = [val for (_, val) in sorted_zip_ab]
print(sorted_list)

# 5. sort a list of string
str_list = ["blue", "red", "green", "purple", "yellow"]
# a. by alphabetical order
str_list.sort()
print (str_list)

# b. by length of string
# str_list.sort(key=len)
# print(str_list)
# or, this will not modify the original list
sorted_str_list = sorted(str_list, key=len)
print(sorted_str_list)

# 6. check the existence of a file
import os

# a. if file exists
if_file_exist = os.path.isfile('./http2.py')
print(if_file_exist)

# b. if directory exists
if_folder_exist = os.path.isdir('../misc')
# if_folder_exist = os.path.exists('../misc')
print(if_folder_exist)