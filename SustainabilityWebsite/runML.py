import spacy

def runML(output_dir, test_text):
    # Test the saved model
    print("Loading from", output_dir)
    nlp2 = spacy.load(output_dir)
    doc2 = nlp2(test_text)
    list = []
    for ent in doc2.ents:
        list.append([ent.label_, ent.text])

    return(list)


