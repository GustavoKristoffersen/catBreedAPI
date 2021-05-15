from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..api.main import app, get_db
from ..api.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_post_breed_should_succeed() -> None:
    response = client.post('/breeds', json={
        'name': 'test1',
        'location_of_origin': 'test1',
        'coat_length': 1,
        'body_type': 'test1',
        'pattern': 'test1', 
})
    
    assert response.status_code == 201

    response = client.get('/breeds/1')

    response_content = response.json()

    assert response_content['name'] == 'test1'
    assert response_content['location_of_origin'] == 'test1'
    assert response_content['coat_length'] == 1.0
    assert response_content['body_type'] == 'test1'
    assert response_content['pattern'] == 'test1'
    assert 'id' in response_content

def test_post_multiple_breeds_should_suceed() -> None:
    response = client.post('/breeds', json=[
        {
            'name': 'test2',
            'location_of_origin': 'test2',
            'coat_length': 2,
            'body_type': 'test2',
            'pattern': 'test2'
        },
        {
            'name': 'test3',
            'location_of_origin': 'test3',
            'coat_length': 3,
            'body_type': 'test3',
            'pattern': 'test3'
        }
    ])

    assert response.status_code == 201 
    assert type(response.json()) == list

    response = client.get('/breeds?name=test2')
    assert response.status_code == 200

    response = client.get('/breeds?name=test3')
    assert response.status_code == 200


def test_get_all_breeds_should_suceed() -> None:
    response = client.get('/breeds')

    assert response.status_code == 200

    response_content = response.json()
    
    assert type(response_content) == list
    assert 'name' in response_content[0]
    assert 'location_of_origin' in response_content[0]
    assert 'coat_length' in response_content[0]
    assert 'body_type' in response_content[0]
    assert 'pattern' in response_content[0]
    assert 'id' in response_content[0]


def test_get_single_breed_should_succeed() -> None:
    response = client.get('/breeds/1')
    
    assert response.status_code == 200

    response_content = response.json()

    assert response_content['id'] == 1
    assert 'name' in response_content
    assert 'location_of_origin' in response_content
    assert 'coat_length' in response_content
    assert 'body_type' in response_content
    assert 'pattern' in response_content
    assert 'id' in response_content

def test_get_filtered_breed_should_succeed() -> None:
    response = client.get('/breeds?body_type=test2&name=test2')
    
    assert response.status_code == 200


    response_content = response.json()

    assert type(response_content) == list
    assert response_content[0]['id'] == 2
    assert response_content[0]['body_type'] == 'test2'
    assert response_content[0]['name'] == 'test2'

def test_update_breed_should_suceed() -> None:
    response = client.put('/breeds/1', json={
        'name': 'test1',
        'location_of_origin': 'altered_test1',
        'coat_length': 1,
        'body_type': 'test1',
        'pattern': 'test1', 
})

    assert response.status_code == 200

    response = client.get('breeds/1')
    response_content = response.json()

    assert response_content['id'] == 1
    assert response_content['name'] == 'test1'
    assert response_content['location_of_origin'] == 'altered_test1'
    assert response_content['coat_length'] == 1.0
    assert response_content['body_type'] == 'test1'
    assert response_content['pattern'] == 'test1'


def test_partially_update_breed_should_suceed() -> None:
    response = client.patch('/breeds/2', json={'body_type' : 'altered_test2'})

    assert response.status_code == 200
    assert response.json()['id'] == 2
    assert response.json()['body_type'] == 'altered_test2'

    response = client.get('/breeds/2')

    assert response.json()['id'] == 2
    assert response.json()['body_type'] == 'altered_test2'


def test_update_breed_with_exiting_name_should_fail() -> None:
    response = client.patch('/breeds/3', json={'name': 'test1'})

    assert response.status_code == 400

    assert response.json() == {'detail': 'Breed with this name already exists'}


def test_update_breed_that_does_not_exist_should_fail() -> None:
    id = 10
    response = client.patch(f'/breeds/{id}', json={'name': 'test10'})

    assert response.status_code == 404

    assert response.json() == {'detail': f'Breed with id {id} does not exist'}


def test_delete_breed_should_suceed() -> None:
    id = 1
    response = client.delete(f'breeds/{id}')

    assert response.status_code == 200
    assert response.json() == {'message': f'item with id {id} deleted'}

    response = client.get(f'/breeds/{id}')

    assert response.status_code == 404
    assert response.json() == {'detail': f'Breed with id {id} does not exist'}

    client.delete('breeds/2')
    client.delete('breeds/3')



