$PROJECT_ID = "agentic-ecommerce-ai"
$REGION = "us-central1"
$INDEX_ID = "9176535040534773760"
$ENDPOINT_ID = "6715757648827908096"
$DEPLOYED_INDEX_ID = "ecommerce_rag_deployed_v2"
$VECTOR_DATA_URI = "gs://agentic-ecommerce-ai/vector_data"

Write-Host "Project: $PROJECT_ID"
Write-Host "Region: $REGION"
Write-Host "Endpoint: $ENDPOINT_ID"
Write-Host "Index: $INDEX_ID"
Write-Host "Deployed Index ID: $DEPLOYED_INDEX_ID"
Write-Host ""

$confirm = Read-Host "Undeploy the deployed index from the endpoint? (yes/no)"
if ($confirm -eq "yes") {
    gcloud ai index-endpoints undeploy-index $ENDPOINT_ID `
      --deployed-index-id=$DEPLOYED_INDEX_ID `
      --region=$REGION `
      --project=$PROJECT_ID
}

$confirm = Read-Host "Delete the Vertex AI index endpoint? (yes/no)"
if ($confirm -eq "yes") {
    gcloud ai index-endpoints delete $ENDPOINT_ID `
      --region=$REGION `
      --project=$PROJECT_ID
}

$confirm = Read-Host "Delete the Vertex AI index? (yes/no)"
if ($confirm -eq "yes") {
    gcloud ai indexes delete $INDEX_ID `
      --region=$REGION `
      --project=$PROJECT_ID
}

$confirm = Read-Host "Delete the GCS vector_data folder at $VECTOR_DATA_URI ? (yes/no)"
if ($confirm -eq "yes") {
    gcloud storage rm --recursive $VECTOR_DATA_URI
}

$confirm = Read-Host "Remove Firestore delete protection and delete Firestore database? (yes/no)"
if ($confirm -eq "yes") {
    gcloud firestore databases update --database="(default)" `
      --no-delete-protection `
      --project=$PROJECT_ID

    gcloud firestore databases delete --database="(default)" `
      --project=$PROJECT_ID
}

$confirm = Read-Host "Disable Vertex AI, Firestore, and Storage APIs? (yes/no)"
if ($confirm -eq "yes") {
    gcloud services disable aiplatform.googleapis.com --project=$PROJECT_ID
    gcloud services disable firestore.googleapis.com --project=$PROJECT_ID
    gcloud services disable storage.googleapis.com --project=$PROJECT_ID
}

Write-Host ""
Write-Host "Cleanup flow finished."
