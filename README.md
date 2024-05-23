# VertexAI_GenAI
export GOOGLE_CLOUD_PROJECT=fluid-dreamer-423211-s9
gcloud config set project fluid-dreamer-423211-s9


export GOOGLE_CLOUD_PROJECT=exploregcp-422706
export GOOGLE_APPLICATION_CREDENTIALS=./exploregcp-422706-b1801cc53037.json
gcloud auth login
gcloud config set project exploregcp-422706
gcloud auth configure-docker
docker build -t gcr.io/exploregcp-422706/csa .
docker push gcr.io/exploregcp-422706/csa