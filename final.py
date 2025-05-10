from pulp import *
# تعریف مدل
model = LpProblem("Maximize_Profit", LpMaximize)

# اندیس‌ها
routes = [1, 2, 3, 4, 5]  # مسیرها i
train_types = [3, 4, 5]    #  (j) انواع قطارها (سه‌ستاره، چهارستاره، پنج‌ستاره)
scenarios = [1, 2, 3]       # (s)سناریوها



# هزینه کل قطار (T_j)
total_cost = {
    3: 256,  # سه‌ستاره
    4: 258,  # چهارستاره
    5: 340   # پنج‌ستاره
}


# هزینه هر صندلی (B_j)
variable_cost_per_seat = {
    3: 0.4,   # سه‌ستاره
    4: 0.6,   # چهارستاره
    5: 0.8    # پنج‌ستاره
}



# ظرفیت قطارها (A_j)
capacity = {
    3: 600,  # سه‌ستاره (۶۰۰ صندلی)
    4: 400,  # چهارستاره (۴۰۰ صندلی)
    5: 400   # پنج‌ستاره (۴۰۰ صندلی)
}



# قیمت پایه بلیط (P_ij)

base_price = {

    (1, 3): 0.6,
    (1, 4): 0.9,
    (1, 5): 1.3,

    (2, 3): 0.48,
    (2, 4): 0.72,
    (2, 5): 1.04,

    (3, 3): 0.54,
    (3, 4): 0.81,
    (3, 5): 1.17,

    (4, 3): 0.6,
    (4, 4): 0.9,
    (4, 5): 1.3,

    (5, 3): 1.02,
    (5, 4): 1.53,
    (5, 5): 2.21,

}




# قیمت لحظه‌آخری (C_j) -
last_min_price ={
    
    3: 0.4,  # سه‌ستاره
    4: 0.6,  # چهارستاره
    5: 0.8   # پنج‌ستاره

}



# 
demand = {

    #  j = 5

    (1, 1, 5): 900,
    (1, 2, 5): 500,
    (1, 3, 5): 340,
    (1, 5, 5): 700,
    (1, 4, 5): 520,
    (2, 1, 5): 1700,
    (2, 2, 5): 1300,
    (2, 3, 5): 720,
    (2, 5, 5): 1900,
    (2, 4, 5): 1100,
    (3, 1, 5): 520,
    (3, 2, 5): 310,
    (3, 3, 5): 230,
    (3, 5, 5): 710,
    (3, 4, 5): 260,

    #  j = 4

    (1, 1, 4): 1200,
    (1, 2, 4): 700,
    (1, 3, 4): 370,
    (1, 5, 4): 1000,
    (1, 4, 4): 520,
    (2, 1, 4): 2700,
    (2, 2, 4): 1500,
    (2, 3, 4): 900,
    (2, 5, 4): 1900,
    (2, 4, 4): 1100,
    (3, 1, 4): 530,
    (3, 2, 4): 410,
    (3, 3, 4): 230,
    (3, 5, 4): 510,
    (3, 4, 4): 360,

    #  j = 3

    (1, 1, 3): 1300,
    (1, 2, 3): 1300,
    (1, 3, 3): 680,
    (1, 5, 3): 1700,
    (1, 4, 3): 520,
    (2, 1, 3): 3600,
    (2, 2, 3): 2500,
    (2, 3, 3): 1670,
    (2, 5, 3): 2900,
    (2, 4, 3): 1400,
    (3, 1, 3): 1730,
    (3, 2, 3): 910,
    (3, 3, 3): 530,
    (3, 5, 3): 1410,
    (3, 4, 3): 460

}



n = {}
for s in scenarios:
    for i in routes:
        for j in train_types:
            # تعیین محدودیت بالایی بر اساس نوع قطار (j)
            if j in [4, 5]:
                up_bound = 4  # حداکثر ۴ قطار برای چهارستاره و پنج‌ستاره
            else:
                up_bound = 3  # حداکثر ۳ قطار برای سه‌ستاره
            
            # تعریف متغیر با upBound مناسب
            n[(s, i, j)] = LpVariable(
                name=f"n_{s}_{i}_{j}",
                lowBound=0,
                upBound=up_bound,
                cat='Integer'
            )


