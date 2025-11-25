# Simple question bank focused on "AI in Python" and related topics for teens
# Each question has keys: q (text), options (list of 4), a (index of correct answer 0..3)


import random


QUESTIONS = [
{"q": "Mana library Python populer untuk pembelajaran mesin?", "options": ["scikit-learn", "pillow", "Flask", "Requests"], "a": 0},
{"q": "Library yang biasa dipakai untuk visi komputer adalah...", "options": ["NumPy", "OpenCV", "Matplotlib", "BeautifulSoup"], "a": 1},
{"q": "Salah satu model NLP yang terkenal adalah...", "options": ["Naive Bayes", "R-CNN", "BERT", "YOLO"], "a": 2},
{"q": "Untuk menyimpan data terstruktur di Python, kita sering memakai...", "options": ["SQLite", "HTML", "CSS", "SVG"], "a": 0},
{"q": "Fungsi `fit()` pada model ML biasanya digunakan untuk...", "options": ["Menyimpan model ke file", "Melatih model dengan data", "Menampilkan grafik", "Membagi dataset"], "a": 1},
{"q": "Paket Pydantic biasa dipakai untuk...", "options": ["Validasi data", "Membuat grafik", "Memanggil API", "Membuat template HTML"], "a": 0},
{"q": "Framework Python untuk membuat API modern dan cepat ialah...", "options": ["Django", "Flask", "FastAPI", "Tkinter"], "a": 2},
{"q": "Untuk manipulasi array numerik besar, library yang cocok adalah...", "options": ["NumPy", "Pandas", "Flask", "OpenCV"], "a": 0},
]




def get_random_question():
    q = random.choice(QUESTIONS)
    q_copy = {"q": q['q'], "options": q['options'][:], "a": q['a']}
    options = q_copy['options']
    correct = q_copy['a']
    combined = list(enumerate(options))
    random.shuffle(combined)
    new_options = [opt for idx,opt in combined]
    original_correct_text = options[correct]
    new_correct_index = new_options.index(original_correct_text)
    return {"q": q_copy['q'], "options": new_options, "a": new_correct_index}