get_csv_error0 = lambda: "\n".join ([
    "Category0,Product0,27.34",
    "Category0,Product1,41.44",
    "Category1|Category2,Product2",
    "Category2,Product3,37.36",
    "Category6,Product4,13.64",
    "Category3,Product5,26.33",
    "Category5,Product6,20.09",
    "Category4,Product7,47.75",
    "Category4,Product8,15.47",
    "Category0,Product9,41.3",
    "Category0|Category1|Category2,Product10,17.98",
])

get_csv_error1 = lambda: "\n".join ([
    "Category0,Product0,27.34",
    "Category0,Product1,x",
    "Category1|Category2,Product2,29.89",
    "Category2,Product3,37.36",
    "Category6,Product4,13.64",
    "Category3,Product5,26.33",
    "Category5,Product6,20.09",
    "Category4,Product7,47.75",
    "Category4,Product8,15.47",
    "Category0,Product9,41.3",
    "Category0|Category1|Category2,Product10,17.98",
])

get_csv_error2 = lambda: "\n".join ([
    "Category0,Product0,27.34",
    "Category0,Product1,-1.2",
    "Category1|Category2,Product2,29.89",
    "Category2,Product3,37.36",
    "Category6,Product4,13.64",
    "Category3,Product5,26.33",
    "Category5,Product6,20.09",
    "Category4,Product7,47.75",
    "Category4,Product8,15.47",
    "Category0,Product9,41.3",
    "Category0|Category1|Category2,Product10,17.98",
])


get_data0 = lambda: "\n".join ([
    "Category0,Product0,27.34",
    "Category0,Product1,41.44",
    "Category1|Category2,Product2,29.89",
    "Category2,Product3,37.36",
    "Category6,Product4,13.64",
    "Category3,Product5,26.33",
    "Category5,Product6,20.09",
    "Category4,Product7,47.75",
    "Category4,Product8,15.47",
    "Category0,Product9,41.3",
    "Category0|Category1|Category2,Product10,17.98",
])

with open("products_error1.csv", "w") as ferr1, \
    open("products_error2.csv", "w") as ferr2, \
    open("products_error3.csv", "w") as ferr3, \
    open("products.csv", "w") as fin:
    ferr1.write(get_csv_error0())
    ferr2.write(get_csv_error1())
    ferr3.write(get_csv_error2())
    fin.write(get_data0())

