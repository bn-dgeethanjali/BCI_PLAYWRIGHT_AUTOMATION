// Jenkins CI/CD Pipeline for BCI Playwright MCP Automation
// Runs UI tests using Playwright MCP Server

pipeline {
    agent any

    parameters {
        choice(
            name: 'PROJECT',
            choices: ['rulegenai', 'mailxray', 'all'],
            description: 'Select project to test'
        )
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'prod'],
            description: 'Select environment'
        )
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'login', 'workspace', 'rule_generation', 'rules_management'],
            description: 'Select test suite to run'
        )
        booleanParam(
            name: 'HEADLESS',
            defaultValue: true,
            description: 'Run in headless mode'
        )
    }

    environment {
        PYTHON_VERSION = '3.9'
        USE_MCP = 'true'
        MCP_PROJECT = "${params.PROJECT}"
        HEADLESS = "${params.HEADLESS}"

        // Credentials from Jenkins Credentials Store
        RULEGENAI_USERNAME = credentials('rulegenai-username')
        RULEGENAI_PASSWORD = credentials('rulegenai-password')
    }

    options {
        timeout(time: 60, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        ansiColor('xterm')
    }

    stages {
        // ============================================
        // Stage: Setup
        // ============================================
        stage('Setup') {
            steps {
                script {
                    echo "🚀 Setting up BCI Playwright MCP Tests"
                    echo "Project: ${params.PROJECT}"
                    echo "Environment: ${params.ENVIRONMENT}"
                    echo "Test Suite: ${params.TEST_SUITE}"
                }

                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest-html pytest-xdist allure-pytest
                    playwright install chromium
                    playwright install-deps chromium
                '''

                sh '''
                    mkdir -p screenshots/${MCP_PROJECT}
                    mkdir -p reports/${MCP_PROJECT}
                    mkdir -p allure-results
                '''
            }
        }

        // ============================================
        // Stage: Lint
        // ============================================
        stage('Lint') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pip install flake8 black
                    flake8 tests/ pages/ mcp/ --max-line-length=120 --ignore=E501,W503 || true
                    black --check tests/ pages/ mcp/ --line-length=120 || true
                '''
            }
        }

        // ============================================
        // Stage: Run Tests
        // ============================================
        stage('Run Tests') {
            steps {
                script {
                    def testPath = "tests/ui/${params.PROJECT}/"

                    if (params.TEST_SUITE != 'all') {
                        testPath = "tests/ui/${params.PROJECT}/test_${params.TEST_SUITE}.py"
                    }

                    sh """
                        . .venv/bin/activate

                        pytest ${testPath} \\
                            -v \\
                            --tb=short \\
                            --html=reports/${params.PROJECT}/report.html \\
                            --self-contained-html \\
                            --junitxml=reports/${params.PROJECT}/junit.xml \\
                            --alluredir=allure-results \\
                            -n auto \\
                            || true
                    """
                }
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: "reports/${params.PROJECT}/junit.xml"
                }
            }
        }

        // ============================================
        // Stage: Generate Allure Report
        // ============================================
        stage('Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    post {
        always {
            // Archive artifacts
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'screenshots/**/*', allowEmptyArchive: true

            // Publish HTML report
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: "reports/${params.PROJECT}",
                reportFiles: 'report.html',
                reportName: 'Playwright Test Report',
                reportTitles: 'BCI Playwright MCP Test Results'
            ])

            // Clean workspace
            cleanWs()
        }

        success {
            echo '✅ Tests completed successfully!'

            // Slack notification (if configured)
            // slackSend(
            //     channel: '#test-automation',
            //     color: 'good',
            //     message: "✅ BCI Playwright Tests PASSED\nProject: ${params.PROJECT}\nBuild: ${env.BUILD_URL}"
            // )
        }

        failure {
            echo '❌ Tests failed!'

            // Slack notification (if configured)
            // slackSend(
            //     channel: '#test-automation',
            //     color: 'danger',
            //     message: "❌ BCI Playwright Tests FAILED\nProject: ${params.PROJECT}\nBuild: ${env.BUILD_URL}"
            // )
        }
    }
}
