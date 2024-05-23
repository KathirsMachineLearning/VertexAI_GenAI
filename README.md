# VertexAI_GenAI
export GOOGLE_CLOUD_PROJECT=fluid-dreamer-423211-s9
gcloud config set project fluid-dreamer-423211-s9

export GOOGLE_CLOUD_PROJECT=fluid-dreamer-423211-s9
export GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
gcloud auth login
gcloud config set project fluid-dreamer-423211-s9
gcloud auth configure-docker
docker build -t gcr.io/fluid-dreamer-423211-s9/csa .
docker push gcr.io/fluid-dreamer-423211-s9/csa

python model_dataflow.py --region us-central1 --runner DataflowRunner --project fluid-dreamer-423211-s9 --sdk_container_image gcr.io/fluid-dreamer-423211-s9/csa --sdk_location=container


export GOOGLE_CLOUD_PROJECT=exploregcp-422706
export GOOGLE_APPLICATION_CREDENTIALS=./exploregcp-422706-b1801cc53037.json
gcloud auth login
gcloud config set project exploregcp-422706
gcloud auth configure-docker
docker build -t gcr.io/exploregcp-422706/csa .
docker push gcr.io/exploregcp-422706/csa


python model_dataflow.py --region us-central1 --runner DataflowRunner --project exploregcp-422706 --sdk_container_image gcr.io/exploregcp-422706/csa --sdk_location=container