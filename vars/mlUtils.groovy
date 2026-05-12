
def PYTHON = '/home/dell/MLOPS2/venv/bin/python3'

def ingestData() {
    sh "${PYTHON} src/data_ingest.py"
}
def trainModel() {
    sh "${PYTHON} src/train.py"
}
def deployModel(String modelUri) {
    sh "${PYTHON} src/deploy_model.py '${modelUri}'"
}
def testModel(String modelUri) {
    sh "${PYTHON} src/test_model.py '${modelUri}'"
}
def registerModel(String alias) {
    def runId = readFile('run_id.txt').trim()
    sh "${PYTHON} src/register_model.py '${runId}' '${alias}'"
}
def loadModel(String alias) {
    sh "${PYTHON} src/load_model.py '${alias}'"
}
def updateAlias(String oldAlias, String newAlias) {
    def version = readFile('model_version.txt').trim()
    sh "${PYTHON} src/update_alias.py '${version}' '${oldAlias}' '${newAlias}'"
}
def getRunId() {
    return readFile('run_id.txt').trim()
}
