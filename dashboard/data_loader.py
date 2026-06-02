import pandas as pd
import json
import os

def load_data():
    """Încarcă datele din fișierul JSON curățat"""
    file_path = os.path.join('data', 'E_Commers_jobs_done.json')
    
    try:
        df = pd.read_json(file_path)
        print(f"Date încărcate cu succes: {len(df)} înregistrări")
        print(f"Coloane găsite: {df.columns.tolist()}")
        return df
    except FileNotFoundError:
        print(f"Eroare: Nu s-a găsit fișierul {file_path}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Eroare la încărcare: {e}")
        return pd.DataFrame()

def get_city_counts(df):
    """Calculează numărul de joburi pe oraș"""
    # Folosim coloana 'city' care există
    if 'city' in df.columns:
        city_counts = df['city'].value_counts().reset_index()
        city_counts.columns = ['city', 'count']
        print(f"Găsite {len(city_counts)} orașe distincte")
        return city_counts.head(20)
    else:
        print("Nu s-a găsit coloana 'city'")
        return pd.DataFrame()

def get_skills_dataframe(df):
    """Creează DataFrame cu skill-uri"""
    if 'Skills' in df.columns:
        all_skills = []
        for skills_list in df['Skills'].dropna():
            if isinstance(skills_list, list):
                for skill in skills_list:
                    if skill and skill.strip():
                        all_skills.append({'skill': skill.strip()})
            elif isinstance(skills_list, str):
                # Dacă e string, împarte după virgulă
                for skill in skills_list.split(','):
                    if skill and skill.strip():
                        all_skills.append({'skill': skill.strip()})
        
        if all_skills:
            skills_df = pd.DataFrame(all_skills)
            skills_df = skills_df['skill'].value_counts().reset_index()
            skills_df.columns = ['skill', 'count']
            print(f"Găsite {len(skills_df)} skill-uri unice")
            return skills_df.head(20)
        else:
            print("Nu s-au găsit skill-uri în coloana 'Skills'")
    else:
        print("Nu s-a găsit coloana 'Skills'")
    
    return pd.DataFrame()

def get_job_titles_dataframe(df):
    """Creează DataFrame cu titluri de joburi"""
    # Folosim coloana 'Title' care există
    if 'Title' in df.columns:
        job_titles_df = df['Title'].value_counts().reset_index()
        job_titles_df.columns = ['job_title', 'count']
        print(f"Găsite {len(job_titles_df)} titluri de job distincte")
        return job_titles_df.head(20)
    else:
        print("Nu s-a găsit coloana 'Title'")
        return pd.DataFrame()

def get_unique_skills(df):
    """Extrage skills unice din dataframe"""
    if 'Skills' in df.columns:
        all_skills = []
        for skills_list in df['Skills'].dropna():
            if isinstance(skills_list, list):
                for skill in skills_list:
                    if skill and skill.strip():
                        all_skills.append(skill.strip())
            elif isinstance(skills_list, str):
                for skill in skills_list.split(','):
                    if skill and skill.strip():
                        all_skills.append(skill.strip())
        return list(set(all_skills))
    return []

def filter_by_country(df, country):
    """Filtrează joburile după țară"""
    if 'country' not in df.columns:
        return df
    
    if country == 'Toate' or country == 'All':
        return df
    return df[df['country'] == country]

def prepare_region_data(df):
    """Pregătește date pentru hartă pe regiuni"""
    if 'region' in df.columns:
        region_counts = df['region'].value_counts().reset_index()
        region_counts.columns = ['region', 'count']
        return region_counts
    else:
        print("Nu s-a găsit coloana 'region'")
        return pd.DataFrame()

def prepare_city_data(df, top_n=100):
    """Pregătește date pentru orașe"""
    if 'city' in df.columns:
        city_counts = df['city'].value_counts().reset_index()
        city_counts.columns = ['city', 'count']
        return city_counts.head(top_n)
    else:
        print("Nu s-a găsit coloana 'city'")
        return pd.DataFrame()

def clean_experience_level(df):
    """Combină 'Not Applicable' și 'N/A' în 'Not Required'"""
    if 'Experience' in df.columns:
        df['Experience'] = df['Experience'].replace(['Not Applicable', 'N/A'], 'Not Required')
    return df