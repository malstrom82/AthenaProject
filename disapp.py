import streamlit as st
import joblib
import openai
#import gdown

##################################
import urllib.request

# For saved_model.pk3
url1 = 'https://github.com/malstrom82/AthenaProject/releases/download/version1/saved_model.pk3'
filename1 = url1.split('/')[-1]
urllib.request.urlretrieve(url1, filename1)

# For saved_model.pk4
url2 = 'https://github.com/malstrom82/AthenaProject/releases/download/version1/saved_model.pk4'
filename2 = url2.split('/')[-1]
urllib.request.urlretrieve(url2, filename2)

##################################
# Caching the download function ensures model files are only downloaded once
#@st.cache_data(show_spinner=True)
#def download_model(file_id, output):
#    url = f'https://drive.google.com/uc?id={file_id}'
#    gdown.download(url, output, quiet=False)

## Google Drive file IDs for your model files
#model_file_id_1 = '1LaC4Kh-ANtqeBafUxYabsP_hBAvGPyQE'
#model_file_id_2 = '1FEaetS71MEWf59-jPyvkPH8So3ct2p7j'

# Paths to save the downloaded models
#model_path_1 = 'saved_model.pk3'
#model_path_2 = 'saved_model.pk4'

# Download the model files
#download_model(model_file_id_1, model_path_1)
#download_model(model_file_id_2, model_path_2)

#################################
####################
# Set up OpenAI API key
# REDACTED

# Retrieve the OpenAI API key from Streamlit secrets
api_key = st.secrets["openai"]["api_key"]

# Set up OpenAI API key
openai.api_key = api_key
#####################

page = st.sidebar.selectbox("Choose a Tool", ["Home", "Credibility Checker", "Disinformation Detector", "Legal Helper", "About"])

model_path_1 = "saved_model.pk3"
model_path_2 = "saved_model.pk4"

if page == "Home": 
    st.title("Athena-Disapp: Credibility assessment in your pocket")
    #st.image(imageb)
    st.write("""
    Welcome to our digital suite, where we prioritize information integrity and transparency. Dive deep into our tools and combat disinformation, understand EU legal documents, or assess news authenticity.\n\nFollow the steps below to check an articles credibility, find possible signs of malintent, and get support on legal frameworks.\nOr use the tools separately - it's all up to you!
    """)
    st.header("FIMI")
    st.write("sdfhksjhfkj")
    st.header("Tools & suggested workflow")


    # Create three columns for the layout
    col1, col2, col3 = st.columns(3)


    # Content for Column 1 - Fake News App
    with col1:
        st.write("**Step 1 - Credibility Checker**")
        st.info("""
        The Athena-Disapp is designed to provide a quick check on news articles or snippets. Simply input your text, and our AI will analyze its credibility, providing an assessment based on trusted sources and patterns of misinformation.
        """)


    # Content for Column 2 - Disinformation Detector
    with col2:
        st.write("**Step 2 - Disinformation Detector**")
        st.info("""
        The digital age is rife with misleading content. If a non credible article has been found, our Disinformation Checker swiftly identifies signs of malintent, or if it rather seems like a case of misinformation with no bad intent. Upload content, and our system quickly discerns the factual from the fabricated, ensuring you only absorb trustworthy information.""")


    # Content for Column 3 - EU Legal Document Chatbot
    with col3:
        st.write("**Step 3 - EU Legal Document Chatbot**")
        st.info("""
        EU legal documents are known for their complexity. With our EU Legal Document Chatbot, demystifying these texts becomes seamless. After finding a non credible text, that bare signs of malintent and disinformation, ask questions/chat with legal documents and get concise explanations on how your case relates to regulation, making legal intricacies easier to grasp.""")


