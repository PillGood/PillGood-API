from flask import Blueprint, request, jsonify
from server.services import pill_service
from xml.etree import ElementTree
import requests

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

    db_pills = pill_service.find_pills({'name': item_name})
    if len(db_pills) > 0:
        response_data = []

        for pill in db_pills:
            response_data.append({
                "item_id": pill.pill_id,
                "item_name": pill.name,
                "entp_id": pill.enterprise.enterprise_id,
                "entp_name": pill.enterprise.name
            })
    else:
        xml_root = ElementTree.fromstring(
            search_open_api(item_name)
        )

        response_data = []

        # open api error handling
        result_code = xml_root.find('header').find('resultCode').text
        if result_code != '00':
            result_msg = xml_root.find('header').find('resultMsg').text
            return jsonify({ 'code': 'error', 'message': result_msg }), 503

        # parsing response data (xml format) and commit to db
        items = xml_root.find('body').find('items').findall('item')
        for item in items:
            pill_service.create_pill({
                'pill_id': item.findtext('ITEM_SEQ'),
                'name': item.findtext('ITEM_NAME'),
                'eng_name': item.findtext('ITEM_ENG_NAME'),
                'chart': item.findtext('CHART'),
                'image_url': item.findtext('ITEM_IMAGE'),
                'class_name': item.findtext('CLASS_NAME'),
                'otc_type': item.findtext('ETC_OTC_NAME'),
                'enterprise_id': item.findtext('ENTP_SEQ'),
                'enterprise_name': item.findtext('ENTP_NAME')
            })

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