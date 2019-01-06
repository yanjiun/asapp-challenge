#!/bin/bash

python ../initialize_db.py test.db
python ../src/challenge.py test.db
python test_system.sh
rm  test.db