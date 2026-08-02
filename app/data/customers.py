import random

FIRST_NAMES = [
    "Sipho", "Lebo", "Thabo", "Ayesha", "Naledi",
    "Zanele", "Kagiso", "Mpho", "Peter", "Sarah",
    "John", "Lerato", "Nandi", "Brian", "Tshepo"
]

LAST_NAMES = [
    "Dlamini", "Mokoena", "Nkosi", "Smith",
    "Naidoo", "Pillay", "Van Wyk", "Botha",
    "Mthembu", "Mabaso", "Molefe", "Jacobs"
]

BANKS = [
    "Capitec",
    "Standard Bank",
    "FNB",
    "Nedbank",
    "Absa"
]

PROVINCES = {
    "Gauteng": ["Johannesburg", "Pretoria"],
    "Western Cape": ["Cape Town", "Stellenbosch"],
    "KwaZulu-Natal": ["Durban", "Pietermaritzburg"],
    "Eastern Cape": ["Gqeberha", "East London"]
}

OCCUPATIONS = [
    "Software Engineer",
    "Teacher",
    "Doctor",
    "Nurse",
    "Accountant",
    "Student",
    "Business Owner",
    "Sales Consultant",
    "Electrician",
    "Data Analyst"
]

SEGMENTS = [
    "Standard",
    "Premium",
    "Business"
]

PAYMENT_METHODS = [
    "Visa",
    "Mastercard"
]

RISK_LEVELS = [
    "LOW",
    "MEDIUM",
    "HIGH"
]

INCOME_RANGES = {
    "Student": (2000, 8000),
    "Teacher": (20000, 40000),
    "Doctor": (60000, 180000),
    "Nurse": (22000, 45000),
    "Software Engineer": (35000, 90000),
    "Accountant": (25000, 60000),
    "Business Owner": (20000, 250000),
    "Sales Consultant": (15000, 45000),
    "Electrician": (18000, 50000),
    "Data Analyst": (25000, 70000)
}

def generate_customers(n=1000):

    customers = []

    for i in range(1, n + 1):

        province = random.choice(list(PROVINCES.keys()))
        city = random.choice(PROVINCES[province])

        occupation = random.choice(OCCUPATIONS)

        income_min, income_max = INCOME_RANGES[occupation]

        monthly_income = random.randint(income_min, income_max)

        if monthly_income < 25000:
            segment = "Standard"
        elif monthly_income < 70000:
            segment = "Premium"
        else:
            segment = "Business"


        if monthly_income < 10000:
                 risk_rating = random.choices(
                    ["LOW", "MEDIUM", "HIGH"],
                     weights=[30, 40, 30]
                     )[0]

        elif monthly_income < 50000:
                risk_rating = random.choices(
                ["LOW", "MEDIUM", "HIGH"],
                weights=[60, 30, 10]
                )[0]

        else:
                risk_rating = random.choices(
                ["LOW", "MEDIUM", "HIGH"],
                weights=[80, 15, 5]
                )[0]

        customer = {
            "id": f"CUS-{1000 + i}",

            "first_name": random.choice(FIRST_NAMES),
            "last_name": random.choice(LAST_NAMES),

            "bank": random.choice(BANKS),

            "province": province,
            "city": city,

            "age": random.randint(18, 70),

            "occupation": occupation,

            "monthly_income": monthly_income,

            "segment": segment,

            "average_transaction": round(
                monthly_income * random.uniform(0.01, 0.08),
                    2
                ),

            "preferred_payment": random.choice(PAYMENT_METHODS),

            "risk_rating": risk_rating,

            "is_active": True
        }

        customers.append(customer)

    return customers


CUSTOMERS = generate_customers()