import streamlit as st
import joblib
import openai

page = st.sidebar.selectbox("Choose a Tool", ["Home", "Classifier", "Disinfo", "GPT", "About"])

Model_path_1 = "saved_model.pk3"
Model_path_2 = "saved_model.pk4"

if page == "Home": 
    st.title("Welcome")
    #st.image(imageb)
    st.write("""
    Welcome to our digital suite, where we prioritize information integrity and transparency. Dive deep into our tools and combat disinformation, understand EU legal documents, or assess news authenticity.
    """)
    st.header("FIMI")
    st.write("sdfhksjhfkj")
    st.header("Tools")


    # Create three columns for the layout
    col1, col2, col3 = st.columns(3)


    # Content for Column 1 - Fake News App
    with col1:
        st.write("**Fake News App**")
        st.info("""
        Our Fake News App is designed to provide a quick check on news articles or snippets. Simply input your text, and our AI will analyze its authenticity, providing an assessment based on trusted sources and patterns of misinformation.
        """)


    # Content for Column 2 - Disinformation Checker
    with col2:
        st.write("**Disinformation Checker**")
        st.info("""
        The digital age is rife with misleading content. Our Disinformation Checker swiftly identifies falsehoods. Upload content, and our system quickly discerns the factual from the fabricated, ensuring you only absorb trustworthy information.""")


    # Content for Column 3 - EU Legal Document Chatbot
    with col3:
        st.write("**EU Legal Document Chatbot**")
        st.info("""
        EU legal documents are known for their complexity. With our EU Legal Document Chatbot, demystifying these texts becomes seamless. Input text or ask questions, and get concise explanations, making legal intricacies easier to grasp.""")


if page == "Classifier":
    pipeline = joblib.load(Model_path_1)
    st.title("Article Credibility Analysis")
    # User input for article
    user_input = st.text_area("Enter an article:")

    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    # Add a "Send Question" button
    if st.button("Check article"):
        if user_input:
            user_input_bow = pipeline.named_steps['bow'].transform([user_input])
    # Get the probability for the real news (labeled as '0')
            proba_real = pipeline.predict_proba([user_input])[0][0]  # adjusted the index 
    
    # Check the probability range
            if 0.4 <= proba_real <= 0.6:
                st.write("Analysis not possible - no clear signs for or against this articles credibility. Human analysis needed")
            elif proba_real > 0.6:
                st.write("The provided article has been flagged as '**Probably Credible**'. The analysis is based on a Logistical Regression ML-model, trained on a database of known false and true news articles. \n\nThe model makes no analysis of author intent. It is also important to keep in mind that the models verdict is based on probabilities, and can not be used as the single source for judgement on an articles credibility.")
            else:
                st.write("The provided article has been flagged as '**Probably Not Credible**'. \n\nThe analysis is based on a Logistical Regression ML-model, trained on a database of known false and true news articles. \n\nThe model makes no analysis of author intent. It is also important to keep in mind that the models verdict is based on probabilities, and can not be used as the single source for judgement on an articles credibility.")

if page == 'Disinfo':
    st.title("Disinformation Classifier")
    pipeline = joblib.load(Model_path_2)
    
    # User input for article
    user_input = st.text_area("Enter an article:")

    # Add a "Send Question" button
    if st.button("Check article"):
        if user_input:
            user_input_bow = pipeline.named_steps['bow'].transform([user_input])
    # Get the probability for the real news (labeled as '0')
            proba_real = pipeline.predict_proba([user_input])[0][0]  # adjusted the index
    
    # Check the probability range
            if 0.4 <= proba_real <= 0.6:
                st.write("Classification not possible - no clear signs of either Misinformation or Disinformation.")
            elif proba_real > 0.6:
                st.write("This article has been flagged as **Disinformation**. \n\nThis means that the classifier found high similarity between the article and other articles known to be disinformation. \n\nThe difference between disinformation and misinformation has to do with author intent. The classification of this article indicate a **high** probability of author malintent.\n\nIt is important to keep in mind that this classification is based on probabilities and similarity to historical articles, and does no analysis on author intent. An ML-classifier should never be used as the sole source of decisions.")
            else:
                st.write("This article has been flagged as **Misinformation**. \n\nThis means that the classifier found high similarity between the article and other articles known to be misinformation. \n\nThe difference between disinformation and misinformation has to do with author intent. The classification of this article indicate **low** probability of author malintent.\n\nIt is important to keep in mind that this classification is based on probabilities and similarity to historical articles, and does no analysis on actual author intent. An ML-classifier should never be used as the sole source of decisions.")

