# 百度知道数据，搜索关键词获取数据
# -*- coding:utf-8 -*-

from lxml import etree
import requests

PART_URL = 'https://zhidao.baidu.com/search?word=%D1%F8%D6%B3+%B2%A1+%D3%E3+%CF%BA&ie=gbk&site=-1&sites=0&date=0&pn={}'
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Referer': 'https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word=%D1%F8%D6%B3+%B2%A1+%D3%E3+%CF%BA',
    'Cookie': 'BAIDUID=C390DB92EF88CFB106F1D057B3A2CCE9:FG=1; BIDUPSID=C390DB92EF88CFB106F1D057B3A2CCE9; PSTM=1539307711; BDUSS=5aY0h4SDdiOHZUZHpVeXZDRWwwaldzVnpnWWtmT0s4NXNoWTdsVWJnfkVZOEZjQVFBQUFBJCQAAAAAAAAAAAEAAAA7tE8MbGl1YW9kaQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMTWmVzE1plcVm; H_WISE_SIDS=114178; MCITY=-131%3A; H_PS_PSSID=1425_21122_29522_29519_29098_29567_29221_26350; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=1565265308,1565787543,1566264896,1566283192; Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=1566302478; ZD_ENTRY=empty; delPer=0; PSINO=2',
    'Connection': 'keep-alive'

}

def get_urls():
    response = requests.get(BASE_URL, headers=HEADERS)
    text = response.content.decode('gbk')
    # print(text)

    html = etree.HTML(text)
    urls = html.xpath('//dt[@class="dt mb-4 line"]/a/@href')
    # print(urls)
    return urls

def get_qa(urls):
    qas = {}
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
            ans = ''.join(ans)
            qas[que] = ans.strip()
    return qas

def writeFile(qas,index):
    fp = open('.\\zhidao_data\\zhidao_qa_part2.txt', 'a', encoding='utf-8')
    for qa,an in qas.items():
        fp.write(str(index))
        index += 1
        fp.write('\t')
        fp.write(qa)
        fp.write('\t')
        fp.write(an)
        # fp.write('='*80)
        fp.write('\n')
    fp.close()
    return index


if __name__ == "__main__":
    index = 1
    for x in range(0,75):
        BASE_URL = PART_URL.format(10*x)    #搜索页的页码控制
        # print(BASE_URL)
        # continue
        urls = get_urls()
        qas = get_qa(urls)
        index = writeFile(qas,index)
        print('****抓取第 %s / 75 页成功****' % (x+1))