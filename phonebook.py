from pprint import pprint
import re
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows) # список списков аттрибутов каждого контакта

contacts_dict = {} # создаем словарь для последующего объединения дублирующихся записей
for contact in contacts_list: # перебираем каждый контакт
    fio_contact = contact[0] # определяем содержимое первого поля lastname    
    parts_fio = fio_contact.split() # разбиваем содержимое первого поля, если в нем несколько слов

    io_contact = contact[1] # определяем содержимое второго поля firstname
    parts_io = io_contact.split() # разбиваем содержимое второго поля, если в нем несколько слов

    contact[0] = parts_fio[0]
    if len(parts_fio) == 3: # если в поле lastname Ф + И + О        
        contact[1] = parts_fio[1]
        contact[2] = parts_fio[2]        
    elif len(parts_fio) == 2: # если в поле lastname Ф + И       
        contact[1] = parts_fio[1]
    elif len(parts_fio) == 1: # если в поле lastname Ф
        contact[1] = parts_io[0]
        if len(parts_io) == 2: # если в поле firstname ИО
            contact[2] = parts_io[1]


    pattern = r'(\+7|8|7)?\s*\(?(\d{3,5})\)?[- ]?(\d{1,3})[- ]?(\d{2})[- ]?(\d{2})\s*\(?(доб?\)?\.)?\s?(\d{2,4})?\)?' # регулярное выражение (группировка) для отображения тлф номеров
    new_pattern = r'+7(\2)\3-\4-\5 \6\7' # новый формат отображения тлф номеров
    contact[5] = re.sub(pattern, new_pattern, contact[5]) # замена в тексте формата отображения тлф номеров с помощью регулярного выражения


    lastname = contact[0] # определяем ключ для словаря
    if lastname not in contacts_dict: # если нет в словаре
        contacts_dict[lastname] = contact # добавляем в словарь
    else: # если есть в словаре
        exist_contact = contacts_dict[lastname] # 
        for i in range(len(contact)): # перебираем все атрибуты контакта
            if contact[i] and not exist_contact[i]: # если атрибут есть, но его нет в словаре
                exist_contact[i] = contact[i] # добавляем атрибут в словарь

merged_contacts_list = list(contacts_dict.values()) # превращаем словарь в список

pprint(merged_contacts_list) # выводим новый список списков атрибутов каждого контакта


with open("phonebook_new.csv", "w", encoding='utf-8') as f: # сохраняем получившиеся данные в новый файл
    datawriter = csv.writer(f, delimiter=',')

    datawriter.writerows(merged_contacts_list)