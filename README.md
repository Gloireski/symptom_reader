# symptom_reader

# **Introduction**

## **The Project** 

In today's digital world, we often rely on the internet to explain our symptoms
and provide insights into potential health issues. Symptom_Reader aims to bridge this gap 
by offering reliable diagnoses and holistic treatment options, including OTC medications, in a single click.
While no web application can replace a professional medical diagnosis, Symptom_Reader assists users 
in understanding their symptoms and determining preliminary actions before consulting a doctor.

ymptom_reader is a cutting-edge web application designed to deliver accurate medical 
diagnoses based on user-reported symptoms. It offers comprehensive home remedies and 
over-the-counter medication recommendations for various medical conditions. Inspired by the 
need for accessible and reliable health information, Symptom_reader seamlessly integrates 
holistic and medical treatment options. Beyond identifying illnesses, Symptom_reader 
empowers users with the knowledge to effectively manage and treat their symptoms. This is the core purpose of Symptom_Reader.

## **The Context**

This project serves as our Portfolio Project, marking the conclusion of our Foundations Year at Holberton School.
We had the freedom to select our teammates and choose the focus of our work, provided we deliver a 
functioning program by the end of the three-week development period.

## **The Team**  

We are three software Engineers who are passionate about coding and our diverse careers and cultures
from three different African countries.

- Amanda Mabunda is a South African citizen graduated from Biotechnology, a software engineer
  and founder of Symptom_Reader [@Amatas_aura](https://x.com/Amatas_aura)

- Belem Gloire BEKOUTOU is a Chadian citizen living in Morocco, an IT systems engineering graduate with strong
  software implementation process experience and Co-Founder of Symptom_Reader [@GloireBelem](https://x.com/GloireBelem)

- Ado Abdullateef is a Nigerian citizen, #adul please add your infomation and also fix it on the about us page, you didnt update it
  and co-Founder of Symptom_Reader [@adoabdullateef](https://x.com/adoabdullatee)

follow us on Twitter for more.

## **Blog Posts**

After the development phase, we each wrote a blog post to reflect on the development journey of Symptom_Reader

- Amanda's article [Title](url)
- Belem's article [Title](url)
- Abdullateef's article [Title](url)

## **Tutorial**

[Symtom_Reader](https://gloire-belem.tech/)

Here is a preview of our main feature, resukts page with users diagnosis and recommandations

![Results page](image-url)

Here is a simple flow for the user experience on Symptom_Reader

![Create a simple flow diagram](image-url)

# **Architectre**

## **Overview**

Our web application predominantly employs HTML, CSS, and JavaScript for frontend development. 
We prioritized simplicity and user-friendliness, focusing on crafting intuitive interfaces without heavy reliance on frameworks. 
Bootstrap streamlined tasks such as user authentication. Python Flask handles backend operations, including routing and data processing. 
Machine learning, based on Kaggle disease prediction datasets, aids in disease prediction. 
Our approach emphasizes a balanced blend of technology to ensure a seamless and effective user experience.

![Create a simple flow diagram](image-url)

## **Final model training**

We used training and testing datasets from kaggle, after doing some earlier training on 80% of the data and make sure our models worked well using confusion matrix plots we started final training on the whole dataset. To achieve an accurate and  robust model we combined three machine learning algorithms: Support Vector Classifier, Gaussian Naive Bayes Classifier and Random Forest Classifier. We used label encoder to convert the prognosis column to numerical variable which is more suitable for model training. We finally put the column in dictionary for make sure we have the right name in the inputs.

## **Reading input data and predict**
finally we’ve created a function predict_disease that take as parameter a string of metrics separated by a comma, theses metrics name present will be convert to 1 and the final prediction is done accordingly by combining our three algorithms
