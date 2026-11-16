"""Student resource operations; assertions belong to the tests."""
class StudentsApi:
    def __init__(self, client):
        self.client = client

    def create(self, payload):
        return self.client.request("POST", "/students", json=payload)

    def get(self, student_id):
        return self.client.request("GET", f"/students/{student_id}")

    def update(self, student_id, payload):
        return self.client.request("PUT", f"/students/{student_id}", json=payload)

    def delete(self, student_id):
        return self.client.request("DELETE", f"/students/{student_id}")

    def add_skills(self, student_id, payload):
        return self.client.request("POST", f"/students/{student_id}/skills", json=payload)

    def add_address(self, student_id, payload):
        return self.client.request("POST", f"/students/{student_id}/addresses", json=payload)

    def details(self, student_id):
        return self.client.request("GET", f"/students/{student_id}/details")
