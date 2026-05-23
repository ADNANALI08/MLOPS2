// @Library('mlops-shared-lib') _

node {
    // Step 1: Secure a workspace and pull latest code
    checkout scm
    def jenkinsfile_to_load = ""

    // Step 2: Set the correct file mapping based on the active branch
    if (env.BRANCH_NAME == 'dev') {
        jenkinsfile_to_load = "Jenkinsfile.dev"
    } else if (env.BRANCH_NAME == 'main') {
        jenkinsfile_to_load = "Jenkinsfile.preprod"
    } else if (env.TAG_NAME?.startsWith('v')) {
        jenkinsfile_to_load = "Jenkinsfile.prod"
    } else {
        currentBuild.result = 'ABORTED'
        error("No pipeline defined for branch: ${env.BRANCH_NAME}")
    }

    // Step 3: Safely execute the sub-pipeline file within this workspace
    load jenkinsfile_to_load
}