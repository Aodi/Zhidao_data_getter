from lxml import etree
import requests
from urllib import parse

from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon

"""
ui说明：  

comboBox: 复选框
lineEdit: 输入关键字的输入框
Button1： 检索数据  按钮
Button2: 预览数据  按钮
Button3：获取数据  按钮  
Output:  输出窗口  # 设置文本：edit.setPlainText('''你好，白月黑羽 hello byhy''')
ClearButton：清除内容按钮

"""
HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Referer': 'https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word=%D1%F8%D6%B3+%B2%A1+%D3%E3+%CF%BA',
            'Cookie': 'BAIDUID=C390DB92EF88CFB106F1D057B3A2CCE9:FG=1; BIDUPSID=C390DB92EF88CFB106F1D057B3A2CCE9; PSTM=1539307711; BDUSS=5aY0h4SDdiOHZUZHpVeXZDRWwwaldzVnpnWWtmT0s4NXNoWTdsVWJnfkVZOEZjQVFBQUFBJCQAAAAAAAAAAAEAAAA7tE8MbGl1YW9kaQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMTWmVzE1plcVm; H_WISE_SIDS=114178; MCITY=-131%3A; H_PS_PSSID=1425_21122_29522_29519_29098_29567_29221_26350; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=1565265308,1565787543,1566264896,1566283192; Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=1566302478; ZD_ENTRY=empty; delPer=0; PSINO=2',
            'Connection': 'keep-alive'
        }

class Getdata:
    def __init__(self):
        self.ui = QUiLoader().load("PacApp.ui")

        self.ui.Button1.clicked.connect(self.dataNums)
        self.ui.Button2.clicked.connect(self.preview)
        self.ui.Button3.clicked.connect(self.getdata)
        self.ui.ClearButton.clicked.connect(self.clear)

    def search(self, page):
        # 检索数据
        keyword = self.ui.lineEdit.text()
        if keyword.strip() == '':
            self.print("未检测到输入，请输入关键词")
            return
        # app.exec_()
        # self.print("正在检索关键字“ " + keyword + " ”的数据...")
        url1 = "https://zhidao.baidu.com/search?"
        url2 = parse.urlencode({'word': keyword})
        url3 = '&pn={}'.format(page*10)
        url = url1 + url2 + url3

        response = requests.get(url, headers=HEADERS)
        text = response.content.decode('gbk')
        # print(text)
        html = etree.HTML(text)
        return html

    def dataNums(self):
        global PAGES
        # 检索关键词，查询出检索的数据数量
        keyword = self.ui.lineEdit.text()
        html = self.search(0)

        if keyword.strip() == '':
            return
        self.print("正在检索关键字“ " + keyword + " ”的数据...")
        try:
            pageNums = html.xpath("//div/a[@class='pager-last']/@href")[0].split("pn=")[1]
            PAGES = int(pageNums)
            # self.print("赋值这里的PAGES", PAGES)
            # self.print("赋值这里的PAGES{}".format(PAGES))

            # print(pageNums)
            self.print("已检索到百度知道数据{}多条".format(str(pageNums)))
            self.print('------------------------')
        except IndexError:
            pageNums = html.xpath("//div[@class='pager']/a/@href")[-2].split("pn=")[1]
            PAGES = int(pageNums)
            # self.print("赋值这里的PAGES{}".format(PAGES))
            self.print("已检索到百度知道数据{}多条".format(str(pageNums)))
            self.print('------------------------')
        except Exception as e:
            self.print('出现错误，错误信息：' + str(e) + '\n请检查是否先检索数据？')
            print(e)

    def preview(self):
        global PAGES
        # 检索信息，提取出前5条数据做展示
        self.print("正在获取预览前5条预览数据，请等待...")
        html = self.search(0)
        try:
            urls = html.xpath('//dt[@class="dt mb-4 line"]/a/@href')
            qas = {}
            no = 1 # 计数器
            for url in urls:
                # url = urls[0]
                # print(url)
                response = requests.get(url, headers=HEADERS)
                text = response.content.decode('gbk')
                # print(text)
                qa_html = etree.HTML(text)
                que = qa_html.xpath('//span[@class="ask-title"]/text()')
                if que == []:
                    continue
                que = que[0]
                ans = qa_html.xpath('//div[@class="best-text mb-10"]/p/text()')

                if ans == []:
                    ans = qa_html.xpath('//div[@class="best-text mb-10"]/text()')
                if ans == []:
                    ans = ['没有抓取到信息，请检查xpath语法。']
                else:
                    # 打印问题
                    ans = ''.join(ans)
                    self.print("问题" + str(no) + ':')
                    self.print(que)
                    self.print('----')
                    self.print('答案' + str(no) + ':')
                    self.print(ans)
                    self.print('-----------------')
                    # qas[que] = ans.strip()
                    self.print('\n')
                    no += 1
                    if no == 6:
                        break
        except Exception as e:
            self.print('出现错误，错误信息：' + str(e)+ '\n请检查是否先检索数据？')



    def getdata(self):
        # 获取数据
        global PAGES
        keyword = self.ui.lineEdit.text()
        if keyword.strip() == '':
            self.print("请输入关键词")
        self.print("正在获取数据，需要一段时间，请耐心等待...")

        for i in range((PAGES+10)//10):
            html = self.search(i*10)
            self.print("正在获取第{}页数据，请稍等，共{}页".format(str(i+1), str(PAGES//10)))

            try:
                urls = html.xpath('//dt[@class="dt mb-4 line"]/a/@href')
                qas = {}
                for url in urls:
                    QApplication.processEvents()
                    response = requests.get(url, headers=HEADERS)
                    text = response.content.decode('gbk')
                    qa_html = etree.HTML(text)
                    que = qa_html.xpath('//span[@class="ask-title"]/text()')
                    if que == []:
                        continue
                    que = que[0]
                    ans = qa_html.xpath('//div[@class="best-text mb-10"]/p/text()')

                    if ans == []:
                        ans = qa_html.xpath('//div[@class="best-text mb-10"]/text()')
                    if ans == []:
                        ans = ['没有抓取到信息，请检查xpath语法。']
                    else:
                        ans = ''.join(ans)
                        qas[que] = ans.strip()

                index = 1
                fp = open('.\\zhidaoda_{}.txt'.format(keyword), 'a', encoding='utf-8')
                for qa, an in qas.items():
                    fp.write(str(index))
                    index += 1
                    fp.write('\t')
                    fp.write(qa)
                    fp.write('\t')
                    fp.write(an)
                    fp.write('\n')
                fp.close()
            except Exception as e:
                self.print("获取数据出现错误,错误信息：" + str(e))


        self.print("文件获取完毕，写入文件成功。\n")


    def clear(self):
        self.ui.Output.clear()

    def print(self, line):
        self.ui.Output.appendPlainText(line)
        # 刷新窗口
        QApplication.processEvents()

if __name__ == '__main__':
    PAGES = 0
    app = QApplication([])
    app.setWindowIcon(QIcon('jbr.png'))
    getdata = Getdata()
    getdata.ui.show()
    app.exec_()
