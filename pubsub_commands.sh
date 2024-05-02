-- gcloud commands 
gcloud pubsub topics create labtopic2
gcloud pubsub topics list
gcloud pubsub subscriptions create --topic labtopic2 labtopic2sub1
gcloud pubsub subscriptions list

gcloud pubsub topics publish labtopic2 --message="How are you?"
gcloud pubsub topics publish labtopic2 --message="How are you 2?"
gcloud pubsub topics publish labtopic2 --message="How are you 3?"

gcloud pubsub subscriptions pull labtopic2sub1 --auto-ack --limit 3

gcloud pubsub subscriptions delete labtopic2sub1
gcloud pubsub topics delete labtopic2
