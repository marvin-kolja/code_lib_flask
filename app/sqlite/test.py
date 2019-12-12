def run():
    from operation_functions import Operations
    op = Operations()

    userData = op.get_data_by_userId(2)
    userFirst = userData[0][1]
    userLast = userData[0][2]
    userEmail = userData[0][3]

    bookData = op.get_book_data_by_userId(2)

    print(userFirst)
    print(userLast)
    print(userEmail)
    print(bookData)
    for book in bookData:
        print("\nTitle: " + str(bookData[book][1]))
        print("BookID: " + str(bookData[book][2]))
        print("Rent Date: " + str(bookData[book][3]))
        print("Return Date: " + str(bookData[book][4]))

if __name__ == "__main__":
    run()