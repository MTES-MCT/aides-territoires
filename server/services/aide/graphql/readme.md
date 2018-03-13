# HelloWorld

## Example query

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
