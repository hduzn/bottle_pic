#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   app.py
@Time    :   2023/07/14
@Author  :   HDUZN
@Version :   1.0
@Contact :   hduzn@vip.qq.com
@License :   (C)Copyright 2023-2024
@Desc    :   1.批量压缩图片文件大小
             2.批量修改图片日期
             3.图片转pdf
             pip install bottle, pillow
'''

# here put the import lib
from bottle import Bottle, request, static_file, template, HTTPError
from PIL import Image
import os, zipfile, datetime, random, string, shutil

app = Bottle()

@app.route('/')
def index():
    return template('templates/index.html')

@app.route('/css/<filename:path>')
def send_css(filename):
    return static_file(filename, root='css')

@app.route('/js/<filename:path>')
def send_js(filename):
    return static_file(filename, root='js')

# @app.route('/ex_templates/<filename:path>')
# def send_xlsx(filename):
#     return static_file(filename, root='ex_templates')

@app.route('/favicon.ico')
def favicon():
    return static_file('favicon.ico', root='.')
   
# 1.压缩图片文件大小
@app.route('/func1')
def func():
    return template('templates/func1.html')

# 2.修改图片日期
@app.route('/func2')
def func2():
    return template('templates/func2.html')

# 3.图片转pdf
@app.route('/func3')
def func3():
    return template('templates/func3.html')

# 压缩图片文件大小
@app.route('/upload1', method='POST')
def upload1():
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    upload_files = request.files.getall('file[]')  # 获取上传的文件列表
    if upload_files:
        delete_files_in_dir(f'output') # 清空output目录
        user_id = generate_unique_name() # 创建唯一的用户id
        user_dir = f'uploads/{user_id}'
        os.makedirs(user_dir) # 创建用户目录

        with zipfile.ZipFile(f'{user_dir}/output_{user_id}.zip', 'w') as myzip:
            for upload_file in upload_files:
                # 判断文件是否为图片文件，后缀为jpg, png, bmp等
                if upload_file.raw_filename.split('.')[-1].lower() in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
                    # 如果是图片文件，按照选择的压缩比例，把图片进行压缩
                    compression_ratio = int(request.forms.get('compression')) / 100
                    img = Image.open(upload_file.file)
                    img = img.resize((int(img.size[0] * compression_ratio), int(img.size[1] * compression_ratio)))
                    temp_file_path = f'{user_dir}/{upload_file.raw_filename}'
                    img.save(temp_file_path)
                    myzip.write(temp_file_path, arcname=upload_file.raw_filename)
                    os.remove(temp_file_path)
        shutil.copy(f'{user_dir}/output_{user_id}.zip', f'output/output_{user_id}.zip') # 复制压缩包到output目录
        shutil.rmtree(user_dir) # 删除用户目录
        return static_file(f'output_{user_id}.zip', root='output', download=True)
    else:
        return HTTPError(400, 'No files uploaded')

# 修改图片日期
@app.route('/upload2', method='POST')
def upload2():
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    upload_files = request.files.getall('file[]')  # 获取上传的文件列表
    if upload_files:
        delete_files_in_dir(f'output') # 清空output目录
        user_id = generate_unique_name() # 创建唯一的用户id
        user_dir = f'uploads/{user_id}'
        os.makedirs(user_dir) # 创建用户目录

        with zipfile.ZipFile(f'{user_dir}/output_{user_id}.zip', 'w') as myzip:
            for upload_file in upload_files:
                # 判断文件是否为图片文件，后缀为jpg, png, bmp等
                if upload_file.raw_filename.split('.')[-1].lower() in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
                    # 如果是图片文件，修改图片的日期，并添加到压缩包后，删除原文件
                    # new_filename = os.path.join('output', os.path.basename(upload_file.raw_filename))  
                    # upload_file.save(new_filename)  
                    # image_date = request.forms.get('date')  # 获取选择的日期
                    # if image_date:
                    #     image_datetime_str = image_date + " 12:30:07"
                    #     image_datetime = datetime.datetime.strptime(image_datetime_str, '%Y-%m-%d').strftime('%Y:%m:%d %H:%M:%S')
                    #     # image_datetime = datetime.strptime(image_date, '%Y-%m-%d')  # 将日期转换为datetime格式  
                    #     os.utime(new_filename, (image_datetime.timestamp(), image_datetime.timestamp()))  # 修改文件的时间戳为选择的日期时间  
                    # myzip.write(new_filename, os.path.basename(new_filename))  # 将修改后的文件添加到压缩包中  
                    # os.remove(new_filename)  # 删除原文件
                    
                    # 修改日期通过复制文件实现
                    img = Image.open(upload_file.file)
                    # 创建新文件
                    new_file = f'uploads/{upload_file.raw_filename}'
                    # 保存图像为新文件
                    # img.save(new_file, optimize=False, quality=100) # 禁用压缩
                    img.save(new_file) 
                    myzip.write(new_file, arcname=upload_file.raw_filename)
                    os.remove(new_file)
        shutil.copy(f'{user_dir}/output_{user_id}.zip', f'output/output_{user_id}.zip') # 复制压缩包到output目录
        shutil.rmtree(user_dir) # 删除用户目录
        return static_file(f'output_{user_id}.zip', root='output', download=True)
    else:
        return HTTPError(400, 'No files uploaded')

# 图片转pdf
@app.route('/upload3', method='POST')
def upload3():
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    upload_files = request.files.getall('file[]')  # 获取上传的文件列表
    if upload_files:
        delete_files_in_dir(f'output') # 清空output目录
        user_id = generate_unique_name() # 创建唯一的用户id
        user_dir = f'uploads/{user_id}'
        os.makedirs(user_dir) # 创建用户目录
        # with zipfile.ZipFile(f'{user_dir}/output_{user_id}.zip', 'w') as myzip:
        img_list = []
        for upload_file in upload_files:
            # 判断文件是否为图片文件，后缀为jpg, png, bmp等
            if upload_file.raw_filename.split('.')[-1].lower() in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
                img_list.append(Image.open(upload_file.file))
        
        # 将所有图片文件合并到一个pdf文件中
        if img_list:
            pdf_file_path = f'{user_dir}/output_{user_id}.pdf'
            img_list[0].save(pdf_file_path, "PDF", resolution=100.0, save_all=True, append_images=img_list[1:])
            # myzip.write(pdf_file_path, arcname='output.pdf')

            shutil.copy(pdf_file_path, f'output/output_{user_id}.pdf') # 复制压缩包到output目录
            shutil.rmtree(user_dir) # 删除用户目录

    return static_file(f'output_{user_id}.pdf', root='output', download=True)

# 按时间生成唯一的名字
def generate_unique_name():
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S')

    letters = string.ascii_letters + string.digits
    random_digits = ''.join(random.choice(letters) for _ in range(4))
    return timestamp + random_digits

# 删除目录下的所有文件
def delete_files_in_dir(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9882') # 8080