##########################################################
if page == "GPT":
    # Set up OpenAI API key
    openai.api_key = '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'

    st.title("Legal Framework Resource")
    left_column, right_column = st.columns([1,2])

    # Sample dictionary containing framework to website mapping
    framework_websites = {
        "GDPR": "https://gdpr-info.eu/",
        "AI Act": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A52021PC0206",
        "NIS 2 Directive": "https://eur-lex.europa.eu/eli/dir/2022/2555",
        "2019 Cybersecurity Act": "https://eur-lex.europa.eu/eli/reg/2019/881/oj",
        "e-Evidence Act": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32023R1543", #osäker på denna länken
        "Digital Service Act": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A32022R2065",
        "AI Liability Act": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52022PC0496",
        # ... add other documents and their corresponding websites here ...
    }

    def get_framework_description(framework):
        descriptions = {
            "GDPR": "The General Data Protection Regulation (GDPR) is a regulation in EU law on data protection and privacy in the European Union and the European Economic Area.",
            "AI Act": "The AI Act proposes regulations for artificial intelligence in the European Union.",
            "NIS 2 Directive": "The Directive on Security of Network and Information Systems (NIS 2) is the first piece of EU-wide legislation on cybersecurity.",
            "2019 Cybersecurity Act": "The Cybersecurity Act reinforces the mandate of the European Union Agency for Cybersecurity (ENISA).",
            "e-Evidence Act": "The e-Evidence Act pertains to electronic evidence in criminal matters.",
            "Digital Service Act": "The Digital Service Act aims to create a safer digital space.",
            "AI Liability Act": "The AI Liability Act is a conceptual framework for AI operations.",
            "Blank": "With Blank, the search will be general using all documents."
        }
        website_url = framework_websites.get(framework, None)
        return descriptions.get(framework, "Description not available."), website_url

    with left_column:
        #st.sidebar.title("Navigation")
        #st.sidebar.write("""
        #- [Disinformation Checker](#)
        #- [Legal Surfer](#)
        #- [Metrics & Graphs](#)
        #- [About the App](#)
        #""")
        st.info("This tool is here to help guide your deep journey into the magical world of EU legislation.\n\nSelect a specific legal framework to research below, or leave on 'Blank' to post  general question related to all relevant frameworks. \n\nThen select your level of expertise (Advanced - You have knowledge of key concepts and the relevant legal frameworks. Simplified - you want extra support in the answer). \n\nAfter this, send your question by pressing the button below.")
        
        legal_frameworks = ["Blank", "GDPR", "AI Act", "NIS 2 Directive",
                            "2019 Cybersecurity Act", "e-Evidence Act", "Digital Service Act", "AI Liability Act"]
        
        selected_framework = st.selectbox("Choose a Legal Framework:", legal_frameworks)
        description, website_url = get_framework_description(selected_framework)
        st.write(description)
        
        if website_url:
            st.write(f"[Source for {selected_framework}]({website_url})")

    with right_column:
        #st.write("Choose Your Expertise Level")
        expertise_level = st.radio("Select your level of expertise/the level of depth you want in the answer:", ("Advanced", "Simplified"))

        if expertise_level == "Advanced":
            st.write("You selected 'Advanced'. Enter your legal question in free format:")
            legal_question = st.text_area("Ask question here:")
        else:
            st.write("You selected 'Simplified'. Enter your legal question in free format:")
            legal_question = st.text_area("Ask question here:")

        # Add a "Send Question" button
        if st.button("Send Question"):
            if legal_question:
                # Create system messages and the user's message for the ChatGPT API
                messages = [
                    {"role": "system", "content": "You are helping EU law makers and decision makers with interpreting legal documents, especially regarding questions of disinformation, fake news and malinformation."},
                    {"role": "system", "content": "Keep the answers concise and factual, but assume that the reader is at expert level and have deep knowledge about key concepts and the relevant legal frameworks."},
                    {"role": "system", "content": "base your answers on the following legal frameworks: GDPR, AI Act, NIS 2 Directive, 2019 Cybersecurity Act, e-Evidence Act, Digital Service Act, AI Liability Act"},
                    {"role": "system", "content": "at the end of the reply, always note any sources you refer to or use in the response. when possible, mention the website to the sources."},
                ]

                if expertise_level == "Simplified":
                    # Append the message for Novice users
                    messages.append({"role": "user", "content": "Use a simplified language in all your answers, assume that the user do not have knowledge about key concepts and need some extra support in your answer."})


                # Add an additional system message if a specific framework is selected
                if selected_framework != "Blank":
                    messages.append({"role": "system", "content": f"Base your answer mainly on this legal framework {selected_framework}, how does the question relate to this framework?"})
                
                messages.append({"role": "user", "content": legal_question})

                # Use the ChatGPT API with the messages
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.3
                )
                
                response = completion.choices[0].message.content
                right_column.write(response)



