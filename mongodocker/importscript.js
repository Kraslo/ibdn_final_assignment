// init_db.js

// Importar los datos utilizando un script de shell
var exec = require('child_process').exec;
exec('bash /pcreativa/resources/import_distances.sh', function(err, stdout, stderr) {
    if (err) {
        print('Error importing data: ' + stderr);
    } else {
        print('Data imported successfully: ' + stdout);

        // Conectar a la base de datos y crear el índice
        var db = connect("mongodb://localhost:27017/agile_data_science");
        db.origin_dest_distances.createIndex({ Origin: 1, Dest: 1 });
	printjson(db.origin_dest_distances.findOne());
        print('Index created successfully');
    }
});

