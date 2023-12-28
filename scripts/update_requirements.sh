#!/bin/bash

# Script to update requierements

# environments can be: develop, testing, stage and production

environments=("develop")

for i in ${!environments[@]}; do
    environment=${environments[$i]}
    echo "Environment: ${environment}"
    pip-compile -r requirements/${environment}.in -o requirements/$(date +'%Y%m%d').${environment}
done
