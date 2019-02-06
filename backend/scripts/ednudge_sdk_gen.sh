#!/usr/bin/env bash

if [[ -z "$1" ]]; then
  echo "Usage: ${0} ednudge_api_url"
  exit -1
else
  ednudge_api_url=$1
fi

ednudge_swagger_url="${ednudge_api_url}/documentation/json"


mv ./ednudge-sdk-python ./ednudge-sdk-python_$(date +%Y-%m-%d-%H-%M)
mkdir ednudge-sdk-python

cd ednudge-sdk-python
docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate -i ${ednudge_swagger_url} -l python -o /local -DpackageName=ednudge_api
cd ..


