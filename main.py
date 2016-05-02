import requests
import bs4
import xlsxwriter

#通过网络页面页数获取Url

def GetUrls(PageNum):
    suffix = "&page=" + str(PageNum)
    url = root_url + suffix
    return(url)


def GetData(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    data = soup.select('li.li a[title]')
    return data

root_url = "http://cdm.ccchina.gov.cn/sdxm.aspx?clmId=163" #自愿减排项目公示网址首页
frontpage = requests.get(root_url)
front_soup = bs4.BeautifulSoup(frontpage.text, "html.parser")
data = front_soup.select('div.pages_bg a')
strings = [a.attrs.get('href') for a in data if a.string == "»" ]
strings[0]=strings[0].replace("sdxm.aspx?clmId=163&page=","")
PageNum = int(strings[0])
print("目前最大页数为：",PageNum)                           #目前最多的页数，自动获取

Project_Names = []      #项目名称
Project_pub_times = []  #项目公示时间


for page in range(0,PageNum):                                #每页进行数据抓取
    print("正在读取第%d页"%page)
    CurrentPageUrl = GetUrls(page)
    CurrentData = GetData(CurrentPageUrl)
    Project_Names.extend([a.string for a in CurrentData])
    Project_pub_times.extend([a.attrs.get('title') for a in CurrentData])
print("共读取%d条记录"%len(Project_Names))

workbook = xlsxwriter.Workbook('CCERInfo.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1','项目名称')
worksheet.write('B1','公示时间')

#写入数据
worksheet.write_column('A2',Project_Names)
worksheet.write_column('B2',Project_pub_times)
workbook.close()
