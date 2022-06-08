gcloud builds submit --tag gcr.io/cc-project-351909/streamlit-cc  --project=cc-project-351909

gcloud run deploy --image gcr.io/cc-project-351909/streamlit-cc --platform managed  --project=cc-project-351909 --allow-unauthenticated