from flask import Blueprint, request, jsonify
import requests, xmltodict
from xml.etree import ElementTree

pill_bp = Blueprint('pill', __name__, url_prefix='/pill')

API_URL = 'http://apis.data.go.kr/1470000/MdcinGrnIdntfcInfoService/getMdcinGrnIdntfcInfoList'
API_TOKEN = '5MkwNOpsxG7bTvpEyKpaRAAqMLgXZ82LYeMkaUQMZ62aipvWuS92MaQO%2FdyT9qdFcK0ySiGOIWAsd57tDveaUg%3D%3D'

API_REQUEST_URL = '%s?ServiceKey=%s' % (API_URL, API_TOKEN)

@pill_bp.route('/find', methods=['GET'])
def get_pills():
    name = request.args.get('name')

    url = '%s&item_name=%s&numOfRows=10&pageNo=1' % (API_REQUEST_URL, name)
    response_text = requests.get(url).text

    xml_root = ElementTree.fromstring(response_text)

    response_data = []

    result_code = xml_root.find('header').find('resultCode').text
    if result_code != '00':
        result_msg = xml_root.find('header').find('resultMsg').text
        return result_msg, 503

    items = xml_root.find('body').find('items').findall('item')
    for item in items:
        response_data.append({
            "item_id": item.findtext('ITEM_SEQ'),
            "item_name": item.findtext('ITEM_NAME'),
            "entp_id": item.findtext('ENTP_SEQ'),
            "entp_name": item.findtext('ENTP_NAME')
        })
        
    return jsonify(response_data)