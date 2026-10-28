from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import os 
from dotenv import load_dotenv
from google import genai
from google.genai import types

app = FastAPI()

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo .env")

client = genai.Client(api_key=api_key)

class MensagemUsuario(BaseModel):
    mensagem: str

class CadastroNotasSchema(BaseModel):
    nome_aluno: str
    disciplina: str
    nota: float
    resposta_final: str

banco_de_dados = []
   

@app.get("/", include_in_schema=False)
def pagina_inicial():
    return RedirectResponse(url="/docs")


@app.get("/api/alunos")
def listar_alunos():
    return {"alunos": banco_de_dados}

@app.post("/api/chat")
def chat(dados: MensagemUsuario):
    try:
        prompt = f"""
            Você é um assistente escolar responsável por resgistrar notas.
            Analise a mensagem do usuário e extraia:
            - nome do aluno;
            - disciplina;
            - nota.
            Depois, escreva uma resposta_final amigável confirmando o registro da nota, utilizando os dados extraídos.

            Se algum dado estiver ausente ou não puder ser identificado, não invente informações. Informe na resposta_final quais dados precisam ser esclarecidos.
            Mensagem do usuário:
            {dados.mensagem}
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CadastroNotasSchema
            )
        )

        resultado = CadastroNotasSchema.model_validate_json(
            response.text
        )

        if(
            resultado.nome_aluno.strip() and
            resultado.disciplina.strip()
            and 0 <= resultado.nota <= 10 
        ): 
            banco_de_dados.append({
            "nome_aluno": resultado.nome_aluno,
            "disciplina": resultado.disciplina,
            "nota": resultado.nota
        })
            status = "Nota cadastrada com sucesso."
        else: 
            status= "Cadastro não realizado" 

        return {
            "status": status,
            "dados_extraidos": {
                "nome_aluno": resultado.nome_aluno,
                "disciplina": resultado.disciplina,
                "nota": resultado.nota
            },
            "resposta_final": resultado.resposta_final,
        }

    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar a mensagem: {erro}",
        )