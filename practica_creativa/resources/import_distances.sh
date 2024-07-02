#!/bin/bash

# Import our enriched airline data as the 'airlines' collection
mongoimport -d agile_data_science -c origin_dest_distances --file /pcreativa/data/origin_dest_distances.jsonl
mongosh agile_data_science --eval 'db.origin_dest_distances.ensureIndex({Origin: 1, Dest: 1})'
mongosh agile_data_science --eval 'printjson(db.origin_dest_distances.findOne())'

cp -r  /pcreativa/data/* /data_ibdn/
# cambiamos mongo por mongosh porque así es el comando
