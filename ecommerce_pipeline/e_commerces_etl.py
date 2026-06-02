"""
E-Commerce Job Market Analysis - ETL Pipeline
Versiunea unificată - FĂRĂ DEPENDENȚE EXTERNE (doar re pentru skill extraction)
"""

import os
import json
import glob
import re
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from collections import Counter
from typing import List, Dict, Any, Set, Optional

# =====================================================
# CONFIGURARE CĂI (PATH CONFIGURATION)
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
DATA_HELPERS_DIR = os.path.join(BASE_DIR, "data", "helpers")
LOCATION_REPORTS_DIR = os.path.join(DATA_HELPERS_DIR, "location_reports")

# Creează folderele dacă nu există
for dir_path in [DATA_RAW_DIR, DATA_PROCESSED_DIR, DATA_HELPERS_DIR, LOCATION_REPORTS_DIR]:
    os.makedirs(dir_path, exist_ok=True)


# =====================================================
# FUNCȚII DE UTILITATE (UTILITY FUNCTIONS)
# =====================================================

def load_json(filepath: str) -> Any:
    """Încarcă un fișier JSON și returnează conținutul."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"  ⚠️ Fișier negăsit: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"  ⚠️ JSON invalid: {filepath}")
        return None


def save_json(data: Any, filepath: str, indent: int = 4) -> str:
    """Salvează datele într-un fișier JSON."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    items_count = len(data) if isinstance(data, list) else 'N/A'
    print(f"  ✅ Salvat: {os.path.basename(filepath)} ({items_count} items)")
    return filepath


def save_processed(data: Any, filename: str) -> str:
    """Salvează date procesate în folderul processed/."""
    return save_json(data, os.path.join(DATA_PROCESSED_DIR, filename))


def save_helper(data: Any, filename: str) -> str:
    """Salvează fișiere helper în folderul helpers/."""
    return save_json(data, os.path.join(DATA_HELPERS_DIR, filename))


def load_processed(filename: str) -> Any:
    """Încarcă date procesate din folderul processed/."""
    return load_json(os.path.join(DATA_PROCESSED_DIR, filename))


def load_helper(filename: str) -> Any:
    """Încarcă fișiere helper din folderul helpers/."""
    return load_json(os.path.join(DATA_HELPERS_DIR, filename))


