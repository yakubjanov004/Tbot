data = [('Myusername871', "Ulug'bek", None), ('yakubjanov_004', "Ulug'bek", None),('yakubjanov_004', "Ulug'bek", None),('Myusername871', "Ulug'bek", None),('Myusername871', "Ulug'bek", None),('Myusername871', "Ulug'bek", None),('Myusername871', "Ulug'bek", None)]
unique_values = set()
my_list = []
text = ""
for item in data:
    unique_values.add(item)
    for value in unique_values:
        for i in value:
            my_list.append(i)   
        text += f"Username @{my_list[0]}, First name {my_list[1]}, Last name {my_list[2]}\n"
        my_list.clear()
print(text)


    
