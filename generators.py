import os
import numpy as np
import nbformat as nbf
import mdutils


def ktx_to_dict(input_file, keystarter = '<'):
    """ 
        parsing keyed text to a python dictionary. 
        把ktx数据从文件当中读出来，换成字典形式
    """
    answer = dict() # 字典

    with open(input_file, 'r+', encoding = 'utf-8') as f:
        lines = f.readlines() #按行读出

    k, val = '', ''
    for line in lines:
        if line.startswith(keystarter): # 对于每个新的key值
            k = line.replace(keystarter, '').strip() # 将key的箭头换掉
            val = '' #value值清空重新开始读入 
        else:
            val += line  # 增加当前value内容

        if k: # 每次更新一下当前键值对信息
            answer.update({k: val.strip()})

    return answer

def dict_to_ktx(input_dict, output_file, keystarter = '<'):
    """ 
        Store a python dictionary to a keyed text
        逆向操作，把字典存储为ktx文件
        直接写文件
    """
    with open(output_file, 'w+') as f:
        for k, val in input_dict.items():
            f.write(f'{keystarter} {k}\n')
            f.write(f'{val}\n\n')
    return

HEADERS = ktx_to_dict(os.path.join('source', 'headers.ktx'))
QHA = ktx_to_dict(os.path.join('source', 'exercises100.ktx'))

'''
    ---------------------
    以上是预设模块直接运行
    以下是提供支持的模块
    ---------------------
'''


def create_jupyter_notebook(destination_filename = '100_Numpy_exercises.ipynb', answer_type = 0):
    """ 
        Programmatically create jupyter notebook with the questions
        saved under source files 
        参数化生成Notebook
        在同文件夹下方生成
    """

    # Create cells sequence 
    # notebook的 cell序列
    nb = nbf.v4.new_notebook()

    nb['cells'] = []

    # - Add header:
    nb['cells'].append(nbf.v4.new_markdown_cell(HEADERS["header"]))
    nb['cells'].append(nbf.v4.new_markdown_cell(HEADERS["sub_header"]))
    nb['cells'].append(nbf.v4.new_markdown_cell(HEADERS["jupyter_instruction"]))

    nb['cells'].append(nbf.v4.new_code_cell('import generators as ge'))

    # - 增加问题MD块, 提示代码块，作业代码块，答案代码块
    for n in range(1, 101):
        nb['cells'].append(nbf.v4.new_markdown_cell(f'### {n}. ' + QHA[f'q{n}']))
        nb['cells'].append(nbf.v4.new_code_cell(f'ge.hint({n})'))
        nb['cells'].append(nbf.v4.new_code_cell(''))
        if answer_type == 0:
            nb['cells'].append(nbf.v4.new_code_cell(f'ge.answer({n})'))
        else:
            nb['cells'].append(nbf.v4.new_code_cell(QHA[f'a{n}']))

    # Delete file if one with the same name is found
    # 删除同名文件
    if os.path.exists(destination_filename):
        os.remove(destination_filename)

    # Write sequence to file
    # 写入序列
    nbf.write(nb, destination_filename)
    return

'''
    以下是随机生成问题模块
'''

def question(n = 1): # 生成问题
    print(f'{n}. ' + QHA[f'q{n}'])
    return

def hint(n = 1): # 生成提示
    print(QHA[f'h{n}'])
    return

def answer(n = 1): # 生成答案
    print(QHA[f'a{n}'])
    return

def pick(): # 随机生成
    id = np.random.randint(1, 100)
    question(id)
    return id

# def create_markdown(destination_filename = '100_Numpy_exercises', with_hints = False, with_solutions = False):
#     '''
#         生成MarkDown版本的内容
#         没有做什么改动，代码非常直观
#     '''
#     if with_hints:
#         destination_filename += '_with_hints'
#     if with_solutions:
#         destination_filename += '_with_solutions'

#     # Initialise file
#     mdfile = mdutils.MdUtils(file_name = destination_filename)

#     # Add headers
#     mdfile.write(HEADERS["header"] + '\n')
#     mdfile.write(HEADERS["sub_header"] + '\n')

#     # Add questions (and hint or answers if required)
#     for n in range(1, 101):
#         mdfile.new_header(title = f"{n}. {QHA[f'q{n}']}", level = 4)
#         if with_hints:
#             mdfile.write(f"`{QHA[f'h{n}']}`")
#         if with_solutions:
#             mdfile.insert_code(QHA[f'a{n}'], language = 'python')

#     # Delete file if one with the same name is found
#     if os.path.exists(destination_filename):
#         os.remove(destination_filename)

#     # Write sequence to file
#     mdfile.create_md_file()
#     return

# def create_rst(destination_filename, with_ints = False, with_answers = False):
#     # TODO: use rstdoc python library.
#     #  also see possible integrations with https://github.com/rougier/numpy-100/pull/38
#     pass
