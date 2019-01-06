#!/bin/bash

python initialize_db.py test.db
python src/challenge.py test.db &
python test/test_system.py
rm  test.db