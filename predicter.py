from pymongo import MongoClient
from dotenv import load_dotenv
import os
import random

load_dotenv()

uri = os.getenv("MONGODB_URI")

client = MongoClient(uri)

db = client["predicter"]

themes = db["themes"]
instructions = db["instructions"]
questions = db["generated_questions"]


def database():
    if themes.count_documents({}) == 0:
        themes.insert_many([
            {
                "theme": "Confidentiality",
                "actors": [
                    "a senior advocate practising in Nairobi",
                    "a newly admitted advocate",
                    "a partner in a commercial law firm"
                ],
                "clients": [
                    "a political candidate",
                    "a foreign investor",
                    "a high-profile businesswoman"
                ],
                "conduct": [
                    "disclosed confidential information to a journalist",
                    "shared privileged documents with a third party",
                    "discussed the client's matter on a public platform"
                ],
                "aggravation": [
                    "without the client's consent",
                    "while the matter was pending before court",
                    "after receiving express instructions to the contrary"
                ]
            },
            {
                "theme": "Conflict of Interest",
                "actors": [
                    "an advocate acting in a conveyancing transaction",
                    "a litigation advocate",
                    "a law firm partner"
                ],
                "clients": [
                    "two parties to the same transaction",
                    "a former client",
                    "a company in which the advocate has an interest"
                ],
                "conduct": [
                    "acted for both sides in the transaction",
                    "represented a client against a former client",
                    "continued acting despite a personal financial interest"
                ],
                "aggravation": [
                    "without making full disclosure",
                    "despite objections raised by the affected party",
                    "while deriving financial benefit"
                ]
            },
            {
                "theme": "Duty to Court",
                "actors": [
                    "an advocate appearing before the High Court",
                    "counsel in a constitutional petition",
                    "an advocate in a commercial dispute"
                ],
                "clients": [
                    "a litigant before the court",
                    "a corporate client",
                    "a public body"
                ],
                "conduct": [
                    "failed to disclose material facts to the court",
                    "filed pleadings containing false information",
                    "misrepresented facts during oral submissions"
                ],
                "aggravation": [
                    "leading to the grant of interim orders",
                    "causing prejudice to the opposing party",
                    "resulting in delay of justice"
                ]
            },
            {
                "theme": "Client Funds",
                "actors": [
                    "an advocate handling settlement funds",
                    "a sole practitioner",
                    "a partner in a law firm"
                ],
                "clients": [
                    "a client entitled to settlement proceeds",
                    "a beneficiary of a transaction",
                    "a former client"
                ],
                "conduct": [
                    "deposited client funds into a personal account",
                    "delayed remittance of client money",
                    "failed to keep proper books of account"
                ],
                "aggravation": [
                    "without reasonable explanation",
                    "despite repeated demands by the client",
                    "contrary to the Advocates Accounts Rules"
                ]
            }
        ])

    if instructions.count_documents({}) == 0:
          instructions.insert_many([
            {
                "type": "analysis",
                "text": "Identify and discuss the ethical issues arising from the advocate’s conduct",
                "support": [
                    "with reference to the Advocates Act",
                    "with reference to the LSK Code of Conduct",
                    "using relevant legal principles"
                ],
                "marks": [8, 10, 12]
            },
            {
                "type": "procedure",
                "text": "Explain the disciplinary process that may be instituted against the advocate",
                "support": [
                    "including the role of the Advocates Complaints Commission",
                    "including the role of the Advocates Disciplinary Tribunal",
                    "outlining possible sanctions"
                ],
                "marks": [8, 10]             }
        ])
           
def scenario(theme):
    actor = random.choice(theme["actors"])
    client = random.choice(theme["clients"])
    conduct = random.choice(theme["conduct"])
    aggravation = random.choice(theme["aggravation"])
    return (
        f"{actor} acts for {client}. "
        f"During the course of the representation, the advocate {conduct} "
        f"{aggravation}."
    )

def build_instruction(item):
    support1, support2 = random.sample(item["support"], 2)
    marks = random.choice(item["marks"])
    return f"{item['text']} {support1} and {support2}. ({marks} marks)"

def generate_question():
    theme_list = list(themes.find())
    instruction_list = list(instructions.find())
    theme_a, theme_b = random.sample(theme_list, 2)
    scenario_a = scenario(theme_a)
    scenario_b = scenario(theme_b)
    part_a = build_instruction(random.choice(instruction_list))
    part_b = build_instruction(random.choice(instruction_list))

    question = (
        "QUESTION ONE - PROFESSIONAL ETHICS\n\n"
        f"{scenario_a}\n\n"
        f"Further, it later emerged that the same advocate also {scenario_b.lower()}\n\n"
        f"(a) {part_a}\n\n"
        f"(b) {part_b}"
    )
    return {
        "year": 2026,
        "themes": [theme_a["theme"], theme_b["theme"]],
        "question": question
    }

def generate_questions():
    output = []
    for _ in range(4):
        q = generate_question()
        questions.insert_one(q)
        output.append(q["question"])
    return output


if __name__ == "__main__":
    database()
    questions = generate_questions()

    for i in range(len(questions)):
     print(f"PROBABLE QUESTION {i + 1}")
     print(questions[i])