# متغیرهای تصمیم
x = {}
for s in scenarios:
    for i in routes:
        for j in train_types:
            for k in train_types:
                if k >= j:  # شرط ارتقا به قطارهای هم‌سطح یا بالاتر
                    x[(s, i, j, k)] = LpVariable(
                        name=f"x_{s}_{i}_{j}_{k}",
                        lowBound=0,
                        cat='Integer'
                    )


l = {}
for s in scenarios:
    for i in routes:
        if i != 5:
            for j in train_types:
                l[(s, i, j)] = LpVariable(
                    name=f"l_{s}_{i}_{j}",  
                    lowBound=0,            
                    cat='Integer'           
                )



# تابع هدف
model += (1/3) * (
    lpSum([base_price.get((i, j)) * x[s, i, j, k] 
        for s in scenarios 
        for i in routes 
        for j in train_types 
        for k in train_types if k >= j]) +


    lpSum([last_min_price[j] * l[s, i, j]
        for s in scenarios 
        for i in routes 
        for j in train_types 
        if i != 5 ]) -

    lpSum([total_cost[j] * n[s, i, j] 
        for s in scenarios 
        for i in routes 
        for j in train_types]) - 


    lpSum([
        (capacity[j] * n[s, 5, j] - x[s, 5, j, j] - (x[s, 5, j-1, j] if j > 3 else 0) - (x[s, 5, j-2, j] if j > 4 else 0)) * variable_cost_per_seat[j]
        for s in scenarios
        for j in train_types if j in [3, 4]
    ])

)


# i = 1 (Tehran_Mashhad)

    # s = 1

        # Demand

model += (
    lpSum([x[(1, 1, 3, k)] for k in train_types if k >= 3]) <= 1300
), "0"

model += (
    lpSum([x[(1, 1, 4, k)] for k in train_types if k >= 4]) <= 1200
), "1"


model += (
    x[(1, 1, 5, 5)] <= 900
), "2"

        #Capacity

model += (
    x[(1, 1, 3, 3)] + l[(1, 1, 3)] == 600 * n[(1, 1, 3)]
), "3"


model += (
    x[(1, 1, 4, 4)] + x[(1, 1, 3, 4)] + l[(1, 1, 4)] == 400 * n[(1, 1, 4)]
), "4"

model += (
    x[(1, 1, 5, 5)] + x[(1, 1, 4, 5)] + x[(1, 1, 3, 5)] + l[(1, 1, 5)] == 400 * n[(1, 1, 5)]
), "5"



    # s = 2

        # Demand


model += (
    lpSum([x[(2, 1, 3, k)] for k in train_types if k >= 3]) <= 3600
), "6"

model += (
    lpSum([x[(2, 1, 4, k)] for k in train_types if k >= 4]) <= 2700
), "7"

model += (
    x[(2, 1, 5, 5)] <= 1700
), "8"

        #Capacity

model += (
    x[(2, 1, 3, 3)] + l[(2, 1, 3)] == 600 * n[(2, 1, 3)]
), "9"

model += (
    x[(2, 1, 4, 4)] + x[(2, 1, 3, 4)] + l[(2, 1, 4)] == 400 * n[(2, 1, 4)]
), "10"

model += (
    x[(2, 1, 5, 5)] + x[(2, 1, 4, 5)] + x[(2, 1, 3, 5)] + l[(2, 1, 5)] == 400 * n[(2, 1, 5)]
), "11"


    # s = 3

        # Demand


model += (
    lpSum([x[(3, 1, 3, k)] for k in train_types if k >= 3]) <= 1730
), "12"

model += (
    lpSum([x[(3, 1, 4, k)] for k in train_types if k >= 4]) <= 530
), "13"

model += (
    x[(3, 1, 5, 5)] <= 520
), "14"


        # Capacity


model += (
    x[(3, 1, 3, 3)] + l[(3, 1, 3)] == 600 * n[(3, 1, 3)]
), "15"

model += (
    x[(3, 1, 4, 4)] + x[(3, 1, 3, 4)] + l[(3, 1, 4)] == 400 * n[(3, 1, 4)]
), "16"

model += (
    x[(3, 1, 5, 5)] + x[(3, 1, 4, 5)] + x[(3, 1, 3, 5)] + l[(3, 1, 5)] == 400 * n[(3, 1, 5)]
), "17"

# i = 4 (Mashhad_BanderAbbas)

# s = 1

    # Demand

model += (
    lpSum([x[(1, 4, 3, k)] for k in train_types if k >= 3]) <= 520
), "18"

