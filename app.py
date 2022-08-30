import snscrape.modules.twitter as sntwitter
import tkinter as tk
import xlsxwriter

root = tk.Tk()


def Search():
    print('def search')
    limit = int(limit_text_box.get("1.0", "end-1c"))
    print('limit: ' + str(limit))
    query = str(search_text_box.get("1.0", "end-1c"))
    print(query)
    print('query: ' + query)

    count = 0
    workbook = xlsxwriter.Workbook(
        str(file_text_box.get("1.0", "end-1c"))+'.xlsx')
    worksheet = workbook.add_worksheet("tweets")

    worksheet.write(0, 0, "id")
    worksheet.write(0, 1, "username")
    worksheet.write(0, 2, "hashtags")
    worksheet.write(0, 3, "content")
    worksheet.write(0, 4, "date")

    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if count >= limit:
            break

        count += 1

        worksheet.write(count, 0, str(count))
        worksheet.write(count, 1, tweet.user.username)
        hashtags = ''
        if tweet.hashtags:
            for hashtag in tweet.hashtags:
                hashtags += '#'+hashtag

        worksheet.write(count, 2, hashtags)
        worksheet.write(count, 3, tweet.content)
        worksheet.write(count, 4, str(tweet.date))

        # print('\033[32m' + tweet.user.username +' (' + str(tweet.date) + '): ')
        # print('\033[37m' + tweet.content)
        # print('\033[31m----------------------------------------------\033[39m')

    workbook.close()
    print('done')


root.title('Tweets to xlsx (by Maros Meciar)')
canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=4)

file_instructions = tk.Label(
    root, text="File name:", font="Roboto")
file_instructions.grid(columnspan=1, column=0, row=0)
file_text_box = tk.Text(root, height=1, width=50, padx=10, pady=10)
file_text_box.grid(columnspan=2, column=1, row=0)


search_instructions = tk.Label(
    root, text="Search settings:", font="Roboto")
search_instructions.grid(columnspan=1, column=0, row=1)
search_text_box = tk.Text(root, height=1, width=50, padx=10, pady=10)
search_text_box.grid(columnspan=2, column=1, row=1)

limit_instructions = tk.Label(
    root, text="Number of tweets limit:", font="Roboto")
limit_instructions.grid(columnspan=1, column=0, row=2)
limit_text_box = tk.Text(root, height=1, width=50, padx=10, pady=10)
limit_text_box.grid(columnspan=2, column=1, row=2)

commit_text = tk.StringVar()
commit_btn = tk.Button(root, textvariable=commit_text,
                       font="Roboto", bg="#5ab9db", fg="white", height=2, width=15, command=lambda: Search())
commit_text.set("Generate xlsx")
commit_btn.grid(column=1, row=3)

root.mainloop()
