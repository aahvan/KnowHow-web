from celery import shared_task
from app.web.db.models import Document, AnalyzeResults
from app.web.files import download
from app.chat import create_emdeddings
from app.web.csvxls import handle_csvxls
from app.chat.audio_analyzer import run_audio_analyzer
from app.web import files
from app.chat import build_chat, ChatArgs
from flask import g, current_app
import uuid
import pprint
import asyncio


# @shared_task()
def process_document(document_id, file_extension):
    document = Document.find_by(id=document_id)
    # NOTE: Handling differenet type of files:
    with download(document.id) as file_path:
        print("Running embeddings::::")
        if file_extension in ["txt", "docx", "pdf", "doc"]:
            create_emdeddings(document.id, file_path, file_extension)
        elif file_extension in ["csv", "xls", "xlsx"]:
            handle_csvxls(document.name, document.user_id, file_path, file_extension)
        elif file_extension in ["wav", "mp3"]:
            print("Running audio analyzer::" + f"analysis_results/{document.name.split(".")[0]}.txt")
            download_url = files.create_download_url(document.id);
            pprint.pp(download_url)
            run_audio_analyzer(download_url[0], f"analysis_results/{document.name.split(".")[0]}.txt", document.id)

        else:
            raise ValueError("Invalid file extension")
    # NOTE: Generate the summary of the document with predefined prompts:
    # print("Generating summary with custom prompt::::")
    # prompts = get_analyzer_prompt()
    # NOTE: NO need for converation id but still keeping it for consistency with TODO:refactor
    # conversation_id=str(uuid.uuid4())
    # char_args = ChatArgs(
    #     conversation_id=conversation_id,
    #     document_id=document.id,
    #     streaming=False,
    #     metadata={
    #         "conversation_id": conversation_id,
    #         "document_id": document.id,
    #         "user_id": g.user.id
    #     }
    # )
    # chat = build_chat(char_args)
    # # NOTE: Looping through prompts and generate response
    # for prompt in prompts:
    #     content = chat.invoke(prompt["prompt"])["answer"]
    #     AnalyzeResults.create(document_id=document.id, prompt=prompt["analyst_input"], content=content)