model += (
    lpSum([x[(1, 4, 4, k)] for k in train_types if k >= 4]) <= 520
), "19"

model += (
    x[(1, 4, 5, 5)] <= 520
), "20"

    # Capacity

model += (
    x[(1, 4, 3, 3)] + l[(1, 4, 3)] == 600 * n[(1, 4, 3)]
), "21"

model += (
    x[(1, 4, 4, 4)] + x[(1, 4, 3, 4)] + l[(1, 4, 4)] == 400 * n[(1, 4, 4)]
), "22"

model += (
    x[(1, 4, 5, 5)] + x[(1, 4, 4, 5)] + x[(1, 4, 3, 5)] + l[(1, 4, 5)] == 400 * n[(1, 4, 5)]
), "23"


    # s = 2

        # Demand

model += (
    lpSum([x[(2, 4, 3, k)] for k in train_types if k >= 3]) <= 1400
), "24"

model += (
    lpSum([x[(2, 4, 4, k)] for k in train_types if k >= 4]) <= 1100
), "25"

model += (
    x[(2, 4, 5, 5)] <= 1100
), "26"

        # Capacity

model += (
    x[(2, 4, 3, 3)] + l[(2, 4, 3)] == 600 * n[(2, 4, 3)]
), "27"

model += (
    x[(2, 4, 4, 4)] + x[(2, 4, 3, 4)] + l[(2, 4, 4)] == 400 * n[(2, 4, 4)]
), "28"

model += (
    x[(2, 4, 5, 5)] + x[(2, 4, 4, 5)] + x[(2, 4, 3, 5)] + l[(2, 4, 5)] == 400 * n[(2, 4, 5)]
), "29"


    # s = 3

        # Demand

model += (
    lpSum([x[(3, 4, 3, k)] for k in train_types if k >= 3]) <= 460
), "30"

model += (
    lpSum([x[(3, 4, 4, k)] for k in train_types if k >= 4]) <= 360
), "31"

model += (
    x[(3, 4, 5, 5)] <= 260
), "32"


        # Capacity

model += (
    x[(3, 4, 3, 3)] + l[(3, 4, 3)] == 600 * n[(3, 4, 3)]
), "33"

model += (
    x[(3, 4, 4, 4)] + x[(3, 4, 3, 4)] + l[(3, 4, 4)] == 400 * n[(3, 4, 4)]
), "34"

model += (
    x[(3, 4, 5, 5)] + x[(3, 4, 4, 5)] + x[(3, 4, 3, 5)] + l[(3, 4, 5)] == 400 * n[(3, 4, 5)]
), "35"


# i = 2 (Tehran_Isfahan)

# s = 1

    # Demand

model += (
    lpSum([x[(1, 2, 3, k)] for k in train_types if k >= 3]) <= 1300
), "36"

model += (
    lpSum([x[(1, 2, 4, k)] for k in train_types if k >= 4]) <= 700
), "37"

model += (
    x[(1, 2, 5, 5)] <= 500
), "38"

    #Capacity

model += (
    x[(1, 2, 3, 3)] + l[(1, 2, 3)] == 600 * n[(1, 2, 3)] + 600 * n[(1, 5, 3)] - x[(1, 5, 3, 3)]
), "39"

model += (
    x[(1, 2, 4, 4)] + x[(1, 2, 3, 4)] + l[(1, 2, 4)] == 400 * n[(1, 2, 4)] + 400 * n[(1, 5, 4)] - x[(1, 5, 4, 4)] - x[(1, 5, 3, 4)]
), "40"

model += (
    x[(1, 2, 5, 5)] + x[(1, 2, 4, 5)] + x[(1, 2, 3, 5)] + l[(1, 2, 5)] == 400 * n[(1, 2, 5)] + 400 * n[(1, 5, 5)] - x[(1, 5, 5, 5)] - x[(1, 5, 4, 5)] - x[(1, 5, 3, 5)]
), "41"

# s = 2

    # Demand

model += (
    lpSum([x[(2, 2, 3, k)] for k in train_types if k >= 3]) <= 2500
), "42"

model += (
    lpSum([x[(2, 2, 4, k)] for k in train_types if k >= 4]) <= 1500
), "43"

model += (
    x[(2, 2, 5, 5)] <= 1300
), "44"

    # Capacity

