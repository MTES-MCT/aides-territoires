# email

## example mutation :

```javascript
mutation AideSave($name:String!, $description:String!) {
  AideSave(name: $name, description: $description) {
    name
    description
  }
}
```

variables :

```json
{ "name": "aide name", "description": "aide description" }
```
