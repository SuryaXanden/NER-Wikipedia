# -*- coding: utf-8 -*-
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag
import wikipedia as wiki
from flask import Flask, render_template, request, jsonify
# from werkzeug import secure_filename
import re, json

def get_from_wiki(item):
    item = item.strip()
    item = re.sub(r"\W", ' ', item, 0, re.MULTILINE)

    answers = {"summary" : "", "desc": ""}
    try:
        summary = wiki.summary(item)
        sentence = nltk.sent_tokenize(summary)
        one_sentence = sentence[0].lower()

        # XS regex BEGIN
        regex_to_remove_anything_within_brackets = r"\s?(\(.*\)|(\{.*\})|(\<.*\>)|(\[.*\]))\s?"
        one_sentence = re.sub(regex_to_remove_anything_within_brackets, ' ', one_sentence, 0, re.MULTILINE)
        # XS regex END
        
        # print("Summary:")
        # print(one_sentence)
        # print()
        answers["summary"] = one_sentence

        one_sentence = nltk.word_tokenize(one_sentence)
        one_sentence = nltk.pos_tag(one_sentence)

        # NLTK regex
        nltk_pattern = """segment: {<DT><JJ>+<NN>+}"""

        cp = nltk.RegexpParser(nltk_pattern)
        cs = cp.parse(one_sentence)

        # # print(cs)
        # # print()

        # Tag 1 whole sentence
        pos_tagged_words = []
        chunks = []
        for i in cs:
            if type(i) == nltk.tree.Tree:
                chunks += [ list(t) for t in i ]
            else:
                pos_tagged_words.append(list(i))

        # print("Found chunk:")
        # print(chunks)

        chunked_nns  = [ i for i in chunks if i[1] == "NN"  ]
        # for i in chunked_nns:
            # print(i[0], end=" ")
            
        desc = " ".join(i[0] for i in chunked_nns)

        # print(desc)
        answers["desc"] = desc

        # # # print()
        # # # filtered_nns = [ i for i in pos_tagged_words if i[1] == "NN"  ]
        # # # chunked_nns  = [ i for i in chunks if i[1] == "NN"  ]
        # # # # chunked_dts  = [ i for i in chunks if i[1] == "DT"  ]
        
        # # # # final: DT     NN
        # # # # final_dt = chunked_dts[0][0]
        # # # final_nn = ''

        # # # for i in range(len(filtered_nns)):
        # # #     if filtered_nns[i][0] == "company":
        # # #         final_nn = chunked_nns[0][0]
        # # #         break
        # # # else:
        # # #     final_nn = ""

        # # # # actions before printing
        # # # print(item,":", final_nn)
        # # # # print(item,":",final_dt , final_nn)
        return answers
        # return json.dumps(answers)

    except:
        print("In except block")
        # print(json.dumps({"summary" : "", "desc": ""}))
        return '' 
        # return jsonify({"summary" : "", "desc": ""})


# while 1:
#     item = input("\nEnter a search word or 'exit' to exit: ") or ''
#     item = item.lower() or ''
#     if item.lower() == 'exit':
#         exit()
#     elif len(item)>2:
#             get_from_wiki(item)

app = Flask(__name__)

@app.route('/')#, methods = ['GET'])
def index():
    if request.args.get("q"):
        item = request.args.get("q")
        # print("Query: ",item)
        with open("inputs.txt",'a') as f:
            f.write(str(item) + '\n')
        answers = get_from_wiki(item)
        # return answers
        if answers:
            return jsonify(answers)
        else:
            return jsonify({"summary" : "", "desc": ""})

    else:    
        return render_template('index.html')

if __name__ == "__main__":
    # app.run(debug=True,threaded= True, port="80")
    app.run(host='0.0.0.0', port=80,debug=False,threaded=True)