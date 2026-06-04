# Technical Assessment Submission: Intelligent Web Scraper & Entity Extractor

* **Candidate:** Karthika Rajagopal R S  
* **Target Role:** AI Engineer / Applied AI Engineer  
* **Date:** June 2026  
* **Company:** Tatos Technologies Pvt Ltd  

---

## 3. Completed Expected Deliverables

All deliverables outlined in the technical assessment brief have been fully implemented, validated locally, and successfully pushed to the repository.

### A. Source Code Repository
* **Repository Link:** `https://github.com/KarthikaRajagopal44/Web-Scrapper-Agent`
* **Architecture:** Built as a modular, production-grade microservice following industry-standard clean-code and MVC design patterns. The codebase is strictly organized into layers of concern:

```text
intelligent-extractor/
├── .env                  # Local secret keys (Excluded from Git)
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation and demo instructions
└── src/
    ├── main.py           # FastAPI entry point & API Router
    ├── config.py         # App configurations & environment settings
    ├── schemas/
    │   ├── request.py    # Request payload validators
    │   └── extraction.py # Target Pydantic extraction schemas (E-commerce / Legal)
    ├── services/
    │   ├── scraper.py    # Async network fetcher & clean HTML parser
    │   └── extractor.py  # LLM structured output calling with context safeguards
    └── utils/
        └── exceptions.py # Structured custom API exception handlers