model += (
    x[(2, 2, 3, 3)] + l[(2, 2, 3)] == 600 * n[(2, 2, 3)] + 600 * n[(2, 5, 3)] - x[(2, 5, 3, 3)]
), "45"

model += (
    x[(2, 2, 4, 4)] + x[(2, 2, 3, 4)] + l[(2, 2, 4)] == 400 * n[(2, 2, 4)] + 400 * n[(2, 5, 4)] - x[(2, 5, 4, 4)] - x[(2, 5, 3, 4)]
), "46"

model += (
    x[(2, 2, 5, 5)] + x[(2, 2, 4, 5)] + x[(2, 2, 3, 5)] + l[(2, 2, 5)] == 400 * n[(2, 2, 5)] + 400 * n[(2, 5, 5)] - x[(2, 5, 5, 5)] - x[(2, 5, 4, 5)] - x[(2, 5, 3, 5)]
), "47"

# s = 3

    # Demand

model += (
    lpSum([x[(3, 2, 3, k)] for k in train_types if k >= 3]) <= 910
), "48"

model += (
    lpSum([x[(3, 2, 4, k)] for k in train_types if k >= 4]) <= 410
), "49"

model += (
    x[(3, 2, 5, 5)] <= 310
), "50"

    # Capacity

model += (
    x[(3, 2, 3, 3)] + l[(3, 2, 3)] == 600 * n[(3, 2, 3)] + 600 * n[(3, 5, 3)] - x[(3, 5, 3, 3)]
), "51"

model += (
    x[(3, 2, 4, 4)] + x[(3, 2, 3, 4)] + l[(3, 2, 4)] == 400 * n[(3, 2, 4)] + 400 * n[(3, 5, 4)] - x[(3, 5, 4, 4)] - x[(3, 5, 3, 4)]
), "52"

model += (
    x[(3, 2, 5, 5)] + x[(3, 2, 4, 5)] + x[(3, 2, 3, 5)] + l[(3, 2, 5)] == 400 * n[(3, 2, 5)] + 400 * n[(3, 5, 5)] - x[(3, 5, 5, 5)] - x[(3, 5, 4, 5)] - x[(3, 5, 3, 5)]
), "53"





# i = 3 (Isfahan_BandarAbbas)

    # s = 1

        # Demand

model += (
    lpSum([x[(1, 3, 3, k)] for k in train_types if k >= 3]) <= 680
), "54"

model += (
    lpSum([x[(1, 3, 4, k)] for k in train_types if k >= 4]) <= 370
), "55"

model += (
    x[(1, 3, 5, 5)] <= 340
), "56"

    # Capacity

model += (
    x[(1, 3, 3, 3)] + l[(1, 3, 3)] == 600 * n[(1, 3, 3)] + 600 * n[(1, 5, 3)] - x[(1, 5, 3, 3)]
), "57"

model += (
    x[(1, 3, 4, 4)] + x[(1, 3, 3, 4)] + l[(1, 3, 4)] == 400 * n[(1, 3, 4)] + 400 * n[(1, 5, 4)] - x[(1, 5, 4, 4)] - x[(1, 5, 3, 4)]
), "58"

model += (
    x[(1, 3, 5, 5)] + x[(1, 3, 4, 5)] + x[(1, 3, 3, 5)] + l[(1, 3, 5)] == 400 * n[(1, 3, 5)] + 400 * n[(1, 5, 5)] - x[(1, 5, 5, 5)] - x[(1, 5, 4, 5)] - x[(1, 5, 3, 5)]
), "59"

    # s = 2

        # Demand

model += (
    lpSum([x[(2, 3, 3, k)] for k in train_types if k >= 3]) <= 1670
), "60"

model += (
    lpSum([x[(2, 3, 4, k)] for k in train_types if k >= 4]) <= 900
), "61"

model += (
    x[(2, 3, 5, 5)] <= 720
), "62"

    # Capacity

model += (
    x[(2, 3, 3, 3)] + l[(2, 3, 3)] == 600 * n[(2, 3, 3)] + 600 * n[(2, 5, 3)] - x[(2, 5, 3, 3)]
), "63"

model += (
    x[(2, 3, 4, 4)] + x[(2, 3, 3, 4)] + l[(2, 3, 4)] == 400 * n[(2, 3, 4)] + 400 * n[(2, 5, 4)] - x[(2, 5, 4, 4)] - x[(2, 5, 3, 4)]
), "64"

