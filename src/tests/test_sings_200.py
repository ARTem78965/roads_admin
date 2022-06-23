from app import app

app.app_context().push()

test_client = app.test_client()


def test_sings_200():
    r = test_client.post(
        '/sings',
        json={'name_sing': 'test'},
        content_type='application/json',
    )
    assert r.status_code == 201

    sing_id = r.get_json()['id']

    r = test_client.get('/sings')
    assert r.status_code == 200

    r = test_client.put(
        '/sings',
        json={'name_sing': 'test1'},
        content_type='application/json',
        query_string={'id': sing_id},
    )
    assert r.status_code == 200

    r = test_client.delete(
        '/sings',
        json='',
        content_type='application/json',
        query_string={'id': sing_id},
    )
    assert r.status_code == 204

    r = test_client.get(
        '/sing',
        query_string={'id': sing_id},
    )
    assert r.status_code == 404
