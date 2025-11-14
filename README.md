# 📦 Product Sentiment Analyzer & Review Dashboard

A web-based application that scrapes product reviews from e-commerce websites, analyzes sentiments using NLP, and visualizes insights through an interactive dashboard.

# I Overview

The **Product Sentiment Analyzer & Review Dashboard** is designed to help users understand customer opinions about products by collecting reviews automatically and processing them using machine learning techniques.
The dashboard presents sentiment trends, statistics, and insights in an intuitive and interactive manner.

This project is divided into **8 major modules**:

1. **Web Scraping Module** – Scraping reviews from Amazon/Flipkart
2. **Data Preprocessing Module** – Cleaning and preparing text data
3. **Sentiment Analysis Model Module** – Building NLP model
4. **Database & Storage Module** – Storing products, reviews, and sentiments
5. **Backend Integration Module** – API to connect frontend, model & DB
6. **Frontend Dashboard Module** – Web interface for users
7. **Data Visualization Module** – Charts and sentiment insights
8. **Testing, Deployment & Documentation Module** – Final testing & hosting


# II Technologies Used

### **Backend & Core**

* Python
* Flask / Django
* Selenium
* BeautifulSoup
* Pandas, NumPy
* NLTK / spaCy
* Scikit-learn / BERT

### **Frontend**

* React / HTML / CSS / JavaScript
* Bootstrap / Tailwind (optional)

### **Database**

* MySQL / MongoDB / SQLite

### **Visualization**

* Matplotlib
* Plotly / Chart.js

### **Deployment**

* Render / Heroku / AWS EC2


## III Features

###  **1. Dynamic Review Scraping**

* Extract real-time reviews from Amazon & Flipkart
* Handles pagination and dynamic loading
* Saves data in structured format

###  **2. Sentiment Analysis**

* Classifies reviews into **Positive / Negative / Neutral**
* Model built using NLP techniques
* Achieves high accuracy and robustness

###  **3. Interactive Dashboard**

* Search for any product
* View sentiment distribution
* Time-based sentiment trend charts
* Review statistics and visual insights

###  **4. Database Storage**

* Efficiently stores scraped reviews and processed sentiments
* API endpoints for CRUD operations

###  **5. Full Automation**

* Automated scraping → preprocessing → sentiment annotation → dashboard visualization


## IV How to Run the Project

### **1️⃣ Clone the repository**

```
git clone https://github.com/your-username/Product-Sentiment-Analyzer.git
cd Product-Sentiment-Analyzer
```

### **2️⃣ Install dependencies**

```
pip install -r requirements.txt
```

### **3️⃣ Run the backend server**

```
python app.py
```

### **4️⃣ Run the frontend (if using React)**

```
npm install
npm start
```

### **5️⃣ Access the dashboard**

Open your browser and visit:

```
http://localhost:3000
```

## V Testing

* Unit testing for each module
* Integration testing of API + Database
* UI/UX testing for frontend dashboard
* Performance testing of scrapers

---

## VI Deployment

The app can be deployed using:

* **Render**
* **Heroku**
* **AWS EC2**


## 📜 License

This project is licensed under the **MIT License** – free for academic and personal use.


## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to open an issue or submit a pull request.

## ⭐ Acknowledgements

* BeautifulSoup & Selenium for scraping
* NLTK/spaCy for NLP
* Plotly/Chart.js for visualizations
* Flask/Django community

