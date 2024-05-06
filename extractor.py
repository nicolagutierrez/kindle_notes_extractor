import os, sys
from dotenv import load_dotenv

load_dotenv()
directory = os.getenv("DIRECTORY_PATH", None)
kindle_file = os.getenv("KINDLE_FILE", "My Clippings.txt")
highlight_term = os.getenv("HIGHLIGHT_TERM", None)
note_term = os.getenv("NOTE_TERM", None)
bookmark_term = os.getenv("BOOKMARK_TERM", None)

if (
    directory is None
    or highlight_term is None
    or note_term is None
    or bookmark_term is None
):
    print("Please set the environment variables, refer to the README.md file")
    sys.exit(1)


def extraction(book):
    input_file = os.path.join(directory, kindle_file)
    output_file = os.path.join(directory, book + "_notes.txt")
    cnt = 0
    flag = 0
    book_details = {"page": None, "quote": "", "note": "", "pos": None}
    arr_notes = []

    print("Processing " + input_file + " in search of " + book + " notes...")

    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            if line == "\n":
                continue

            line = line.replace("\ufeff", "")
            if line.startswith(book):
                cnt += 1
                continue

            if line.startswith("=========="):
                cnt = 0
                if book_details["page"] is not None and (
                    book_details["quote"] or book_details["note"]
                ):
                    arr_notes.append(book_details)
                book_details = {"page": None, "quote": "", "note": "", "pos": None}
                continue

            if cnt == 1 and flag == 0:
                if not line.startswith("- "):
                    book_details["quote"] += line.strip()
                    continue

                details = line.split("|")
                page = details[0].split(" ")[-2]
                pos = details[1].split(" ")[-2]

                if line.startswith(highlight_term):
                    flag = 1
                if line.startswith(note_term):
                    flag = 2
                if line.startswith(bookmark_term):
                    book_details["page"] = page
                    book_details["pos"] = pos
                    continue

                if flag > 0:
                    book_details["page"] = page
                    book_details["pos"] = pos
                    continue

            if cnt == 1 and flag == 1:
                book_details["quote"] += line.strip()
                flag = 0
                continue

            if cnt == 1 and flag == 2:
                book_details["note"] += line.strip()
                flag = 0
                continue

        # FILTERING
        pos_groups = {}
        for d in arr_notes:
            r = str(d["pos"]).split("-")
            if len(r) == 1:
                pos_groups[int(r[0])] = d
                continue

            start = int(r[0])
            if start not in pos_groups or int(r[1]) > int(
                pos_groups[start]["pos"].split("-")[1]
            ):
                pos_groups[start] = d

        pos_groups = dict(sorted(pos_groups.items()))
        arr_notes = list(pos_groups.values())

        # STORE
        for element in arr_notes:
            if element["quote"]:
                outfile.write(
                    "- **Quote:** "
                    + element["quote"]
                    + " - page "
                    + element["page"]
                    + ", pos: "
                    + element["pos"]
                    + "\n"
                )
            elif element["note"]:
                outfile.write(
                    "- **Notes:** "
                    + element["note"]
                    + " - page "
                    + element["page"]
                    + ", pos: "
                    + element["pos"]
                    + "\n"
                )
            else:
                outfile.write(
                    "- **Bookmark:** page "
                    + element["page"]
                    + ", pos: "
                    + element["pos"]
                    + "\n"
                )

            outfile.write("\n")

        print("Done!")


def get_last_book():
    with open(os.path.join(directory, kindle_file), "r") as infile:
        lines = infile.readlines()
        return lines[-5].split("(")[0]


if __name__ == "__main__":
    books = sys.argv[1:]
    if len(books) == 0:
        print("Using last book read...")
        books.append(get_last_book())
        print("Last book read: " + books[0])
        print("Do you want to proceed? (y/n)")
        response = input()
        if response.lower() != "y":
            print("Exiting...")
            sys.exit(1)

    for book in books:
        extraction(book)
