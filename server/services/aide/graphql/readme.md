# HelloWorld

## aideGet

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

## aideSave

mutation

```
mutation($title:String!, $description:String) {
  saveAide(title:$title, description:$description) {
    title
    description
  }
}
```

variables

```
{
  "title": "title",
  "description": "description"
}
```

response

```
{
  "data": {
    "aideSave": {
      "title": "title",
      "description": "description"
    }
  }
}
```
