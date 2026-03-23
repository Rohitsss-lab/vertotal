pipeline {
    agent any
    tools {
        nodejs 'NodeJS-20'
    }
    parameters {
        string(name: 'REPO_NAME',    defaultValue: 'ver1',  description: 'Triggering repo')
        string(name: 'REPO_VERSION', defaultValue: '1.0.0', description: 'New version')
        string(name: 'BUMP_TYPE',    defaultValue: 'patch', description: 'Bump type')
    }
    environment {
        GIT_REPO_URL = 'https://github.com/Rohitsss-lab/vertotal.git'
    }
    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: "${env.GIT_REPO_URL}",
                        credentialsId: 'github-token'
                    ]]
                ])
            }
        }
        stage('Process Versions') {
            steps {
                withEnv([
                    "REPO_NAME=${params.REPO_NAME}",
                    "REPO_VERSION=${params.REPO_VERSION}",
                    "BUMP_TYPE=${params.BUMP_TYPE}"
                ]) {
                    bat '"C:\\Program Files\\Python313\\python.exe" process_versions.py'
                }
            }
        }
        stage('Read Results') {
            steps {
                script {
                    env.NEW_UMBRELLA_VERSION = readFile('NEW_UMBRELLA_VERSION.txt').trim()
                    env.NEW_TAG              = readFile('NEW_TAG.txt').trim()
                    env.VER1_VERSION         = readFile('VER1_VERSION.txt').trim()
                    env.VER2_VERSION         = readFile('VER2_VERSION.txt').trim()
                }
            }
        }
        stage('Show Versions') {
            steps {
                echo "Umbrella : ${env.NEW_UMBRELLA_VERSION}"
                echo "ver1     : ${env.VER1_VERSION}"
                echo "ver2     : ${env.VER2_VERSION}"
                echo "Tag      : ${env.NEW_TAG}"
                bat 'type versions.json'
            }
        }
        stage('Commit and Tag') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-token',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    bat '''
                        git config user.email "jenkins@ci.com"
                        git config user.name "Jenkins"
                        git checkout -b release/v%NEW_UMBRELLA_VERSION%
                        git add versions.json
                        git commit -m "chore: umbrella version %NEW_UMBRELLA_VERSION%"
                        git remote set-url origin https://%GIT_USER%:%GIT_TOKEN%@github.com/Rohitsss-lab/vertotal.git
                        git push origin release/v%NEW_UMBRELLA_VERSION%
                        git checkout main
                        git merge release/v%NEW_UMBRELLA_VERSION%
                        git push origin main
                        git tag %NEW_TAG%
                        git push origin %NEW_TAG%
                    '''
                }
            }
        }
    }
    post {
        success { echo "vertotal pipeline done — tag ${env.NEW_TAG} created" }
        failure { echo "vertotal pipeline FAILED" }
    }
}
