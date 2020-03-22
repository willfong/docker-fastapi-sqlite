# Docker / FastAPI / Vue / DynamoDB

This is a template repository for an opinionated proof-of-concept architecture.


## Guiding Principles

- Local development - The entire infrastrucutre must easily run locally for end-to-end testing
- Cloud deployment - We're focused on AWS-specifics here


## Getting Started

1. https://github.com/willfong/docker-fastapi-ddb/generate to create your own copy of this template


## Vue

Start with: `npm install`
Build with: `npm run build; cp -r dist/* ../static`


## DynamoDB Notes

There is no need to specify AWS credentials. dynamodb-local just needs to have a non-empty string.

Use Terraform to provision the DDB schema: `terraform apply -auto-approve`

Manually check tables: `aws dynamodb scan --endpoint-url http://localhost:8000 --table-name Users`


## Environment File

The system looks for `.env` in the checkout folder:
```
AWS_ACCESS_KEY_ID=no_key_needed
AWS_SECRET_ACCESS_KEY=no_key_needed
AWS_REGION_NAME=us-west-2
FACEBOOK_CLIENT_ID=123...890
FACEBOOK_CLIENT_SECRET=123...abc
DDB_ENDPOINT_URL=http://ddb:8000
REDIS_ENDPOINT_URL=redis
STATSD_ENDPOINT_URL=statsd
STATSD_PREFIX=myapp
```


## Google Auth
What all the keys mean
https://developers.google.com/identity/protocols/OpenIDConnect


## Production Deployment Notes

- Create `.env` file
- `docker-compose up`
- `npm install`
- `npm run build; cp -r dist/* ../static`
- `terraform init`
- `terraform apply -auto-approve`


Redis:
```
redis      | 1:M 16 Feb 2020 17:04:48.923 # You requested maxclients of 10000 requiring at least 10032 max file descriptors.
redis      | 1:M 16 Feb 2020 17:04:48.923 # Server can't set maximum open files to 10032 because of OS error: Operation not permitted.
redis      | 1:M 16 Feb 2020 17:04:48.923 # Current maximum open files is 4096. maxclients has been reduced to 4064 to compensate for low ulimit. If you need higher maxclients increase 'ulimit -n'.
redis      | 1:M 16 Feb 2020 17:04:48.924 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
redis      | 1:M 16 Feb 2020 17:04:48.924 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
```

## Docker

Delete all Docker related stuff, start over
```
docker container stop $(docker container ls -aq); docker container rm $(docker container ls -aq); docker image prune -a -f 
```

## Font Awesome

https://github.com/FortAwesome/vue-fontawesome

