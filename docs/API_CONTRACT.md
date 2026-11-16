# Demo API contract

All request and non-empty response bodies use JSON. Student IDs are opaque strings.
Success responses wrap their resource in `{"data": ...}`; errors return
`{"error": "message"}`. There is no authentication in the loopback demo server.

| Method | Route | Success | Behavior |
| --- | --- | --- | --- |
| POST | `/students` | 201 | Create a student; return generated ID and fields |
| GET | `/students/{id}` | 200 | Return student |
| PUT | `/students/{id}` | 200 | Replace provided student profile fields |
| DELETE | `/students/{id}` | 204 | Delete student and all nested data; empty body |
| POST | `/students/{id}/skills` | 201 | Append skill; return appended object |
| POST | `/students/{id}/addresses` | 201 | Append address; return appended object |
| GET | `/students/{id}/details` | 200 | Return profile, skills and addresses |

Profile requires non-blank string `first_name`, `last_name`, and ISO calendar date
`date_of_birth` (`YYYY-MM-DD`). `middle_name` is optional. Generated `id`,
`skills` and `addresses` cannot be supplied through the profile payload.
A skill requires non-blank `skill`; an address requires non-blank `city`.
Extra fields on child records are preserved. Invalid input returns 400.
Unknown IDs return 404 with `Student not found`, including repeated deletion.
Unknown routes return 404. No list endpoint, persistence, authentication, retries,
or production concurrency guarantees are provided by the demo server.
