## SystemObject
To prevent dependencies errors, you as developer need to specify `dependencies` in your configuration file(-s)<br>

### 
First, open configuration file.

> configs/managers.json
```json
{
    "first_manager": {
      "required": true,
      "protected": [
         "shared"
      ],
      "dependencies": ["second_manager"]
    },
    "second_manager": {
      "required": true,
      "protected": [
         "shared"
      ]
    }
}
```

Then, after first init steps, you can access 