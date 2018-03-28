# HelloWorld

## Example query

query :

```
query helloWorld($name: String!) {
  helloWorld(name:$name) {
    message
  }
}
```

variables :

```
{"name": "Yann"}
```

response:

```
{
  "data": {
    "helloWorld": {
      "message": "hello Yann !"
    }
  }
}
```
