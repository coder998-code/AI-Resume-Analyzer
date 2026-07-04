from pypdf import PdfReader


def load_resumes(files):

    resumes = []

    for file in files:

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted


        resumes.append({

            "name": file.name,

            "text": text

        })


    return resumes