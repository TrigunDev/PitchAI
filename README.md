# 📧 AI Cold Email Generator
Cold email generator for services company using llama 3.3, langchain and streamlit. It allows users to input the URL of a company's careers page. The tool then extracts job listings from that page and generates personalized cold emails. These emails include relevant portfolio links sourced from a vector database, based on the specific job descriptions. 

**Imagine a scenario:**

- Amazon needs a Software Development Engineer II and is spending time and resources in the hiring process, on boarding, training etc
- XYZ is Software Development company can provide a dedicated software development engineer to Amazon. So, the business development executive (Trigun) from XYZ is going to reach out to Amazon via a cold email.

<img width="1832" height="906" alt="Screenshot 2026-07-29 191154" src="https://github.com/user-attachments/assets/057c378d-7d73-4b16-9ca0-216043ad80f8" />

---

## Architecture Diagram
<img width="1182" height="430" alt="coldEmailGeneratorArchitectureDiagram" src="https://github.com/user-attachments/assets/436ea920-3d21-4061-8cea-771f34280c3a" />

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| AI Model | llama 3.3 |
| Vector Database | ChromaDB |
| LLM Framework | LangChain |
| Frontend | Streamlit |

---

## 📂 Folder Structure

```text
ColdEmailGenerator/
├── app/
│   ├── chains.py                 # LangChain prompt chains
│   ├── portfolio.py              # Portfolio management & retrieval
│   ├── utils.py                  # Utility functions
│   ├── main.py                   # Streamlit application
│   ├── .env                      # Environment variables
│   └── resource/
│       └── my_portfolio.csv      # Portfolio dataset
│
├── vectorstore/                  # ChromaDB vector database
│
├── .gitignore                    # Git ignore rules
└── README.md                     # Project documentation
```

---

## Set-up
1. To get started we first need to get an API_KEY from here: https://console.groq.com/keys. Inside `app/.env` update the value of `GROQ_API_KEY` with the API_KEY you created. 


2. To get started, first install the required Python libraries.
   
3. Run the streamlit app:
   ```commandline
   streamlit run app/main.py
   ```
   
