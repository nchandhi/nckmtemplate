@description('Specifies the location for resources.')
param solutionName string 
param solutionLocation string
@secure()
param azureOpenAIApiKey string
param azureOpenAIApiVersion string
param azureOpenAIEndpoint string
@secure()
param azureSearchAdminKey string
param azureSearchServiceEndpoint string
param azureSearchIndex string
param sqlServerName string
param sqlDbName string
param sqlDbUser string
@secure()
param sqlDbPwd string
// param managedIdentityObjectId string

var functionAppName = '${solutionName}-rag-fn'
var storageaccountname = '${solutionName}ragfnacc'
var dockerImage = 'DOCKER|kmcontainerreg.azurecr.io/km-rag-function:citationfunc'
var environmentName = '${solutionName}-rag-fn-env'

// var sqlServerName = 'nc2202-sql-server.database.windows.net'
// var sqlDbName = 'nc2202-sql-db'
// var sqlDbUser = 'sqladmin'
// var sqlDbPwd = 'TestPassword_1234'

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageaccountname
  location: resourceGroup().location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
  }
}

resource managedenv 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: environmentName
  location: solutionLocation
  properties: {
    zoneRedundant: false
    kedaConfiguration: {}
    daprConfiguration: {}
    customDomainConfiguration: {}
    workloadProfiles: [
      {
        workloadProfileType: 'Consumption'
        name: 'Consumption'
      }
    ]
    peerAuthentication: {
      mtls: {
        enabled: false
      }
    }
    peerTrafficConfiguration: {
      encryption: {
        enabled: false
      }
    }
  }
}

resource azurefn 'Microsoft.Web/sites@2023-12-01' = {
  name: functionAppName
  location: solutionLocation
  kind: 'functionapp,linux,container,azurecontainerapps'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    siteConfig: {
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount};EndpointSuffix=core.windows.net'
        }
        {
          name: 'PYTHON_ENABLE_INIT_INDEXING'
          value: '1'
        }
        {
          name: 'PYTHON_ISOLATE_WORKER_DEPENDENCIES'
          value: '1'
        }
        {
          name: 'SQLDB_DATABASE'
          value: sqlDbName
        }
        {
          name: 'SQLDB_PASSWORD'
          value: sqlDbPwd
        }
        {
          name: 'SQLDB_SERVER'
          value: sqlServerName
        }
        {
          name: 'SQLDB_USERNAME'
          value: sqlDbUser
        }
        {
          name: 'AZURE_OPEN_AI_ENDPOINT'
          value: azureOpenAIEndpoint
        }
        {
          name: 'AZURE_OPEN_AI_API_KEY'
          value: azureOpenAIApiKey
        }
        {
          name: 'OPENAI_API_VERSION'
          value: azureOpenAIApiVersion
        }
        {
          name: 'AZURE_OPEN_AI_DEPLOYMENT_MODEL'
          value: 'gpt-4o-mini'
        }
        {
          name: 'AZURE_AI_SEARCH_ENDPOINT'
          value: azureSearchServiceEndpoint
        }
        {
          name: 'AZURE_AI_SEARCH_API_KEY'
          value: azureSearchAdminKey
        }
        {
          name: 'AZURE_AI_SEARCH_INDEX'
          value: azureSearchIndex
        }
      ]
      linuxFxVersion: dockerImage
      functionAppScaleLimit: 10
      minimumElasticInstanceCount: 0
    }
    managedEnvironmentId: managedenv.id
    workloadProfileName: 'Consumption'
    resourceConfig: {
      cpu: 1
      memory: '2Gi'
    }
    storageAccountRequired: false
  }
}

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().id, resourceGroup().id, azurefn.id, 'StorageBlobDataContributor')
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe') // Storage Blob Data Contributor
    principalId: azurefn.identity.principalId
  }
}


