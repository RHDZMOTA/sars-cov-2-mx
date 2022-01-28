import os



COV_TOKEN = os.environ.get("COV_TOKEN")
COV_GIST_ID = os.environ.get("COV_GIST_ID")
COV_FILENAME = os.environ.get("COV_FILENAME")

URL_TEMPLATE = "https://datos.covid-19.conacyt.mx/Downloads/Files/Casos_Diarios_Estado_Nacional_Confirmados_{date}.csv"
URL_GIST = "https://gist.githubusercontent.com/RHDZMOTA/{gist_id}/raw/{filename}".format(
    gist_id=COV_GIST_ID,
    filename=COV_FILENAME
)
