## Girder-jobmock devops tools.

Girder-jobmock provides several tools for bringing up an instance quickly and easily to test jobs against. It provides a Makefile with the following targets:

+ *init* - Install python and ansible requirements, run docker-compose up and provision with ansible
+ *stop* - Run docker-compose stop
+ *start* - Run docker-compose start
+ *kill* - Run docker-compose stop,  then docker-compose kill
+ *clean* - Kill all containers and uninstall requirements

To get started run:
```
make init
``` 

Girder should be available at http://127.0.0.1:8080 username: admin, password: letmein

## Developing Girder with girder-jobmock

There is also a special target ```dev``` that may be used in conjunction with the environment variable ```GIRDER_PATH```

E.g. Run:
```
export GIRDER_PATH=/path/to/my/girder
make dev init
```

This will run docker-compose and ansible against a girder container which has mounted ```/path/to/my/girder``` at ```/girder``` within the container.

Targets,  ```init```, ```start```, ```stop```, and ```kill``` may all be prefixed with ```dev```.
