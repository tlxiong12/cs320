import json
import zipfile
import csv
from io import TextIOWrapper

f = open("banks.json")
data = f.read()
f.close()


def load_bank_data():
    banks = json.load(open("banks.json"))
    return {bank['name']: {'lei': bank['lei'], 'count': bank['count'], 'period': bank['period']} for bank in banks}
#banks = json.load(open("banks.json"))
bank_data = load_bank_data()


race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "5": "White",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander"
}
class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            if r in race_lookup:
                self.race.add(race_lookup[r])
                # self.race.add(r)
            else:
                continue

                
    def __repr__(self):
        return f"Applicant('{self.age}', {sorted(self.race)})"

    def lower_age(self):
        return int(self.age.replace('<', '').replace('>', '').split('-')[0])
                   
    def __lt__(self, other):
        return Applicant.lower_age(self) < Applicant.lower_age(other)
                   
class Loan:
    def __init__(self, values):
        self.loan_amount = self.float_extract(values["loan_amount"])
        self.property_value = self.float_extract(values["property_value"])
        self.interest_rate = self.float_extract(values["interest_rate"])

        self.applicants = []
        applicant_age = values['applicant_age']
        applicant_races = [values[key] for key in values if key.startswith('applicant_race-')]
        self.applicants.append(Applicant(applicant_age, applicant_races))
            
        if values.get('co-applicant_age') != '9999':
            co_applicant_age = values['co-applicant_age']
            co_applicant_races = [values[key] for key in values if key.startswith('co-applicant_race-')]
            self.applicants.append(Applicant(co_applicant_age, co_applicant_races))
                   
                   
    def float_extract(self, string):
        if string == "NA" or string == "Exempt":
            return -1.0
        else:
            try:
                return float(string)
            except ValueError:
                return -1.0
                   
    def __str__(self):
        return f"<Loan: {self.interest_rate:.1f}% on ${self.loan_amount:.1f} with {len(self.applicants)} applicant(s)>"
                   
    def __repr__(self):
        return self.__str__()
                   
    def yearly_amounts(self, yearly_payment):
        assert self.interest_rate > 0
        assert self.loan_amount > 0

        amt = self.loan_amount
        while amt > 0:
            yield amt
            interest = amt * (self.interest_rate / 100)
            amt += interest
            amt -= yearly_payment
            
class Bank:
    def __init__(self, name):
        self.lei = bank_data[name]["lei"]
        self.loan_list = []
        self.load_loans()
        # self.name = name
        # for bank in banks:
        #     if bank["name"] == self.name:
        #         self.loan_list.append(bank)
                
    def load_loans(self):
        with zipfile.ZipFile('wi.zip', 'r') as zip_ref:
            with zip_ref.open('wi.csv') as loan_file:
                with TextIOWrapper(loan_file, encoding = 'utf-8') as text_file:
                    csv_reader = csv.DictReader(text_file)
                    for row in csv_reader:
                        if row['lei'] == self.lei:
                            loan = Loan(row)
                            self.loan_list.append(loan)
        
        
    def __len__(self):
        return len(self.loan_list)
    
    def __getitem__(self, idx):
        return self.loan_list[idx]

            
            
# class Bank:
#     def __init__(self, name):
#         self.lei = banks[name]["lei"]
#         self.loan_list = []
#         self.load_loans()
    
#     def __getitem__(self, idx):
#         return self.loan_list[idx]
    
#     def __len__(self):
#         return len(self.loan_list)
