# -*- coding:utf-8 -*-
# pyllowo, 2021/6/1

from lxml import etree
from urllib.parse import quote

from hexi_online_spider_v001_mini.audio_tool import md5_use, str_similar, clear_text
from cartoon_search_unit.cartoon_spider_settings import CARTOON_CONF
from spider import CartoonSpider


class NormalCartoon(CartoonSpider):
    def __init__(self):
        super().__init__()
        self.admin = 'https://www.kukk.net'
        self.platform = '酷看漫画'  # 平台名
        self.page_size = 28  # 每页的个数
        # self.per_max = 2
        # self.per_max = self.page_size  # 只取20条
        self.turn_page = False  # 是否能翻页
        # self.max_page = None  # 翻页的最大页数
        # self.start_page = 1  # 开始页数

    # def request(self, url, method='POST', **kwargs):
    #     """
    #     params=None, data=None, headers=None, cookies=None, files=None,
    #     auth=None, timeout=None, allow_redirects=True, proxies=None,
    #     hooks=None, stream=None, verify=None, cert=None, json=None
    #     """
    #     return requests.request(method=method, url=url, headers=self.headers,data=data, proxies=self.proxies, **kwargs)

    def search_songs(self, keyword, **kwargs):
        # 页码开始页默认为1
        # 页码为1 步长为1时
        # page = self.page(**kwargs)
        # 页码为其他 步长为1时
        url = self.admin + '/search?keyword={}'
        # 默认添加了headers
        # 如需其他headers 传入self.search 中   # headers={xx}
        print(url.format(keyword))
        return self.search(url=url.format(keyword), **kwargs)

        # 解析函数重写

    def parse(self, response, **kwargs):
        response.encoding = 'utf-8'
        try:
            response_data = etree.HTML(response.text)
        except:
            return []
        else:
            result_list = []

            # qin_quaq_list_data = response_data.xpath('//div[@class="fusion-posts-container fusion-blog-layout-grid fusion-blog-layout-grid-4 isotope fusion-no-meta-info fusion-posts-container-infinite fusion-blog-rollover "]')
            # class中包含category-pg的
            qin_quaq_list_data = response_data.xpath('//*[@class="mh-list col7"]/li')
            for q_l in qin_quaq_list_data[:self.per_max]:
                # xpath_demo = ''.join(q_l.xpath(''))
                qin_quan_url_str = self.admin + ''.join(q_l.xpath('./div/a/@href'))  # 侵权链接
                print(qin_quan_url_str)
                # # >< 由于搜索中没有展示作者名， 所以去详情页找作者 顺便把详情也找到
                try:
                    # response_data = json.loads(response.text)
                    # 第二次请求  编码乱码问题
                    data1 = self.request(qin_quan_url_str)
                    data1.encoding = data1.apparent_encoding
                    qin_quan_info_data = etree.HTML(data1.text)
                    # qin_quan_info_data = etree.HTML(self.qin_quan_info(qin_quan_url_str).text)
                except:
                    continue
                #
                # qin_quan_info_temp = qin_quan_info_data.xpath('/html/body/div[1]/section/div[2]/div[2]/p[2]')[0]

                # qin_quan_info_temp = qin_quan_info_data.xpath("//div[@class='fade in']/text()")
                qin_quan_author_str = str(''.join(qin_quan_info_data.xpath('//*[@class="subtitle"][2]/text()'))).replace(
                    "作者：", "")  # 侵权作者
                # print(qin_quan_author_str)

                # if not qin_quan_author_str:
                #     continue
                qin_quan_title_str = ''.join(q_l.xpath('./div/a/@title'))  # 侵权标题
                # print(qin_quan_title_str)
                yangben_id = kwargs.get('id', '')

                qin_quan_dict = dict()
                qin_quan_dict['yang_ben_author_str'] = kwargs.get('yang_ben_author_str', '')  # 样本作者
                qin_quan_dict['yang_ben_title_str'] = kwargs.get('yang_ben_title_str', '')  # 样本标题
                qin_quan_dict['yang_ben_url_str'] = kwargs.get('yang_ben_url_str', '')  # 样本链接
                qin_quan_dict['yang_ben_id_int'] = kwargs.get('yang_ben_id_int', '')  # 样本ID 数值类型
                qin_quan_dict['yang_ben_mid_str'] = kwargs.get('yang_ben_mid_str', '')  # 样本ID 字符串形式
                qin_quan_dict['yang_ben_task_id_int'] = kwargs.get('yang_ben_task_id_int', '')  # 样本主任务ID
                qin_quan_dict['yang_ben_platform_str'] = kwargs.get('yang_ben_platform_str', '')  # 样本平台
                qin_quan_dict['yang_ben_batch_id_int'] = kwargs.get('yang_ben_batch_id_int', '')  # 样本批次ID
                qin_quan_dict['yang_ben_batch_id_int'] = kwargs.get('yang_ben_batch_id_int', '')  # 样本批次ID

                qin_quan_dict['search_key_words_str'] = kwargs.get('search_key_words_str', '')  # 搜索关键词
                qin_quan_dict['qin_quan_platform_str'] = self.platform  # 侵权平台
                qin_quan_dict['qin_quan_author_str'] = qin_quan_author_str  # 侵权作者
                qin_quan_dict['qin_quan_title_str'] = qin_quan_title_str.replace("\r", "").replace("\n", "").replace(
                    "\t", "")  # 侵权标题
                qin_quan_dict['qin_quan_url_str'] = qin_quan_url_str  # 侵权链接
                # qin_quan_dict['qin_quan_id_int'] = qin_quan_id_int  # 样本ID 数值类型
                # qin_quan_dict['qin_quan_mid_str'] = qin_quan_mid_str  # 侵权ID 字符串形式

                qin_quan_dict['qin_quan_url_hash_str'] = str(yangben_id) + '|' + md5_use(
                    qin_quan_url_str)  # 唯一索引，样本task_id 侵权url（md5）

                qin_quan_dict['similar_number_float'] = ''  # 作品相似度
                qin_quan_dict['title_similar_number_float'] = float(
                    str_similar(clear_text(kwargs.get('yang_ben_title_str', '')),
                                clear_text(qin_quan_title_str)))  # 标题相似度
                qin_quan_dict['author_similar_number_float'] = float(str_similar(
                    clear_text(kwargs.get('yang_ben_author_str', '')), clear_text(qin_quan_author_str)))  # 作者名称相似度
                qin_quan_dict['qin_quan_type_int'] = 7  # 侵权类型 4 （0 图文，1，视频，2音频）
                qin_quan_dict['qin_quan_platform_id_int'] = ''  # 默认空
                qin_quan_dict["qin_quan_flag_int"] = -1

                if qin_quan_dict["title_similar_number_float"] >= CARTOON_CONF["qin_quan_similar"] and qin_quan_dict[
                    "author_similar_number_float"] >= CARTOON_CONF["qin_quan_similar"]:
                    qin_quan_dict["qin_quan_flag_int"] = 1
                result_list.append(qin_quan_dict)
            return result_list


search_normals = NormalCartoon().search_songs

if __name__ == '__main__':
    kwags = {
        "id": 574979,
        "video_title": "班淑传奇",
        "video_url": "https://v.youku.com/v_show/id_XMTM3MjQ5NjEzMg==.html?spm=a2h0c.8166622.PhoneSokuProgram_1.dselectbutton_1&showid=f2103904e95911e4b2ad#班淑传奇第38集",
        "video_author": "",
        "video_album": "",
        "video_platform": "优酷1030测试电视剧一部4_55_1",
        "video_check_platform": "2",
        "sub_table_name": "sub_4_55",
        "task_type": 1,
        "page_num": 1,
        "search_key_words": "班淑传奇",
        # "confirm_key_words": "班淑传奇",
        # "filter_key_words_list": "片花_穿帮_片头曲_片尾曲_预告_插曲_翻唱_翻唱_发布会_演唱_演奏_合唱_专访_合奏_打call_宣传_原唱_cover_原曲_片花_穿帮_音乐_主题歌_有声小说_片头_片尾",
    }
    info = NormalCartoon().search_songs('我的', **kwags)
    print(info)
    print(len(info))
