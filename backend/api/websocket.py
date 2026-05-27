# import json
# import traceback
# import asyncio
# from uuid import UUID
# from pathlib import Path
# from typing import Annotated
# from langchain_community.document_loaders import PyPDFLoader

# from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, HTTPException, UploadFile, File, Depends
# from sqlmodel import select


# from service.auth_service import get_current_user, AuthService
# from service.chat_service import ChatService
# from database.session import SessionDep
# from database.model import MAX_MESSAGE_LENGTH, User


# from core.graph import compiled_graph
# from schema.agent import BusinessCaseInput

# router = APIRouter(prefix="/ws", tags=["chats"])
# CurrentUserDep = Annotated[User, Depends(get_current_user)]

# # 1. Mise à jour du mapping pour correspondre aux nœuds de TARA
# NODE_TO_FRONT_KEY = {
#     "planner": "planner",
#     "retriever": "retriever",
#     "analyst": "analyst",
#     "strategist": "strategist",
#     "generator": "generator",
#     "evaluator": "evaluator"
# }

# current_file_path = Path(__file__).resolve()
# UPLOAD_DIR = current_file_path.parent.parent / "uploads"
# UPLOAD_DIR.mkdir(exist_ok=True)

# # [Le endpoint /upload reste identique à ta version d'origine, on le conserve pour le RAG de ton binôme]
# # ...

# @router.websocket("/{conversation_id}")
# async def websocket_endpoint(
#     websocket: WebSocket,
#     session: SessionDep,
#     conversation_id: UUID,
#     token: str = Query(...)
# ):
#     # 1. Validation de l'utilisateur (inchangé)
#     auth_service = AuthService(session)
#     try:
#         email = auth_service.decode_token(token)
#         user = session.exec(select(User).where(User.email == email)).first()
#         if not user:
#             raise HTTPException(status_code=401)
#     except Exception:
#         await websocket.close(code=1008)
#         return

#     chat_service = ChatService(session)
#     await websocket.accept()

#     # 2. Chargement de l'historique
#     history = chat_service.get_conversation_history(conversation_id, user.id)
#     if history is None:
#         await websocket.send_json({"type": "error", "content": "Accès refusé."})
#         await websocket.close(code=1008)
#         return

#     await websocket.send_json({"type": "history", "messages": history})

#     try:
#         while True:
#             data = await websocket.receive_json()
#             user_message = data.get("content", "").strip()
            
#             if not user_message:
#                 continue
#             if len(user_message) > MAX_MESSAGE_LENGTH:
#                 await websocket.send_json({"type": "error", "content": f"Message trop long."})
#                 continue

#             # Sauvegarde du message utilisateur
#             chat_service.save_message(conversation_id, user_message, "user")

#             try:
#                 # Notification de démarrage au front
#                 await websocket.send_json({"type": "status", "content": "agent_starting"})

#                 # 3. Préparation de l'Input TARA
#                 # On suppose ici que le premier message sert à définir le contexte de l'entreprise
#                 # Si un fichier a été uploadé, ton binôme (RAG) ira le lire dans UPLOAD_DIR
#                 business_case = BusinessCaseInput(
#                     company_name="Cas Client (Conversation)", 
#                     context_text=user_message
#                 )
                
#                 matched_files = list(UPLOAD_DIR.glob(f"{conversation_id}_source.*"))
#                 extracted_doc_text = None
                
#                 if matched_files:
#                     file_path = matched_files[0]
#                     try:
#                         if file_path.suffix.lower() == ".pdf":
#                             # Extraction du texte du PDF
#                             loader = PyPDFLoader(str(file_path))
#                             pages = loader.load()
#                             extracted_doc_text = "\n".join([p.page_content for p in pages])
#                         else:
#                             # Extraction pour les fichiers TXT/CSV/JSON
#                             with open(file_path, "r", encoding="utf-8") as f:
#                                 extracted_doc_text = f.read()
                        
#                         # Optionnel : On prévient le front-end qu'on a bien lu le fichier
#                         print(f"📄 Fichier {file_path.name} lu avec succès ({len(extracted_doc_text)} caractères).")
#                     except Exception as e:
#                         print(f"⚠️ Erreur lors de la lecture du fichier uploadé : {e}")
                
#                 # --- PRÉPARATION DE L'INPUT TARA ---
#                 business_case = BusinessCaseInput(
#                     company_name="Cas Client", 
#                     context_text=user_message,
#                     document_content=extracted_doc_text  # On injecte le texte du document ici !
#                 )
                            
#                 initial_state = {
#                     "business_case": business_case,
#                     "planner_analysis": None,
#                     "retrieved_context": None,
#                     "canvas_analysis": None,
#                     "strategic_trajectory": None,
#                     "final_roadmap": None
#                 }

#                 final_roadmap_data = None
                
#                 # 4. Exécution de LangGraph en mode Streaming (astream)
#                 # astream() renvoie les mises à jour d'état dès qu'un nœud a terminé
#                 async for output in compiled_graph.astream(initial_state): # type: ignore
#                     # output est un dict avec la clé du nœud qui vient de s'exécuter
#                     for node_name, node_state in output.items():
                        
#                         front_key = NODE_TO_FRONT_KEY.get(node_name, node_name)
                        
#                         # Animation UI : On signale que ce nœud vient de se terminer
#                         await websocket.send_json({
#                             "type": "agent_step", 
#                             "node": front_key, 
#                             "status": "completed"
#                         })
                        
#                         # Si c'est le générateur, on capture la roadmap Pydantic finale
#                         if node_name == "generator" and "final_roadmap" in node_state:
#                             final_roadmap_data = node_state["final_roadmap"]

#                 # 5. Formatage de la réponse finale
#                 if final_roadmap_data:
#                     # On convertit l'objet Pydantic en texte Markdown lisible pour le chat
#                     response_text = f"### Roadmap Stratégique Générée\n\n"
#                     response_text += f"**Analyse Stratégique :**\n{final_roadmap_data.rationale.why_transform}\n\n"
#                     response_text += "### Initiatives Prioritaires\n"
#                     for init in final_roadmap_data.initiatives:
#                         response_text += f"- **{init.title}** ({init.priority}) : {init.description} *[Budget: {init.budget_effort}]*\n"
#                 else:
#                     response_text = "L'agent n'a pas pu générer la roadmap."

#                 # Sauvegarde et envoi
#                 chat_service.save_message(conversation_id, response_text, "assistant")
                
#                 # Notification de fin
#                 await websocket.send_json({"type": "message", "content": response_text})
#                 await websocket.send_json({"type": "status", "content": "connected"})

#             except Exception as e:
#                 error_trace = traceback.format_exc()
#                 print(f"Erreur Agent TARA: {error_trace}")
#                 await websocket.send_json({"type": "error", "content": f"Erreur lors de l'analyse : {str(e)}"})

#     except WebSocketDisconnect:
#         print(f"Déconnexion de l'utilisateur {user.email} (Conv: {conversation_id})")