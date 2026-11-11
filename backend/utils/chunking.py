from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text_in_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50,
        length_function=len,
        # It tries to split on double newlines, then single, then spaces
        separators=["\n\n", "\n", " ", ""]

    )

    #split_text  returns a list of strings 
    chunks = text_splitter.split_text(text)

    return chunks