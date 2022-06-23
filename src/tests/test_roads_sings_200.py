from app import app

app.app_context().push()

test_client = app.test_client()


def test_roads_sings_200():
    r = test_client.post(
        '/roads',
        json={'number_road': 'test', 'name_road': 'test'},
        content_type='application/json',
    )
    assert r.status_code == 201

    road_id = r.get_json()['id']

    r = test_client.post(
        '/sings',
        json={'name_sing': 'Пешеходный переход'},
        content_type='application/json',
    )
    assert r.status_code == 201

    sing_id = r.get_json()['id']

    r = test_client.post(
        '/roads/sings',
        data={
            'road_id': road_id,
            'latitude': 19.999,
            'longitude': 19.999,
            'image': open('src/app/recognition/img/1.jpg', 'rb'),
        },
        content_type='multipart/form-data',
    )
    assert r.status_code == 201

    road_sing_id = r.get_json()['id']

    r = test_client.get('/roads/sings')
    assert r.status_code == 200

    r = test_client.put(
        '/roads/sings',
        data={
            'road_id': road_id,
            'latitude': 29.999,
            'longitude': 29.999,
            'image': open('src/app/recognition/img/1.jpg', 'rb'),
        },
        query_string={
            'id': road_sing_id,
        },
        content_type='multipart/form-data',
    )
    assert r.status_code == 200

    r = test_client.delete(
        '/roads/sings',
        json='',
        content_type='application/json',
        query_string={'id': road_sing_id},
    )
    assert r.status_code == 204

    r = test_client.delete(
        '/roads/sings',
        json='',
        content_type='application/json',
        query_string={'id': road_sing_id},
    )
    assert r.status_code == 404

    r = test_client.delete(
        '/sings',
        json='',
        content_type='application/json',
        query_string={'id': sing_id},
    )
    assert r.status_code == 204

    r = test_client.delete(
        '/roads',
        json='',
        content_type='application/json',
        query_string={'id': road_id},
    )
    assert r.status_code == 204
