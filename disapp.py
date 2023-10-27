if page == "Credibility Checker":
    st.title("Article Credibility Analysis")
    st.write("This is an AI-powered credibility application. Developed by master-students at Gothenburg's University in collaboration with RISE, the Research Institutes of Sweden. Learn more about the project in the about section.")
    st.write("Paste the body of an article you want to check if it is credible or not. A machine learning (ML) classifier will predict if the article is credible or not. And the OpenAI large language model will make further analysis and give you insights to fake news, misinformation and applicable legal frameworks.")
    st.write("For the analysis of the text, ChatGPT was utilized. Customizing prompts enabled the extraction of specific analytical insights from the verdict. The machine learning (ML) verdict is integrated within the prompt messages, holding the highest value. ChatGPT operates based on information available up to January 2022.")
    st.write("Option 1: Paste an article or text you want to analyze, and press 'Analyze article'.\n\nOption 2 (TO BE ADDED): Together with your article, add the news outlet/source and author of the article, do get a deeper analysis.\n\nOption 3: If you only want a quick check on an author or source, enter them below and press 'Check only source' or 'Check only author'.")
    st.write("For now, only enter text into 1 text-box, and press the relevant analyze-button. Functionality will be added with a later update.")
    
    left_column, right_column = st.columns([1,2])
    #st.set_option('deprecation.showPyplotGlobalUse', False)     ## gör denna nåt?
    with left_column:
        st.image("textanalys.jpeg", caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    
    with right_column:
        artikel_input = st.text_input("Paste your article here:", help="""**Examples of prompts for chat-GPT**:   
        - Your primary task is to analyze the given text, identifying indicators of potential disinformation or fake news. This analysis should span across linguistic cues, historical veracity, and more.  
        - Ensure responses are succinct and fact-driven. Your role is to guide EU decision-makers by analyzing for signs of disinformation within relevant legal frameworks.""")

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
                {"role": "system", "content": "Ensure responses are succinct and fact-driven, max around 100 words."},
            ]
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.3
            )
            response = completion.choices[0].message.content
            right_column.write(response)
        
        # Handle "Send Author" button press
        if send_author_button:
            messages = [
                # ... messages tailored for author analysis ...
                {"role": "system", "content": f"Your role is to nalyze the provided author: {author_input} for credibility, in terms of previous articles, and connections to fake news or disinformation."},
                {"role": "system", "content": "Use your knowledge about the author, and give a description of the author, and in what way he/she can be tied to fake news or disinformation, or if the author can be seen as credible. Motivate your answer, and make sure to mention the authors name in your response."},
                {"role": "system", "content": "Ensure responses are succinct and fact-driven, max around 100 words."},
            ]
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.3
            )
            response = completion.choices[0].message.content
            right_column.write(response)
        
        # Handle main "Analyze" button press
        if send_request:
            user_input = artikel_input
            ### cash kod ####
            #pipeline = model1
            #user_input_bow = pipeline.named_steps['bow'].transform([user_input])
            #proba_real = pipeline.predict_proba([user_input])[0][0]
            ##############
            pipeline = joblib.load(model1)            ## modellen
            user_input_bow = pipeline.named_steps['bow'].transform([user_input])
            proba_real = pipeline.predict_proba([user_input])[0][0]  # adjusted the index
            # Check the probability range
            if 0.4 <= proba_real <= 0.6:
                st.write("Analysis not possible - no clear signs for or against this articles credibility. Human analysis needed")
                clverdict = "Credibility Analysis Not Possible."
            elif proba_real > 0.6:
                st.write("Important note: The model makes no analysis of author intent. It is also important to keep in mind that the models verdict is based on probabilities, and can not be used as the single source for judgement on an articles credibility.")
                clverdict = "Probably Credible."
            else:
                st.write("Important note: The ML model used makes no analysis of author intent. It is also important to keep in mind that the models verdict is based on probabilities, and can not be used as the single source for judgement on an articles credibility.")
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
                    "content": f"If you receive a source in {source_input}, use this as the source in the 'Source Verification' below. If you receive a source in {source_input}, name it and give a short description of it (maximum one sentence), pointing out how it is most likely credible/not credible. If you do not recieve a source, State 'No source found.'. If you receive a source, but you are unable to verify its credibility, state this and explain why you were not able to determine its credibility."
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
                messages.append({"role": "system", "content": f"This is the source/media outlet of the article you are analysing: {source_input}."})
                messages.append({"role": "system", "content": "for the source/media outlet verification, use your historical knowledge, to decide if this source/media outlet has previously posted credible content, or not."})
                #messages.append({"role": "system", "content": "Be sure to mention the source by name in your verdict."})           ### för test      
                #messages.append({"role": "system", "content": "Ensure responses are succinct and fact-driven."})
            
            if author_input:
                messages.append({"role": "system", "content": f"This is the author of the article you are analysing: {author_input}."})
                messages.append({"role": "system", "content": "for the author credibility analysis, use your historical knowledge, to decide if this author has previously written credible work in credible media, or not."})
                #messages.append({"role": "system", "content": "Be sure to mention the author by name in your verdict."})          ### för test  
                #messages.append({"role": "system", "content": "Ensure responses are succinct and fact-driven."})
        
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
