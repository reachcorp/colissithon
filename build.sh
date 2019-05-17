rm -rf ./docker/context/dockerdist/*
touch ./docker/context/dockerdist/README.md
mkdir -p ./docker/context/dockerdist/src/ && cp -Rf ./src/* ./docker/context/dockerdist/src/
mkdir -p ./docker/context/dockerdist/samples/ && cp -Rf ./samples/* ./docker/context/dockerdist/samples/
cp -Rf ./colissithon.iml ./docker/context/dockerdist/
cp -Rf ./send_colis.py ./docker/context/dockerdist/
cp -Rf ./eat_and_dispatch.py ./docker/context/dockerdist/
cp -Rf ./colissithon_param.yml ./docker/context/dockerdist/
cp -Rf ./setup.py ./docker/context/dockerdist/
cp -Rf ./entrypoint.sh ./docker/context/dockerdist/
cp -Rf ./requirements.txt ./docker/context/

docker-compose -f ./docker/colissithon.yml build
