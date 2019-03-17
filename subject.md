Problem 1 - JSON handling

We are running a web application which stores it's configuration in a simple JSON file. Here is an example of such configuration:

```json
{
  "page1": {
    "initialSettings": {
      "position": [10,12],
      "color": "white"
    },
    "available-filters": {
      "name-filter": {
        "column": "name",
        "sort": "desc"
      }
    }
  },
  "page2": {
    "initialSettings": {
      "position": [14,20],
      "color": "red"
    },
    "available-filters": {
      ...
    }
  },
}
```

Your task: write a procedure/function/program that modifies arbitrary value in the configuration file on arbitrary position. The program has 2 inputs. One is the configuration file itself and second is a file which contains list of changes to be applied. The resulting json should be printed to the terminal or written to a file on disk with arbitrary name. You can use any technology language but preferably Python. You are allowed to use a library which parses the JSON file for you. You don't have to parse the files manually - use the best tool that you find.

Example:
- Configuration file:

```json
{
  "page1": {
    "initialSettings": {
      "position": [10,12],
      "color": "white"
    },
    "available-filters": {
      "name-filter": {
        "column": "name",
        "sort": "desc"
      }
    }
  }
}
```

- File containing input changes in the following form:

```
"page1.initiaSettings.color": "green"
"page1.available-filters.name-filter.sort": "asc"
```

- Resulting configuration file should be:

```json
{
  "page1": {
    "initialSettings": {
      "position": [10,12],
      "color": "green"
    },
    "available-filters": {
      "name-filter": {
        "column": "name",
        "sort": "asc"
      }
    }
  }
}
```

Note that the changes file should be able to handle any valid JSON structure as long as it fits in single line. For instance the following two changes should also be correctly applied:

```
"page1.initiaSettings.position": [24,30]
"page1.available-filters.name-filter: { "column": "lastName", "sort": "desc" }
```
