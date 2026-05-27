import math
from dataclasses import dataclass
import pandas as pd

@dataclass
class Document:
    title: str
    body: str

# Vector Space Indexer
class Indexer:
    def magnitude(self, concordance):
        if type(concordance) != dict:
            raise ValueError("Argument must be of type dict")
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)
    def relation(self, concordance1, concordance2):
        if type(concordance1) != dict or type(concordance2) != dict:
            raise ValueError("Arguments must be of type dict")
        relevance = 0
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        if (self.magnitude(concordance1) * self.magnitude(concordance2)) != 0:
            return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))
        else:
            return 0
    def concordance(self, document):
        if type(document) != str:
            raise ValueError("Argument must be of type string")
        con = {}
        for word in document.split(' '):
            if word in con:
                con[word] = con[word] + 1
            else:
                con[word] = 1

        return con
    def search(self, documents, search_term):
        matches = []

        for i in range(len(documents)):
            relation = self.relation(
                self.concordance(search.lower()),
                self.concordance(documents[i].body.lower())
            )
            if relation != 0:
                matches.append((relation, documents[i]))

        return matches
        

# Process Documents
df = pd.read_csv("documents.csv")
documents = [
    Document(
        row["title"].replace("\n", " "),
        row["body"].replace("\n", " ").strip()
    )
    for _, row in df.iterrows()
]


indexer = Indexer()

search = input("Search: ")

matches = indexer.search(documents, search)


if len(matches) > 0:
    if len(matches) > 5:
        print(f"\nShowing Top 5 out of {len(matches)}:")
    else:
        print(f"\nShowing {len(matches)} results:")
    
    matches.sort(key=lambda x: x[0], reverse=True)
    for i in range(len(matches[:5])):
        line = f"{i + 1}: {matches[i][1].title} [Relevance: {round(matches[i][0] * 100, 2)}%]"
        line_length = len(line) + 1
        print("-" * line_length)
        print(line)
        print("-" * line_length)
else:
    print("\nNo Results!")