if page == "Credibility Checker":
    st.title("Article Credibility Analysis")
    left_column, right_column = st.columns([1,2])
    st.set_option('deprecation.showPyplotGlobalUse', False)     ## gör denna nåt?

    with right_column:
        artikel_input = st.text_input("Paste your article here:")

        col1, col2 = st.columns(2)
        source_input = col1.text_input("For deeper analysis, paste the news outlet or source here (optional):")
        send_source_button = col2.button("Check only source")

        col3, col4 = st.columns(2)
        author_input = col3.text_input("For deeper analysis, paste the author name here (optional):")
        send_author_button = col4.button("Check only author")
        
        send_request = st.button("Analyze article")

        # Handle "Send Source" button press
        if send_source_button:
            messages = [
                # ... messages tailored for source analysis ...
                {"role": "system", "content": f"Your role is to nalyze the provided source/news outlet: {source_input} for credibility, in terms of previous articles and publications, and connections to fake news or disinformation."},
                {"role": "system", "content": "Use your knowledge about the source, and give a description of the source, and in what way it can be tied to fake news or disinformation, or if the source can be seen as credible. Motivate your answer, and make sure to mention the source by name in your response."},
            ]
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.3
            )
            response = completion.choices[0].message.content
            right_column.write(response)

        # Handle "Send Author" button press
        elif send_author_button:
            messages = [
                # ... messages tailored for author analysis ...
                {"role": "system", "content": f"Your role is to nalyze the provided author: {author_input} for credibility, in terms of previous articles, and connections to fake news or disinformation."},
                {"role": "system", "content": "Use your knowledge about the author, and give a description of the author, and in what way he/she can be tied to fake news or disinformation, or if the author can be seen as credible. Motivate your answer, and make sure to mention the authors name in your response."},
            ]
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.3
            )
            response = completion.choices[0].message.content
            right_column.write(response)

        # Handle main "Analyze" button press
        elif send_request:
            user_input = artikel_input
            pipeline = joblib.load(model_path_1)            ## modellen
            user_input_bow = pipeline.named_steps['bow'].transform([user_input])
            proba_real = pipeline.predict_proba([user_input])[0][0]  # adjusted the index
        # Check the probability range
            if 0.4 <= proba_real <= 0.6:
                st.write("Analysis not possible - no clear signs for or against this articles credibility. Human analysis needed")
                clverdict = "Credibility Analysis Not Possible."
            elif proba_real > 0.6:
                st.write("The provided article has been flagged as '**Probably Credible**'. The analysis is based on a Logistical Regression ML-model, trained on a database of known false and true news articles. \n\nThe model makes no analysis of author intent. It is also important to keep in mind that the models verdict is based on probabilities, and can not be used as the single source for judgement on an articles credibility.")
                clverdict = "Probably Credible."
            else:
                st.write("The provided article has been flagged as '**Probably Not Credible**'. \n\nThe analysis is based on a Logistical Regression ML-model, trained on a database of known false and true news articles. \n\nThe model makes no analysis of author intent. It is also important to keep in mind that the models verdict is based on probabilities, and can not be used as the single source for judgement on an articles credibility.")
                clverdict = "Probably Not Credible."
            
            messages = [
                # ... messages for complete analysis ...
                {"role": "system",
                    "content": "Your primary task is to analyze the given text, identifying indicators of potential disinformation or fake news. This analysis should span across linguistic cues, historical veracity, and more."
                },
                {"role": "system",
                    "content": "Ensure responses are succinct and fact-driven. Your role is to guide EU decision-makers by analyzing for signs of disinformation within relevant legal frameworks."
                },
                {"role": "system",
                    "content": "Structure your analysis under the following headers: 'Analytics:', 'Summary:', 'Legality:', 'Disclaimer:'."
                },
                {"role": "system",
                    "content": "In the 'Analytics' section, present each analytical tool, its analysis, and the verdict, all in a clear list."
                },
                ######## för test ###########################################
                #{"role": "system",
                #    "content": "You can simulate analytical results and scenarios. The goal is to assess the feasibility and effectiveness of the concept."
                #},
                {"role": "system",
                    "content": "For the analytics section, use the following headers and sub-headers: ML Classifier assessment, Source verification, Author verification, Textual analysis (sub: Fact checking & Sentiment analysis), Network analysis (sub: Propagation pattern analysis & Source cluster analysis), Linguistic analysis (Sub: Spelling and Grammar check & Writing style analysis), Bias & Agenda analysis, Historical crosscheck."
                },
                {"role": "system",
                    "content": "Use the following prompts for analysis:"
                },
                ######## classifiern ###################################################
                {"role": "system",
                    #"content": "ML classifier assessment: 'Based on a ML classifier (xx logistic regression, trained on yy database), this article is classified as most likely (placeholder).'. For now, make this verdict true/false, based on the majority of the other metrics used below. Leter use this as the verdict of the ML classifier in your later summarization of all metrics."
                    "content": f"ML classifier assessment: 'Based on a ML classifier (xx logistic regression, trained on yy database), this article is classified as {clverdict}.'" ####### få in variabeln här (obs dummy-kod)
                },
                {"role": "system",
                    "content": f"together with 'ML Classifier assessment', also type out the raw text in this variable: {clverdict}."
                },    
                #{"role": "system",
                #    "content": "Source Verification: 'Based on historical data, is this articles source a reputable source for accuracy and credibility?' Response should be: 'Source Verification: The source of this text is reputable/non-reputable based on historical data.', or 'No historical data on this source was found - credibility cannot be confirmed'."
                #},
                {"role": "system",
                    "content": f"If you receive a source in {source_input}, use this as the source in the 'Source Verification' below. If you receive a source in {source_input}, name it and give a short description of it, pointing out how it is most likely credible/not credible. If you do not recieve a source, State 'No source found.'. If you receive a source, but you are unable to verify its credibility, state this and explain why you were not able to determine its credibility."
                },
                {"role": "system",
                    "content": "Source Verification: 'Based on historical data, is this articles source a reputable source for accuracy and credibility?' Response: Provide a response using the provided text, and your knowledge, or 'No historical data on this source was found - credibility cannot be confirmed'."
                },
                #{"role": "system",
                #    "content": "Author Credibility: 'Historically, how credible is the author in terms of journalistic integrity?' Response: 'Author Credibility: The author of the text is credible/non-credible based on past articles.', or 'No past articles tied to this author was found'."
                #},
                {"role": "system",
                    "content": f"If you receive an author in {author_input}, use this as the source in the 'Source Credibility' section below. If you receive an author in {author_input}, name it and give a short description of it, pointing out how it is most likely credible/not credible. If you do not recieve an author, State 'No Author found.'. If you receive an author, but you are unable to verify its credibility, state this and explain why you were not able to determine its credibility."
                },
                {"role": "system",
                    "content": "Author Credibility: 'Historically, how credible is the author in terms of journalistic integrity?' Response: Provide a response using the provided text and your knowledge, or 'No past articles tied to this author was found'."
                },
                {"role": "system",
                    "content": "Fact Check: 'Is the statements or facts in the provided text historically accurate?' Response: Provide a response using the provided text, and your knowledge."
                },
                {"role": "system",
                    "content": "Sentiment Analysis: 'Does the provided text [text] convey a neutral or biased sentiment?' Response: Provide a response using the provided text, and your knowledge."
                },
                {"role": "system",
                    "content": "Network Analysis: 'Historically, how have similar topics or claims propagated in credibility and source distribution?' Response: 'Network Analysis: Topics similar to this have [spread through reputable channels/been associated with misinformation campaigns].'"
                },
                {"role": "system",
                    "content": "Linguistic Analysis: 'Are there grammatical or spelling errors in this sentence: [sentence]?' Response: 'Linguistic Check: The text [has/doesn't have] significant linguistic errors.'"
                },
                {"role": "system",
                    "content": "Writing Style Analysis: 'Does the text [text] use sensationalist or emotive language indicating bias?' Response: 'Writing Style Check: The text [uses/doesn't use] sensationalist or emotive language.'"
                },
                {"role": "system",
                    "content": "Bias & Agenda Analysis: 'Does the text [text snippet] show indications of political or commercial bias?' Response: 'Bias Analysis: The text [shows/doesn't show] signs of [political/commercial] bias.'"
                },
                {"role": "system",
                    "content": "External Database Check: 'Up to 2022, have similar claims been identified as fake news: [claim or topic]?' Response: 'Database Check: This type of claim [has/hasn't] been identified in historical fake news records.'"
                },
                {"role": "system",
                    "content": "After analysis, aggregate the 'likely true' and 'likely false' verdicts for a summarized result. Example: 'After assessing all metrics, the content appears likely true/mostly false.'"
                },
                {"role": "system",
                    "content": "Always include a Summary-section (after Analysis, before Legality): 'Summary: After assessing all metrics, the content appears to be likely credible/most likely not credible.'. In the summary, analyse all the results from the analysis section, and combine the results into a final verdict. Always include either 'Based on the full analysis, the article is most likely **credible**' and provide your reasoning for this, or 'Based on the full analysis, the article is most likely **not credible**' with your motivation, or a neutral similar answer, if analysis did not provide strong fake/real info."
                },
                {"role": "system",
                    "content": "In the summary section, when you assess all analytic metrics and give your final summarized verdict of credible/not credible, give the result from the ML classifier the most weight. Use the other metrics to support the ML classifier, or to question it's accuracy, if all other metrics diverge from the classifier verdict in their verdicts."
                },
                {"role": "system",
                    "content": "For legality, reference these frameworks: GDPR, AI Act, NIS 2 Directive, 2019 Cybersecurity Act, e-Evidence Act, Digital Service Act, AI Liability Act. Include other relevant EU frameworks only when pertinent. if the text does not relate in any way to one or more legal frameworks, leave the Legality-section empty, with the text 'No relevant connections found to known EU legal frameworks.'."
                },
                {"role": "system",
                    "content": "Always end your response with a disclaimer-section: 'Disclaimer: Labeling an article as 'fake' or 'real'/credible or not credible is provisional due to inherent uncertainties. Consult multiple methods for any credibility assessment.'.  If deemed 'fake', mention the broader societal and individual implications of disinformation. For suspected disinformation, provide avenues for reporting this to relevant authorities."
                },
                {"role": "system",
                    "content": "If external sources are consulted or utilized, list them comprehensively at the end of your response. If none are used, state this."
                },
                {"role": "system",
                    "content": "Your response will be used in a streamlit app. Make sure you use the following formatting: In all your response, make these BOLD: Section headers, sub headers (from 'ML Classifier assessment' to 'External Database Check'), and the 'likely true' or 'likely fake' in the summary-section. Sub-headers with their text should be in pointed lists."
                },
                #{"role": "system",
                #    "content": "For all sections and prompts: If you dont know enough information to make an analysis or provide an answer, state this as 'Not enough information to provide an analysis'. In this case leave that analysis blank, with only this message."
                #},
                ############# FIXA!!
                {"role": "system",
                    "content": "If in your analysis you find signs of disinformation/fake news in the text (it has sensationalist language, biased or infactual content or some other sign), give examples from the text of where you see those signs, and why. Do this for each of the analytic tools above, if you find clear signs."
                },
            ]
            
            if source_input:
                messages.append({"role": "user", "content": f"This is the source/media outlet of the article you are analysing: {source_input}."})
                messages.append({"role": "user", "content": "for the source/media outlet verification, use your historical knowledge, to decide if this source/media outlet has previously posted credible content, or not."})
                messages.append({"role": "user", "content": "Be sure to mention the source by name in your verdict."})           ### för test      

            if author_input:
                messages.append({"role": "user", "content": f"This is the author of the article you are analysing: {author_input}."})
                messages.append({"role": "user", "content": "for the author credibility analysis, use your historical knowledge, to decide if this author has previously written credible work in credible media, or not."})
                messages.append({"role": "user", "content": "Be sure to mention the author by name in your verdict."})          ### för test  


            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.3
            )

            response = completion.choices[0].message.content
            right_column.write(response)

