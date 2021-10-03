from __future__ import unicode_literals, print_function
import plac
from spacy.pipeline import EntityRuler
import random
from pathlib import Path
import spacy
from tqdm import tqdm
from spacy.training import Example

TRAIN_DATA = [
    ('from JFK', {'entities': [(0, 8, 'fromAIRPORT')]}),
    ('from EWR', {'entities': [(0, 8, 'fromAIRPORT')]}),
    ('from SXF', {'entities': [(0, 8, 'fromAIRPORT')]}),
    ('from ERF', {'entities': [(0, 8, 'fromAIRPORT')]}),
    ('from CGN', {'entities': [(0, 8, 'fromAIRPORT')]}),
    ('from MUC', {'entities': [(0, 8, 'fromAIRPORT')]}),
    ('from NUE', {'entities': [(0, 8, 'fromAIRPORT')]}),
    ('from JFK', {'entities': [(0, 8, 'fromAIRPORT')]}),
    ('to JFK', {'entities': [(0, 6, 'toAIRPORT')]}),
    ('to EWR', {'entities': [(0, 6, 'toAIRPORT')]}),
    ('to SXF', {'entities': [(0, 6, 'toAIRPORT')]}),
    ('to ERF', {'entities': [(0, 6, 'toAIRPORT')]}),
    ('to CGN', {'entities': [(0, 6, 'toAIRPORT')]}),
    ('to MUC', {'entities': [(0, 6, 'toAIRPORT')]}),
    ('to JFK', {'entities': [(0, 6, 'toAIRPORT')]}),

    ('I want to fly', {'entities': [(0, 13, 'request')]}),
    ('I want to go', {'entities': [(0, 12, 'request')]}),
    ('I would like to book a flight', {'entities': [(0, 29, 'request')]}),
    ('I would like to fly', {'entities': [(0, 19, 'request')]}),
    ('Show me a flight path options', {'entities': [(0, 29, 'request')]}),
    ('give me flight options', {'entities': [(0, 22, 'request')]}),
    ('what are the flights', {'entities': [(0, 20, 'request')]}),
    ('Find me flights from', {'entities': [(0, 20, 'request')]}),

    ('Find me flights from NUE to CGN', {'entities': [(0, 15, 'request'), (16, 24, 'fromAIRPORT'),(25, 31, 'toAIRPORT')]}),
    ('Find me flights from EWR to MUC', {'entities': [(0, 15, 'request'),(16, 24, 'fromAIRPORT'),(25, 31, 'toAIRPORT')]}),
    ('I would like to fly from JFK to SXF', {'entities': [(0, 19, 'request'), (20, 28, 'fromAIRPORT'),(29, 35, 'toAIRPORT')]}),
    ('I would like to fly from MUC to CGN', {'entities': [(0, 19, 'request'), (20, 28, 'fromAIRPORT'),(29, 35, 'toAIRPORT')]}),
    ('I want to go from ERF to EWR', {'entities': [(0, 12, 'request'),(13, 21, 'fromAIRPORT'),(22, 28, 'toAIRPORT')]}),
    ('I want to go from NUE to JFK', {'entities': [(0, 12, 'request'),(13, 21, 'fromAIRPORT'),(22, 28, 'toAIRPORT')]}),
    ('Show me a flight path options from CGN to JFK', {'entities': [(0, 29, 'request'),(30, 38, 'fromAIRPORT'), (39, 45, 'toAIRPORT')]}),
    ('Show me a flight path options from MUC to SXF', {'entities': [(0, 29, 'request'), (30, 38, 'fromAIRPORT'), (39, 45, 'toAIRPORT')]}),
]
model = None
output_dir = Path(r"C:\Users\Tal\PycharmProjects\FlaskSustainabilityProject\SustainabilityWebsite")
n_iter = 100

# load the model

if model is not None:
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
else:
    nlp = spacy.blank('en')
    print("Created blank 'en' model")

print(nlp.pipe_names)
if 'ner' not in nlp.pipe_names:
    ner = nlp.add_pipe('ner', last=True)
else:
    ner = nlp.get_pipe('ner')

for _, annotations in TRAIN_DATA:
    print(annotations)
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])


other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.begin_training()
    for itn in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        from spacy.training.example import Example
        #pycharm/audiotools/venv/lib/python3.6

        for batch in spacy.util.minibatch(TRAIN_DATA, size=3):
            for text, annotations in batch:
                # create Example
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                # Update the model
                nlp.update([example], losses=losses, drop=0.3)

for text, _ in TRAIN_DATA:
    doc = nlp(text)
    print('Entities', [(ent.text, ent.label_) for ent in doc.ents])

if output_dir is not None:
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.meta['name'] = 'model5'  # rename model
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)

    test_text = 'I would like to fly to BTC from OKC'
    # Test the saved model
    print("Loading from", output_dir)
    nlp2 = spacy.load(output_dir)
    doc2 = nlp2(test_text)
    for ent in doc2.ents:
        print(ent.label_, ent.text)

