from groq import Groq
from dotenv import load_dotenv
import os
from modules.sys_prompt import sys_prompt

load_dotenv()

tone_maps={
    "Casual":"Write like you're explaining to a friend. Use informal language, maybe a light joke if it fits. Very relaxed.",
    "Academic":"Maintain a scholarly tone but still sound like a real student/researcher — not a machine. Keep technical terms.",
}

intensity_maps = {
    "Light": "Make minimal changes. Only fix obvious AI patterns like overused words and missing contractions. Keep the structure and flow mostly intact.",
    "Medium": "Rewrite sentences moderately. Vary sentence lengths, inject natural hedging phrases, replace AI vocabulary, and adjust tone — but don't restructure the whole text.",
    "Heavy": "Aggressively rewrite the text. Significantly restructure sentences, rephrase ideas in a completely different way, vary rhythm heavily, and make it sound like a distinct human voice — while keeping all original meaning intact."
}

def humanize_content(text: str, tone: str = 'Casual', intensity: str = 'Light'):
    try:
        client=Groq(api_key=os.getenv("GROQ_API_KEY"))
    except Exception as e:
        return f"Couldn't load the Api Key: {e}"
    try:
        user_input = f"Rewrite this text:\n\n{text}\n\nTONE: {tone_maps.get(tone, '')}\nINTENSITY: {intensity_maps.get(intensity.lower(), '')}"
        
        chat_completions = client.chat.completions.create(
            model='openai/gpt-oss-20b',
            messages=[
                {'role': 'system', 'content': sys_prompt},
                {'role': 'user', 'content': user_input}
            ],
            temperature=0.85  
        )
        
        result = chat_completions.choices[0].message.content
        
        if intensity == 'Heavy':
            second_pass = f"This text still sounds slightly AI-written. Make it sound even more natural and human. Fix any remaining robotic patterns:\n\n{result}"
            chat_completions2 = client.chat.completions.create(
                model='openai/gpt-oss-20b',
                messages=[
                    {'role': 'system', 'content': sys_prompt},
                    {'role': 'user', 'content': second_pass}
                ],
                temperature=0.9
            )
            result = chat_completions2.choices[0].message.content
        return result
    
    except Exception as e:
        return f"Couldn't Generate Response: {e}"