##########################################################
if page == "About": 
    st.header("About")
    st.subheader("The Project")
    st.write("""
        This Streamlit page is created for a project which is a part of the course "Introduction to Human-centered AI” at the University of Gothenburg. We've had the privilege to collaborate with the Research Institutes of Sweden (RISE) for this project. Our wish is to contribute to the recently initiated research initiative, ATHENA, carried out by RISE in collaboration with the European Union's institutions and research partners.
    """)

    st.subheader("ATHENA Project Details")
    st.write("""
    ATHENA (An exposition on the foreign information manipulation and interference) is an EU project comprising 14 organizations from 11 countries, led by Trilateral, a UK-based research company. Its core mission is to safeguard democratic processes in the European Union (EU) from foreign information manipulation and interference (FIMI).
    """)
    st.write("""
    Through a combination of machine-learning algorithms, field studies, and cutting-edge detection tools, the project aims to extend the solution-space for policymakers, private stakeholders, and civil society actors to counteract FIMI.
    """)
    st.write("""
    Given the evolving tactics, techniques, and procedures (TTPs) of adversaries, ATHENA aspires to bolster EU's capability to counteract influence operations. This is achieved through a suite of tools, including a unique knowledge graph, toolbox, and dashboard, developed in tandem with law enforcement authorities, policymakers, CSOs, and the media.
    """)
    st.write("There are five core objectives to the project, represented in this image:")

    st.subheader("Machine Learning Model Metrics")
    st.write("**Transparency Note**")
    st.write("As students of the university of Gothenburg's masters program “Human-centered AI” a central part of our project is a steadfast commitment to transparency. It's crucial for users to understand how our model works, its strengths, and its limitations. By being transparent about these details we can ensure that users have the necessary context to interpret the model's outputs.")
    st.write("**Learning Accuracy:** Our model correctly learned from the examples 99.9% of the time.")
    st.write("**Testing Accuracy:** On new articles, it correctly identified \"fake\" news 96.12% of the time.")
    st.write("**Mistakes:** It wrongly called a real article \"fake\" 5.64% of the time. It wrongly called a fake article \"real\" 2.15% of the time.") # Used FPR and FNR here
    st.write("**Fairness:** Our model was consistent in its decisions, correctly identifying fake news 97.85% of the time across different articles.") # Used EO here
    st.write("**Trustworthiness:** If the model says an article is \"fake,\" it's right 94.89% of the time. If the model says an article is \"real,\" it's right 97.62% of the time.") # Used PPV and NPV here

    st.write("""
    Our news-checking model is reliable and fair in its predictions, but it's always wise to double-check news from other sources.
    """)




    st.subheader("Team Members")
    st.write("- Jonathan: [Email/Contact]")
    st.write("- Magnus: [Email/Contact]")
    st.write("- Linus: [Email/Contact]")
    st.write("- Ebba: [Email/Contact]")
    st.write(
        "For more about our MSc program, [you can check out the page for the program](https://www.gu.se/en/study-gothenburg/human-centered-artificial-intelligence-masters-programme-t2hai).")