model += (
    x[(2, 3, 5, 5)] + x[(2, 3, 4, 5)] + x[(2, 3, 3, 5)] + l[(2, 3, 5)] == 400 * n[(2, 3, 5)] + 400 * n[(2, 5, 5)] - x[(2, 5, 5, 5)] - x[(2, 5, 4, 5)] - x[(2, 5, 3, 5)]
), "65"

    # s = 3

        # Demand

model += (
    lpSum([x[(3, 3, 3, k)] for k in train_types if k >= 3]) <= 530
), "66"

model += (
    lpSum([x[(3, 3, 4, k)] for k in train_types if k >= 4]) <= 230
), "67"

model += (
    x[(3, 3, 5, 5)] <= 230
), "68"

    # Capacity

model += (
    x[(3, 3, 3, 3)] + l[(3, 3, 3)] == 600 * n[(3, 3, 3)] + 600 * n[(3, 5, 3)] - x[(3, 5, 3, 3)]
), "69"

model += (
    x[(3, 3, 4, 4)] + x[(3, 3, 3, 4)] + l[(3, 3, 4)] == 400 * n[(3, 3, 4)] + 400 * n[(3, 5, 4)] - x[(3, 5, 4, 4)] - x[(3, 5, 3, 4)]
), "70"

model += (
    x[(3, 3, 5, 5)] + x[(3, 3, 4, 5)] + x[(3, 3, 3, 5)] + l[(3, 3, 5)] == 400 * n[(3, 3, 5)] + 400 * n[(3, 5, 5)] - x[(3, 5, 5, 5)] - x[(3, 5, 4, 5)] - x[(3, 5, 3, 5)]
), "71"

# i = 5 (Tehran_BandarAbbas)

    # s = 1

        # Demand

model += (
    lpSum([x[(1, 5, 3, k)] for k in train_types if k >= 3]) <= 1700
), "72"

model += (
    lpSum([x[(1, 5, 4, k)] for k in train_types if k >= 4]) <= 1000
), "73"

model += (
    x[(1, 5, 5, 5)] <= 700
), "74"

        # Capacity

model += (
    x[(1, 5, 3, 3)] <= 600 * n[(1, 5, 3)]
), "75"

model += (
    x[(1, 5, 4, 4)] + x[(1, 5, 3, 4)] <= 400 * n[(1, 5, 4)]
), "76"

model += (
    x[(1, 5, 5, 5)] + x[(1, 5, 4, 5)] + x[(1, 5, 3, 5)] <= 400 * n[(1, 5, 5)]
), "77"

    # s = 2

        # Demand

model += (
    lpSum([x[(2, 5, 3, k)] for k in train_types if k >= 3]) <= 2900
), "78"

model += (
    lpSum([x[(2, 5, 4, k)] for k in train_types if k >= 4]) <= 1900
), "79"

model += (
    x[(2, 5, 5, 5)] <= 1900
), "80"

        # Capacity

model += (
    x[(2, 5, 3, 3)] <= 600 * n[(2, 5, 3)]
), "81"

model += (
    x[(2, 5, 4, 4)] + x[(2, 5, 3, 4)] <= 400 * n[(2, 5, 4)]
), "82"

model += (
    x[(2, 5, 5, 5)] + x[(2, 5, 4, 5)] + x[(2, 5, 3, 5)] <= 400 * n[(2, 5, 5)]
), "83"

    # s = 3

        # Demand

model += (
    lpSum([x[(3, 5, 3, k)] for k in train_types if k >= 3]) <= 1410
), "84"

model += (
    lpSum([x[(3, 5, 4, k)] for k in train_types if k >= 4]) <= 510
), "85"

model += (
    x[(3, 5, 5, 5)] <= 710
), "86"

        # Capacity

model += (
    x[(3, 5, 3, 3)] <= 600 * n[(3, 5, 3)]
), "87"

model += (
    x[(3, 5, 4, 4)] + x[(3, 5, 3, 4)] <= 400 * n[(3, 5, 4)]
), "88"

model += (
    x[(3, 5, 5, 5)] + x[(3, 5, 4, 5)] + x[(3, 5, 3, 5)] <= 400 * n[(3, 5, 5)]
), "89"




# Solve the model
model.solve()

# Print solution status
print("Status:", LpStatus[model.status])

