import uuid
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def get_answer(extracted_text, user_question):
    # Parça boyutunu 500'e çekerek daha odaklanmış bir arama sağlıyoruz
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(extracted_text)

    embeddings = OllamaEmbeddings(model="llama3")
    unique_id = str(uuid.uuid4())
    
    # Her işlem için izole edilmiş koleksiyon oluştur
    vector_db = Chroma.from_texts(
        texts=chunks, 
        embedding=embeddings,
        collection_name=f"tusas_{unique_id}"
    )
    
    # En yakın 5 parçayı getir
    retriever = vector_db.as_retriever(search_kwargs={"k": 5})
    llm = ChatOllama(model="llama3", temperature=0)

    # SİSTEM TALİMATI
    template = """Sen TUSAŞ Teknik Asistanısın. 
    GÖREVİN: Sadece ve sadece sana verilen "Bağlam" metnine dayanarak soruyu cevaplamak.
    
    KURALLAR:
    1. SADECE bağlamda geçen bilgileri kullan. Kendi genel kültürünü veya dış bilgini ASLA ekleme.
    2. Eğer sorunun cevabı bağlam içinde açıkça geçmiyorsa (Örn: Mars, genel tarih vb.), mutlaka ve sadece şunu söyle: 'Bu bilgi yüklenen belgede bulunmamaktadır.'
    3. Cevabı verirken doğrudan konuya gir; "Belgeye göre", "Analizlerime göre" gibi giriş cümleleri kurma.
    4. Soru hangi dildeyse o dilde cevap ver.
    5. Metindeki başlıklar veya içerikler karışmış/kaymış olsa dahi anlamsal bir bütünlük kurarak cevap üret.

    Bağlam: 
    {context}
    
    Soru: {question}
    Cevap:"""
    
    prompt = ChatPromptTemplate.from_template(template)

    # Zincir yapısı (RAG Chain)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()} 
        | prompt 
        | llm 
        | StrOutputParser()
    )

    # Yanıtı üret
    response = chain.invoke(user_question)
    
    # Belleği (Vektör Veritabanını) temizle
    vector_db.delete_collection()
    
    return response