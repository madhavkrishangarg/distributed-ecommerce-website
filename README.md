Technologies used: python, grpc, google cloud platform

install grpcio and grpcio-tools
$ python3 -m pip install grpcio
$ python3 -m pip install grpcio-tools



To generate server and client code run the following command in grpc directory:

$ python3 -m grpc_tools.protoc -I./protos --python_out=./code --pyi_out=./code --grpc_python_out=./code ./protos/market.proto

change directory to grpc/code

We need to change the ip addresses in the files market.py, seller-1.py, seller-2.py, buyer-1.py, buyer-2.py because every time the VM instance on GCP restarts, the external IP address of the instances change

Change lines 13 and 16 in all the seller and buyer files

run the market server:
$ python3 market.py

run sellers:
$ python3 seller-1.py
$ python3 seller-2.py

run buyers:
$python3 buyer-1.py
$python3 buyer-2.py
