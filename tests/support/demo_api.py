"""Local reference API for repeatable HTTP tests. Not a production web service."""
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock
import json
import uuid


class DemoServer(ThreadingHTTPServer):
    def __init__(self):
        super().__init__(("127.0.0.1", 0), Handler)
        self.students = {}
        self.lock = Lock()
        self.daemon_threads = True


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def respond(self, status, payload=None):
        data = json.dumps(payload).encode() if payload is not None else b""
        self.send_response(status)
        if data:
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def body(self):
        if self.headers.get_content_type() != "application/json":
            raise ValueError("Expected application/json")
        size = int(self.headers.get("Content-Length", "0"))
        if not 0 < size <= 65536:
            raise ValueError("Invalid payload size")
        try:
            result = json.loads(self.rfile.read(size))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ValueError("Invalid JSON") from None
        if not isinstance(result, dict):
            raise ValueError("Expected a JSON object")
        return result

    @staticmethod
    def validate_student(payload):
        for field in ("first_name", "last_name", "date_of_birth"):
            if not isinstance(payload.get(field), str) or not payload[field].strip():
                raise ValueError(f"{field} is required")
        try:
            date.fromisoformat(payload["date_of_birth"])
        except ValueError:
            raise ValueError("date_of_birth must use YYYY-MM-DD") from None
        return {key: payload[key] for key in
                ("first_name", "middle_name", "last_name", "date_of_birth") if key in payload}

    def dispatch(self):
        parts = self.path.strip("/").split("/")
        if parts[0] != "students":
            return self.respond(404, {"error": "Route not found"})
        try:
            with self.server.lock:
                records = self.server.students
                if parts == ["students"] and self.command == "POST":
                    data = self.validate_student(self.body())
                    identifier = uuid.uuid4().hex
                    records[identifier] = dict(data, id=identifier, skills=[], addresses=[])
                    return self.respond(201, {"data": records[identifier]})
                identifier = parts[1] if len(parts) >= 2 else None
                if identifier not in records:
                    return self.respond(404, {"error": "Student not found"})
                student = records[identifier]
                if len(parts) == 2:
                    if self.command == "GET":
                        return self.respond(200, {"data": student})
                    if self.command == "PUT":
                        student.update(self.validate_student(self.body()))
                        return self.respond(200, {"data": student})
                    if self.command == "DELETE":
                        del records[identifier]
                        return self.respond(204)
                if len(parts) == 3:
                    kind = parts[2]
                    if kind == "details" and self.command == "GET":
                        return self.respond(200, {"data": student})
                    if kind in {"skills", "addresses"} and self.command == "POST":
                        payload = self.body()
                        key = "skill" if kind == "skills" else "city"
                        if not isinstance(payload.get(key), str) or not payload[key].strip():
                            raise ValueError(f"{key} is required")
                        student[kind].append(payload)
                        return self.respond(201, {"data": payload})
                return self.respond(404, {"error": "Route not found"})
        except ValueError as error:
            return self.respond(400, {"error": str(error)})

    do_GET = do_POST = do_PUT = do_DELETE = dispatch
