import uuid
import pytest


@pytest.mark.smoke
def test_create_student_returns_id_and_fields(create_student, student_payload):
    response = create_student(student_payload)
    assert response.headers["Content-Type"].startswith("application/json")
    data = response.json()["data"]
    assert isinstance(data["id"], str) and data["id"]
    for key, value in student_payload.items():
        assert data[key] == value


@pytest.mark.smoke
def test_get_created_student(students, student_id, student_payload):
    response = students.get(student_id)
    assert response.status_code == 200
    assert response.json()["data"]["id"] == student_id
    assert response.json()["data"]["first_name"] == student_payload["first_name"]


@pytest.mark.regression
def test_update_persists_changes(students, student_id, student_payload):
    payload = dict(student_payload, middle_name="Updated")
    response = students.update(student_id, payload)
    assert response.status_code == 200
    readback = students.get(student_id)
    assert readback.status_code == 200
    assert readback.json()["data"]["middle_name"] == "Updated"
    assert readback.json()["data"]["id"] == student_id


@pytest.mark.regression
def test_delete_removes_created_student(students, student_id):
    response = students.delete(student_id)
    assert response.status_code == 204
    assert response.content == b""
    assert students.get(student_id).status_code == 404
    assert students.delete(student_id).status_code == 404


@pytest.mark.negative
@pytest.mark.parametrize("operation", ["get", "update", "delete"])
def test_missing_student(students, student_payload, operation):
    identifier = uuid.uuid4().hex
    method = getattr(students, operation)
    response = method(identifier, student_payload) if operation == "update" else method(identifier)
    assert response.status_code == 404
    assert response.json()["error"] == "Student not found"


@pytest.mark.negative
@pytest.mark.parametrize("field,value", [
    ("first_name", ""), ("first_name", None), ("last_name", " "),
    ("date_of_birth", "not-a-date"), ("date_of_birth", "2000-02-30"),
])
def test_invalid_student_is_rejected(students, student_payload, field, value):
    payload = dict(student_payload, **{field: value})
    response = students.create(payload)
    assert response.status_code == 400
    assert field in response.json()["error"]


@pytest.mark.negative
def test_form_payload_is_rejected(client, student_payload):
    response = client.session.post(client.base_url + "/students", data=student_payload,
                                   timeout=client.timeout)
    assert response.status_code == 400
    assert response.json()["error"] == "Expected application/json"


@pytest.mark.regression
def test_student_skills_address_workflow(students, student_id):
    skill = {"skill": "Python", "experience_years": 3}
    address = {"city": "Bengaluru", "country": "India"}
    skill_response = students.add_skills(student_id, skill)
    assert skill_response.status_code == 201
    assert skill_response.json()["data"] == skill
    address_response = students.add_address(student_id, address)
    assert address_response.status_code == 201
    assert address_response.json()["data"] == address
    response = students.details(student_id)
    assert response.status_code == 200
    details = response.json()["data"]
    assert details["id"] == student_id
    assert skill in details["skills"]
    assert address in details["addresses"]


@pytest.mark.negative
@pytest.mark.parametrize("operation", ["add_skills", "add_address"])
def test_empty_child_payload_is_rejected(students, student_id, operation):
    response = getattr(students, operation)(student_id, {})
    assert response.status_code == 400
    assert "required" in response.json()["error"]
