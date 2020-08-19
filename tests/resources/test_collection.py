from unittest.mock import patch

from stac_api.clients.postgres.base import PostgresClient
from stac_api.errors import DatabaseError

from ..conftest import _raise_exception


def test_create_and_delete_collection(app_client, load_test_data):
    """Test creation and deletion of a collection"""
    test_collection = load_test_data("test_collection.json")
    test_collection["id"] = "test"

    resp = app_client.post("/collections", json=test_collection)
    assert resp.status_code == 200

    resp = app_client.delete(f"/collections/{test_collection['id']}")
    assert resp.status_code == 200


def test_create_collection_conflict(app_client, load_test_data):
    """Test creation of a collection which already exists"""
    # This collection ID is created in the fixture, so this should be a conflict
    test_collection = load_test_data("test_collection.json")
    resp = app_client.post("/collections", json=test_collection)
    assert resp.status_code == 409


def test_delete_missing_collection(app_client):
    """Test deletion of a collection which does not exist"""
    resp = app_client.delete("/collections/missing-collection")
    assert resp.status_code == 404


def test_update_collection_already_exists(app_client, load_test_data):
    """Test updating a collection which already exists"""
    test_collection = load_test_data("test_collection.json")
    test_collection["keywords"].append("test")
    resp = app_client.put("/collections", json=test_collection)
    assert resp.status_code == 200

    resp = app_client.get(f"/collections/{test_collection['id']}")
    assert resp.status_code == 200
    resp_json = resp.json()
    assert "test" in resp_json["keywords"]


def test_update_new_collection(app_client, load_test_data):
    """Test updating a collection which does not exist (same as creation)"""
    test_collection = load_test_data("test_collection.json")
    test_collection["id"] = "new-test-collection"

    resp = app_client.put("/collections", json=test_collection)
    assert resp.status_code == 200

    resp = app_client.get(f"/collections/{test_collection['id']}")
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json["id"] == test_collection["id"]


def test_get_all_collections(app_client, load_test_data):
    """Test reading all collections"""
    test_collection = load_test_data("test_collection.json")
    test_collection["id"] = "new-test-collection"

    resp = app_client.post("/collections", json=test_collection)
    assert resp.status_code == 200

    resp = app_client.get("/collections")
    assert resp.status_code == 200
    resp_json = resp.json()

    assert test_collection["id"] in [coll["id"] for coll in resp_json]


def test_collection_not_found(app_client):
    """Test read a collection which does not exist"""
    resp = app_client.get("/collections/does-not-exist")
    assert resp.status_code == 404


def test_create_collection_database_error(app_client, load_test_data):
    """Test 424 is raised on database error"""
    test_collection = load_test_data("test_collection.json")
    with patch.object(PostgresClient, "lookup_id", _raise_exception(DatabaseError())):
        resp = app_client.post("/collections", json=test_collection)
        assert resp.status_code == 424


def test_update_collection_database_error(app_client, load_test_data):
    """Test 424 is raised on database error"""
    test_collection = load_test_data("test_collection.json")
    with patch.object(PostgresClient, "lookup_id", _raise_exception(DatabaseError())):
        resp = app_client.post("/collections", json=test_collection)
        assert resp.status_code == 424


def test_get_collection_database_error(app_client, load_test_data):
    """Test 424 is raised on database error"""
    test_collection = load_test_data("test_collection.json")
    with patch.object(PostgresClient, "lookup_id", _raise_exception(DatabaseError())):
        resp = app_client.get(f"/collections/{test_collection['id']}")
        assert resp.status_code == 424


def test_delete_collection_database_error(app_client, load_test_data):
    """Test 424 is raised on database error"""
    test_collection = load_test_data("test_collection.json")
    with patch.object(PostgresClient, "commit", _raise_exception(DatabaseError())):
        resp = app_client.delete(f"/collections/{test_collection['id']}")
        assert resp.status_code == 424
