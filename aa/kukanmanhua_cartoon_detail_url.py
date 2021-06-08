from lxml import etree

from detail_app_mini import audio_tool

# 基础的类
from detail_app_mini.audio_tool import BaseSpider


class BaseCartoon(BaseSpider):

    def parse_search_qin_quan(self, response, **kwargs) -> list:
        try:
            # print(response.text)
            # response_data = json.loads(response.text)
            response.encoding = response.apparent_encoding
            response_data = etree.HTML(response.text)
        except:
            return []
        else:
            # *
            result_list = []
            qin_quaq_list_data = response_data.xpath('//*[@id="detail-list-select"]/li')
            for q_l in qin_quaq_list_data:
                dic_info = {}
                qin_quan_url = "https://www.kukk.net" + ''.join(q_l.xpath('./a/@href'))  
                qin_quan_title = ''.join(q_l.xpath('./a/text()')).replace(' ', '')
                dic_info["qin_quan_url"] = qin_quan_url
                dic_info["qin_quan_title"] = qin_quan_title
                result_list.append(dic_info)
            return result_list


detail_url = BaseCartoon(use_proxy=False).detail_url

if __name__ == '__main__':
    info = detail_url(url="https://www.kukk.net/book/516")
    print(len(info))
    print(info)
