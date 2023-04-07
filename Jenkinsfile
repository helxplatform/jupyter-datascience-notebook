@Library('pipeline-utils@master') _

CCV = ""

pipeline {
  agent {
    kubernetes {
        yaml '''
kind: Pod
metadata:
  name: kaniko
spec:
  containers:
  - name: jnlp
    workingDir: /home/jenkins/agent
  - name: kaniko
    workingDir: /home/jenkins/agent
    image: gcr.io/kaniko-project/executor:debug
    imagePullPolicy: Always
    resources:
      requests:
        cpu: "1.0"
        memory: "4Gi"
        ephemeral-storage: "7Gi"
      limits:
        cpu: "1.0"
        memory: "4Gi"
        ephemeral-storage: "7Gi"
    command:
    - /busybox/cat
    tty: true
    volumeMounts:
    - name: jenkins-docker-cfg
      mountPath: /kaniko/.docker
  - name: go
    workingDir: /home/jenkins/agent
    image: golang:1.19.1
    imagePullPolicy: Always
    resources:
      requests:
        cpu: "512m"
        memory: "512Mi"
        ephemeral-storage: "256Mi"
      limits:
        cpu: "512m"
        memory: "1024Mi"
        ephemeral-storage: "256Mi"
    command:
    - /bin/bash
    tty: true
  volumes:
  - name: jenkins-docker-cfg
    secret:
      secretName: rencibuild-imagepull-secret
      items:
      - key: .dockerconfigjson
        path: config.json
'''
        }
    }
    environment {
        PATH = "/busybox:/kaniko:/ko-app/:$PATH"
        GITHUB_CREDS = credentials("${env.GITHUB_CREDS_ID_STR}")
        DOCKERHUB_CREDS = credentials("${env.CONTAINERS_REGISTRY_CREDS_ID_STR}")
        REGISTRY = "${env.REGISTRY}"
        REG_OWNER="helxplatform/jupyter"
        REPO_NAME="datascience-notebook"
        COMMIT_HASH="${sh(script:"git rev-parse --short HEAD", returnStdout: true).trim()}"
        IMAGE_NAME="${REGISTRY}/${REG_OWNER}/${REPO_NAME}"
    }
    stages {
        stage('Build') {
            steps {
                script {
                    container(name: 'go', shell: '/bin/bash') {
                        if (BRANCH_NAME.equals("master") || BRANCH_NAME.equals("main" )) {
                            CCV = go.ccv()
                        }
                    }
                    container(name: 'kaniko', shell: '/busybox/sh') {
                        def tagsToPush = ["$IMAGE_NAME:$BRANCH_NAME", "$IMAGE_NAME:$COMMIT_HASH"]
                        if (CCV != null && !CCV.trim().isEmpty() && BRANCH_NAME.equals("master") || BRANCH_NAME.equals("main")) {
                            tagsToPush.add("$IMAGE_NAME:$CCV")
                        } else if (BRANCH_NAME.equals("develop")) {
                            def now = new Date()
                            def currTimestamp = now.format("yyyy-MM-dd'T'HH.mm'Z'", TimeZone.getTimeZone('UTC'))
                            tagsToPush.add("$IMAGE_NAME:$currTimestamp")
                        }
                        kaniko.buildAndPush("./Dockerfile", tagsToPush, true)
                    }
                }
            }
        }
    }
}
