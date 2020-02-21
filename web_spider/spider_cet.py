import requests as rt
import json
import re
import openpyxl as xl
import sys
from openpyxl.styles import colors,fonts

def query_grade(info):
    """
    通过输入学生信息返回学生具体英语成绩
    :param info: 学生信息列表，info[0]为15位准考证号，info[1]为学生姓名
    :return:学生具体成绩列表，grade[0]:总分；grade[1]:听力；grade[2]：阅读；grade[3]：写作与翻译；grade[4]:CET4(CET6)
    """
    # 定义一些查询所用的参数常量
    url_param = 'http://cet.neea.edu.cn/cet/js/data.js'
    header_param = {'Referer': 'http://cet.neea.edu.cn/cet/query_c.html',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/80.0.3987.116 Safari/537.36'
                    }
    param_param = {'v': '2'}
    url_query = 'http://cachecloud.neea.cn/cet/query'
    header_query = {'Host': 'cachecloud.neea.cn',
                    'Referer': 'http://cet.neea.edu.cn/cet/query_c.html',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/80.0.3987.116 Safari/537.36 '
                    }
    # 获取编码所用字符
    if info[0][9] == '1':
        code = 'CET4-D'
    else:
        code = 'CET6-D'
    r = rt.get(url_param, params=param_param, headers=header_param)
    text_param = ''
    if r.status_code == 200:
        pos1 = r.text.find('{')
        pos2 = len(r.text)
        text = r.text[pos1:pos2-2]
        dict_param = json.loads(text)
        for dic in dict_param['rdsub']:
            if dic['code'] == code:
                text_param = dic['tab']
    else:
        raise Exception('获取参数失败')
    # 查询成绩
    param_query = {'data': text_param + ','+info[0]+','+info[1]}
    r = rt.get(url_query, params=param_query, headers=header_query)
    if r.status_code == 200:
        list_query = re.split(r"[:',]", r.text)
        for text in list_query:
            if text == '':
                list_query.remove(text)
        grade = [[]]
        for index, text in enumerate(list_query):
            if text == 's':
                grade[0] = list_query[index+1]
            elif text == 'l':
                grade.append(list_query[index+1])
            elif text == 'r':
                grade.append(list_query[index+1])
            elif text == 'w':
                grade.append(list_query[index+1])
        grade.append(code[:4])
        return grade
    else:
        raise Exception('查询成绩错误')


def main():
    try:
        workbook = xl.load_workbook(sys.argv[1])
        sheet = workbook.active
        info_list = [[]]
        for row in sheet.values:
            info_list.append([row[5], row[1]])
        info_list = info_list[2:]
        for info in info_list:
            grade = query_grade(info)
            for result in grade:
                info.append(result)
        sheet['G1'] = '成绩总分'
        sheet['H1'] = '考试类别'
        sheet['I1'] = '听力'
        sheet['J1'] = '阅读'
        sheet['K1'] = '写作与翻译'
        for index, info in enumerate(info_list):
            sheet['G'+str(index+2)] = info[2]
            sheet['H'+str(index+2)] = info[6]
            sheet['I'+str(index+2)] = info[3]
            sheet['J'+str(index+2)] = info[4]
            sheet['K'+str(index+2)] = info[5]
            if float(info[2]) < 425:
                sheet['B'+str(index+2)].font = fonts.Font(color=colors.RED)
            elif float(info[2]) >= 550:
                sheet['B'+str(index+2)].font = fonts.Font(color=colors.BLUE)
        workbook.save(sys.argv[1])
        print('成绩打印成功！')
    except FileNotFoundError as e:
        print('文件路径有误！')


if __name__ == '__main__':
    main()