from xml.etree import ElementTree
import json
import requests

token= '5MkwNOpsxG7bTvpEyKpaRAAqMLgXZ82LYeMkaUQMZ62aipvWuS92MaQO%2FdyT9qdFcK0ySiGOIWAsd57tDveaUg%3D%3D'
url = 'http://apis.data.go.kr/1470000/MdcinGrnIdntfcInfoService/getMdcinGrnIdntfcInfoList?ServiceKey=%s&item_name=&entp_name=&numOfRows=100&pageNo=%d'

response_data = []

for page in range(1, 203):
    print("[crawler] working in %s page" % (page))
    xml_root = ElementTree.fromstring(
        requests.get(url % (token, page)).text
    )

    result_code = xml_root.find('header').find('resultCode').text
    if result_code != '00':
        continue

    items = xml_root.find('body').find('items').findall('item')
    for item in items:
        response_data.append({
            'item_id': item.findtext('ITEM_SEQ'),
            'item_name': item.findtext('ITEM_NAME'),
            'item_eng_name': item.findtext('ITEM_ENG_NAME'),
            'entp_id': item.findtext('ENTP_SEQ'),
            'entp_name': item.findtext('ENTP_NAME'),
            'chart': item.findtext('CHART'),
            'image': item.findtext('ITEM_IMAGE'),
            'class': item.findtext('CLASS_NAME'),
            'otc_name': item.findtext('ETC_OTC_NAME')
        })

with open("./result.json", "w") as file:
    file.write(json.dumps(response_data, ensure_ascii=False))
