# email

## Example mutation : sending a email

### mutation :

```js
mutation {
  sendContactFormEmail(from: "yann@yann.fr", text:"Hello world") {
    from
    text
  }
}
```

response:
```
{
  "data": {
    "sendContactFormEmail": {
      "from": "yann@yann.fr",
      "text": "hello world"
    }
  }
}
```

### mutation with variables:

```js
mutation sendContactFormEmail($from:String!,$text:String!) {
  sendContactFormEmail(from: $from, text:$text) {
    from
    text
  }
}
```

variables :

```json
{"from": "yann@yann.fr","text": "hello world"}
```

response:

```json
{
  "data": {
    "sendContactFormEmail": {
      "from": "yann@yann.fr",
      "text": "hello world"
    }
  }
}
```
