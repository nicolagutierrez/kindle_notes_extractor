# kindle_notes_extractor
Simple extractor for kindle quote and notes

### Usage
1. Create a `.env` file in order to define the `DIRECTORY_PATH` environment variable. This variable should contain the path to the directory where the kindle notes are stored (the standard name of the file is `My Clippings.txt`). It is necessary to set also the environment variables related to the short phrases used to introduce notes, bookmarks, and highlights. An example of the `.env` file is the following (considering the italian version):
```
DIRECTORY_PATH=""/path/to/your/directory""
HIGHLIGHT_TERM="- La tua evidenziazione a pagina"
NOTE_TERM="- La tua nota a pagina"
BOOKMARK_TERM="- Il tuo segnalibro a pagina"
```
    
  - *If you have a custom name for the file, you can define the `KINDLE_FILE` environment variable in the `.env` file.*
2. Run the script passing the title of books (the title must be precise)
3. The script will generate a file with the quotes and notes of the book in the same directory where the kindle notes file is located.
