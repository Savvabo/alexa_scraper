import requests
from parsel import Selector
import mongodb_storage


WEBSITE = "google.com"
url = "https://www.alexa.com/siteinfo/{}".format(WEBSITE)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0'
}


def get_selector():
    response = requests.request("GET", url, headers=HEADERS)
    content = response.text
    selector = Selector(text=content)
    return selector


def get_site_rank(selector: Selector):
    site_rank = selector.xpath('//*[@class="rankmini-global"]/div/text()').getall()[1].split()[0]
    return int(site_rank)



def get_site_time(selector: Selector):
    site_time = selector.xpath('//*[@class="rankmini-daily"]/div/text()').get().split()[0]
    return site_time


def get_keywords_traffic(selector: Selector):
    keywords_traffic = dict()
    rows = selector.xpath('//*[@id="card_mini_topkw"]//div[@class="Row"]')
    for row in rows:
        keyword = row.xpath('.//span/text()')[0].get()
        percent = row.xpath('.//span/text()')[1].get()
        percent = float(percent.strip('%'))
        keywords_traffic[keyword] = percent
    return keywords_traffic


def get_traffic_sources(selector: Selector):
    values_selector = selector.xpath('//*[@class="FolderTarget"]/div[1]/div/div[2]/span/text()').getall()
    sources_keys = selector.xpath('//*[@class="FolderTarget"]//*[@class="Third"]/@title').getall()
    sources_values = [float(value.split()[0].strip('%')) for value in values_selector]
    sources_dict = dict(zip(sources_keys, sources_values))
    return sources_dict


def get_total_site_linking_in(selector: Selector):
    total_site_linking_in = selector.xpath('//*[@class="enun"]/span[1]/text()').get()
    return total_site_linking_in


def get_alexa_data():
    selector = get_selector()
    alexa_data = dict()
    alexa_data['site_rank'] = get_site_rank(selector)
    alexa_data['site_time'] = get_site_time(selector)
    alexa_data['keywords_traffic'] = get_keywords_traffic(selector)
    alexa_data['traffic_sources'] = get_traffic_sources(selector)
    alexa_data['total_site_linking_in'] = get_total_site_linking_in(selector)
    return alexa_data


def run():
    alexa_data = get_alexa_data()
    mongo_instance = mongodb_storage.MongoDBStorage()
    mongo_instance.run(alexa_data, WEBSITE)


if __name__ == '__main__':
    run()
