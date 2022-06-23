from app import app

app.app_context().push()

test_client = app.test_client()


def test_roads_200():
    r = test_client.post(
        '/roads',
        json={'number_road': 'test', 'name_road': 'test'},
        content_type='application/json',
    )
    assert r.status_code == 201

    road_id = r.get_json()['id']

    r = test_client.get('/roads')
    assert r.status_code == 200

    r = test_client.put(
        '/roads',
        json={'number_road': 'test1', 'name_road': 'test1'},
        content_type='application/json',
        query_string={'id': road_id},
    )
    assert r.status_code == 200

    r = test_client.delete(
        '/roads',
        json='',
        content_type='application/json',
        query_string={'id': road_id},
    )
    assert r.status_code == 204

    r = test_client.get(
        '/road',
        query_string={'id': road_id},
    )
    assert r.status_code == 404
