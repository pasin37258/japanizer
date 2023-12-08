import openai
import streamlit as st
import json
import pandas as pd

user_api_key = st.sidebar.text_input("OpenAI API key", type="password")
client = openai.OpenAI(api_key=user_api_key)
prompt = """
            Act as Japanese linguist. You will recieve a Japanese sentence which may contains with hiragana(ひらがな), katakana(カタカナ), and kanji(漢字).
            You have four main tasks to do. 
            List all of your answers in a JSON object, one answer per line.
            These are your tasks:
            1) Translate the sentence:
            1.1 Give me three possible Japanese to English translated sentences.
            1.2 List all of the Japanese words/vocabulary that found in the sentence and follow this instruction:
            - If the word is kanji, give me a furigana(ふりがな)
            - Give a English meaning for each Japanese word.
            - Give a part of speech of each word. If the word is adjective, you need to tell if it i-adjective(い形容詞) or na-adjective(な形容詞). 
            If the word is verb, you need to tell if it transitive verb(他動詞) or intransitive verb(自動詞)
            2) Analyze the sentence:
            2.1 Analyze the grammar of sentence. List grammar which used in the sentence and explain why the sentence used each grammar.
            2.2 Analyze the word form/conjugation which used in the sentence whether verb, adjective or noun. List what form is it and why the sentence used each form.
            2.3 Analyze the Japanese particles(助詞) which used in the sentence. List the particles and explain why the sentence used each particle.
            3) List the kanji from the sentence:
            3.1 List all of kanji found in the sentence. For each kanji follow this instruction:
            - Kanji has it own meaning. So, give me each kanji meaning.
            - Give me each kanji stroke count.
            - Kanji has many way to read and can be consist with other kanji. So, give me kun-yomi(訓読み) and on-yomi(音読み).
            - Give me five examples of word that has each kanji consisted, ordered by word frequency, give me a furigana and give me meaning of each word.
            4) Write a short example conversation use the sentence given. Conversation is between Aさん and Bさん.
            -Give a furigana(ふりがな) and translate the written conversation to English.

            Give all of your answers in a JSON object which contains following keys:
            "Translation": {"Translations" (1.1), "Vocabulary" (1.2): [{"Word", "Furigana", "Meaning", "Part of Speech"}]},
            "Analysis" (2): {"Grammar" (2.1), "Conjugation" (2.2), "Particles" (2.3)},
            "Kanji" (3): [{"Kanji" (3.1), "Meaning", "Stroke Count", "Kun-yomi", "On-yomi", "Examples": [{"Word", "Furigana", "Meaning"}]}],
            "Example" (4): {"Conversation", "Furigana", "Translation"}
        """

st.title('Japanizer')
caption = """This website can help you learn advanced Japanese from just one Japanese sentence.
            The AI will give you results that contains
            3 possible English translations, Vocabulary, Grammar, Kanji, and Example conversation."""
st.markdown(caption)

user_input = st.text_area("Enter Japanese text:", "日本語")

submit_button = st.button("Submit")

if submit_button:
    messages_so_far = [
        {"role": "system", "content": prompt},
        {'role': 'user', 'content': user_input},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_so_far
    )
    answer_dictionary = response.choices[0].message.content

    ad = json.loads(answer_dictionary)
    print (ad)

    translations = ad["Translation"]["Translations"]
    print(translations)
    st.markdown('**English translations:**')
    st.table(translations)

    vocab = ad["Translation"]["Vocabulary"]
    print(vocab)
    st.markdown('**Vocabulary:**')
    vocab_df = pd.DataFrame.from_dict(vocab)
    print(vocab_df)
    st.table(vocab_df)

    grammar = ad["Analysis"]["Grammar"]
    print(grammar)
    st.markdown('**Grammar:**')
    st.table(grammar)

    conjugation = ad["Analysis"]["Conjugation"]
    print(conjugation)
    st.markdown('**Conjugation:**')
    st.table(conjugation)

    particles = ad["Analysis"]["Particles"]
    print(particles)
    st.markdown('**Particles:**')
    st.table(particles)

    kanji = ad["Kanji"]
    print(kanji)
    st.markdown('**Kanji:**')
    kanji_df = pd.DataFrame.from_dict(kanji)
    print(kanji_df)
    st.table(kanji_df)

    example_con = ad["Example"]["Conversation"]
    print(example_con)
    furigana_con = ad["Example"]["Furigana"]
    print(furigana_con)
    trans_con = ad["Example"]["Translation"]
    print(trans_con)
    st.markdown('**Example conversation:**')
    st.table(example_con, furigana_con, trans_con)
