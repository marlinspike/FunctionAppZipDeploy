# Deploy a Function App with ZIP Deployment

## Start local storage emulator
`azurite --silent`

## Create Azure Resources

### Create resource group (if not already created)
az group create --name WebAppTest --location canadacentral

### Create storage account (required for Functions)
az storage account create \
    --name funcstore123unique \
    --location canadacentral \
    --resource-group WebAppTest \
    --sku Standard_LRS

### Create the Consumption Plan
az functionapp plan create \
    --resource-group WebAppTest \
    --name WebAppTestPlan \
    --location canadacentral \
    --number-of-workers 1 \
    --sku EP1 \
    --is-linux true

### Create the Function App
az functionapp create \
    --resource-group WebAppTest \
    --plan WebAppTestPlan \
    --runtime python \
    --runtime-version 3.11 \
    --functions-version 4 \
    --name WebAppTestFuncApp \
    --os-type linux \
    --storage-account funcstore123unique

## Deploy the Function App

### Zip the files (make sure you're in the function-app directory)
zip -r function_app.zip .

### Deploy using ZIP deploy
az functionapp deployment source config-zip \
    --resource-group WebAppTest \
    --name WebAppTestFuncApp \
    --src function_app.zip