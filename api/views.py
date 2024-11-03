# api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

from myproject.settings import ENGINE_ID, GOOGLE_SEARCH_API, GROQ_API


load_dotenv()

from groq import Groq




class ExternalDataView(APIView):

    def google_search(self, search_term, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return res['items']
    
    def get_google_searches(self, sentence):

        results = self.google_search(
            sentence, GOOGLE_SEARCH_API, ENGINE_ID, num=3)
        return results
    
    def format_sources(self,results):
        sources = []
        sources_text = ""
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title available')
            link = result.get('link', 'No link available')
            snippet = result.get('snippet', 'No snippet available')
            
            sources.append(link)
            
            sources_text += f"Source {i}:\nTitle: {title}\nURL: {link}\nSummary: {snippet}\n\n"
            
        return sources_text, sources
    
    def post(self, request):
        sentence = request.data.get("sentence")
        try:
            search_res = self.get_google_searches(sentence=sentence)
            
            sources_text, sources = self.format_sources(search_res)
            
           
            prompt = (
                f"Answer the following question based on the provided sources and your intelligence too making it your answer.\n\n"
                f"Question: {sentence}\n\n"
                f"Sources:\n{sources_text}\n"
                f"Please provide a concise answer to the question and at end give citations links {sources}"
            )
            client = Groq(
            api_key=GROQ_API)
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-8b-8192",
            )

        
            return Response(chat_completion.choices[0].message.content, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

      