---
layout: post
comments: true
title:  "CI & CD for a Django Application on Kubernetes using Gitlab CI"
description: "Writing CI & CD for a django application on Kubernetes - Best Practices"
keywords: "Kubernetes, Django, Python, PostgreSQL, Docker, Gitlab, Continous Integration, Continous Delivery"
date:   2018-07-20
categories: [python, django, kubernetes, postgresql, docker, continous integration, continous delivery]
author: Santosh
---

This tutorial explains how to setup continuous integration and continuous delivery for a Django project hosted on kubernetes using Gitlab CI

`Note:`
This tutorial is a continuation from the previous tutorial which can be found on [GitHub](https://github.com/yvsssantosh/django-on-k8s) or [Gitlab](https://gitlab.com/yvsssantosh/django-on-k8s)

`Pre-requisites:`
* A ready kubernetes cluster
* Django application to deploy on the cluster

For this tutorial to work, we need to run it on `GitLab Repository` as we are going to write a corresponding `GitLab CI` file.

Before we jump into the CI file, rather than giving full access to gitlab to control the whole project lets create a new role for GitLab CI which gives full access only to our kubernetes cluster & our container registry.

### Role for GitLab CI

Navigate to <https://console.cloud.google.com/iam-admin/roles> to create a new role.

In the filter table, search for `Kubernetes Engine Admin OR Storage Admin`. Once we find the two options, create a new role from selection. Name the new role as `Gitlab CI` and save it.

```
Note:
Its NOT RECOMMENDED to give Kubernetes Admin OR Storage Admin access to Gitlab CI Role
Just as a part of tutorial, full access is being given. Give access ONLY based on requirement.
```

![](/assets/images/django-gitlab-ci-cd/create_from_role.png)

Now lets create a new service account, based on the role Gitlab CI which we just created now.
Navigate to <https://console.cloud.google.com/iam-admin/serviceaccounts> and click on `Create Service Account`

![](/assets/images/django-gitlab-ci-cd/create_service_account.png)

As observed I've created a new service account named `gitlab-ci`. Note that Project Role contains the previously created role `Gitlab CI`

Once we click on `Save`, a dialog box pops up asking to save a json file. Save the file at the required destination.

Now that we have the private key which authenticates to our Kubernetes Cluster and also has access to our Container Registry, encode the file data so as to pass it as a variable in Gitlab CI

```sh
# Navigate to the directory where the file has been saved. And then run the following command
cat test-gcp-*.json | base64

# This generates an encoded key (which is quite big!!). Make sure to copy the key
# as this has to be pasted in an environment variable in our Gitlab Project.
```

* Lets navigate to our CI & CD settings in our project at https://gitlab.com/GITLAB_USERNAME/PROJECT_NAME/settings/ci_cd

* Create two new variables with following keys & values
```
KEY = GCLOUD_SERVICE_KEY
VALUE = ENCODED_KEY_GENERATED_FROM_JSON

KEY = GCP_PROJECT_ID
VALUE = gcr.io/YOUR_GOOGLE_PROJECT_ID
```

![](/assets/images/django-gitlab-ci-cd/gitlab_variables.png)

This finishes the initial stage of setup, where roles are created & associated with service accounts and gitlab variables are setup

### The Supreme `.gitlab-ci.yml`

Lets see `.gitlab-ci.yml` file and understand various stages involved in it

```yml
# Gitlab CI yml file
# GitLab CI uses the services keyword to define what docker containers should be linked with your base image. Since we are using docker as our image we'll be using docker:dind i.e. Docker-In-Docker-Image
services:
- docker:dind

# Since we are using Alpine, everything is not installed by default.
# Thus we are setting up the basics
before_script:
  - apk update && apk upgrade && apk add --no-cache bash openssh
  
# Environemt Variable for docker:dind service explaining to use overlay2 as supporting driver for docker
variables:
  DOCKER_DRIVER: overlay2

# This is the major part of the code which explains the stages present in our pipeline.
# In a django application we have various stages which include testing, packing the code,
# performing migrations, collecting static files and running the application.
# The various stages are broadly classified into 3 main categories:

# 1. Test       2. Release      3. Deploy

stages:
- test
- release
- deploy

# Stage I
# Testing Phase:
# This is where the main code is tested.
# Other options like code coverage, etc are also written in this phase
test:
  stage: test
  # This repo includes python3, pip3 and postgres so that I need not
  # setup python and postgres separately.
  image: vaeum/alpine-python3-pip3
  before_script:
    # Installing requirements
    - pip install -r requirements.txt
  variables:
    # Connecting to testDB
    POSTGRES_DB: postgres
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: ''
    POLLSAPI_PG_HOST: postgres
  services:
    - postgres:9.6-alpine
  script:
    # Command to test our application
    - python manage.py test

# Stage II
# Release Phase
# In this phase, we package our code using docker
# as we deploy containerized applications on kubernetes
release:
  stage: release
  image: docker:latest
  before_script:
   # Note the image in L#69 being a docker image. This is because in release we
   # need to package our application using docker and login so that we'll be able
   # to push our images to Google Container Registry

   # Pre-requisites required to install google cloud sdk on gitlab runner
   - export COMMIT_SHA=$(echo $CI_COMMIT_SHA | cut -c1-8)
   - apk update
   - apk upgrade
   - apk add python python-dev py-pip build-base 
   - apk add --update ca-certificates
   - apk add --update -t deps curl
   - apk del --purge deps
   - rm /var/cache/apk/*

  script:
    # Build our image using docker
    - docker build -t $GCP_PROJECT_ID/$CI_PROJECT_NAME:$COMMIT_SHA .

    # Write our GCP service account private key into a file
    - echo $GCLOUD_SERVICE_KEY | base64 -d > ${HOME}/gcloud-service-key.json
    
    # Download and install Google Cloud SDK
    - wget https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz
    - tar zxvf google-cloud-sdk.tar.gz && ./google-cloud-sdk/install.sh --usage-reporting=false --path-update=true
    
    # Update gcloud components
    - google-cloud-sdk/bin/gcloud --quiet components update

    # Give access to gcloud project
    - google-cloud-sdk/bin/gcloud auth activate-service-account --key-file ${HOME}/gcloud-service-key.json  || die "unable to authenticate service account for gcloud"
    
    # Get current projects credentials to access it
    - google-cloud-sdk/bin/gcloud container clusters get-credentials pollsapi --zone asia-south1-a --project test-gcp-208915
    
    # Configure container registry to push using docker
    - docker login -u _json_key --password-stdin https://gcr.io < ${HOME}/gcloud-service-key.json

    # Push the image using docker
    - docker push $GCP_PROJECT_ID/$CI_PROJECT_NAME:$COMMIT_SHA

    # The tag, only master indicates that whenever code is pushed to master branch,
    # only then run the pipeline
  environment: production
  only:
    - master

# Stage III - I
# Deployment Phase
# In this phase, migrations are performed.
# Note that this is a manual stage as migrations are not run for each commit.
# If needed to run for every merge/commit to master branch, then comment when:manual
migrations:
  image: google/cloud-sdk:alpine
  stage: deploy
  variables:
    KUBE_LATEST_VERSION: "v1.8.5"
  before_script:
   # Pre-requisites required to install kybectl command line on gitlab runner
   - export COMMIT_SHA=$(echo $CI_COMMIT_SHA | cut -c1-8)
   - apk update
   - apk upgrade
   - apk add --update ca-certificates
   - apk add --update -t deps curl
   - curl -L https://storage.googleapis.com/kubernetes-release/release/${KUBE_LATEST_VERSION}/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl
   - chmod +x /usr/local/bin/kubectl
   - apk del --purge deps
   - rm /var/cache/apk/*

  script:
    # Write our GCP service account private key into a file
    - echo $GCLOUD_SERVICE_KEY | base64 -d > ${HOME}/gcloud-service-key.json
    
    # Update gcloud components
    - gcloud --quiet components update

    # Give access to gcloud project
    - gcloud auth activate-service-account --key-file ${HOME}/gcloud-service-key.json  || die "unable to authenticate service account for gcloud"
    - gcloud container clusters get-credentials pollsapi --zone asia-south1-a --project test-gcp-208915
    
    # Update the image tag inside the file polls-migration.yml using sed
    - sed -i 's/${TAG}/'"$COMMIT_SHA"'/g' polls-migration.yml

    # Run kubectl apply to apply any changes made in env variables, etc
    - kubectl apply -f polls-migration.yml
  environment: production
  
  # Note that when: manual indicates that this is a manual action
  # and will only trigger if they user clicks play button, in the pipeline
  when: manual
  only:
    - master

# Stage III - II
# Deployment Phase
# In this phase we will be collecting static files.
# Usually collecting static files is a one time operation and is 
# not done every time. For this reason this has been made a manual branch
# meaning, it has to be triggered manually whenever required
collect-static:
  image: google/cloud-sdk:alpine
  stage: deploy
  variables:
    KUBE_LATEST_VERSION: "v1.8.5"
  before_script:
   # Pre-requisites required to install kybectl command line on gitlab runner
   - export COMMIT_SHA=$(echo $CI_COMMIT_SHA | cut -c1-8)
   - apk update
   - apk upgrade
   - apk add --update ca-certificates
   - apk add --update -t deps curl
   - curl -L https://storage.googleapis.com/kubernetes-release/release/${KUBE_LATEST_VERSION}/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl
   - chmod +x /usr/local/bin/kubectl
   - apk del --purge deps
   - rm /var/cache/apk/*

  script:
    # Write our GCP service account private key into a file
    - echo $GCLOUD_SERVICE_KEY | base64 -d > ${HOME}/gcloud-service-key.json
    
    # Update gcloud components
    - gcloud --quiet components update

    # Give access to gcloud project
    - gcloud auth activate-service-account --key-file ${HOME}/gcloud-service-key.json  || die "unable to authenticate service account for gcloud"
    - gcloud container clusters get-credentials pollsapi --zone asia-south1-a --project test-gcp-208915
    
    # Update the image tag inside the file polls-collect-static.yml using sed
    - sed -i 's/${TAG}/'"$COMMIT_SHA"'/g' polls-collect-static.yml

    # Run kubectl apply to apply any changes made in env variables, etc
    - kubectl apply -f polls-collect-static.yml
  environment: production
  when: manual
  only:
    - master

# Stage III - III
# Deployment Phase
# In this phase, we make sure to update our application based on
# the data in current commit and mainly focus on application deployment.
deploy:
  image: google/cloud-sdk:alpine
  stage: deploy
  variables:
    KUBE_LATEST_VERSION: "v1.8.5"
  before_script:
   # Pre-requisites required to install kybectl command line on gitlab runner
   - export COMMIT_SHA=$(echo $CI_COMMIT_SHA | cut -c1-8)
   - apk update
   - apk upgrade
   - apk add --update ca-certificates
   - apk add --update -t deps curl
   - curl -L https://storage.googleapis.com/kubernetes-release/release/${KUBE_LATEST_VERSION}/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl
   - chmod +x /usr/local/bin/kubectl
   - apk del --purge deps
   - rm /var/cache/apk/*

  script:
    # Write our GCP service account private key into a file
    - echo $GCLOUD_SERVICE_KEY | base64 -d > ${HOME}/gcloud-service-key.json
    
    # Update gcloud components
    - gcloud --quiet components update

    # Give access to gcloud project
    - gcloud auth activate-service-account --key-file ${HOME}/gcloud-service-key.json  || die "unable to authenticate service account for gcloud"
    - gcloud container clusters get-credentials pollsapi --zone asia-south1-a --project test-gcp-208915
    
    # Run kubectl apply to apply any changes made in env variables, etc
    - kubectl apply -f pollsapi.yml

    # Update deployment with new image
    - kubectl set image deployment/polls-api ${CI_PROJECT_NAME}=$GCP_PROJECT_ID/$CI_PROJECT_NAME:$COMMIT_SHA
  environment: production
  only:
    - master

```

`For any queries, please create an issue.`