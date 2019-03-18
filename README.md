# ConfigEditor

## Usage
```bash
python3 config_editor.py                                                                                                                              
usage: config_editor.py [-h] -f FILE -c CHANGES [-o OUTPUT] [-p]

Modifies arbitrary value in the configuration file on arbitrary position

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The json configuration file you want to change
  -c CHANGES, --changes CHANGES
                        The file containing the instructions about the changes
  -o OUTPUT, --output OUTPUT
                        Output file
  -p, --path-create
Ex:
 python3 config_editor.py -f ./testconf.json -c ./change1.txt
{"page1": {"initialSettings": {"position": [10, 12], "color": "green"}, "available-filters": {"name-filter": {"column": "name", "sort": "asc"}}}}
 python3 config_editor.py -f ./testconf.json -c ./change2.txt
{"page1": {"initialSettings": {"position": [24, 30], "color": "white"}, "available-filters": {"name-filter": {"column": "lastName", "sort": "desc"}}}}
 python3 config_editor.py -f ./testconf.json -c ./change3.txt -p 
{"page1": {"initialSettings": {"position": [10, 12], "color": "white"}, "available-filters": {"name-filter": {"column": "name", "sort": "asc"}}}, "not": {"existing": {"path": "green"}}}
```