def parse_date(date_str: str) -> Optional[date]:
    """
    Extrage data (primele 10 caractere) și o transformă într-un obiect 'date'.
    (Aceeași logică ca în notebook, celula 12)
    """
    if not date_str or not isinstance(date_str, str) or len(date_str) < 10:
        return None
    
    try:
        # Extragem doar portiunea YYYY-MM-DD (primele 10 caractere)
        return datetime.strptime(date_str[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


# =====================================================
# STEP 1: COMBINĂ DATE BRUTE (COMBINE RAW DATA)
# =====================================================

def combine_raw_data() -> Dict[str, List]:
    """
    Combină toate fișierele brute din fiecare sursă.
    Similar cu celulele 8 și 9 din E_Commers_filter.ipynb
    """
    print("\n" + "="*60)
    print("STEP 1: COMBINĂ DATE BRUTE")
    print("="*60)
    
    surse_config = {
        "linkedin": {"pattern": "dataset_linkedin*.json", "key": "jobUrl"},
        "glassdoor": {"pattern": "dataset_glassdoor*.json", "key": "apply_url"},
        "stepstone": {"pattern": "dataset_stepstone*.json", "key": "id"}
    }
    
    combined_data = {}
    
    for sursa, config in surse_config.items():
        print(f"\n📁 Procesez {sursa.upper()}...")
        pattern = os.path.join(DATA_RAW_DIR, config["pattern"])
        files = glob.glob(pattern)
        
        if not files:
            print(f"  ⚠️ Nu s-au găsit fișiere pentru {sursa}. Verifică folderul {DATA_RAW_DIR}")
            combined_data[sursa] = []
            continue
        
        all_items = []
        for filepath in files:
            data = load_json(filepath)
            if isinstance(data, list):
                all_items.extend(data)
            elif isinstance(data, dict):
                all_items.append(data)
        
        # Deduplicare bazată pe cheia unică
        seen = set()
        unique_items = []
        for item in all_items:
            key_value = item.get(config["key"])
            if key_value and key_value not in seen:
                seen.add(key_value)
                unique_items.append(item)
            elif not key_value:
                unique_items.append(item)
        
        combined_data[sursa] = unique_items
        print(f"  ✅ {len(unique_items)} joburi unice (din {len(all_items)} totale)")
        
        # Salvează versiunea unică în helpers
        save_helper(unique_items, f"{sursa}_unic.json")
    
    return combined_data


# =====================================================
# STEP 2: NORMALIZARE ȘI FILTRARE (NORMALIZE & FILTER)
# =====================================================
# EXACT ca în celula 12 din E_Commers_filter.ipynb

def normalize_linkedin(job: Dict) -> Dict:
    """Transforma un job LinkedIn in formatul comun."""
    return {
        "title": job.get("title"),
        "location": job.get("location"),
        "published_date": job.get("publishedAt"),
        "company_name": job.get("companyName"),
        "description": job.get("description"),
        "salary": job.get("salary"),
        "work_sector": job.get("sector"),
        "work_type": job.get("workType"),
        "experience": job.get("experienceLevel"),
        "skills": None,  # Se va completa ulterior
        "job_type": job.get("contractType"),
        "source": "linkedin"
    }


def normalize_glassdoor(job: Dict) -> Dict:
    """Transforma un job Glassdoor in formatul comun."""
    # Combinam "country" si "location"
    loc_parts = [job.get("country"), job.get("location")]
    location = " ".join(part for part in loc_parts if part)

    return {
        "title": job.get("title"),
        "location": location or None,
        "published_date": job.get("posted_date"),
        "company_name": job.get("company_name"),
        "description": job.get("skills"),
        "salary": job.get("salary_range"),
        "work_sector": "N/A",
        "work_type": job.get("category"),
        "experience": job.get("experience"),
        "skills": job.get("skills"),
        "job_type": job.get("job_type"),
        "source": "glassdoor"
    }


def normalize_stepstone(job: Dict) -> Dict:
    """Transforma un job Stepstone in formatul comun."""
    return {
        "title": job.get("title"),
        "location": job.get("location"),
        "published_date": job.get("datePosted"),
        "company_name": job.get("companyName"),
        "description": job.get("textSnippet"),
        "salary": job.get("salary"),
        "work_sector": "N/A",
        "work_type": "N/A",
        "experience": "N/A",
        "skills": job.get("skills"),
        "job_type": job.get("job_type"),
        "source": "stepstone"
    }


def normalize_and_filter() -> List[Dict]:
    """
    Normalizează toate joburile și filtrează ultimele 6 luni.
    """
    print("\n" + "="*60)
    print("STEP 2: NORMALIZARE ȘI FILTRARE (ULTIMELE 6 LUNI)")
    print("="*60)
    
    surse_normalizare = {
        "linkedin": normalize_linkedin,
        "glassdoor": normalize_glassdoor,
        "stepstone": normalize_stepstone
    }
    
    all_jobs = []
    total_procesate = 0
    total_pastrate = 0
    total_expirate = 0
    total_fara_data = 0
    
    # =====================================================
    # LOGICA ORIGINALĂ PENTRU DATELE DIN 2025
    # =====================================================
    # Date fixe pentru proiectul din octombrie-noiembrie 2025
    ziua_de_referinta = date(2025, 10, 31)  # 31 octombrie 2025
    data_limita = ziua_de_referinta - relativedelta(months=6)  # 30 aprilie 2025
    
    # =====================================================
    # LOGICA DINAMICĂ (comentată - pentru date actuale)
    # =====================================================
    # today = date.today()
    # ziua_de_referinta = today + timedelta(days=1)
    # data_limita = ziua_de_referinta - relativedelta(months=6)
    
    print(f"📅 Data de referinta: {ziua_de_referinta}")
    print(f"📅 Data limita (se pastreaza joburile >=): {data_limita}")
    
    for sursa, norm_func in surse_normalizare.items():
        filename = f"{sursa}_unic.json"
        filepath = os.path.join(DATA_HELPERS_DIR, filename)
        jobs = load_json(filepath)
        
        if not jobs:
            print(f"  ⚠️ Nu s-au găsit date pentru {sursa}")
            continue
        
        print(f"\n📁 Procesez {sursa.upper()}: {len(jobs)} joburi")
        
        for job_brut in jobs:
            total_procesate += 1
            
            # Normalizare
            job_comun = norm_func(job_brut)
            
            # Parsare data (doar primele 10 caractere)
            data_publicare_str = job_comun.get("published_date")
            data_publicare_obj = parse_date(data_publicare_str)
            
            # Filtrare - păstrează joburile mai noi decât data_limita
            if data_publicare_obj:
                if data_publicare_obj >= data_limita:
                    all_jobs.append(job_comun)
                    total_pastrate += 1
                else:
                    total_expirate += 1
            else:
                total_fara_data += 1
    
    print(f"\n📊 Rezumat filtrare:")
    print(f"   Total joburi procesate: {total_procesate}")
    print(f"   ✅ Joburi pastrate (>= {data_limita}): {total_pastrate}")
    print(f"   ❌ Joburi eliminate (prea vechi): {total_expirate}")
    print(f"   ❌ Joburi eliminate (fara data parsabila): {total_fara_data}")
    
    # Salvează în processed
    save_processed(all_jobs, "01_e_commers_jobs.json")
    
    return all_jobs


# =====================================================
# STEP 3: ÎNCĂRCARE ȘI COMBINARE SKILL-URI (LOAD & COMBINE SKILLS)
# =====================================================

def load_and_combine_skills() -> Set[str]:
    """
    Încarcă skill-uri din multiple surse și le combină.
    Similar cu celula 2 din Title_and_description.ipynb
    """
    print("\n" + "="*60)
    print("STEP 3: ÎNCĂRCARE ȘI COMBINARE SKILL-URI")
    print("="*60)
    
    all_skills = set()
    skill_sources = ["unique_skills.json", "json_skills1.json", "json_skills2.json"]
    
    for source in skill_sources:
        filepath = os.path.join(DATA_HELPERS_DIR, source)
        data = load_json(filepath)
        
        if data and isinstance(data, dict) and "skills" in data:
            skills = data["skills"]
            if isinstance(skills, list):
                all_skills.update(skills)
                print(f"  ✅ {source}: +{len(skills)} skill-uri")
        elif data and isinstance(data, list):
            all_skills.update(data)
            print(f"  ✅ {source}: +{len(data)} skill-uri")
        elif data and isinstance(data, dict):
            # Fallback pentru alte structuri
            for key in ["skills", "skill", "unique_skills"]:
                if key in data and isinstance(data[key], list):
                    all_skills.update(data[key])
                    print(f"  ✅ {source}: +{len(data[key])} skill-uri (din cheia '{key}')")
                    break
        else:
            print(f"  ⚠️ {source}: nu s-a găsit sau format necunoscut")
    
    # Salvează skill-urile combinate
    skills_list = sorted(all_skills)
    save_helper({"skills": skills_list}, "unique_skills_combined.json")
    print(f"\n📊 Total skill-uri unice combinate: {len(skills_list)}")
    
    return all_skills


# =====================================================
# STEP 3b: EXTRAGERE SKILL-URI DIN DESCRIERI (EXTRACT SKILLS FROM DESCRIPTION)
# =====================================================
# FOLOSEȘTE DOAR RE (regex) - FĂRĂ NLTK

def extract_skills_from_descriptions() -> List[Dict]:
    """
    Extrage skill-uri din descrierile joburilor folosind regex.
    FĂRĂ NLTK - doar re (regex)
    """
    print("\n" + "="*60)
    print("STEP 3b: EXTRAGERE SKILL-URI DIN DESCRIERI")
    print("="*60)
    
    # Încarcă datele din etapa anterioară
    jobs = load_processed("01_e_commers_jobs.json")
    if not jobs:
        print("  ⚠️ Nu s-au găsit joburi de procesat")
        return []
    
    # Încarcă skill-urile cunoscute
    skills_data = load_helper("unique_skills_combined.json")
    known_skills = set(skills_data.get("skills", [])) if skills_data else set()
    
    print(f"📚 Skill-uri cunoscute pentru căutare: {len(known_skills)}")
    
    # Compilează regex pentru fiecare skill (căutare cuvânt întreg, ignoră majuscule)
    skill_patterns = {}
    for skill in known_skills:
        if skill and isinstance(skill, str):
            try:
                # Escape caractere speciale (ex: C++, Node.js)
                # \b pentru limită de cuvânt
                pattern = re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
                skill_patterns[skill] = pattern
            except re.error:
                # Dacă nu se poate compila, încearcă fără \b
                try:
                    pattern = re.compile(re.escape(skill), re.IGNORECASE)
                    skill_patterns[skill] = pattern
                except re.error:
                    pass
    
    print(f"📝 Regex compilate: {len(skill_patterns)}")
    
    updated_jobs = []
    jobs_with_skills = 0
    
    for job in jobs:
        description = job.get("description", "")
        new_job = job.copy()
        
        if not description or not isinstance(description, str):
            new_job["skills"] = []
            updated_jobs.append(new_job)
            continue
        
        found_skills = set()
        for skill_name, pattern in skill_patterns.items():
            if pattern.search(description):
                found_skills.add(skill_name)
        
        new_job["skills"] = list(found_skills)
        if found_skills:
            jobs_with_skills += 1
        updated_jobs.append(new_job)
    
    print(f"✅ Joburi cu skill-uri extrase: {jobs_with_skills}/{len(updated_jobs)}")
    
    # Salvează
    save_processed(updated_jobs, "02_e_commers_jobs_with_skills.json")
    
    return updated_jobs


# =====================================================
# STEP 4: FILTRARE JOBURI DUPĂ TITLURI (FILTER BY JOB TITLES)
# =====================================================

def filter_by_job_titles() -> List[Dict]:
    """
    Filtrează joburile pe baza titlurilor relevante.
    Similar cu celulele 4-6 din E_Commers_filter.ipynb
    """
    print("\n" + "="*60)
    print("STEP 4: FILTRARE JOBURI DUPĂ TITLURI")
    print("="*60)
    
    # Încarcă datele
    jobs = load_processed("02_e_commers_jobs_with_skills.json")
    if not jobs:
        print("  ⚠️ Nu s-au găsit joburi de procesat")
        return []
    
    # Încarcă titlurile relevante din job_title.json
    titles_data = load_helper("job_title.json")
    if not titles_data:
        print("  ⚠️ job_title.json nu a fost găsit. Se sare peste filtrare.")
        return jobs
    
    # Extrage lista de titluri
    if isinstance(titles_data, dict):
        relevant_titles_raw = titles_data.get("job title", [])
    elif isinstance(titles_data, list):
        relevant_titles_raw = titles_data
    else:
        relevant_titles_raw = []
    
    relevant_titles = [str(t).lower() for t in relevant_titles_raw if t]
    print(f"📋 Titluri relevante încărcate: {len(relevant_titles)}")
    
    # Câmpuri în care să caute (exact ca în V2)
    search_fields = ["title", "description", "work_sector", "work_type"]
    
    filtered_jobs = []
    for job in jobs:
        # Combină textul din TOATE câmpurile relevante
        search_text = ""
        for field in search_fields:
            value = job.get(field)
            if isinstance(value, str):
                search_text += " " + value.lower()
            elif isinstance(value, list):
                search_text += " " + " ".join(value).lower()
        
        match_found = any(title in search_text for title in relevant_titles)
        
        if match_found:
            filtered_jobs.append(job)
    
    print(f"✅ Joburi după filtrare: {len(filtered_jobs)} (din {len(jobs)})")
    
    save_processed(filtered_jobs, "03_e_commers_jobs_filtered.json")
    
    return filtered_jobs


# =====================================================
# STEP 5: ANALIZĂ ȘI DIVIZARE LOCAȚII (LOCATION SPLIT)
# =====================================================

def analyze_locations() -> Dict:
    """Analizează formatele locațiilor și generează raport."""
    print("\n" + "="*60)
    print("STEP 5: ANALIZĂ LOCAȚII")
    print("="*60)
    
    jobs = load_processed("03_e_commers_jobs_filtered.json")
    if not jobs:
        print("  ⚠️ Nu s-au găsit joburi")
        return {}
    
    formats = {1: set(), 2: set(), 3: set(), "other": set()}
    
    for job in jobs:
        location = job.get("location", "")
        if not isinstance(location, str) or not location.strip():
            continue
        
        parts = [p.strip() for p in location.split(",")]
        num_parts = len(parts)
        
        if num_parts == 1:
            formats[1].add(location)
        elif num_parts == 2:
            formats[2].add(location)
        elif num_parts == 3:
            formats[3].add(location)
        else:
            formats["other"].add(location)
    
    report = {
        "locations_with_1_part_to_review": sorted(list(formats[1])),
        "locations_with_2_parts_to_review": sorted(list(formats[2])),
        "locations_with_3_parts_correct": sorted(list(formats[3]))
    }
    
    print(f"📊 Locații corecte (3 părți): {len(formats[3])}")
    print(f"📊 Locații parțiale (2 părți): {len(formats[2])}")
    print(f"📊 Locații incomplete (1 parte): {len(formats[1])}")
    
    save_helper(report, "location_reports/location_analysis.json")
    
    return report


def split_locations() -> List[Dict]:
    """
    Divizează locațiile în city, region, country.
    Similar cu celula 19 din E_Commers_filter.ipynb
    """
    print("\n" + "="*60)
    print("STEP 5b: DIVIZARE LOCAȚII")
    print("="*60)
    
    jobs = load_processed("03_e_commers_jobs_filtered.json")
    if not jobs:
        return []
    
    updated_jobs = []
    partial_jobs = []
    
    for job in jobs:
        new_job = job.copy()
        location = job.get("location", "")
        
        # Inițializează câmpurile
        new_job["city"] = None
        new_job["region"] = None
        new_job["country"] = None
        
        if isinstance(location, str) and location.strip():
            parts = [p.strip() for p in location.split(",")]
            num_parts = len(parts)
            
            if num_parts == 1:
                new_job["country"] = parts[0]
            elif num_parts == 2:
                new_job["city"] = parts[0]
                new_job["country"] = parts[1]
            elif num_parts >= 3:
                new_job["city"] = parts[0]
                new_job["region"] = parts[1]
                new_job["country"] = parts[2]
            else:
                new_job["city"] = location
        
        updated_jobs.append(new_job)
        
        # Identifică joburile parțiale (fără region)
        if new_job.get("city") and not new_job.get("region"):
            partial_jobs.append(new_job)
    
    print(f"✅ Joburi procesate: {len(updated_jobs)}")
    print(f"📌 Joburi parțiale (fără region): {len(partial_jobs)}")
    
    save_processed(updated_jobs, "04_e_commers_jobs_locations_split.json")
    save_helper(partial_jobs, "location_reports/incomplete_locations.json")
    
    return updated_jobs


# =====================================================
# STEP 6: FINALIZARE ȘI CURĂȚARE (FINALIZE & CLEAN)
# =====================================================

def finalize_locations() -> List[Dict]:
    """
    Finalizează locațiile și curăță datele.
    Similar cu celula 20 din E_Commers_filter.ipynb
    """
    print("\n" + "="*60)
    print("STEP 6: FINALIZARE LOCAȚII")
    print("="*60)
    
    jobs = load_processed("04_e_commers_jobs_locations_split.json")
    if not jobs:
        return []
    
    # Încarcă joburile parțiale pentru corectare
    partial_jobs = load_helper("location_reports/incomplete_locations.json")
    partial_dict = {}
    if partial_jobs:
        for job in partial_jobs:
            title = job.get("title", "")
            if title:
                partial_dict[title] = job
    
    final_jobs = []
    for job in jobs:
        new_job = job.copy()
        
        # Dacă nu are region, dar are city, folosește city ca region
        if not new_job.get("region") and new_job.get("city"):
            new_job["region"] = new_job["city"]
        
        # Curăță câmpurile goale (None sau string gol)
        for field in ["title", "description", "skills", "location"]:
            value = new_job.get(field)
            if value == "" or value is None:
                new_job[field] = None
        
        final_jobs.append(new_job)
    
    print(f"✅ Joburi finalizate: {len(final_jobs)}")
    
    save_processed(final_jobs, "05_e_commers_jobs_final.json")
    
    return final_jobs


# =====================================================
# STEP 7: STATISTICI ȘI ANALIZĂ (STATISTICS)
# =====================================================

def generate_statistics():
    """Generează statistici despre joburi, skill-uri, etc."""
    print("\n" + "="*60)
    print("STEP 7: STATISTICI ȘI ANALIZĂ")
    print("="*60)
    
    jobs = load_processed("05_e_commers_jobs_final.json")
    if not jobs:
        return
    
    total_jobs = len(jobs)
    
    # Statistici joburi
    sources = Counter(job.get("source") for job in jobs)
    experiences = Counter(job.get("experience") for job in jobs)
    job_types = Counter(job.get("job_type") for job in jobs)
    
    # Statistici skill-uri
    all_skills = []
    for job in jobs:
        skills = job.get("skills", [])
        if isinstance(skills, list):
            all_skills.extend(skills)
    
    skill_counts = Counter(all_skills).most_common(20)
    
    # Statistici locații
    cities = Counter(job.get("city") for job in jobs if job.get("city"))
    regions = Counter(job.get("region") for job in jobs if job.get("region"))
    
    stats = {
        "total_jobs": total_jobs,
        "sources": dict(sources),
        "experience_levels": dict(experiences),
        "job_types": dict(job_types),
        "top_20_skills": skill_counts,
        "top_20_cities": dict(cities.most_common(20)),
        "top_regions": dict(regions.most_common(10))
    }
    
    print(f"\n📊 STATISTICI FINALE:")
    print(f"   Total joburi: {total_jobs}")
    print(f"   Surse: {dict(sources)}")
    print(f"   Skill-uri unice: {len(set(all_skills))}")
    print(f"   Orașe distincte: {len(cities)}")
    print(f"   Regiuni distincte: {len(regions)}")
    
    save_helper(stats, "statistics.json")
    
    return stats


# =====================================================
# PIPELINE PRINCIPAL (MAIN PIPELINE)
# =====================================================

def run_full_pipeline():
    """Rulează întregul pipeline ETL."""
    print("\n" + "="*60)
    print("🚀 PIPELINE ETL - E-COMMERCE JOB MARKET ANALYSIS")
    print("="*60)
    
    # Verifică dacă există date brute în folderul raw
    if not os.path.exists(DATA_RAW_DIR) or not any(os.scandir(DATA_RAW_DIR)):
        print(f"\n⚠️ ATENȚIE: Folderul {DATA_RAW_DIR} este gol!")
        print("   Mută fișierele dataset_*.json în folderul 'data/raw/' înainte de a rula pipeline-ul.")
        print("\n📁 Structura așteptată:")
        print("   data/raw/dataset_linkedin_*.json")
        print("   data/raw/dataset_glassdoor_*.json")
        print("   data/raw/dataset_stepstone_*.json")
        return None
    
    step1_data = combine_raw_data()
    step2_data = normalize_and_filter()
    step3_skills = load_and_combine_skills()
    step3b_data = extract_skills_from_descriptions()
    step4_data = filter_by_job_titles()
    step5_report = analyze_locations()
    step5b_data = split_locations()
    step6_data = finalize_locations()
    step7_stats = generate_statistics()
    
    print("\n" + "="*60)
    print("✅ PIPELINE ETL FINALIZAT CU SUCCES!")
    print("="*60)
    print("\n📁 Structura fișierelor generate:")
    print(f"\n   📂 {DATA_PROCESSED_DIR}")
    print("      ├── 01_e_commers_jobs.json")
    print("      ├── 02_e_commers_jobs_with_skills.json")
    print("      ├── 03_e_commers_jobs_filtered.json")
    print("      ├── 04_e_commers_jobs_locations_split.json")
    print("      └── 05_e_commers_jobs_final.json")
    print(f"\n   📂 {DATA_HELPERS_DIR}")
    print("      ├── unique_skills_combined.json")
    print("      ├── statistics.json")
    print("      ├── linkedin_unic.json")
    print("      ├── glassdoor_unic.json")
    print("      ├── stepstone_unic.json")
    print("      └── location_reports/")
    print("          ├── location_analysis.json")
    print("          └── incomplete_locations.json")
    
    return step6_data


if __name__ == "__main__":
    final_data = run_full_pipeline()
    if final_data:
        print(f"\n🎯 Datele finale sunt gata pentru dashboard: {len(final_data)} joburi")
    else:
        print("\n⚠️ Pipeline-ul nu a rulat complet. Verifică fișierele sursă în data/raw/")