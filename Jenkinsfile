pipeline {
    agent any
    parameters {
        string(name: 'REPO_NAME',      defaultValue: 'ver1',  description: 'Triggering repo')
        string(name: 'REPO_VERSION',   defaultValue: '1.0.0', description: 'New version')
        string(name: 'BUMP_TYPE',      defaultValue: 'patch', description: 'Bump type')
        string(name: 'DEPLOY_VERSION', defaultValue: '',      description: 'Fill to deploy e.g. 1.0.15 — leave blank for version bump')
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

        // ══════════════════════════════════════════
        // DEPLOY MODE
        // ══════════════════════════════════════════
        stage('Checkout Tag for Deploy') {
            when {
                expression { return params.DEPLOY_VERSION != null && params.DEPLOY_VERSION.trim() != '' }
            }
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "refs/tags/v${params.DEPLOY_VERSION}"]],
                    userRemoteConfigs: [[
                        url: "${env.GIT_REPO_URL}",
                        credentialsId: 'github-token'
                    ]]
                ])
                echo "Checked out vertotal at tag v${params.DEPLOY_VERSION}"
            }
        }
        stage('Read Deploy Versions') {
            when {
                expression { return params.DEPLOY_VERSION != null && params.DEPLOY_VERSION.trim() != '' }
            }
            steps {
                withEnv(["DEPLOY_VERSION=${params.DEPLOY_VERSION}"]) {
                    bat '"C:\\Program Files\\Python313\\python.exe" deploy.py'
                }
                script {
                    env.DEPLOY_VER1 = readFile('DEPLOY_VER1_VERSION.txt').trim()
                    env.DEPLOY_VER2 = readFile('DEPLOY_VER2_VERSION.txt').trim()
                }
                echo "==========================================="
                echo "DEPLOY MODE — vertotal v${params.DEPLOY_VERSION}"
                echo "ver1 will deploy : ${env.DEPLOY_VER1}"
                echo "ver2 will deploy : ${env.DEPLOY_VER2}"
                echo "NO version bump — NO commit — NO tag"
                echo "==========================================="
            }
        }
        stage('Deploy ver1') {
            when {
                expression { return params.DEPLOY_VERSION != null && params.DEPLOY_VERSION.trim() != '' }
            }
            steps {
                echo "Deploying ver1 at version ${env.DEPLOY_VER1}"
                build job: 'ver1',
                      wait: true,
                      parameters: [
                          string(name: 'DEPLOY_TAG',          value: env.DEPLOY_VER1),
                          string(name: 'TRIGGERED_BY_DEPLOY', value: 'true')
                      ]
                echo "ver1 v${env.DEPLOY_VER1} deployed successfully"
            }
        }
        stage('Deploy ver2') {
            when {
                expression { return params.DEPLOY_VERSION != null && params.DEPLOY_VERSION.trim() != '' }
            }
            steps {
                echo "Deploying ver2 at version ${env.DEPLOY_VER2}"
                build job: 'ver2',
                      wait: true,
                      parameters: [
                          string(name: 'DEPLOY_TAG',          value: env.DEPLOY_VER2),
                          string(name: 'TRIGGERED_BY_DEPLOY', value: 'true')
                      ]
                echo "ver2 v${env.DEPLOY_VER2} deployed successfully"
            }
        }

        // ══════════════════════════════════════════
        // VERSION BUMP MODE
        // ══════════════════════════════════════════
        stage('Checkout Main for Bump') {
            when {
                expression { return params.DEPLOY_VERSION == null || params.DEPLOY_VERSION.trim() == '' }
            }
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
            when {
                expression { return params.DEPLOY_VERSION == null || params.DEPLOY_VERSION.trim() == '' }
            }
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
            when {
                expression { return params.DEPLOY_VERSION == null || params.DEPLOY_VERSION.trim() == '' }
            }
            steps {
                script {
                    env.NEW_UMBRELLA_VERSION = readFile('NEW_UMBRELLA_VERSION.txt').trim()
                    env.NEW_TAG              = readFile('NEW_TAG.txt').trim()
                    env.VER1_VERSION         = readFile('VER1_VERSION.txt').trim()
                    env.VER2_VERSION         = readFile('VER2_VERSION.txt').trim()
                }
                echo "==========================================="
                echo "VERSION BUMP MODE"
                echo "Umbrella : ${env.NEW_UMBRELLA_VERSION}"
                echo "ver1     : ${env.VER1_VERSION}"
                echo "ver2     : ${env.VER2_VERSION}"
                echo "Tag      : ${env.NEW_TAG}"
                echo "==========================================="
                bat 'type versions.json'
            }
        }
        stage('Commit and Tag') {
            when {
                expression { return params.DEPLOY_VERSION == null || params.DEPLOY_VERSION.trim() == '' }
            }
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
                        git tag %NEW_TAG% || echo "Tag already exists skipping"
                        git push origin %NEW_TAG% || echo "Tag already pushed skipping"
                    '''
                }
            }
        }
    }
    post {
        success {
            script {
                if (params.DEPLOY_VERSION != null && params.DEPLOY_VERSION.trim() != '') {
                    echo "DEPLOY SUCCESS — vertotal v${params.DEPLOY_VERSION} deployed"
                    echo "ver1 v${env.DEPLOY_VER1} is running"
                    echo "ver2 v${env.DEPLOY_VER2} is running"
                } else {
                    echo "VERSION BUMP SUCCESS — tag ${env.NEW_TAG} created"
                }
            }
        }
        failure { echo "vertot pipeline FAILED" }
    }
}
