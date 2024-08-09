
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import BertTokenizerFast, BertForTokenClassification, BertForSequenceClassification
import torch
from typing import List, Dict

app = FastAPI()

# Model ve tokenizer'ları yükleme
ner_model = BertForTokenClassification.from_pretrained(r"C:\Users\dilai\OneDrive\Desktop\API\ner_model\ner_model")
ner_tokenizer = BertTokenizerFast.from_pretrained(r"C:\Users\dilai\OneDrive\Desktop\API\ner_model\ner_tokenizer")
sentiment_model = BertForSequenceClassification.from_pretrained(r"C:\Users\dilai\OneDrive\Desktop\API\sentiment_model\sentiment_model")
sentiment_tokenizer = BertTokenizerFast.from_pretrained(r"C:\Users\dilai\OneDrive\Desktop\API\sentiment_model\sentiment_tokenizer")


class Item(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    entity_list: List[str]
    results: List[Dict[str, str]]

@app.post("/predict", response_model=PredictionResponse)
async def predict(item: Item):
    text = item.text

    # Tokenizer ile metni tokenize etme
    ner_inputs = ner_tokenizer(text, return_tensors="pt", is_split_into_words=False)
    sentiment_inputs = sentiment_tokenizer(text, return_tensors="pt", is_split_into_words=False)

    # NER Tahmini Yapma
    with torch.no_grad():
        ner_outputs = ner_model(**ner_inputs)
        ner_predictions = torch.argmax(ner_outputs.logits, dim=2)
        ner_predictions = ner_predictions.squeeze().tolist()
    
    # Sentiment Analizi Yapma
    with torch.no_grad():
        sentiment_outputs = sentiment_model(**sentiment_inputs)
        sentiment_prediction = torch.argmax(sentiment_outputs.logits, dim=1).item()

    # NER Tahminlerini İşleme
    tokens = ner_tokenizer.convert_ids_to_tokens(ner_inputs['input_ids'][0])
    labels = [ner_model.config.id2label[label] for label in ner_predictions]

    entities = []
    current_entity = []
    current_label = None

    for token, label in zip(tokens, labels):
        if token in ['[CLS]', '[SEP]']:
            continue
        if label.startswith('B-') or (label.startswith('I-') and current_label != label[2:]):
            if current_entity:
                entities.append(" ".join(current_entity))
                current_entity = []
            current_entity.append(token)
            current_label = label[2:]
        elif label.startswith('I-') and current_label == label[2:]:
            current_entity.append(token)
        else:
            if current_entity:
                entities.append(" ".join(current_entity))
                current_entity = []
            current_label = None

    if current_entity:
        entities.append(" ".join(current_entity))


    # Sentiment etiketlerinin tanımlanması (örnek)
    sentiment_labels = {0: "olumsuz", 1: "nötr", 2: "olumlu"}  # Bu sadece bir örnektir
    sentiment = sentiment_labels.get(sentiment_prediction, "bilinmiyor")

    # Sonuçları Hazırlama
    result = {
        "entity_list": entities,
        "results": [
            {"entity": entity, "sentiment": sentiment}
            for entity in entities
        ]
    }
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7777)



