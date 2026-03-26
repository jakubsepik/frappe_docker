import deepl
import csv
import sys
import time
import os

API_KEY = "a326cb99-c020-4a18-976d-5b4ed80c2885:fx"
INPUT = "erpnext_sk.csv"
OUTPUT = "erpnext_sk_translated.csv"
PROGRESS = "erpnext_sk_progress.csv"
DELAY = 0.5  # sekundy medzi requestmi
MAX_RETRY = 5

translator = deepl.Translator(API_KEY)

# Nacitaj vstup
with open(INPUT, newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))

total = len(rows)
usage = translator.get_usage()
print(f"Celkom riadkov: {total}")
print(f"Zostatok znakov: {usage.character.limit - usage.character.count:,}")

# Nacitaj progress ak existuje
done = {}
if os.path.exists(PROGRESS):
    with open(PROGRESS, newline="", encoding="utf-8") as f:
        for r in csv.reader(f):
            if len(r) >= 2:
                done[r[0]] = r[1]
    print(f"Obnovujem z progresu: {len(done)} uz prelozených")

progress_f = open(PROGRESS, "a", newline="", encoding="utf-8")
progress_w = csv.writer(progress_f)

results = []
fail = 0

for i, row in enumerate(rows):
    src = row[0] if row else ""

    if not src:
        results.append(row)
        continue

    # Uz prelozene
    if src in done:
        results.append([src, done[src]] + row[2:])
        continue

    # Preloz s retry
    translated = None
    for attempt in range(1, MAX_RETRY + 1):
        try:
            r = translator.translate_text(src, source_lang="EN", target_lang="SK")
            translated = r.text
            break
        except Exception as e:
            msg = str(e)
            if "Too many requests" in msg or "429" in msg:
                wait = 2**attempt
                print(
                    f"  Rate limit riadok {i+1}, čakám {wait}s (pokus {attempt}/{MAX_RETRY})"
                )
                time.sleep(wait)
            else:
                print(f"  CHYBA riadok {i+1}: {msg}", file=sys.stderr)
                break

    if translated is not None:
        done[src] = translated
        progress_w.writerow([src, translated])
        progress_f.flush()
        results.append([src, translated] + row[2:])
    else:
        fail += 1
        results.append(row)

    if i % 100 == 0 and i > 0:
        print(f"{i}/{total} ({round(i/total*100)}%) | chyby: {fail}")

    time.sleep(DELAY)

progress_f.close()

with open(OUTPUT, "w", newline="", encoding="utf-8-sig") as f:
    csv.writer(f).writerows(results)

print(f"\nHotovo! Prelozených: {len(done)}, chýb: {fail}")
print(f"Uložené: {OUTPUT}")
