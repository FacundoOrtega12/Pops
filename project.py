

def list_items(filename):
    file = open(filename, "r")
    item_list = []
    for line in file:
        item = line.split(",")
        item_tup = (item[0], item[1].strip())
        item_list.append(item_tup)
    return item_list

def create_alphabetical(book_list):
        book_title_list = []
        alpha_book_list = []
        for book in book_list:
            book_title_list.append(book[0].lower())
        book_title_list.sort()
        for title in book_title_list:
            for book in book_list:
                if title == book[0].lower():
                    alpha_book_list.append(book)
                else:
                    pass
        return alpha_book_list

def display_alpha(books):
    for book in books:
        title = book[0]
        rating = book[1]
        print(f"{title}  --  {rating}")


def list_byrating(list, rating):
    rating_list = []
    for book in list:
        if book[1] == rating:
            rating_list.append(book)
    return rating_list


def check_entry(entry:tuple, book_list):
    entry_title = entry[0]
    for book in book_list:
        title = book[0]
        if entry_title == title:
            return False
        else:
            pass
    return True

def archive_entry(entry, book_list):
    with open('booklist.txt', 'w') as file:
        for book in book_list:
            title = book[0]
            rating = book[1]
            file.write(f"{title},{rating}\n")
        file.write(f"{entry[0]},{entry[1]}\n")

def main():
    try:
        open("booklist.txt", "x")
        book_list = []
    except FileExistsError:
        book_list = list_items("booklist.txt")
    
    running = True

    while running:
        print()
        title = input("Title: ")
        rating = input("rating out of 10: ") 
        try:
            valid = True
        except ValueError:
            valid = False
        if 1 <= int(rating) <= 10: 
            new_entry = (title, int(rating))
        else:
            print("invalid rating")
            valid = False
        if valid and check_entry(new_entry, book_list):
            print(f"{new_entry[0]} has been added to your book collection.")
            archive_entry(new_entry, book_list)
            book_list = list_items("booklist.txt")
            alpha_book_list = create_alphabetical(book_list)

            print("\n" * 2)
            display_alpha(alpha_book_list)
            print("\n" * 2)
            choice = input("Would you like to add another book to your collection?( yes | no ): ").strip().lower()
            if choice == "yes":
                pass
            else:
                running = False
        else:
            print(f"{new_entry[0]} is already in your book collection, please try a new entry")
   






       

    









if __name__ == "__main__":
    main()

