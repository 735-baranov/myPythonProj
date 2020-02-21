import shutil
import os

path = 'X:\\python_base'

list_names = os.listdir(path)
roots = []
for name in list_names:
    roots.append(path+'\\'+name)
# print(roots)

needed_symb = 1000
t_dirs = []
for t_path in roots:
    for root, dirs, files in os.walk(t_path):
        for d in dirs:
            t_dirs.append(os.path.join(root, d))

        for f in files:
            file = t_path + '\\' + os.path.relpath(os.path.join(root, f), t_path)
            
            n_symb = os.path.getsize(file)
            file_extension = os.path.splitext(f)[1]

            if file_extension == '.py' and n_symb >= needed_symb:
                # copy_path = path.split('\\')
                # #
                # type_path = ''
                # for i in range(0, len(copy_path)-1):
                #     type_path += copy_path[i]

                try:
                    file = t_path+'\\'+os.path.relpath(os.path.join(root, f), t_path)
                    shutil.move(file, t_path+'\\')
                except:
                    continue
            else:

                file = t_path + '\\' + os.path.relpath(os.path.join(root, f), t_path)
                os.chmod(file, 0o777)
                # print(os.access(path, os.W_OK))
                os.remove(file)

for d in t_dirs:
    try:
        shutil.rmtree(d)
    except:
        continue

for t_path in roots:
    list = os.listdir(t_path)
    if len(list) == 0:
        shutil.rmtree(t_path)