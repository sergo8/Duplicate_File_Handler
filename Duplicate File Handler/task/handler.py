import os
import sys
import hashlib


class DuplicateFileHandler:
    def __init__(self):
        self.args = sys.argv  # get a list of arguments

    def prepare(self):
        try:
            path = self.args[1]
            file_extension = input('Enter file format:\n')

            options = {1: 'Descending', 2: 'Ascending'}
            print('Size sorting options:', '1. Descending', '2. Ascending', sep='\n')

            while True:
                option = int(input('Enter a sorting option:\n'))
                if option == 1:
                    reverse_order = True
                elif option == 2:
                    reverse_order = False
                else:
                    print('\nWrong option\n')
                    continue

                storage_dict = {}

                if option in options.keys():
                    for root, dirs, files in os.walk(path, topdown=False):
                        for name in files:
                            file_path = os.path.join(root, name)

                            if file_path.endswith(file_extension):
                                if os.path.getsize(file_path) not in storage_dict.keys():
                                    storage_dict.update({os.path.getsize(file_path): [file_path]})
                                else:
                                    storage_dict.get(os.path.getsize(file_path)).append(file_path)

                    sorted_dict = self.execute(storage_dict, reverse_order)
                    result_dict = self.check_duplicates(sorted_dict)
                    self.delete_file(result_dict)
                    break

        except IndexError:
            print('Directory is not specified')

    @staticmethod
    def execute(storage_dict_funct, reverse_order_funct):
        storage_dict_funct = {k: v for k, v in sorted(storage_dict_funct.items(), key=lambda item: item[0],
                                                      reverse=reverse_order_funct)}

        for item in storage_dict_funct.items():
            if len(item[-1]) > 1:
                print(f'\n{item[0]} bytes')
                for file in item[-1]:
                    print(file)
        return storage_dict_funct

    def check_duplicates(self, files_dictionary):
        while True:
            check = input('\nCheck for duplicates?\n')

            if check == 'yes' and files_dictionary:

                result_dict = {}
                for size, files_list in files_dictionary.items():
                    path_list = []
                    hash_list = []
                    for path in files_list:
                        with open(path, 'r') as file:
                            string = file.read()
                            string = string.encode()
                            m = hashlib.md5()
                            m.update(string)
                            path_list.append(path)
                            hash_list.append(m.hexdigest())

                    for path, hash_num in zip(path_list, hash_list):
                        if hash_list.count(hash_num) > 1 and size not in result_dict.keys():
                            result_dict.update({size: {hash_num: [path]}})
                        elif hash_list.count(hash_num) > 1 and hash_num in result_dict.get(size).keys():
                            result_dict.get(size).get(hash_num).append(path)
                        elif hash_list.count(hash_num) > 1 and size in result_dict.keys() and hash_num not in result_dict.get(size).keys():
                            result_dict.get(size).update({hash_num: [path]})

                if result_dict:
                    num = 1
                    for key, value in result_dict.items():
                        print(f'\n{key} bytes')
                        for hash_num, files in value.items():
                            print(f'Hash: {hash_num}')
                            for file in files:
                                print(f'{num}. {file}')
                                num += 1
                else:
                    print('\nNo duplicates\n')

                list_of_files = [k for i in result_dict.values() for j in i.values() for k in j]
                dict_of_files = {n: path for n, path in enumerate(list_of_files, 1)}

                return dict_of_files

            elif check == 'no':
                break
            else:
                continue

    def delete_file(self, dict_of_files):

        while True:
            delete = input('\nDelete files?\n')
            if delete == 'yes':

                while True:
                    flag = False
                    files_to_delete = input('\nEnter file numbers to delete:\n').split()

                    if len(files_to_delete) == 0 or not ''.join(files_to_delete).isdigit():
                        print('Wrong format')
                        continue

                    files_to_delete = [int(n) for n in files_to_delete]
                    list_file_num = [num for num in dict_of_files.keys()]

                    print(files_to_delete)
                    print(list_file_num)

                    for item in files_to_delete:
                        print(item)
                        if item in list_file_num:
                            flag = True
                            continue
                        else:
                            print('\nWrong format\n')
                            break

                    if flag:
                        file_names_to_delete = [name for n, name in dict_of_files.items() if n in files_to_delete]

                        size_of_files = []
                        for filename in file_names_to_delete:
                            size_of_files.append(os.path.getsize(filename))
                            os.remove(filename)

                        print(f'\nTotal freed up space: {sum(size_of_files)} bytes\n')
                        break
                break
            elif delete == 'no':
                break
            else:
                print('\nWrong option\n')


if __name__ == "__main__":
    duplicate_file_handler = DuplicateFileHandler()
    duplicate_file_handler.prepare()