#######################################################################

    #pipeline = joblib.load(model_path_1)
    #st.title("Article Credibility Analysis")
    # User input for article
    #user_input = st.text_area("Enter an article:")

    #st.set_option('deprecation.showPyplotGlobalUse', False)
    
    # Add a "Send Question" button
    #if st.button("Check article"):
        #if user_input:
            #user_input_bow = pipeline.named_steps['bow'].transform([user_input])
    # Get the probability for the real news (labeled as '0')
            #proba_real = pipeline.predict_proba([user_input])[0][0]  # adjusted the index 
    
    # Check the probability range
            #if 0.4 <= proba_real <= 0.6:
                #st.write("Analysis not possible - no clear signs for or against this articles credibility. Human analysis needed")
            #    clverdict = "Unavailable"
            #elif proba_real > 0.6:
                #st.write("The provided article has been flagged as '**Probably Credible**'. The analysis is based on a Logistical Regression ML-model, trained on a database of known false and true news articles. \n\nThe model makes no analysis of author intent. It is also important to keep in mind that the models verdict is based on probabilities, and can not be used as the single source for judgement on an articles credibility.")
             #   clverdict = "Credible"
            #else:
                #st.write("The provided article has been flagged as '**Probably Not Credible**'. \n\nThe analysis is based on a Logistical Regression ML-model, trained on a database of known false and true news articles. \n\nThe model makes no analysis of author intent. It is also important to keep in mind that the models verdict is based on probabilities, and can not be used as the single source for judgement on an articles credibility.")
            #    clverdict = "Not Credible"

if page == 'Disinformation Detector':
    st.title("Disinformation Detector")
    pipeline = joblib.load(model_path_2)
    
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
if page == "Legal Helper":
    # Set up OpenAI API key
    # REDACTED

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
