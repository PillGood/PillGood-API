from flask import Blueprint, request, jsonify
import requests, xmltodict
from xml.etree import ElementTree

pill_bp = Blueprint('pill', __name__, url_prefix='/pill')


API_URL = 'http://apis.data.go.kr/1470000/MdcinGrnIdntfcInfoService/getMdcinGrnIdntfcInfoList'
API_TOKEN = '5MkwNOpsxG7bTvpEyKpaRAAqMLgXZ82LYeMkaUQMZ62aipvWuS92MaQO%2FdyT9qdFcK0ySiGOIWAsd57tDveaUg%3D%3D'

API_REQUEST_URL = '%s?ServiceKey=%s' % (API_URL, API_TOKEN)


def search_open_api(item_name, entp_name=''):
    url = API_REQUEST_URL + '&item_name=%s&entp_name=%s&numOfRows=10&pageNo=1' % (item_name, entp_name)
    response_text = requests.get(url).text

    return response_text


@pill_bp.route('/info', methods=['GET'])
def get_pill_info():
    item_id = request.args.get('item_id')
    item_name = request.args.get('item_name')
    entp_name = request.args.get('entp_name')

    if not item_id or not item_name or not entp_name:
        return jsonify({ 'code': 'error', 'message': 'wrong query string' }), 400

    xml_root = ElementTree.fromstring(
        search_open_api(item_name, entp_name)
    )

    # open api error handling
    result_code = xml_root.find('header').find('resultCode').text
    if result_code != '00':
        result_msg = xml_root.find('header').find('resultMsg').text
        return jsonify({ 'code': 'error', 'message': result_msg }), 503

    # find equal item
    items = xml_root.find('body').find('items').findall('item')
    filtered_item = list(filter(lambda l: l.findtext('ITEM_SEQ') == item_id, items))

    if len(filtered_item) == 0:
        return jsonify({})

    item = filtered_item[0]
    return jsonify({
        'code': 'success',
        'data': {
            'item_id': item.findtext('ITEM_SEQ'),
            'item_name': item.findtext('ITEM_NAME'),
            'item_eng_name': item.findtext('ITEM_ENG_NAME'),
            'entp_id': item.findtext('ENTP_SEQ'),
            'entp_name': item.findtext('ENTP_NAME'),
            'chart': item.findtext('CHART'),
            'image': item.findtext('ITEM_IMAGE'),
            'class': item.findtext('CLASS_NAME'),
            'otc_name': item.findtext('ETC_OTC_NAME')
        }
    })


@pill_bp.route('/find', methods=['GET'])
def find_pills():
    item_name = request.args.get('item_name')
    if not item_name:
        return jsonify({ 'code': 'error', 'message': 'wrong parameter' }), 503

    xml_root = ElementTree.fromstring(
        search_open_api(item_name)
    )

    response_data = []

    # open api error handling
    result_code = xml_root.find('header').find('resultCode').text
    if result_code != '00':
        result_msg = xml_root.find('header').find('resultMsg').text
        return jsonify({ 'code': 'error', 'message': result_msg }), 503

    # parsing response data (xml format)
    items = xml_root.find('body').find('items').findall('item')
    for item in items:
        response_data.append({
            "item_id": item.findtext('ITEM_SEQ'),
            "item_name": item.findtext('ITEM_NAME'),
            "entp_id": item.findtext('ENTP_SEQ'),
            "entp_name": item.findtext('ENTP_NAME')
        })
        
    return jsonify({
        'code': 'success',
        'data': response_data
    })