# Print ALL variables (including zeros) بدون اعشار
# فقط متغیرهای با مقدار غیر صفر چاپ شوند؟ (True یا False)

for var in model.variables():
    if var.name.startswith("n_") or var.name.startswith("x_") or var.name.startswith("l_"):
        if var.varValue != 0:
            print(f"{var.name}: {int(var.varValue)}")




# بخش اول تابع هدف
objective_part1 = (
    lpSum([base_price.get((i, j)) * x[1, i, j, k].varValue 
        for i in routes 
        for j in train_types 
        for k in train_types if k >= j]) +
    lpSum([last_min_price[j] * l[1, i, j].varValue
        for i in routes 
        for j in train_types 
        if i != 5 ]) -
    lpSum([total_cost[j] * n[1, i, j].varValue 
        for i in routes 
        for j in train_types]) - 
    lpSum([
        (capacity[j] * n[1, 5, j].varValue 
        - x[1, 5, j, j].varValue 
        - (x[1, 5, j-1, j].varValue if j > 3 else 0) 
        - (x[1, 5, j-2, j].varValue if j > 4 else 0)
        ) * variable_cost_per_seat[j]
        for j in train_types if j in [3, 4]
    ])
)

# بخش دوم تابع هدف
objective_part2 = (
    lpSum([base_price.get((i, j)) * x[2, i, j, k].varValue 
        for i in routes 
        for j in train_types 
        for k in train_types if k >= j]) +
    lpSum([last_min_price[j] * l[2, i, j].varValue
        for i in routes 
        for j in train_types 
        if i != 5 ]) -
    lpSum([total_cost[j] * n[2, i, j].varValue 
        for i in routes 
        for j in train_types]) - 
    lpSum([
        (capacity[j] * n[2, 4, j].varValue 
        - x[2, 5, j, j].varValue 
        - (x[2, 5, j-1, j].varValue if j > 3 else 0) 
        - (x[2, 5, j-2, j].varValue if j > 4 else 0)
        ) * variable_cost_per_seat[j]
        for j in train_types if j in [3, 4]
    ])
)

# بخش سوم تابع هدف
objective_part3 = (
    lpSum([base_price.get((i, j)) * x[3, i, j, k].varValue 
        for i in routes 
        for j in train_types 
        for k in train_types if k >= j]) +
    lpSum([last_min_price[j] * l[3, i, j].varValue
        for i in routes 
        for j in train_types 
        if i != 5 ]) -
    lpSum([total_cost[j] * n[3, i, j].varValue 
        for i in routes 
        for j in train_types]) - 
    lpSum([
        (capacity[j] * n[3, 5, j].varValue 
        - x[2, 5, j, j].varValue 
        - (x[2, 5, j-1, j].varValue if j > 3 else 0) 
        - (x[2, 5, j-2, j].varValue if j > 4 else 0)
        ) * variable_cost_per_seat[j]
        for j in train_types if j in [3, 4]
    ])
)


from pulp import value

print()
print(f"in first scenario, the highest income is : {value(objective_part1):.2f}")
print(f"in second scenario, the highest income is : {value(objective_part2):.2f}")
print(f"in third scenario, the highest income is : {value(objective_part3):.2f}")
print()
print(f"throughout the year, the highest income is : {value(objective_part1 + objective_part2 + objective_part3):.2f}")
print(f"average income for each scenario (Max Z) is : {value((objective_part1 + objective_part2 + objective_part3)/3):.2f}")

print()


for s in scenarios:
    for i in routes:
        n_s_i_3 = n[(s, i, 3)].varValue
        n_s_i_4 = n[(s, i, 4)].varValue
        n_s_i_5 = n[(s, i, 5)].varValue
        
        denominator = 600*n_s_i_3 + 400*n_s_i_4 + 400*n_s_i_5
        
        if denominator != 0:
            ratio = 100*600*n_s_i_3 / denominator
            print(f"Scenario {s}, Route {i}, train type 3 : {ratio:.2f} %")

            ratio_2 = 100*400*n_s_i_4 / denominator
            print(f"Scenario {s}, Route {i}, train type 4: {ratio_2:.2f} %")

            ratio_3 = 100*400*n_s_i_5 / denominator
            print(f"Scenario {s}, Route {i}, train type 5: {ratio_3:.2f} %")

        else:
            print(f"Scenario {s}, Route {i}: No trains assigned (zero denominator)")



