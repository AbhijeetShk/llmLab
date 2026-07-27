from worker import ModelWorker

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

worker = ModelWorker(MODEL_NAME)

response = worker.generate(
    "Explain Retrieval Augmented Generation."
)

print(response)