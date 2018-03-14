# HelloWorld

## getUser

query :

```
query aide($id: String!) {
  aide(id:$id) {
    id
    title
    description
  }
}
```

variables :

```
{"id": "76YUIHJK"}
```

response:

```
{
  "data": {
    "aide": {
      "id": "76YUIHJK",
      "title": "aide de test",
      "description": "description aide de test"
    }
  }
}
```

## saveUser

mutation

```json
mutation saveUser($name:String!, $mail:String!, $password:String!){
  saveUser(name:$name, mail: $mail, password: $password) {
    id
    name
    mail
  }
}
```

variables

```json
{
  "name": "Yann",
  "mail": "yann.boisselier@gmail.com",
  "password": "hello"
}
```

response

```json
{
  "data": {
    "saveUser": {
      "name": "Yann",
      "mail": "yann.boisselier@gmail.com"
    }
  }
}
```
