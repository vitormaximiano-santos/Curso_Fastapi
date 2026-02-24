import requests

headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzcyNDg3ODc3fQ.B2X9o5LiAZbJ0o0F5yzwOqGsGhVlfX_ofp3xYprkdAc"}

requesicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers = headers)

print(requesicao)
print(requesicao.json())


"""conta:admin01: {
  "nome": "admin01",
  "email": "admin1@gmail.com",
  "senha": "ad01",
  "ativo": true,
  "admin": true
}"""