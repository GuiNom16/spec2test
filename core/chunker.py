from config.settings import CHUNK_SIZE

def chunk_text(text, max_chars=CHUNK_SIZE):
    """
    Split text into chunks for LLM processing.
    
    Args:
        text (str): Input text to chunk
        max_chars (int): Maximum characters per chunk
        
    Returns:
        list: List of text chunks
    """
    if not text or not text.strip():
        return []
    
    # Split by paragraphs first
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    
    if not paragraphs:
        return []
    
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        # If adding this paragraph would exceed the limit
        if len(current_chunk) + len(paragraph) + 1 > max_chars and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph
        else:
            if current_chunk:
                current_chunk += "\n" + paragraph
            else:
                current_chunk = paragraph
    
    # Add the last chunk if it has content
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    # Filter out empty chunks
    return [chunk for chunk in chunks if chunk.strip()]
