#!/bin/bash

apt update;
apt -y install python3-pip;
pip3 install flask;

instance_id=$(ec2metadata --instance-id);

python3 -c "
from flask import Flask

app = Flask(__name__)

@app.route('/')
def default_route():
    return 'Instance "$instance_id" is responding now! '

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
";
