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
            qin_quaq_list_data = response_data.xpath('//*[@class="video_list fn-clear"]/a')
            for q_l in qin_quaq_list_data:
                dic_info = {}
                qin_quan_url = "http://www.youkan5.com" + ''.join(q_l.xpath('./@href'))  # 侵权链接
                qin_quan_title = ''.join(q_l.xpath('./@title')).replace(' ', '')
                dic_info["qin_quan_url"] = qin_quan_url
                dic_info["qin_quan_title"] = qin_quan_title
                result_list.append(dic_info)
            return result_list


detail_url = BaseCartoon(use_proxy=False).detail_url

if __name__ == '__main__':
    info = detail_url(url="http://www.youkan5.com/8/")
    print(len(info))
    print(info)
