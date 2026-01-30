
import pandas as pd

def load_profiles(path):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()
    profiles = []
    for _, r in df.iterrows():
        profiles.append({
            "profile_id": str(r["profile_id"]).strip(),
            "seed_key": str(r.get("seed_key","")),
            "password": str(r.get("password",""))
        })
    return profiles
