import logging

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import PyPDF2
from agents.orchestrator.graph import orchestrator

router = APIRouter()
logger = logging.getLogger(__name__)

# --- Fonction utilitaire pour extraire le texte ---
async def extract_text_from_file(file: UploadFile) -> str:
    """Extrait le texte d'un fichier uploadé selon son extension."""
    try:
        # Lecture d'un fichier texte
        if file.filename.endswith(".txt"): # type: ignore
            content = await file.read()
            return content.decode("utf-8")
            
        # Lecture d'un fichier PDF
        elif file.filename.endswith(".pdf"): # type: ignore
            reader = PyPDF2.PdfReader(file.file)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
            
        else:
            raise HTTPException(status_code=400, detail="Format de fichier non supporté. Utilisez PDF ou TXT.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture du fichier: {str(e)}")


@router.post("/analyze", summary="Réceptionne le cas d'entreprise (avec fichier optionnel) et lance l'analyse")
async def analyze_business_case(
    # Utilisation de Form() au lieu de Pydantic pour permettre l'upload de fichier
    company_name: str = Form(..., description="Le nom de l'entreprise étudiée"),
    context_text: str = Form(..., description="Le texte brut décrivant la situation"),
    document: UploadFile = File(None, description="Document PDF ou TXT optionnel")
):
    try:
        # 1. Extraction du texte si un document est fourni
        document_content = ""
        if document:
            document_content = await extract_text_from_file(document)

        # 2. Préparation du texte global injecté dans le graphe
        business_case_text = f"Entreprise : {company_name}\nContexte : {context_text}"
        if document_content:
            business_case_text += f"\n\n--- Informations extraites du document ({document.filename}) ---\n{document_content}"

        # 3. Initialisation de l'état LangGraph
        initial_state = {
            "business_case": business_case_text,
            "why": "",
            "what": "",
            "how": "",
            "structured_problem": "",
            "why_context": "",
            "what_context": "",
            "how_context": "",
            "global_context": "",
            "canvas_analysis": "",
            "strategic_analysis": "",
            "roadmap": "",
            "evaluation": "",
            "is_valid": False,
        }
        
        print(f"--- Réception de l'input pour : {company_name} ---")
        if document:
            print(f"Fichier joint : {document.filename} (Extrait: {len(document_content)} caractères)")
        
        # 4. Exécution du graphe multi-agents
        final_state = await orchestrator.ainvoke(initial_state) # type: ignore
        
        return {
            "status": "success",
            "company": company_name,
            "results": {
                "structured_problem": final_state.get("structured_problem"),
                "canvas_analysis": final_state.get("canvas_analysis"),
                "strategic_analysis": final_state.get("strategic_analysis"),
                "roadmap": final_state.get("roadmap"),
                "evaluation": final_state.get("evaluation"),
                "is_valid": final_state.get("is_valid")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur lors de l'analyse du cas d'entreprise")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")