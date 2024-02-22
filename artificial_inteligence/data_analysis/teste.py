import spacy

# Carrega o modelo de linguagem
nlp = spacy.load("pt_core_news_sm")

# Texto para análise
texto = "Esta sala comercial localiza-se no centro de Niterói, desfrutando de uma posição estratégica e conveniente. Com amplas janelas que permitem a entrada de luz natural, o espaço é arejado e proporciona uma atmosfera agradável para trabalho. Os acabamentos modernos e o design funcional garantem uma aparência profissional. Além disso, a proximidade a serviços essenciais e o fácil acesso a transportes públicos fazem deste local uma escolha ideal para negócios. Entre em contato e agendamos uma visita na Davi Saramago -"

# Processa o texto
doc = nlp(texto)

# Reconhecimento de Entidades Nomeadas (NER)
for ent in doc.ents:
    print(ent.text, ent.label_)
    print(ent.sentiment)

# Tokenização e análise de POS (Part-of-Speech)
for token in doc:
    print(token.text, token.lemma_, token.pos_)
