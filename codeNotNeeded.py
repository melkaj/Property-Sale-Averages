
#
# CODE USED ON JUPYTER BUT NOT NEEDED ANYMORE
#
# excel_list = os.listdir('./data')
# print(len(excel_list))
# for item in excel_list:
#     file_name = item[0:-4] + 'csv'
#     years = ["2005", "2006", "2007", "2008"]
#     elem = (item[0:4])
#     if (elem in years):
#         file_name = item[0:-3] + 'csv'
#         print(file_name)
#         file_path = "./csv-files/" + file_name
#         pd.read_excel("./data/" + item).to_csv(file_path, index=False)
# print("DONE")